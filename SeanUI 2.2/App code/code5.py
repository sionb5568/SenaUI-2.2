import pygame
import sys
from datetime import datetime
import math

pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY2 = ( 106, 108, 109)
WINDOW_COLOR = (169, 169, 169)
BAR_COLOR = (105, 105, 105)
BUTTON_COLOR = (255, 0, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Clock")


small_font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 24)


window_width = 800
window_height = 600
bar_height = 30
corner_radius = 5
button_width = 60
button_height = 20

window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

background_image_path = 'background image/background.PNG'  
inner_image_path = 'Clock App image/IMG_8504.png'  

try:
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    background_image = pygame.transform.flip(background_image, True, False)  # 좌우 반전

    inner_image = pygame.image.load(inner_image_path).convert_alpha()
    inner_image = pygame.transform.scale(inner_image, (window_width, window_height - bar_height))
except pygame.error:
    print("Error loading images. Make sure the paths are correct.")
    pygame.quit()
    sys.exit()


def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def render_button(surface, text, x, y, width, height, radius):
    button_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(surface, BUTTON_COLOR, button_rect, radius)
    text_surface = button_font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)
    return button_rect


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_clock(surface, x, y, radius):
    now = datetime.now()
    seconds_angle = (now.second / 60.0) * 360
    minutes_angle = ((now.minute + now.second / 60.0) / 60.0) * 360
    hours_angle = ((now.hour % 12 + now.minute / 60.0) / 12.0) * 360

    pygame.draw.circle(surface, WHITE, (x, y), radius)
    pygame.draw.circle(surface, GRAY2, (x, y), radius, 7)

    for i in range(12):
        angle = math.radians(i * 30)
        x1 = x + math.cos(angle) * (radius - 10)
        y1 = y + math.sin(angle) * (radius - 10)
        x2 = x + math.cos(angle) * (radius - 20)
        y2 = y + math.sin(angle) * (radius - 20)
        pygame.draw.line(surface, BLACK, (x1, y1), (x2, y2), 4)


    hour_angle_rad = math.radians(hours_angle - 90)
    hour_x = x + math.cos(hour_angle_rad) * (radius * 0.5)
    hour_y = y + math.sin(hour_angle_rad) * (radius * 0.5)
    pygame.draw.line(surface, BLACK, (x, y), (hour_x, hour_y), 6)


    minute_angle_rad = math.radians(minutes_angle - 90)
    minute_x = x + math.cos(minute_angle_rad) * (radius * 0.75)
    minute_y = y + math.sin(minute_angle_rad) * (radius * 0.75)
    pygame.draw.line(surface, BLACK, (x, y), (minute_x, minute_y), 4)


    second_angle_rad = math.radians(seconds_angle - 90)
    second_x = x + math.cos(second_angle_rad) * (radius * 0.85)
    second_y = y + math.sin(second_angle_rad) * (radius * 0.85)
    pygame.draw.line(surface, RED, (x, y), (second_x, second_y), 2)


dragging = False
offset_x = 0
offset_y = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if window_x <= mouse_pos[0] <= window_x + window_width and window_y <= mouse_pos[1] <= window_y + bar_height:
                dragging = True
                offset_x = window_x - mouse_pos[0]
                offset_y = window_y - mouse_pos[1]
            elif quit_button.collidepoint(mouse_pos):  
                running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = event.pos
                window_x = mouse_pos[0] + offset_x
                window_y = mouse_pos[1] + offset_y

    screen.blit(background_image, (0, 0))

    pygame.draw.rect(screen, WINDOW_COLOR, (window_x, window_y, window_width, window_height))
    pygame.draw.rect(screen, BAR_COLOR, (window_x, window_y, window_width, bar_height))
    pygame.draw.circle(screen, BAR_COLOR, (window_x + corner_radius, window_y + bar_height // 2), corner_radius)
    pygame.draw.circle(screen, BAR_COLOR, (window_x + window_width - corner_radius, window_y + bar_height // 2), corner_radius)
    screen.blit(inner_image, (window_x, window_y + bar_height))

    quit_button = render_button(screen, "Quit", screen_width - button_width - 10, 10, button_width, button_height, corner_radius)

    draw_clock(screen, window_x + window_width // 2, window_y + window_height // 3, 100)


    current_time_str = datetime.now().strftime("Seoul %H:%M:%S")
    draw_text(current_time_str, small_font, WHITE, screen, window_x + window_width // 2, window_y + window_height // 2 + 100)

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
