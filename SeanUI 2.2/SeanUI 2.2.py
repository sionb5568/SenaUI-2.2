import pygame
import sys
import os
import traceback
import subprocess

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_WHITE = (245, 246, 246, 50)  
RED = (255, 0, 0)
white = (255,255,255)

radius = 1000

password = "1234"  #Change password
user_name = "User(pin:1234)"  

def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Sean OS")

    background_image_path = "background image/background.PNG"
    user_image_path = "User image/IMG_8816.PNG"
    logo_image_path = "User image/IMG_8810.PNG"
    font_path = None


    background_image = pygame.image.load(background_image_path)
    user_image = pygame.image.load(user_image_path)
    logo_image = pygame.image.load(logo_image_path)

 
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
    user_image = pygame.transform.scale(user_image, (170, 170))
    logo_image = pygame.transform.scale(logo_image, (30, 30))

    password_entered = False
    input_password = ""

    while not password_entered:
        screen.blit(background_image, (0, 0))

     
        user_image_rect = user_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2.5))
        screen.blit(user_image, user_image_rect)


        draw_text(screen, user_name, (screen.get_width() // 2, screen.get_height() // 2 + 20), font_size=35, color=WHITE)

 
        input_box_width = 150
        input_box_height = 25
        input_box_x = (screen.get_width() - input_box_width) // 2
        input_box_y = screen.get_height() // 2 + 46
        input_box_surface = pygame.Surface((input_box_width, input_box_height), pygame.SRCALPHA)
        pygame.draw.rect(input_box_surface, TRANSPARENT_WHITE, input_box_surface.get_rect(), border_radius=20)
        screen.blit(input_box_surface, (input_box_x, input_box_y))

        draw_text(screen, '*' * len(input_password), (input_box_x + input_box_width // 2, input_box_y + input_box_height // 2 + 8), font_size=45, color=BLACK)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    if input_password == password:
                        password_entered = True
                    else:
                        input_password = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_password = input_password[:-1]
                elif len(input_password) < 4:
                    input_password += event.unicode

        pygame.display.flip()


    run_main_ui(screen, background_image, logo_image, font_path)

def run_main_ui(screen, background_image, logo_image, font_path):
    try:
        app_count = 7


        top_bar_height = 40
        top_bar_rect = pygame.Rect(0, 0, screen.get_width(), top_bar_height)

   
        bottom_bar_rect = pygame.Rect(0, screen.get_height() - 100, screen.get_width(), 100)

        apps = create_apps(app_count, bottom_bar_rect)


        draw_background(screen, background_image)

        top_bar_surface = pygame.Surface((screen.get_width(), top_bar_height), pygame.SRCALPHA)
        pygame.draw.rect(top_bar_surface, (245, 246, 246, 80), top_bar_surface.get_rect(), border_radius=30)
        screen.blit(top_bar_surface, (0, 0))


        screen.blit(logo_image, (10, 5))


        seanos_text = "SeanUI"
        seanos_font = pygame.font.Font(font_path, 30)
        seanos_text_render = seanos_font.render(seanos_text, True, (255, 255, 255))
        seanos_text_rect = seanos_text_render.get_rect(center=(top_bar_rect.centerx, top_bar_rect.centery + 5))
        screen.blit(seanos_text_render, seanos_text_rect)

        bottom_bar_surface = pygame.Surface((app_count * (80 + 20), 110), pygame.SRCALPHA)
        pygame.draw.rect(bottom_bar_surface, (245, 246, 246, 120), bottom_bar_surface.get_rect(), border_radius=30)
        screen.blit(bottom_bar_surface, ((screen.get_width() - bottom_bar_surface.get_width()) // 2, screen.get_height() - 130))


        for app in apps:
            app.draw(screen)


        quit_button_rect = pygame.Rect(screen.get_width() - 100, 10, 70, 20)
        pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10)
        draw_text(screen, "Quit", quit_button_rect.center, font_size=20, color=WHITE)

        pygame.display.flip()

        app_process = None
        password_screen = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if logo_image.get_rect().collidepoint(event.pos):
                        password_screen = True 
                    for app in apps:
                        if app.rect.collidepoint(event.pos):
                            if app_process is not None:
                                app_process.terminate()
                                app_process = None
                            toggle_fullscreen(screen, background_image)
                            app_process = open_app(app.name)
                            app_process.wait() 
                            toggle_fullscreen(screen, background_image)
                if password_screen:
                    main()  
    except Exception as e:
        traceback.print_exc()
        pygame.quit()
        sys.exit()

def toggle_fullscreen(screen, background_image):
    if screen.get_flags() & pygame.FULLSCREEN:
        pygame.display.set_mode((screen.get_width(), screen.get_height()))
    else:
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

  
    draw_background(screen, background_image)
    draw_ui(screen)
    pygame.display.flip()

def draw_ui(screen):

    top_bar_height = 40
    top_bar_rect = pygame.Rect(0, 0, screen.get_width(), top_bar_height)

    top_bar_surface = pygame.Surface((screen.get_width(), top_bar_height), pygame.SRCALPHA)
    pygame.draw.rect(top_bar_surface, (255, 255, 255, 50), top_bar_surface.get_rect(), border_radius=30)
    screen.blit(top_bar_surface, (0, 0))

    logo_image = pygame.image.load("User image/IMG_8810.PNG")
    logo_image = pygame.transform.scale(logo_image, (30, 30))
    screen.blit(logo_image, (10, 5))

    seanos_text = "SeanUI"
    seanos_font = pygame.font.Font(None, 30)
    seanos_text_render = seanos_font.render(seanos_text, True, (255, 255, 255))
    seanos_text_rect = seanos_text_render.get_rect(center=(top_bar_rect.centerx, top_bar_rect.centery + 5))
    screen.blit(seanos_text_render, seanos_text_rect)


    bottom_bar_rect = pygame.Rect(0, screen.get_height() - 100, screen.get_width(), 100)

    bottom_bar_surface = pygame.Surface((7 * (80 + 20), 110), pygame.SRCALPHA)
    pygame.draw.rect(bottom_bar_surface, (255, 255, 255, 50), bottom_bar_surface.get_rect(), border_radius=30)
    screen.blit(bottom_bar_surface, ((screen.get_width() - bottom_bar_surface.get_width()) // 2, screen.get_height() - 130))

    apps = create_apps(7, bottom_bar_rect)
    for app in apps:
        app.draw(screen)

    quit_button_rect = pygame.Rect(screen.get_width() - 100, 10, 70, 20)
    pygame.draw.rect(screen, (255, 0, 0, 150), quit_button_rect, border_radius=10)
    draw_text(screen, "Quit", quit_button_rect.center, font_size=20, color=(255, 255, 255))

class App:
    def __init__(self, name, rect, position, color=(220, 220, 220)):
        self.name = name
        self.rect = rect
        self.position = position
        self.color = color
        self.icon_image = None

        self.load_icon_image()

    def load_icon_image(self):
        if self.name == "SeanUI":
            icon_path = "App icon/Untitled25_20230608195827.PNG"
        elif self.name == "Weather":
            icon_path = "App icon/무제67_20240619163216.PNG"
        elif self.name == "Web":
            icon_path = "App icon/IMG_8809.png"
        elif self.name == "Clock":
            icon_path = "App icon/무제68_20240619205736 2.PNG"
        elif self.name == "Calculator":
            icon_path = "App icon/무제67_20240619162149.PNG"
        elif self.name == "Notes":
            icon_path = "App icon/스크린샷 2024-06-22 오후 7.35.31.png"
        elif self.name == "Drawing":
            icon_path = "App icon/IMG_8834.PNG"

        self.icon_image = pygame.image.load(icon_path).convert_alpha()
        self.icon_image = pygame.transform.scale(self.icon_image, (self.rect.width - 10, self.rect.height - 10))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=15)
        if self.icon_image:
            surface.blit(self.icon_image, (self.rect.x + 5, self.rect.y + 5))
        draw_text(surface, self.name, self.position, font_size=15, color=(255, 255, 255))

def draw_text(surface, text, pos, font_size=20, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect)

def draw_background(surface, background_image):
    surface.blit(background_image, (0, 0))

def create_apps(app_count, bottom_bar_rect):
    app_width = 80
    app_height = 80
    app_gap = 20
    total_app_width = app_count * (app_width + app_gap) - app_gap

    start_x = bottom_bar_rect.left + (bottom_bar_rect.width - total_app_width) // 2
    _offset = -60

    apps = []
    for i in range(app_count):
        app_rect = pygame.Rect(start_x + i * (app_width + app_gap), bottom_bar_rect.top - app_height - _offset,
                               app_width, app_height)
        _position = (start_x + i * (app_width + app_gap) + app_width // 2, bottom_bar_rect.bottom - 30)

        if i == 0:
            app = App("SeanUI", app_rect, _position, color=(79, 114, 160))
        elif i == 1:
            app = App("Weather", app_rect, _position, color=(19, 93, 169))
        elif i == 2:
            app = App("Web", app_rect, _position, color=(255, 255, 255))
        elif i == 3:
            app = App("Clock", app_rect, _position, color=(0, 0, 0))
        elif i == 4: 
            app = App("Calculator", app_rect, _position, color=(255, 255, 255))
        elif i == 5:
            app = App("Notes", app_rect, _position, color=(255, 255, 255))
        elif i == 6:
            app = App("Drawing", app_rect, _position, color=(245, 245, 245))
        apps.append(app)
    return apps

def open_app(app_name):
    if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
        toggle_fullscreen()
    app_paths = {
        "SeanUI": "App code/code2.py",
        "Weather": "App code/code3.py",
        "Web": "App code/code4.py",
        "Clock": "App code/code5.py",
        "Calculator": "App code/code6.py",
        "Notes": "App code/code7.py",
        "Drawing": "App code/code8.py",
    }
    return subprocess.Popen([sys.executable, app_paths[app_name]])

def load_code(file_path=None):
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
            exec(code)

def save_code_index(index):
    with open("/Volumes/SEAN/SeanOS(USB)/code_index.txt", "w") as file:
        file.write(str(index))

def load_code_index():
    if os.path.exists("/Volumes/SEAN/SeanOS(USB)/code_index.txt"):
        with open("/Volumes/SEAN/SeanOS(USB)/code_index.txt", "r") as file:
            return int(file.read())
    return 2

if __name__ == "__main__":
    main()