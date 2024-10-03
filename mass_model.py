import pygame
import sys
import math
import random

class Circle:
    def __init__(self, name, pos, velocity, radius, mass, color):
        self.name = name
        self.pos = pos
        self.velocity = velocity
        self.radius = radius
        self.mass = mass
        # self.mass = radius
        self.color = color
        self.position_history = [pos]  # Initialize position history with the starting position
        self.position_history_num = 100

        self.V = 4
        self.mass_ration_parameter = 3

    def __str__(self):
        return "Name: " + self.name + ", act. pos: " + str(self.pos) + ", act. vel: " + str(self.velocity)

    def update_position(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.position_history.append(self.pos.copy())  # Add the current position to the history
        # Keep only the last 50 positions
        if len(self.position_history) > self.position_history_num:
            self.position_history.pop(0)
        # print(self.pos)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [int(self.pos[0]), int(self.pos[1])], int(self.radius))
        for pos in self.position_history[-self.position_history_num:]:
            pygame.draw.circle(screen, self.color, [int(pos[0]), int(pos[1])], int(1))

    @staticmethod
    def check_collision(circle1, circle2):
        distance = math.sqrt((circle1.pos[0] - circle2.pos[0]) ** 2 + (circle1.pos[1] - circle2.pos[1]) ** 2)
        return distance < circle1.radius + circle2.radius


    def handle_boundary_collision(self, screen_width, screen_height):
        # print("boundary collision")
        # print(type(self.velocity))
        # print(type(self.velocity[0]))
        # print(type(self.velocity[1]))
        if self.pos[0] + self.radius >= screen_width or self.pos[0] - self.radius <= 0:
            self.velocity[0] *= -1
        if self.pos[1] + self.radius >= screen_height or self.pos[1] - self.radius <= 0:
            self.velocity[1] *= -1


    def handle_circle_collision(self, circles):
        i = 0
        while i < len(circles):
            circle = circles[i]
            has_merged = False

            if circle != self:
                if self.check_collision(self, circle):
                    # Calculate relative velocity magnitude and mass ratio
                    rel_vel = math.sqrt(
                        (self.velocity[0] - circle.velocity[0]) ** 2 + (self.velocity[1] - circle.velocity[1]) ** 2)
                    mass_ratio = max(self.mass, circle.mass) / min(self.mass, circle.mass)

                    if rel_vel < 4 or mass_ratio > 3:
                        # Merge circles
                        self.merge(circle)
                        circles.remove(circle)
                        has_merged = True
                        break  # Exit loop after merge since 'self' has changed
                    else:
                        # Handle elastic collision
                        self.elastic_collision(circle)
            i += 1
            if not has_merged:
                i += 1

    def merge(self, other_circle):
        self.mass += other_circle.mass
        self.radius = math.sqrt(self.radius ** 2 + other_circle.radius ** 2)
        self.velocity = [(self.velocity[0] * self.mass + other_circle.velocity[0] * other_circle.mass) / self.mass,
                         (self.velocity[1] * self.mass + other_circle.velocity[1] * other_circle.mass) / self.mass]
        self.pos = [(self.pos[0] * self.mass + other_circle.pos[0] * other_circle.mass) / self.mass,
                    (self.pos[1] * self.mass + other_circle.pos[1] * other_circle.mass) / self.mass]
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # New color

    def elastic_collision(self, other_circle):
        total_mass = self.mass + other_circle.mass
        self.velocity = [
            (self.velocity[0] * (self.mass - other_circle.mass) + 2 * other_circle.mass * other_circle.velocity[
                0]) / total_mass,
            (self.velocity[1] * (self.mass - other_circle.mass) + 2 * other_circle.mass * other_circle.velocity[
                1]) / total_mass
        ]
        other_circle.velocity = [
            (other_circle.velocity[0] * (other_circle.mass - self.mass) + 2 * self.mass * self.velocity[
                0]) / total_mass,
            (other_circle.velocity[1] * (other_circle.mass - self.mass) + 2 * self.mass * self.velocity[1]) / total_mass
        ]