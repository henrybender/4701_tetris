import pygame
import random
import torch

counter = 0

class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key

def random_move():
  #choose random direction to move
  move = random.randint(0,3)
  if move == 0:
      event = Event(pygame.KEYDOWN, pygame.K_LEFT)
  elif move == 1:
      event = Event(pygame.KEYDOWN, pygame.K_RIGHT)
  elif move == 2:
    event = Event(pygame.KEYDOWN, pygame.K_DOWN)
  else:
      event = Event(pygame.KEYDOWN, pygame.K_UP)
  return [event]



def DeepQ(game, model):
    global counter
    counter += 1
    if counter < 100:
        return []
    counter = 0
    results = game.get_all_states()
    next_actions, next_states = zip(*results.items())
    next_states = torch.stack(next_states)
    if torch.cuda.is_available():
        next_states = next_states.cuda()
    predictions = model(next_states)[:, 0]
    index = torch.argmax(predictions).item()
    action = next_actions[index]
    position, rotation = action
    e = []
    figure_x = 3
    figure_rot = 0
    print("rotation: "+ str(rotation))
    print("position: "+ str(position))
    if position <0:
        position =0
    if position>9:
        position=9
    while figure_rot != rotation:
        e.append(Event(pygame.KEYDOWN, pygame.K_UP))
        figure_rot+=1
    while figure_x < position:
        e.append(Event(pygame.KEYDOWN, pygame.K_RIGHT))
        figure_x +=1
    while  figure_x > position:
        e.append(Event(pygame.KEYDOWN, pygame.K_LEFT))
        figure_x -= 1
    return e
