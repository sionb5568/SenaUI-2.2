import pygame
import platform

pygame.init()


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Sample")

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


font_size = 24
font = pygame.font.Font(None, font_size)
button_font = pygame.font.Font(None, font_size)


background_image_path = '/user/sample'  
background_image = pygame.image.load(background_image_path).convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_image = pygame.transform.flip(background_image, True, False)  # 좌우 반전

inner_image_path = '/user/sample'  
inner_image = pygame.image.load(inner_image_path).convert_alpha()
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

    quit_button = render_button(screen, "Quit", screen_width - button_width - 20, 20, button_width, button_height, corner_radius)

    pygame.display.flip()


pygame.quit()
