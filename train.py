from random import random, randint, sample
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import os
import shutil
from DQN import DQN
from tetris import Tetris
from collections import deque, namedtuple

BATCH_SIZE = 512
GAMMA = 0.99
EPS_START = 1
EPS_END = 0.001
EPS_DECAY = 2000
SAVE_INTERVAL = 10
LEARNING_RATE = 0.001
EPOCHS = 3000
MEMORY_SIZE = 30000

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


def select_action(epoch, results, model):
  sample = random()
  if results:
    next_actions, next_states = zip(*results.items())
    next_states = torch.stack(next_states)
    if torch.cuda.is_available():
      next_states = next_states.cuda()
  eps_threshold = EPS_END + (max(EPS_DECAY - epoch, 0) * (EPS_START - EPS_END) / EPS_DECAY)
  model.eval()
  random_action = sample <= eps_threshold
  if random_action or not results:
    if not results:
      action_index = randint(0, 8)
    else:
      action_index = randint(0, len(results)-1)
  else:
    with torch.no_grad():
      predictions = model(next_states)[:, 0]
      action_index = torch.argmax(predictions).item()
  model.train()
  next_state = next_states[action_index, :]
  action = next_actions[action_index]
  return action, next_state

def optimize_model(memory, model, optimizer, criterion):
  if len(memory) < MEMORY_SIZE / 10:
    return
  batch = memory.sample(min(len(memory), BATCH_SIZE))
  state_batch, reward_batch, next_state_batch, done_batch = zip(*batch)
  state_batch = torch.stack(tuple(state for state in state_batch))
  reward_batch = torch.from_numpy(np.array(reward_batch, dtype=np.float32)[:, None])
  next_state_batch = torch.stack(tuple(state for state in next_state_batch))
  if torch.cuda.is_available():
    state_batch = state_batch.cuda()
    reward_batch = reward_batch.cuda()
    next_state_batch = next_state_batch.cuda()

  state_action_values = model(state_batch)
  model.eval()
  with torch.no_grad():
    prediction_batch = model(next_state_batch)
  model.train()
  expected_state_action_values = torch.cat(
            tuple(reward if done else reward + GAMMA * prediction for reward, done, prediction in
                  zip(reward_batch, done_batch, prediction_batch)))[:, None]
  optimizer.zero_grad()
  loss = criterion(state_action_values, expected_state_action_values)
  loss.backward()
  optimizer.step()



def train():
  torch.cuda.seed()
  env = Tetris(20, 10)
  model = DQN()
  optimizer = optim.Adam(model.parameters(), lr = LEARNING_RATE)
  criterion = nn.MSELoss()
  memory = ReplayMemory(MEMORY_SIZE)
  state = env.get_new_state()
  
  if torch.cuda.is_available():
    model.cuda()
    state = state.cuda()
  epoch = 0
  while epoch < EPOCHS:
    results = env.get_all_states()
    if results:
      action, next_state = select_action(epoch, results, model)
    else:
      action = (randint(0,8), 0)
      next_state = state
    if torch.cuda.is_available():
      next_state = next_state.cuda()
    x, rotations = action
    reward, done = env.step(rotations, x)
    memory.push(state, reward, next_state, done)

    if not done:
      state = next_state
      continue
    else:
      score = env.score
      pieces = env.pieces
      cleared = env.cleared
      state = env.get_new_state()
    epoch += 1
    optimize_model(memory, model, optimizer, criterion)

    print("Epoch: {}/{}, Score: {}, Pieces {}, Cleared lines: {}".format(
    epoch,
    EPOCHS,
    score,
    pieces,
    cleared))

train()


  