import pygame
import sys
from pygame.locals import *


pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LINE_COLOR = (230, 230, 230)
ORANGE = (255, 165, 0)
TRANSPARENT_ORANGE = (255, 165, 0, 128)
WINDOW_COLOR = (169, 169, 169)  
BAR_COLOR = (105, 105, 105)  
BUTTON_COLOR = (255, 0, 0)  
BUTTON_TEXT_COLOR = (255, 255, 255) 

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Notes")


window_width = 800
window_height = 600
bar_height = 30
button_width = 60  
button_height = 20  
corner_radius = 5  


window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2


font_size = 24
font = pygame.font.Font(None, font_size)
button_font = pygame.font.Font(None, font_size)


background_image_path = 'background image/background.PNG'  
background_image = pygame.image.load(background_image_path).convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_image = pygame.transform.flip(background_image, True, False)  


inner_image_path = 'background image/background.PNG'  
inner_image = pygame.image.load(inner_image_path).convert_alpha()
inner_image = pygame.transform.scale(inner_image, (window_width, window_height - bar_height))


input_box = pygame.Rect(50, 50, window_width - 100, window_height - 100)
color_inactive = GRAY
color_active = BLACK
color = color_inactive
active = False
text = ''


menu_items = ["Notes", "SeanUI"]
menu_rects = [pygame.Rect(i * 100 + 300, 10, 100, 20) for i in range(len(menu_items))]

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def render_button(surface, text, x, y, width, height, radius):
    button_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(surface, BUTTON_COLOR, button_rect, radius)
    text_surface = button_font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)
    return button_rect

def draw_textbox():
    window_surface = pygame.Surface((window_width, window_height))
    window_surface.fill(WHITE)
    draw_lines(window_surface)
    draw_text(window_surface)
    draw_menu_bar(window_surface)
    for i, item in enumerate(menu_items):
        item_surface = font.render(item, True, BLACK)
        text_rect = item_surface.get_rect(center=(menu_rects[i].centerx, menu_rects[i].centery))
        window_surface.blit(item_surface, text_rect)
    pygame.draw.rect(window_surface, color, input_box, 2)
    screen.blit(window_surface, (window_x, window_y + bar_height))

def draw_menu_bar(surface):
    menu_bar_width = window_width - 400
    menu_bar_height = 30
    menu_bar_x = 200
    menu_bar_y = 5
    menu_bar = pygame.Surface((menu_bar_width, menu_bar_height), pygame.SRCALPHA)
    pygame.draw.rect(menu_bar, TRANSPARENT_ORANGE, menu_bar.get_rect(), border_radius=15)
    surface.blit(menu_bar, (menu_bar_x, menu_bar_y))

def draw_lines(surface):
    line_height = 40  
    for y in range(input_box.y, input_box.y + input_box.height, line_height):
        pygame.draw.line(surface, LINE_COLOR, (input_box.x, y), (input_box.x + input_box.width, y))

def draw_text(surface):
    lines = text.splitlines()  
    y_offset = input_box.y + 5  
    for line in lines:
        txt_surface = font.render(line, True, color)
        surface.blit(txt_surface, (input_box.x + 10, y_offset))
        y_offset += 40  

def new_file():
    global text
    text = ''


dragging = False
offset_x = 0
offset_y = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if window_x <= mouse_pos[0] <= window_x + window_width and window_y <= mouse_pos[1] <= window_y + bar_height:
                dragging = True
                offset_x = window_x - mouse_pos[0]
                offset_y = window_y - mouse_pos[1]
            elif quit_button.collidepoint(mouse_pos): 
                running = False
            else:
                if input_box.collidepoint(mouse_pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

                for i, rect in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos):
                        if menu_items[i] == "New":
                            new_file()
                        elif menu_items[i] == "Exit":
                            running = False

        elif event.type == MOUSEBUTTONUP:
            dragging = False
        elif event.type == MOUSEMOTION:
            if dragging:
                mouse_pos = event.pos
                window_x = mouse_pos[0] + offset_x
                window_y = mouse_pos[1] + offset_y

        if event.type == KEYDOWN:
            if active:
                if event.key == K_RETURN:
                    text += '\n'  
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                else:
                   
                    new_line = False
                    lines = text.splitlines()
                    current_line = lines[-1] if lines else ''
                    test_line = current_line + event.unicode
                    test_width, _ = font.size(test_line)
                    if test_width > input_box.width - 20:
                        new_line = True
                    if new_line:
                        text += '\n'
                    text += event.unicode


    screen.blit(background_image, (0, 0))


    window_rect = pygame.Rect(window_x, window_y, window_width, window_height)
    bar_rect = pygame.Rect(window_x, window_y, window_width, bar_height)
    pygame.draw.rect(screen, WINDOW_COLOR, window_rect)
    pygame.draw.rect(screen, BAR_COLOR, bar_rect)

    screen.blit(inner_image, (window_x, window_y + bar_height))

   
    quit_button = render_button(screen, "Quit", screen_width - button_width - 20, 20, button_width, button_height, corner_radius)

   
    draw_textbox()


    pygame.display.flip()


pygame.quit()
sys.exit()