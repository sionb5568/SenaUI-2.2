import pygame
import urllib.request
import json
import datetime
import time


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Weather")

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
weather_font = pygame.font.Font(None, 36)
weather_temp_font = pygame.font.Font(None, 72)

API_KEY = "qrWfS4Y9MzQxy3ltAb5YnrV4TVnZqKJP6rFpceg1prgmyv9cttqMBveYdRiIyFCMZz4Pde%2BW6nM0p5niPtwoDw%3D%3D"


def deg_to_dir(deg):
    deg_code = {
        0: 'N', 360: 'N', 180: 'S', 270: 'W', 90: 'E', 22.5: 'NNE', 45: 'NE', 67.5: 'ENE',
        112.5: 'ESE', 135: 'SE', 157.5: 'SSE', 202.5: 'SSW', 225: 'SW', 247.5: 'WSW',
        292.5: 'WNW', 315: 'NW', 337.5: 'NNW'
    }
    close_dir = ''
    min_abs = 360
    if deg not in deg_code:
        for key in deg_code:
            diff = abs(key - deg)
            if diff < min_abs:
                min_abs = diff
                close_dir = deg_code[key]
    else:
        close_dir = deg_code[deg]
    return close_dir

def get_ultra_srt_ncst(nx, ny):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = (now - datetime.timedelta(minutes=40)).strftime("%H%M")

    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey={API_KEY}&numOfRows=100&pageNo=1&base_date={date_str}&base_time={time_str}&nx={nx}&ny={ny}&dataType=JSON"
    
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    return data


def draw_text(surface, text, x, y, color=(0, 0, 0), font=None, centered=False):
    if font is None:
        font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def render_button(surface, text, x, y, width, height, radius):
    button_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(surface, button_color, button_rect, radius)
    text_surface = button_font.render(text, True, button_text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)
    return button_rect


def display_weather(data):
    if "response" in data and "body" in data["response"] and "items" in data["response"]["body"]:
        weather_info = data["response"]["body"]["items"]["item"]
        weather_dict = {item["category"]: item["obsrValue"] for item in weather_info}

        y_temp_offset = 150

        if 'T1H' in weather_dict:
            temp = weather_dict['T1H']
            draw_text(screen, f"{temp}°C", window_x + window_width // 2, window_y + y_temp_offset, color=(255, 255, 255), font=weather_temp_font, centered=True)
            y_temp_offset += 100

        if 'PTY' in weather_dict:
            pty = int(weather_dict['PTY'])
            if pty == 0:
                weather_icon = "Sunny" 
            elif pty == 1:
                weather_icon = "Rain"  
            elif pty == 2:
                weather_icon = "Snow"  
            else:
                weather_icon = "Cloudy"  
            draw_text(screen, weather_icon, window_x + window_width // 2, window_y + y_temp_offset, color=(255, 255, 255), font=weather_font, centered=True)
            y_temp_offset += 50

        if 'VEC' in weather_dict and 'WSD' in weather_dict:
            vec = deg_to_dir(float(weather_dict['VEC']))
            wind_speed = weather_dict['WSD']
            draw_text(screen, f"Wind: {vec} {wind_speed}m/s", window_x + window_width // 2, window_y + y_temp_offset, color=(255, 255, 255), font=weather_font, centered=True)
            y_temp_offset += 50

        if 'RN1' in weather_dict:
            rain = weather_dict['RN1']
            draw_text(screen, f"Precipitation: {rain}mm", window_x + window_width // 2, window_y + y_temp_offset, color=(255, 255, 255), font=weather_font, centered=True)
            y_temp_offset += 50

    else:
        draw_text(screen, "Failed to fetch weather information.", window_x + 20, window_y + 20, color=(255, 255, 255), font=weather_font)

dragging = False
offset_x = 0
offset_y = 0


running = True
last_update_time = 0
update_interval = 300  
weather_data = {}
small_window_image = None  

background_image_path = 'background image/background.PNG'
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

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

    current_time = time.time()
    if current_time - last_update_time > update_interval:
        nx, ny = 65, 103  #location: Sejong Saerom, South Korea - If you want South Korea, you edit -> (nx, ny = 65, 103). If you don't want South Korea, you change code all
        weather_data = get_ultra_srt_ncst(nx, ny)  
        last_update_time = current_time


        if "response" in weather_data and "body" in weather_data["response"] and "items" in weather_data["response"]["body"]:
            weather_info = weather_data["response"]["body"]["items"]["item"]
            weather_dict = {item["category"]: item["obsrValue"] for item in weather_info}

            if 'PTY' in weather_dict:
                pty = int(weather_dict['PTY'])
                if pty == 0:
                    small_window_image_path = 'Weather imge/IMG_8835.png'  # sunny
                elif pty == 1:
                    small_window_image_path = 'Weather imge/IMG_8824.png'  #rain
                elif pty == 2:
                    small_window_image_path = 'Weather imge/IMG_8825.png'  # snow
                else:
                    small_window_image_path = 'Weather imge/IMG_8826.png'  # cloudy
            else:
                small_window_image_path = 'Weather imge/IMG_8823.png'  # normal

            small_window_image = pygame.image.load(small_window_image_path)
            small_window_image = pygame.transform.scale(small_window_image, (window_width, window_height - bar_height))

    screen.blit(background_image, (0, 0))

  
    window_rect = pygame.Rect(window_x, window_y, window_width, window_height)
    bar_rect = pygame.Rect(window_x, window_y, window_width, bar_height)
    pygame.draw.rect(screen, window_color, window_rect)
    pygame.draw.rect(screen, bar_color, bar_rect)


    if small_window_image:
        screen.blit(small_window_image, (window_x, window_y + bar_height))

    display_weather(weather_data)

    quit_button = render_button(screen, "Quit", screen_width - button_width - 20, 20, button_width, button_height, corner_radius)


    pygame.display.flip()

pygame.quit()
