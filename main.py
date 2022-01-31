import pygame
from random import randint
from geneticAlgorithm import GeneticSearch


WIDTH = 288
HEIGHT = 512
FPS = 30
POPULATION_SIZE = 100
MAX_UP_SPEED = -9
MAX_DOWN_SPEED = 15
PIPE_SPEED = -4

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
birds = []
pipes = []
fitness = []
generation = 1
birds_alive_num = POPULATION_SIZE
solutions = GeneticSearch(POPULATION_SIZE,0.8,0.08,[3,4,1])
bg = pygame.image.load("sprites/background.png")
bird_image = pygame.image.load("sprites/bird_down.png")
lower_pipe_image = pygame.image.load("sprites/pipe.png")
upper_pipe_image = pygame.transform.rotate(pygame.image.load("sprites/pipe.png"),180)
ground = pygame.image.load("sprites/base.png")
ground_x = 0
ground_y = HEIGHT-112
pipe_count = 0
allow_to_count = True
myfont = pygame.font.SysFont('Comic Sans Ms', 16)
myfont2 = pygame.font.SysFont('Comic Sans Ms', 35)

for i in range(POPULATION_SIZE):
    birds.append({'x': 75, 'y': HEIGHT//3, 'alive': True, 'color':(randint(0,255),randint(0,255),randint(0,255)), 'speed_y': 0})

for i in range(3):
    rand_size = randint(50,242)
    if i == 0:
        pipes.append(({'x': WIDTH, 'y': 0, 'width': 52, 'height': rand_size},{'x': WIDTH, 'y': rand_size+100, 'width': 52, 'height': HEIGHT-(rand_size+100)}))
    else:
        pipes.append(({'x': pipes[i-1][0]['x'] + 175, 'y': 0, 'width': 52, 'height': rand_size},{'x': pipes[i-1][0]['x'] + 175, 'y': rand_size+100, 'width': 52, 'height': HEIGHT-(rand_size+100)}))

for i in range(POPULATION_SIZE):
    fitness.append(1)

def restart():
    global birds, birds_alive_num, pipe_count, allow_to_count
    birds_alive_num = POPULATION_SIZE
    pipe_count = 0
    allow_to_count = True
    for i in range(len(birds)):
        birds[i]['y'] = HEIGHT//3
        birds[i]['alive'] = True
        birds[i]['speed_y'] = 0
    for i in range(POPULATION_SIZE):
        fitness[i] = 1
    pipes.clear()
    for i in range(3):
        rand_size = randint(50,242)
        if i == 0:
            pipes.append(({'x': WIDTH, 'y': 0, 'width': 52, 'height': rand_size},{'x': WIDTH, 'y': rand_size+100, 'width': 52, 'height': HEIGHT-(rand_size+100)}))
        else:
            pipes.append(({'x': pipes[i-1][0]['x'] + 175, 'y': 0, 'width': 52, 'height': rand_size},{'x': pipes[i-1][0]['x'] + 175, 'y': rand_size+100, 'width': 52, 'height': HEIGHT-(rand_size+100)}))


def birds_alive():
    global birds

    for bird in birds:
        if bird['alive']:
            return True
    return False

def colision_bird():
    global birds, pipes

    for i in range(len(birds)):
        if birds[i]['y'] < -20 or birds[i]['y'] >= 372:
            birds[i]['alive'] = False
            continue
        for pipe in pipes:
            if pipe[0]['hitbox'].colliderect(birds[i]['hitbox']) or pipe[1]['hitbox'].colliderect(birds[i]['hitbox']):
                birds[i]['alive'] = False                                                                                            

def colision_pixel(bird,pipe):
    if (pipe['x'] < bird['x']-40 < (pipe['x'] + pipe['width'])) and (pipe['y'] < bird['y']-40 < (pipe['y'] + pipe['height'])):
        return True
    return False
    


running = True
while running:
    #inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    #inputs
    #update
            
    population = solutions.getPopulation()
    for i in range(len(population)):
        inputs = []
        if birds[i]['x'] > pipes[0][0]['x'] + pipes[0][0]['width']:
            inputs.append(((pipes[1][0]['y'] + pipes[1][0]['height'] + 50) - birds[i]['y'])/HEIGHT)
            inputs.append((pipes[1][0]['x'] - birds[i]['x'])/WIDTH)
            inputs.append(birds[i]['speed_y']/MAX_DOWN_SPEED)
        else:
            inputs.append(((pipes[0][0]['y'] + pipes[0][0]['height'] + 50) - birds[i]['y'])/HEIGHT)
            inputs.append((pipes[0][0]['x'] - birds[i]['x'])/HEIGHT)
            inputs.append(birds[i]['speed_y']/MAX_DOWN_SPEED)   
        if birds[i]['alive']:
            if population[i].feedForward(inputs)[0] >= 0.5:
                birds[i]['speed_y'] = MAX_UP_SPEED
                bird_image = pygame.image.load("sprites/bird_up.png")
            else:
                bird_image = pygame.image.load("sprites/bird_down.png")
            if birds[i]['speed_y'] < MAX_DOWN_SPEED:
                birds[i]['speed_y']+=1
            birds[i]['y']+=birds[i]['speed_y']
            fitness[i]+=1
    for i in range(len(pipes)):
        pipes[i][0]['x'] += PIPE_SPEED
        pipes[i][1]['x'] += PIPE_SPEED
    if pipes[0][0]['x'] <= -52:
        rand_size = randint(50,242)
        pipes.pop(0)
        allow_to_count = True
        pipes.append(({'x': pipes[1][0]['x'] + 175, 'y': 0, 'width': 50, 'height': rand_size},{'x': pipes[1][0]['x'] + 175, 'y': rand_size+100, 'width': 50, 'height': HEIGHT-(rand_size+100)}))
    if ground_x <= -48:
        ground_x = 0
    else:
        ground_x+=PIPE_SPEED
    for bird in birds:
        if not bird['alive']:
            birds_alive_num-=1
    for bird in birds:
        if bird['alive'] and bird['x'] > pipes[0][0]['x'] + 26 and allow_to_count:
            allow_to_count = False
            pipe_count+=1
            break
            
            
            
    #draw
    #screen.fill((255,255,255))
    textSurface1 = myfont.render('Generation : %i'%generation, False, (0,0,255))
    textSurface2 = myfont.render('Birds Alive : %i'%birds_alive_num, False, (0,0,255))
    textSurface3 = myfont2.render('%i'%pipe_count, False, (255,255,255))
    screen.blit(bg,(0,0))
    for i in range(len(birds)):
        if birds[i]['alive']:
            bird_hitbox = bird_image.get_rect()
            bird_hitbox.left, bird_hitbox.top = birds[i]['x'] , birds[i]['y']
            birds[i]['hitbox'] = bird_hitbox#pygame.draw.rect(screen,birds[i]['color'],[birds[i]['x']-10,birds[i]['y']-10,20,20])
            screen.blit(bird_image,birds[i]['hitbox'])
    for i in range(len(pipes)):
        upper_pipe_hitbox = upper_pipe_image.get_rect()
        lower_pipe_hitbox = lower_pipe_image.get_rect()
        upper_pipe_hitbox.left, upper_pipe_hitbox.top = pipes[i][0]['x'], -320 + pipes[i][0]['height']
        lower_pipe_hitbox.left, lower_pipe_hitbox.top = pipes[i][1]['x'], pipes[i][1]['y']
        pipes[i][0]['hitbox'] = upper_pipe_hitbox
        pipes[i][1]['hitbox'] = lower_pipe_hitbox
        screen.blit(upper_pipe_image, pipes[i][0]['hitbox'])
        screen.blit(lower_pipe_image, pipes[i][1]['hitbox'])
        #for j in range(len(pipes[i])):
            #pipe_hitbox = pipe_image.get_rect()
            #pipe_hitbox.left, pipe_hitbox.top = pipes[i][j]['x'], pipes[i][j]['y']
            #pipes[i][j]['hitbox'] =  pipe_hitbox#pygame.draw.rect(screen,(0,255,0),[pipes[i][j]['x'],pipes[i][j]['y'],pipes[i][j]['width'],pipes[i][j]['height']])
            #screen.blit(pipe_image,pipes[i][j]['hitbox'])
    #pygame.draw.rect(screen,(0,200,0),[0,HEIGHT-120,WIDTH,HEIGHT-(HEIGHT-120)])
    screen.blit(ground,(ground_x,ground_y))
    screen.blit(textSurface1,(5,HEIGHT - 90))
    screen.blit(textSurface2,(5,HEIGHT - 70))
    screen.blit(textSurface3,(144 - textSurface3.get_width() // 2,20))
    birds_alive_num = POPULATION_SIZE
    colision_bird()
    if not birds_alive():
        generation+=1
        solutions.evolution(fitness.copy())
        restart()
        continue
    
    pygame.display.update()
    clock.tick(FPS)

    
pygame.quit()