from tensorflow.keras.optimizers.legacy import Adam
import gym
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory
import pygame
from environment import MyEnv

# 環境の生成
env = MyEnv()
nb_actions = env.action_space.n

# モデルの定義
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))

# エージェントの設定
memory = SequentialMemory(limit=1000000, window_length=1)
policy = EpsGreedyQPolicy(eps=0.1)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# 学習
dqn.fit(env, nb_steps=200000, visualize=True, verbose=1)

# 評価
dqn.test(env, nb_episodes=3, visualize=True,nb_max_episode_steps=1000)
pygame.quit()   