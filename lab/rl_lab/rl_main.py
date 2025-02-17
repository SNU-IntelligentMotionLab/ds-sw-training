import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from scipy.spatial.transform import Rotation as R

from Simulation import PBDSimulation  
from Renderer import Renderer
from Controls import OrbitCamera  
from Objects import Cube, Plane
from Constraints import DistanceConstraint, AttachmentConstraint

import gymnasium as gym
from gymnasium import spaces
from collections import OrderedDict
from stable_baselines3 import PPO
import os
from stable_baselines3.common.callbacks import CheckpointCallback
import argparse
from World import World, initWorld

import yaml
CONFIG_FILE = "config.yaml"

## World having step_(action) attribute
class World_(World):
    def __init__(self,):
        super(World_, self).__init__()

    def step_(self, action):
        if self.playing:
            self.simulation.step_(action)
            self.sim_time += self.simulation.time_step

class WorldEnv(gym.Env):
    def __init__(self, world):
        super(WorldEnv, self).__init__()
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)

        self.cfg_env = config.get("env", {})

        self.action_scale = self.cfg_env.get("action_scale", 500.0)

        self.world = world
        self.action_space = spaces.Box(low=-500.0, high=500.0, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-100.0, high=100.0, shape=(1,), dtype=np.float32)
        self.max_epi_steps = 300
        self.cur_epi_step = 0

        cube1_center = self.compute_center_pos(0)
        self.prev_cube1_center = cube1_center.copy()

        self.acc_reward = 0.0

    def reset(self, seed=None, options=None):
        self.world.reset()
        cube1_center = self.compute_center_pos(0)
        self.prev_cube1_center = cube1_center.copy()
        self.acc_reward = 0.0

        self.cur_epi_step = 0
        obs = self.get_obs()
        info = {}
        return obs, info
    
    def compute_center_pos(self, obj_idx):
        obj = self.world.get_objects()[obj_idx]
        return obj.curr_pos.mean(axis=-2)
    
    def get_reward(self):
        # ---------------------------------
        # TODO : Implement reward function
        # ---------------------------------
        cube1_center = self.compute_center_pos(0)
        reward = cube1_center[0]

        return reward
    
    def is_terminal_state(self):
        cube1_center = self.compute_center_pos(0)
        return False
        #return cube1_center[1] < 2.5

    def step(self, action):
        self.world.step_(self.action_scale*action)
        self.cur_epi_step += 1

        obs = self.get_obs()
        reward = self.get_reward()
        self.acc_reward += reward

        cube1_center = self.compute_center_pos(0)
        self.prev_cube1_center = cube1_center.copy()

        # trucated : check timeout
        truncated = self.cur_epi_step > self.max_epi_steps
        terminated = self.is_terminal_state()
        info = {}

        return obs, reward, terminated, truncated, info

    def get_obs(self):
        # ---------------------------------
        # TODO : Implement observation function
        # ---------------------------------
        cube1_center = self.compute_center_pos(0)
        obs = [cube1_center[0]]

        return np.array(obs, dtype=np.float32)



def test(env, model):
    world = env.world

    obs = env.get_obs()
    
    while world.running:
        pygame.time.wait(10)
        action, _ = model.predict(obs, deterministic=False)
        world.handle_events()
        #obs, reward, terminated, truncated, info = env.step(world.renderer.user_torque/500.0)
        obs, reward, terminated, truncated, info = env.step(action)

        if terminated:
            env.reset()
            obs = env.get_obs()
        world.render()
    
    pygame.quit()

def train(env, model, exp_name):

    if not os.path.exists('./logs/'+exp_name):
        os.makedirs('./logs/'+exp_name)

    with open('./logs/'+exp_name+"/config.yaml", "w") as f:
        with open(CONFIG_FILE, "r") as f2:
            config = yaml.safe_load(f2)
            yaml.dump(config, f)

    checkpoint_callback = CheckpointCallback(save_freq=40000, save_path='./logs/'+exp_name, name_prefix='rl_model')

    model.learn(total_timesteps=400000, callback=checkpoint_callback)
    env.close()


def main():
    parser = argparse.ArgumentParser(description="Train or test the model with optional model loading")
    # -t 옵션: train 모드 (옵션이 없으면 test 모드)
    parser.add_argument("-t", "--train", action="store_true",
                        help="train mode. If not specified, test mode is assumed.")
    # -l 옵션: 로드할 모델 파일 이름 (없으면 None)
    parser.add_argument("-l", "--load", type=str, default=None,
                        help="specify the model file to load")
    
    parser.add_argument("-n", "--name", type=str, default="",
                        help="specify the name of the experiment")

    args = parser.parse_args()

    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    cfg_policy_kwargs = config.get("policy_kwargs", {})
    cfg_ppo_kwargs = config.get("ppo_kwargs", {})


    world = initWorld(World_())
    env = WorldEnv(world)

    # The value on the side is the default value when the 'key' does not exit.
    # You should change the config.yml file to make any difference.
    policy_kwargs = dict(
        log_std_init=np.log(cfg_policy_kwargs.get("std_init", 0.5)),
        net_arch=cfg_policy_kwargs.get("net_arch", [256, 128]),
    )

    ppo_kwargs = dict(
        n_steps=cfg_ppo_kwargs.get("n_steps", 2048),
        n_epochs=cfg_ppo_kwargs.get("n_epochs", 4),
        batch_size=cfg_ppo_kwargs.get("batch_size", 128),
        verbose=cfg_ppo_kwargs.get("verbose", 1),
        tensorboard_log="./tb_logs/"+args.name,
        learning_rate=cfg_ppo_kwargs.get("learning_rate", 0.0003),
    )

    model = PPO(
        "MlpPolicy",
        env,
        **ppo_kwargs,
        policy_kwargs=policy_kwargs,
    )
    # 모델 로드 여부 확인. 로드하지 않으면 랜덤한 policy network 생성
    if args.load:
        print(f"Loading model: {args.load}")
        model = PPO.load(args.load, env=env)
    else:
        print("No model loading specified.")
        model = PPO(
            "MlpPolicy",
            env,
            gamma=cfg_ppo_kwargs.get("gamma", 0.99),
            **ppo_kwargs,
            policy_kwargs=policy_kwargs,
        )
    # train 또는 test 모드 선택
    if args.train:
        print("Train mode activated.")
        train(env, model, args.name)
    else:
        print("Test mode activated.")
        test(env, model)

if __name__ == "__main__":
    main()