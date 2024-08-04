import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 1920, 1080
TOOLBAR_HEIGHT = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Drawing")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)


screen.fill(WHITE)
pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
drawing = False
last_pos = None
color = BLACK
radius = 5
tool = 'pen' 


def draw_line(screen, start, end, color, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(screen, color, (x, y), radius)

def draw_rounded_rect(surface, color, rect, radius):
  
    rect_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    

    pygame.draw.rect(rect_surf, color, (0, 0, rect.width, rect.height), border_radius=radius)
    
    
    surface.blit(rect_surf, rect.topleft)

def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    pygame.draw.circle(screen, BLACK, (25, 25), 10)
    pygame.draw.line(screen, WHITE, (15, 15), (35, 35), 5)

    pygame.draw.circle(screen, BLACK, (75, 25), 10)

    pygame.draw.rect(screen, RED, (120, 10, 30, 30))

    pygame.draw.rect(screen, GREEN, (160, 10, 30, 30))

    pygame.draw.rect(screen, BLUE, (200, 10, 30, 30))

    pygame.draw.rect(screen, YELLOW, (240, 10, 30, 30))

    pygame.draw.rect(screen, PURPLE, (280, 10, 30, 30))

    pygame.draw.rect(screen, ORANGE, (320, 10, 30, 30))

    pygame.draw.rect(screen, BLACK, (360, 10, 30, 30), 2)
    pygame.draw.rect(screen, BLACK, (400, 10, 30, 30), 2)
    font = pygame.font.SysFont(None, 24)
    text_plus = font.render('+', True, BLACK)
    text_minus = font.render('--', True, BLACK)
    screen.blit(text_plus, (370, 15))
    screen.blit(text_minus, (410, 15))
    

    pygame.draw.rect(screen, BLACK, (440, 10, 30, 30), 2)
    text_clear = font.render('x', True, BLACK)
    screen.blit(text_clear, (450, 15))

  
    quit_rect = pygame.Rect(WIDTH - 100, 10, 80, 30)
    draw_rounded_rect(screen, RED, quit_rect, 15)
    font = pygame.font.SysFont(None, 24)
    text_quit = font.render('Quit', True, WHITE)
    screen.blit(text_quit, (WIDTH - 85, 15))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y <= TOOLBAR_HEIGHT: 
                if 10 <= x <= 40:
                    tool = 'eraser'
                    color = WHITE
                elif 60 <= x <= 90:
                    tool = 'pen'
                    color = BLACK
                elif 120 <= x <= 150:
                    tool = 'pen'
                    color = RED
                elif 160 <= x <= 190:
                    tool = 'pen'
                    color = GREEN
                elif 200 <= x <= 230:
                    tool = 'pen'
                    color = BLUE
                elif 240 <= x <= 270:
                    tool = 'pen'
                    color = YELLOW
                elif 280 <= x <= 310:
                    tool = 'pen'
                    color = PURPLE
                elif 320 <= x <= 350:
                    tool = 'pen'
                    color = ORANGE
                elif 360 <= x <= 390:
                    radius += 1 if radius < 10 else 0
                elif 400 <= x <= 430:
                    radius -= 1 if radius > 1 else 0 
                    screen.fill(WHITE) 
                elif WIDTH - 100 <= x <= WIDTH - 20 and 10 <= y <= 40:
                    pygame.quit()
                    sys.exit()
            else:
                drawing = True
                last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                drawing = False
                last_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if drawing and event.pos[1] > TOOLBAR_HEIGHT:
                if last_pos is not None:
                    draw_line(screen, last_pos, event.pos, color, radius)
                last_pos = event.pos

    draw_toolbar()
    pygame.display.flip()
