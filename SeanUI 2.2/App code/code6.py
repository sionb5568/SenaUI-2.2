import pygame
import sys
import math


pygame.init()


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Calculator")


window_width = 400
window_height = 700
bar_height = 30
window_color = (255, 255, 255)  
bar_color = (105, 105, 105)  
button_color = (255, 0, 0)  
button_text_color = (255, 255, 255)  
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


def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_gradient_rect(surface, rect, color1, color2, radius):
    x, y, w, h = rect
    for i in range(h):
        r = int(color1[0] + (color2[0] - color1[0]) * i / h)
        g = int(color1[1] + (color2[1] - color1[1]) * i / h)
        b = int(color1[2] + (color2[2] - color1[2]) * i / h)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))
    pygame.draw.rect(surface, (0, 0, 0), rect, 1, border_radius=radius)

def render_button(surface, text, x, y, width, height, radius):
    button_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(surface, button_color, button_rect, radius)
    text_surface = button_font.render(text, True, button_text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)
    return button_rect

def draw_button(text, x, y, width, height, color1, color2, font):
    button_rect = pygame.Rect(x, y, width, height)
    draw_gradient_rect(screen, button_rect, color1, color2, corner_radius)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

dragging = False
offset_x = 0
offset_y = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
LIGHT_GREY = (220, 220, 220)
DARK_GREY = (169, 169, 169)

calc_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 35)

calc_button_width = 80
calc_button_height = 80
calc_button_margin = 10

current_input = ""
operator = ""
first_number = None
second_number = None
result = None

def draw_text(text, x, y, font):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

def calculate():
    global result, first_number, second_number, operator

    if first_number is not None and second_number is not None and operator:
        try:
            if operator == "+":
                result = first_number + second_number
            elif operator == "-":
                result = first_number - second_number
            elif operator == "×":
                result = first_number * second_number
            elif operator == "÷":
                result = first_number / second_number
            first_number = result
            second_number = None
            operator = ""
        except ZeroDivisionError:
            result = "Error"
            first_number = None
            second_number = None
            operator = ""


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
            else:
                
                for row in range(4):
                    for col in range(4):
                        x = window_x + calc_button_margin + col * (calc_button_width + calc_button_margin)
                        y = window_y + 130 + calc_button_margin + row * (calc_button_height + calc_button_margin)
                        if x < mouse_pos[0] < x + calc_button_width and y < mouse_pos[1] < y + calc_button_height:
                            button_text = buttons[row][col]

                            if button_text in "0123456789":
                                current_input += button_text
                            elif button_text in "+-×÷":
                                if current_input:
                                    first_number = float(current_input)
                                    current_input = ""
                                    operator = button_text
                            elif button_text == "=":
                                if current_input and first_number is not None:
                                    second_number = float(current_input)
                                    current_input = ""
                                    calculate()
                            elif button_text == "C":
                                current_input = ""

              
                if window_y + 180 + 4 * (calc_button_height + calc_button_margin) < mouse_pos[1] < window_y + 180 + 5 * (calc_button_height + calc_button_margin):
                    if window_x + calc_button_margin < mouse_pos[0] < window_x + calc_button_margin + 2 * calc_button_width + calc_button_margin:
                       
                        current_input = ""
                        first_number = None
                        second_number = None
                        operator = ""
                        result = None
                    elif window_x + calc_button_margin * 3 + 2 * calc_button_width < mouse_pos[0] < window_x + calc_button_margin * 3 + 3 * calc_button_width:
                    
                        current_input = current_input[:-1]
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = event.pos
                window_x = mouse_pos[0] + offset_x
                window_y = mouse_pos[1] + offset_y


    screen.blit(background_image, (0, 0))

  
    window_rect = pygame.Rect(window_x, window_y, window_width, window_height)
    bar_rect = pygame.Rect(window_x, window_y, window_width, bar_height)
    pygame.draw.rect(screen, window_color, window_rect)
    pygame.draw.rect(screen, bar_color, bar_rect)

   
    quit_button = render_button(screen, "Quit", screen_width - button_width - 20, 20, button_width, button_height, corner_radius)


    buttons = [
        ["7", "8", "9", "÷"],
        ["4", "5", "6", "×"],
        ["1", "2", "3", "-"],
        ["C", "0", "=", "+"]
    ]

    for row in range(4):
        for col in range(4):
            x = window_x + calc_button_margin + col * (calc_button_width + calc_button_margin)
            y = window_y + 130 + calc_button_margin + row * (calc_button_height + calc_button_margin)
            if buttons[row][col] in "+-×÷":
                draw_button(buttons[row][col], x, y, calc_button_width, calc_button_height, DARK_GREY, GREY, calc_font)
            else:
                draw_button(buttons[row][col], x, y, calc_button_width, calc_button_height, LIGHT_GREY, WHITE, calc_font)

    
    draw_button("AC", window_x + calc_button_margin, window_y + 180 + 4 * (calc_button_height + calc_button_margin), calc_button_width * 2 + calc_button_margin, calc_button_height, GREY, LIGHT_GREY, calc_font)
    draw_button("D", window_x + calc_button_margin * 3 + calc_button_width * 2, window_y + 180 + 4 * (calc_button_height + calc_button_margin), calc_button_width * 2 + calc_button_margin, calc_button_height, GREY, LIGHT_GREY, calc_font)

 
    display_text = current_input if current_input else (str(result) if result is not None else "")
    draw_text(display_text, window_x + 20, window_y + 60, calc_font)

    pygame.display.flip()


pygame.quit()
sys.exit()
