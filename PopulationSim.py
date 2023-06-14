# https://www.youtube.com/watch?v=WTLPmUHTPqo
# https://youtu.be/eED4bSkYCB8

import pygame
import math
import numpy as np

WIDTH, HEIGHT =  1000, 800
RADIUS_ADULT = 10
RADIUS_YOUNG = 5
POP_SIZE = 50
SPEED = 0.5 # speed of the individual
SIMULATION_STEP_TIME = 1 / 30 # simulation speed in months
MIN_FOR_PROCREATE = 18 * 12 # min months to become parent
LENGTH_OF_PREGNANCY = 9 # lenght of a pregnancy
MAX_NUMBER_OFFSPRING = 5 # maximum number of offspring for female individual
MAX_TIME_PREGNANCY = 12 * 40 # maximum age to be pregnant (in number of month)
CHANCE_OFFSPRING = 0.02 # chance of generate offspring
PERC_FEMALE = 0.5 # percentage of female
AVG_LIFE_YEARS = 70 # average life in years
STD_LIFE_YEARS = 10 # standard deviation life in years

# colors - https://www.pygame.org/docs/ref/color_list.html
BG_COLOR = "azure4"
TEXT_COLOR = "white"
TEXT_BG_COLOR = "black"
IND_MALE_YOUNG = "lightblue"
IND_MALE_ADULT = "blue"
IND_FEMALE_YOUNG = "lightpink"
IND_FEMALE_ADULT = "coral"
IND_FEMALE_PREGNANT = "red"

#
# Get factor 1 or -1 with 50% chance
def rndfact():
  return 1 if np.random.rand() < 0.5 else -1

#
# Individual of the population
class Individual:

  def __init__(self, initial_time, sexFemale, x, y, u, max_time):
    self.sexFemale = sexFemale
    self.x = x
    self.y = y
    self.u = u # direction expressed as a unit vector
    self.max_time = max_time # max time (aka age) of this individual
    self.min_for_procreate = MIN_FOR_PROCREATE # min months to become parent
    self.length_pregnancy = LENGTH_OF_PREGNANCY # length of pregnancy
    self.max_num_pregnancy = MAX_NUMBER_OFFSPRING # maximum number of pregnancies for individual
    
    self.color = pygame.Color("white")
    self.time_pregnant = 0 # number of months of pregnancy
    self.time_life = initial_time # inital age in months
    self.count_pregnancy = 0 # number of pregnancies
    self.alive = True
    self.radius = 0

  def set_color(self):
    if self.sexFemale:
      if self.is_pregnant():
        self.color = pygame.Color(IND_FEMALE_PREGNANT)
      else:
        if self.is_of_age():
          self.color = pygame.Color(IND_FEMALE_ADULT)
        else:
          self.color = pygame.Color(IND_FEMALE_YOUNG)
    else:
      if self.is_of_age():
        self.color = pygame.Color(IND_MALE_ADULT)
      else:
        self.color = pygame.Color(IND_MALE_YOUNG)

  def is_of_age(self):
    return self.time_life >= self.min_for_procreate
      
  def is_pregnant(self):
    return self.sexFemale and self.time_pregnant > 0
    
  def get_distance(self, other):
    other_x, other_y = other.x, other.y
    distance_x = other_x - self.x
    distance_y = other_y - self.y
    return math.sqrt(distance_x ** 2 + distance_y ** 2)
    
  def draw(self, win):
    if not self.alive:
      return 
    
    self.set_color()
    x = self.x + WIDTH / 2
    y = self.y + HEIGHT / 2
    
    if (self.max_time - self.time_life) < 24:
      # dying individual
      pygame.draw.rect(win, self.color, (x - self.radius, y - self.radius, 2*self.radius, 2*self.radius))
    else:
      pygame.draw.circle(win, self.color, (x, y), self.radius)
  
  def update_position(self):
    self.time_life = self.time_life + SIMULATION_STEP_TIME
    
    self.x = SPEED * self.u[0] + self.x
    self.y = SPEED * self.u[1] + self.y
    
    n = np.array([0, 0])
    bounce = False
    if self.y > (HEIGHT / 2 - self.radius): # bottom
      n = np.array([0, 1])
      bounce = True
    elif self.y < -(HEIGHT / 2 - self.radius): # top
      n = np.array([0, -1])
      bounce = True
    elif self.x < -(WIDTH / 2 - self.radius): # left
      n = np.array([1, 0])
      bounce = True
    elif self.x > (WIDTH / 2 - self.radius): # right
      n = np.array([-1, 0])
      bounce = True
      
    if bounce:
      # https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector
      # self.u: current direction as a unit vector
      # n: unit vector orthogonal to the "wall" (i.e., the end of the frame)
      new_u = np.array(self.u) - 2 * (np.dot(self.u, n)) * n
      self.u = new_u.tolist()
  
  def update_life(self, pop):
    if self.time_life > self.max_time:
      self.alive = False
      return False
    
    if self.time_life > self.min_for_procreate:
      self.radius = RADIUS_ADULT    
    else:
      self.radius = RADIUS_YOUNG
  
    if self.sexFemale:
      if not self.is_of_age():
        return False
      
      if self.count_pregnancy > self.max_num_pregnancy:
        return False
      
      if self.time_life > MAX_TIME_PREGNANCY:
        return False
        
      if self.time_pregnant > self.length_pregnancy:
        self.time_pregnant = 0
        return True # give birth
      
      if self.time_pregnant > 0:
        self.time_pregnant = self.time_pregnant + SIMULATION_STEP_TIME
        return False
      
      # proximity to a male of age
      for ix in pop:
        if not ix.sexFemale and ix.is_of_age() and self.get_distance(ix) < 2 * self.radius:
          if np.random.random() < CHANCE_OFFSPRING:
            self.time_pregnant = SIMULATION_STEP_TIME
            self.count_pregnancy = self.count_pregnancy + 1
            return False

    return False
  
def get_random_individual(initial_time):
  sexFemale = np.random.rand() <= PERC_FEMALE
  x = 0 #rndfact() * np.random.randint(0, math.floor(WIDTH / 3))
  y = 0 #rndfact() * np.random.randint(0, math.floor(HEIGHT / 3))
  u = [rndfact() * np.random.random(), rndfact() * np.random.rand()] # random direction
  max_time = np.random.normal(AVG_LIFE_YEARS, STD_LIFE_YEARS) * 12
  return Individual(initial_time, sexFemale, x, y, u, max_time)

#
# MAIN
#

def run_sim():
  pygame.init()
  win = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Population simulation")
  font = pygame.font.SysFont("arial", 20)
  clock = pygame.time.Clock()

  pop = []
  run = True
  months = 12 * 17 # start from a more interesting point
  for i in range(POP_SIZE):
    ix = get_random_individual(months)
    pop.append(ix)

  while run:
    clock.tick(100)
    win.fill(pygame.Color(BG_COLOR))
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    if len(pop) > 0:
      months = months + SIMULATION_STEP_TIME

      # population
      pop2 = []
      for ix in pop:
        ix.update_position()
        if ix.update_life(pop):
          ix2 = get_random_individual(0)
          ix2.x = ix.x # set it close to the mother
          ix2.y = ix.y
          pop2.append(ix2)
        ix.draw(win)

      pop = [ix for ix in pop if ix.alive] + pop2 # keep only the alive ones and add the new offsprings

    # statistics
    text = font.render('Years: ' + str(math.floor(months / 12)) + ', Month: ' + str((math.floor(months) % 12) + 1), True, pygame.Color(TEXT_COLOR), pygame.Color(TEXT_BG_COLOR))
    win.blit(text, (0, 0 * font.get_height()))
    text = font.render('Size: ' + str(len(pop)), True, pygame.Color(TEXT_COLOR), pygame.Color(TEXT_BG_COLOR))
    win.blit(text, (0, 1 * font.get_height()))
    if len(pop) > 0:
      text = font.render('Of age: ' + str(len([ix for ix in pop if ix.is_of_age()])), True, pygame.Color(TEXT_COLOR), pygame.Color(TEXT_BG_COLOR))
      win.blit(text, (0, 2 * font.get_height()))
      text = font.render('Female %: ' + str(math.floor(len([ix for ix in pop if ix.sexFemale]) * 100 / len(pop))), True, pygame.Color(TEXT_COLOR), pygame.Color(TEXT_BG_COLOR))
      win.blit(text, (0, 2 * font.get_height()))
      #text = font.render('Pregnant: ' + str(len([ix for ix in pop if ix.is_pregnant()])), True, pygame.Color(TEXT_COLOR), pygame.Color(TEXT_BG_COLOR))
      #win.blit(text, (0, 3 * font.get_height()))

    pygame.display.update()

  pygame.quit()

if __name__ == "__main__":
  run_sim()