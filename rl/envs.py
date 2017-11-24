import os

import gym
from gym.spaces.box import Box

import numpy as np

from baselines import bench
from baselines.common.atari_wrappers import make_atari, wrap_deepmind

try:
    import pybullet_envs
except ImportError:
    pass

from gym_aigame.envs import Annotator

def make_env(env_id, seed, rank, log_dir):
    def _thunk():
        env = gym.make(env_id)
        env = Annotator(env)

        is_atari = hasattr(gym.envs, 'atari') and isinstance(env.unwrapped, gym.envs.atari.atari_env.AtariEnv)
        if is_atari:
            env = make_atari(env_id)
        #env.seed(seed + rank)
        #env = bench.Monitor(env, os.path.join(log_dir, str(rank)))
        #if is_atari:
        #    env = wrap_deepmind(env)
        env = WrapPyTorch(env)

        return env

    return _thunk


class WrapPyTorch(gym.ObservationWrapper):
    def __init__(self, env=None):
        super(WrapPyTorch, self).__init__(env)
        obs_shape = self.observation_space.shape
        self.observation_space = Box(
            self.observation_space.low[0,0,0],
            self.observation_space.high[0,0,0],
            [obs_shape[2], obs_shape[1], obs_shape[0]]
        )

    def _observation(self, observation):
        return observation.transpose(2, 0, 1)
