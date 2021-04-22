import pygame
import random


class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key

counter = 0
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

counter = 0
def run_ai():
    global counter
    counter += 1
    if counter < 3:
        return []
    counter = 0
    e = Event(pygame.KEYDOWN, pygame.K_UP)
    return [e]
