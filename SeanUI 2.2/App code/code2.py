import pygame


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Welcome to SeanUI")

window_width = 800
window_height = 600
bar_height = 30
window_color = (169, 169, 169)  
bar_color = (105, 105, 105)  
button_color = (255, 0, 0)  
button_text_color = (255, 255, 255)  
button_width = 60  
button_height = 20  
corner_radius = 5  

window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

font_size_title = 48
font_size_description = 24
font_title = pygame.font.Font(None, font_size_title)
font_description = pygame.font.Font(None, font_size_description)
button_font = pygame.font.Font(None, 24) 

background_image_path = 'background image/background.PNG'  
background_image = pygame.image.load(background_image_path).convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


inner_image_path = 'SeanUI App image/IMG_8827.png'  
inner_image = pygame.image.load(inner_image_path).convert()
inner_image = pygame.transform.scale(inner_image, (window_width, window_height - bar_height))


def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def render_button(surface, text, x, y, width, height, radius):
    button_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(surface, button_color, button_rect, radius)
    text_surface = button_font.render(text, True, button_text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)
    return button_rect


dragging = False
offset_x = 0
offset_y = 0

description_text = """SeanUI 2.0 offers a seamless user experience with a complete redesign of app icon, the app and home screens. The new home screen features a Minimalize button to adjust the layout, and apps now reside in a sleek bottom bar. Apps can be launched directly within SeanUI, bypassing Mac OS. The update also introduces drag functionality and a quit button, along with improved performance, faster speeds, and fewer errors."""


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

    window_rect = pygame.Rect(window_x, window_y, window_width, window_height)
    bar_rect = pygame.Rect(window_x, window_y, window_width, bar_height)
    pygame.draw.rect(screen, window_color, window_rect)
    pygame.draw.rect(screen, bar_color, bar_rect)


    screen.blit(inner_image, (window_x, window_y + bar_height))

    text_surface = font_title.render("SeanUI 2.0", True, (0, 0, 0))  
    text_rect = text_surface.get_rect(center=(window_x + window_width // 2, window_y + 50)) 
    screen.blit(text_surface, text_rect)


    lines = []
    words = description_text.split()
    max_width = window_width - 40  
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        test_surface = font_description.render(test_line, True, (255, 255, 255))
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)  

    y_offset = window_y + 150  
    for line in lines:
        text_surface = font_description.render(line, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(window_x + window_width // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += font_size_description + 10  

    quit_button = render_button(screen, "Quit", screen_width - button_width - 20, 20, button_width, button_height, corner_radius)

    
    pygame.display.flip()

pygame.quit()
