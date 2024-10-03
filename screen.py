import pygame
import sys
import math
import random
import mass_model
import interactions_model

# Initialize Pygame
pygame.init()

# Screen setup
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
background_color = (0, 0, 0)

# Button properties
button_color = green
button_hover_color = red
button_position = [250, 200, 140, 50]  # x, y, width, height
button_text = 'Start'

# Font setup
font = pygame.font.Font(None, 36)

# States
page = 'start'  # 'start' or 'end'

# Clock to control frame rate
clock = pygame.time.Clock()


def draw_button(screen, position, text, mouse_pos):
    x, y, width, height = position
    pygame.draw.rect(screen, button_color if not button_hover(position, mouse_pos) else button_hover_color, position)

    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)


def button_hover(position, mouse_pos):
    x, y, width, height = position
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        return True
    return False


# Create circles
# circles = [mass_model.Circle(pos=[random.randint(20, screen_width-20), random.randint(20, screen_height-20)],
#                   velocity=[random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])],
#                   radius=random.randint(10, 30),
#                   color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
#            for _ in range(1)]
basic_distance = 200
circles = []

# circles.append(mass_model.Circle("p1",[screen_width/2 - basic_distance,screen_height/2], [0,0], 20, 78539800,(255,0,0)))
# circles.append(mass_model.Circle("p2",[screen_width/2 + basic_distance,screen_height/2], [0,0], 40, 32169900,(255,0,255)))

circles.append(mass_model.Circle("p1",[screen_width/2 - basic_distance,screen_height/2], [0,14], 5, 785398,(255,0,0)))
circles.append(mass_model.Circle("p2",[screen_width/2 - basic_distance*2,screen_height/2], [0,8], 8, 3216990,(255,0,255)))
circles.append(mass_model.Circle("p3",[screen_width/2 - basic_distance*1.5,screen_height/2], [0,12], 8, 1357168,(0,0,255)))
circles.append(mass_model.Circle("star",[screen_width/2,screen_height/2], [0,0], 35, 2155132560,(255,255,0)))
print(circles[0].V)








gravitation = interactions_model.GravityModel()
collision = interactions_model.CollisionModel(1)
# print(gravitation.gravitation_constant)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and page == 'start':
            if button_hover(button_position, mouse_pos):
                page = 'end'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_x:
                page = 'start'

    # Drawing
    screen.fill(blue if page == 'start' else background_color)

    if page == 'start':
        draw_button(screen, button_position, button_text, mouse_pos)
    elif page == 'end':

        n = len(circles)
        for i, circle in enumerate(circles):
            if circle.name == "star":
                # Handle collision with screen boundaries
                circle.handle_boundary_collision(screen_width, screen_height)
            else:
                # Update circle position
                circle.update_position()

            # Handle interactions between circles, including attraction and collision
            collision.handle_circle_collision(circles)
            gravitation.handle_circle_interaction(circles)

            # Draw the circles
            circle.draw(screen)

            # Draw the "End Page" text on top of the circles
        text_surf = font.render('Gravitation behaviour', True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(screen_width // 2, 20))
        screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()