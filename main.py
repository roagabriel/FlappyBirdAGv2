from platform import architecture
import pygame
from random import randint
from geneticAlgorithm import GeneticSearch
from swarmIntelligence import SwarmIntelligence
from AntColonyOptmization import AntColonyOptmization
from plot import plotNeuralNetwork
import matplotlib.pyplot as plt

GAME_MODE = 0 # 0: Classic // 1: Vertical moviment for pipes
SEARCH_MODE = 0 # 0: AG // 1: PSO // 2: ACO
FPS = 1200 # Define how much fast is the game
""" Global Variables """
#-----------------------------------------------------------
# NN variables 
ARCHITECTURE = [3,3,4,1]
POPULATION_SIZE = 100
FITNESS = []
GENERATION = 1
# GA variables
CROSSOVER_RATE = 0.8
MUTATION_RATE_GA = 0.08

# PSO variables
C1_PARAM = 1.5              # cognitive factor
C2_PARAM = 4.1 - C1_PARAM   # social factor
W_PARAM = 1/2*(C1_PARAM+C2_PARAM)-1 # inertial weight
MUTATION_RATE_PSO = 0.08

# ACO variables
ELITIMS = 2             # how many of the best individuals to keep from one generation to the next
TAU_INICIAL = 10**(-12)         # initial pheromone value
ALPHA = 1              # pheromone sensitivity
RHO_GLOBAL = 0.1        # global pheromone decay rate
RHO_LOCAL = 0.5         # local pheromone decay rate
UPDATE_GAIN = 1       # pheromonone update constant
EXPLORATION_RATE = 1    # exploration constant
MUTATION_RATE_ACO = 0.08
MAXPARVALUE = 60000 
MINPARVALUE = -60000
MESH = 10
if SEARCH_MODE == 0:
    NEURAL_NETWORK = GeneticSearch(
        POPULATION_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE_GA,
        ARCHITECTURE
    )
if SEARCH_MODE == 1:
    NEURAL_NETWORK = SwarmIntelligence(
        POPULATION_SIZE,
        C1_PARAM,
        C2_PARAM,
        W_PARAM,
        MUTATION_RATE_PSO,
        ARCHITECTURE
    )
if SEARCH_MODE == 2:
    NEURAL_NETWORK = AntColonyOptmization(
        POPULATION_SIZE,
        ELITIMS,
        TAU_INICIAL,
        ALPHA,
        RHO_GLOBAL,
        RHO_LOCAL,
        UPDATE_GAIN,
        EXPLORATION_RATE,
        MAXPARVALUE,
        MINPARVALUE,
        MESH,
        MUTATION_RATE_ACO,
        ARCHITECTURE
    )    
#-----------------------------------------------------------
# Game Variables
WIDTH = 288
HEIGHT = 512
MAX_UP_SPEED = -9
MAX_DOWN_SPEED = 15
PIPE_SPEED = -4
ALLOW_TO_COUNT = True

BIRDS = []
PIPES = []
RARY = 1
BIRDS_ALIVE_NUM = POPULATION_SIZE

GROUND_X = 0
GROUND_Y = HEIGHT-112
PIPE_COUNT = 0
LIST_PIPE_COUNT = []
MAX_PIPE_COUNT = 0
LIST_MAX_PIPE_COUNT = []

pygame.init()
pygame.font.init()
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()


BACKGROUND = pygame.image.load("sprites/background.png")
BIRD = pygame.image.load("sprites/bird_down.png")
LOWER_PIPE = pygame.image.load("sprites/pipe.png")
UPPER_PIPE = pygame.transform.rotate(pygame.image.load("sprites/pipe.png"),180)
GROUND = pygame.image.load("sprites/base.png")


MYFONT = pygame.font.SysFont('Comic Sans Ms', 16)
MYFONT2 = pygame.font.SysFont('Comic Sans Ms', 35)

def evaluate():
    global BIRDS, FITNESS, PIPES, GENERATION, PIPE_COUNT, LIST_PIPE_COUNT, MAX_PIPE_COUNT, LIST_MAX_PIPE_COUNT, GROUND_X, GROUND_Y, BIRDS_ALIVE_NUM, ALLOW_TO_COUNT, RARY

    for i in range(POPULATION_SIZE):
        BIRDS.append({
            'x': 75,
            'y': HEIGHT//3,
            'alive': True,
            'color':(randint(0,255),randint(0,255),randint(0,255)),
            'speed_y': 0
        })
        FITNESS.append(1)

    for i in range(3):
        rand_size = randint(50,242)
        if i == 0:
            PIPES.append(({
                'x': WIDTH,
                'y': 0,
                'width': 52,
                'height': rand_size,
                'rary': RARY},
                {
                'x': WIDTH,
                'y': rand_size+100,
                'width': 52,
                'height': HEIGHT-(rand_size+100),
                'rary': RARY
            }))
            RARY += 1
        else:
            PIPES.append(({
                'x': PIPES[i-1][0]['x'] + 175,
                'y': 0,
                'width': 52,
                'height': rand_size,
                'rary': RARY},
                {
                'x': PIPES[i-1][0]['x'] + 175,
                'y': rand_size+100,
                'width': 52,
                'height': HEIGHT-(rand_size+100),
                'rary': RARY
            }))
            RARY += 1


    def restart():
        global BIRDS, BIRDS_ALIVE_NUM, PIPE_COUNT, ALLOW_TO_COUNT, RARY

        BIRDS_ALIVE_NUM = POPULATION_SIZE
        PIPE_COUNT = 0
        RARY = 1
        ALLOW_TO_COUNT = True

        for i in range(len(BIRDS)):
            BIRDS[i]['y'] = HEIGHT//3
            BIRDS[i]['alive'] = True
            BIRDS[i]['speed_y'] = 0

        for i in range(POPULATION_SIZE):
            FITNESS[i] = 1

        PIPES.clear()
        for i in range(3):
            rand_size = randint(50,242)
            if i == 0:
                PIPES.append(({
                    'x': WIDTH,
                    'y': 0,
                    'width': 52,
                    'height': rand_size,
                    'rary': RARY},
                    {
                    'x': WIDTH,
                    'y': rand_size+100,
                    'width': 52,
                    'height': HEIGHT-(rand_size+100),
                    'rary': RARY
                }))
                RARY += 1
            else:
                PIPES.append(({
                    'x': PIPES[i-1][0]['x'] + 175,
                    'y': 0,
                    'width': 52,
                    'height': rand_size,
                    'rary': RARY},
                    {
                    'x': PIPES[i-1][0]['x'] + 175,
                    'y': rand_size+100,
                    'width': 52,
                    'height': HEIGHT-(rand_size+100),
                    'rary': RARY
                }))
                RARY += 1


    def birds_alive():
        global BIRDS

        for bird in BIRDS:
            if bird['alive']:
                return True
        return False


    def colision_bird():
        global BIRDS, PIPES

        for i in range(len(BIRDS)):
            if BIRDS[i]['y'] < -20 or BIRDS[i]['y'] >= 372:
                BIRDS[i]['alive'] = False
                continue
            for pipe in PIPES:
                if pipe[0]['hitbox'].colliderect(BIRDS[i]['hitbox']) or pipe[1]['hitbox'].colliderect(BIRDS[i]['hitbox']):
                    BIRDS[i]['alive'] = False                                                                                            

    
    def colision_pixel(bird,pipe):
        if (pipe['x'] < bird['x']-40 < (pipe['x'] + pipe['width'])) and (pipe['y'] < bird['y']-40 < (pipe['y'] + pipe['height'])):
            return True
        return False
    [3,4,1]
    
    def printNN(NeuralNetwork):
         for i in range(1,len(ARCHITECTURE)): 
            for j in range(ARCHITECTURE[i]):    
                for k in range(ARCHITECTURE[i-1]): 
                    print(f'w({i-1},{j},{k}) = {NeuralNetwork.getNetwork()[i-1][j][k]}')
                    

    plt.ion()
    fig = plt.figure(figsize=(8, 6), dpi=120)
    ax = fig.add_subplot(111)
    multi = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            
        population = NEURAL_NETWORK.getPopulation()
        for i in range(len(population)):
            inputs = []
            #inputs   
            if BIRDS[i]['x'] > PIPES[0][0]['x'] + PIPES[0][0]['width']:
                inputs.append(((PIPES[1][0]['y'] + PIPES[1][0]['height'] + 50) - BIRDS[i]['y'])/HEIGHT)     # distance y between the bird and center gap of the pipe
                inputs.append((PIPES[1][0]['x'] - BIRDS[i]['x'])/WIDTH)                                     # distance x between the bird and the pipe
                inputs.append(BIRDS[i]['speed_y']/MAX_DOWN_SPEED)                                           # normalized y-speed                  
            else:
                inputs.append(((PIPES[0][0]['y'] + PIPES[0][0]['height'] + 50) - BIRDS[i]['y'])/HEIGHT)     # distance y between the bird and center gap of the pipe
                inputs.append((PIPES[0][0]['x'] - BIRDS[i]['x'])/HEIGHT)                                    # distance x between the bird and the pipe
                inputs.append(BIRDS[i]['speed_y']/MAX_DOWN_SPEED)                                           # normalized y-speed 

            #update
            if BIRDS[i]['alive']:
                if population[i].feedForward(inputs)[0] >= 0.5:
                    BIRDS[i]['speed_y'] = MAX_UP_SPEED
                    BIRD = pygame.image.load("sprites/bird_up.png")
                else:
                    BIRD = pygame.image.load("sprites/bird_down.png")
                if BIRDS[i]['speed_y'] < MAX_DOWN_SPEED:
                    BIRDS[i]['speed_y']+=1
                BIRDS[i]['y']+=BIRDS[i]['speed_y']
                FITNESS[i]+=1

        
        for i in range(len(PIPES)):
            PIPES[i][0]['x'] += PIPE_SPEED
            PIPES[i][1]['x'] += PIPE_SPEED
            if GAME_MODE == 1:
                if PIPES[i][0]['rary'] % 2 == 0:
                    if PIPES[i][0]['height'] < 50:
                        multi = -1
                    if PIPES[i][0]['height'] > 242:
                        multi = 1
                    PIPES[i][0]['height'] += multi*PIPE_SPEED/2
                    PIPES[i][1]['y'] += multi*PIPE_SPEED/2
                if PIPES[i][0]['rary'] % 2 -1 == 0:
                    if PIPES[i][0]['height'] < 50:
                        multi = 1
                    if PIPES[i][0]['height'] > 242:
                        multi = -1
                    PIPES[i][0]['height'] -= multi*PIPE_SPEED/2
                    PIPES[i][1]['y'] -= multi*PIPE_SPEED/2 


        if PIPES[0][0]['x'] <= -52:
            rand_size = randint(50,242)
            PIPES.pop(0)
            ALLOW_TO_COUNT = True
            PIPES.append(({
                'x': PIPES[1][0]['x'] + 175,
                'y': 0,
                'width': 50,
                'height': rand_size,
                'rary': RARY},
                {
                'x': PIPES[1][0]['x'] + 175,
                'y': rand_size+100,
                'width': 50,
                'height': HEIGHT-(rand_size+100),
                'rary': RARY
            }))
            RARY += 1

        if GROUND_X <= -48:
            GROUND_X = 0
        else:
            GROUND_X+=PIPE_SPEED

        for bird in BIRDS:
            if not bird['alive']:
                BIRDS_ALIVE_NUM-=1

        for bird in BIRDS:
            if bird['alive'] and bird['x'] > PIPES[0][0]['x'] + 26 and ALLOW_TO_COUNT:
                ALLOW_TO_COUNT = False
                PIPE_COUNT+=1
                break
                
                
        #draw
        if SEARCH_MODE == 0:
            textSurface5 = MYFONT.render('Trainer: AG', False, (0,0,255))
            textSurface1 = MYFONT.render('Generation: %i'%GENERATION, False, (0,0,255))  
        if SEARCH_MODE == 1:
            textSurface5 = MYFONT.render('Trainer: PSO', False, (0,0,255))
            textSurface1 = MYFONT.render('Iteracion: %i'%GENERATION, False, (0,0,255))
        if SEARCH_MODE == 2:
            textSurface5 = MYFONT.render('Trainer: ACO', False, (0,0,255))
            textSurface1 = MYFONT.render('Generation: %i'%GENERATION, False, (0,0,255))
        textSurface2 = MYFONT.render('Birds Alive: %i'%BIRDS_ALIVE_NUM, False, (0,0,255))
        textSurface3 = MYFONT2.render('%i'%PIPE_COUNT, False, (255,255,255))
        textSurface4 = MYFONT.render('Max pipe count: %i'%MAX_PIPE_COUNT, False, (0,0,255))
        SCREEN.blit(BACKGROUND,(0,0))

        for i in range(len(BIRDS)):
            if BIRDS[i]['alive']:
                bird_hitbox = BIRD.get_rect()
                bird_hitbox.left, bird_hitbox.top = BIRDS[i]['x'] , BIRDS[i]['y']
                BIRDS[i]['hitbox'] = bird_hitbox    #pygame.draw.rect(SCREEN,BIRDS[i]['color'],[BIRDS[i]['x']-10,BIRDS[i]['y']-10,20,20])
                SCREEN.blit(BIRD,BIRDS[i]['hitbox'])

        for i in range(len(PIPES)):
            upper_pipe_hitbox = UPPER_PIPE.get_rect()
            lower_pipe_hitbox = LOWER_PIPE.get_rect()
            upper_pipe_hitbox.left, upper_pipe_hitbox.top = PIPES[i][0]['x'], -320 + PIPES[i][0]['height']
            lower_pipe_hitbox.left, lower_pipe_hitbox.top = PIPES[i][1]['x'], PIPES[i][1]['y']
            PIPES[i][0]['hitbox'] = upper_pipe_hitbox
            PIPES[i][1]['hitbox'] = lower_pipe_hitbox
            SCREEN.blit(UPPER_PIPE, PIPES[i][0]['hitbox'])
            SCREEN.blit(LOWER_PIPE, PIPES[i][1]['hitbox'])
            
        SCREEN.blit(GROUND,(GROUND_X,GROUND_Y))
        SCREEN.blit(textSurface5,(5,HEIGHT - 90))
        SCREEN.blit(textSurface1,(5,HEIGHT - 70))
        SCREEN.blit(textSurface2,(5,HEIGHT - 50))
        SCREEN.blit(textSurface3,(144 - textSurface3.get_width() // 2,20))
        SCREEN.blit(textSurface4,(5,HEIGHT - 30))

        BIRDS_ALIVE_NUM = POPULATION_SIZE
        colision_bird()
        
        if not birds_alive():
            if MAX_PIPE_COUNT < PIPE_COUNT:
                MAX_PIPE_COUNT = PIPE_COUNT
            LIST_MAX_PIPE_COUNT.append(MAX_PIPE_COUNT)
            LIST_PIPE_COUNT.append(PIPE_COUNT)

            ax.plot(range(0,GENERATION),LIST_MAX_PIPE_COUNT, color='blue', linewidth=2, label='Best all')
            ax.plot(range(0,GENERATION),LIST_PIPE_COUNT, color='black', linewidth=2, label='Progression')
            ax.grid(True)
            fig.canvas.draw()
            fig.canvas.flush_events()
            ax.set_xlim(left=0, right=GENERATION+1)
            ax.set_xlabel('Generation')
            ax.set_ylabel('Pipe count')
            ax.set_title('Best bird progression')
            ax.legend()
            fig.show()
            plt.pause(0.05)

            GENERATION+=1
            NEURAL_NETWORK.evolution(FITNESS.copy())
            restart()
            try:
                for line in ax.lines:
                    line.remove()
            except:
                next
            try:
                for collection in ax.collections:
                    collection.remove()
            except:
                next
            
            continue
        
        pygame.display.update()
        clock.tick(FPS)
    
    print("Best NN:")
    printNN(NEURAL_NETWORK.BestGlobal)
    print(f"Fitness for best global: {NEURAL_NETWORK.BestGlobalFitness}")
    print(f"Generations: {GENERATION}")


if __name__ == "__main__":
    evaluate()
    pygame.quit()