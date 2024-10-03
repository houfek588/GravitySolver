import mass_model
import math
import random

class CollisionModel:
    def __init__(self, absorbtion):
        self.absorbtion = absorbtion
        self.velocity_condition = 4
        self.mass_condition = 3


    def handle_circle_collision(self, circles):
        i = 0
        while i < len(circles) - 1:
            circle1 = circles[i]
            has_merged = False
            j = i + 1
            while j < len(circles):
                circle2 = circles[j]
                if circle1.check_collision(circle1, circle2):
                    rel_vel = math.sqrt((circle1.velocity[0] - circle2.velocity[0]) ** 2 + (
                                circle1.velocity[1] - circle2.velocity[1]) ** 2)
                    mass_ratio = max(circle1.mass, circle2.mass) / min(circle1.mass, circle2.mass)
                    # print(f"rel_vel = {rel_vel}")
                    # print(f"mass_ratio = {mass_ratio}")

                    if rel_vel < 4 or mass_ratio > 3:
                        print("Merge")
                        merged_circle = self.merge_circles(circle1, circle2)
                        circles[i] = merged_circle  # Replace the first circle with the merged circle
                        circles.pop(j)  # Remove the second circle
                        has_merged = True
                        break  # No need to check other circles against this one
                    # if rel_vel >= 10:
                    # else:
                    #     print("Split")
                    #     # Split into N new circles if rel_vel is greater than 10
                    #     self.split_circles(circle1, circle2, circles, N=3)
                    #     circles.pop(j)  # Remove the second circle
                    #     circles.pop(i)  # Remove the first circle, adjust index accordingly
                    #     has_merged = True  # Prevent further checks against removed circle
                    #     break  # Exit the loop as the original circles have been removed

                    else:
                        self.handle_elastic_collision(circle1, circle2)
                j += 1
            if not has_merged:
                i += 1
        # i = 0
        # while i < len(circles):
        #     circle = circles[i]
        #     has_merged = False
        #
        #     j = 0
        #     while j < len(circles):
        #         if i != j:
        #             other_circle = circles[j]
        #             if circle.check_collision(circle, other_circle):
        #                 # Calculate relative velocity magnitude
        #                 rel_vel = math.sqrt((circle.velocity[0] - other_circle.velocity[0]) ** 2 + (
        #                         circle.velocity[1] - other_circle.velocity[1]) ** 2)
        #                 mass_ratio = max(circle.mass, other_circle.mass) / min(circle.mass, other_circle.mass)
        #
        #                 if rel_vel < 4 or mass_ratio > 3:
        #                     # Merge circles
        #                     new_mass = circle.mass + other_circle.mass
        #                     new_radius = math.sqrt(circle.radius ** 2 + other_circle.radius ** 2)  # Alternative merging strategy
        #                     new_velocity = [(circle.velocity[0] * circle.mass + other_circle.velocity[0] *
        #                                  other_circle.mass) / new_mass,
        #                                 (circle.velocity[1] * circle.mass + other_circle.velocity[1] *
        #                                  other_circle.mass) / new_mass]
        #
        #                     circle.pos = [(circle.pos[0] * circle.mass + other_circle.pos[0] * other_circle.mass) / new_mass,
        #                                  (circle.pos[1] * circle.mass + other_circle.pos[1] * other_circle.mass) / new_mass]
        #                     circle.velocity = new_velocity
        #                     circle.radius = new_radius
        #                     circle.mass = new_mass
        #                     circle.color = (random.randint(0, 255), random.randint(0, 255),
        #                                    random.randint(0, 255))  # New color for merged circle
        #                     circles.pop(j)
        #                     if i > j:
        #                         i -= 1  # Adjust index if necessary
        #                     has_merged = True
        #                     break  # Exit inner loop after merge
        #                 else:
        #                     # self.elastic_collision(circles)
        #                     for i, circle in enumerate(circles):
        #                         for j, other_circle in enumerate(circles[i+1:], start=i+1):
        #                             if circle.check_collision(circle, other_circle):
        #                                 # Calculate the mass-weighted velocities for a more realistic collision response
        #                                 total_mass = circle.mass + other_circle.mass
        #                                 new_velocity_circle = [
        #                                     (circle.velocity[0] * (circle.mass - other_circle.mass) + 2 * other_circle.mass * other_circle.velocity[0]) / total_mass,
        #                                     (circle.velocity[1] * (circle.mass - other_circle.mass) + 2 * other_circle.mass * other_circle.velocity[1]) / total_mass
        #                                 ]
        #                                 new_velocity_other_circle = [
        #                                     (other_circle.velocity[0] * (other_circle.mass - circle.mass) + 2 * circle.mass * circle.velocity[0]) / total_mass,
        #                                     (other_circle.velocity[1] * (other_circle.mass - circle.mass) + 2 * circle.mass * circle.velocity[1]) / total_mass
        #                                 ]
        #                                 circle.velocity = new_velocity_circle
        #                                 other_circle.velocity = new_velocity_other_circle
        #         j += 1
        #     if not has_merged:
        #         i += 1

    def handle_elastic_collision(self, circle1, circle2):
        total_mass = circle1.mass + circle2.mass
        circle1.velocity = [
            (circle1.velocity[0] * (circle1.mass - circle2.mass) + 2 * circle2.mass * circle2.velocity[0]) / total_mass,
            (circle1.velocity[1] * (circle1.mass - circle2.mass) + 2 * circle2.mass * circle2.velocity[1]) / total_mass
        ]
        circle2.velocity = [
            (circle2.velocity[0] * (circle2.mass - circle1.mass) + 2 * circle1.mass * circle1.velocity[0]) / total_mass,
            (circle2.velocity[1] * (circle2.mass - circle1.mass) + 2 * circle1.mass * circle1.velocity[1]) / total_mass
        ]


    def merge_circles(self, circle1, circle2):
        new_mass = circle1.mass + circle2.mass
        new_radius = math.sqrt(circle1.radius ** 2 + circle2.radius ** 2)
        new_velocity = [(circle1.velocity[0] * circle1.mass + circle2.velocity[0] * circle2.mass) / new_mass,
                        (circle1.velocity[1] * circle1.mass + circle2.velocity[1] * circle2.mass) / new_mass]
        new_position = [(circle1.pos[0] * circle1.mass + circle2.pos[0] * circle2.mass) / new_mass,
                        (circle1.pos[1] * circle1.mass + circle2.pos[1] * circle2.mass) / new_mass]

        new_color = (0.5*(circle1.color[0]+circle2.color[0]), 0.5*(circle1.color[1]+circle2.color[1]), 0.5*(circle1.color[2]+circle2.color[2]))

        if circle1.name == "star" or circle2.name == "star":
            new_name = "star"
        else:
            new_name = circle1.name + circle2.name

        return mass_model.Circle(new_name, new_position, new_velocity, new_radius, new_mass, new_color)

    def split_circles(self, circle1, circle2, circles, N):
        total_mass = circle1.mass + circle2.mass
        max_radius = circle1.radius + circle2.radius
        for _ in range(N):

            # Example split logic, adjust as needed:
            new_radius = max(circle1.radius, circle2.radius)/N  # Simplified example, adjust as needed
            new_mass = total_mass / N

            new_velocity = [(circle1.velocity[0] * circle1.mass + circle2.velocity[0] * circle2.mass) / new_mass + random.randint(0, 4),
                            (circle1.velocity[1] * circle1.mass + circle2.velocity[1] * circle2.mass) / new_mass + random.randint(0, 4)]

            for v in new_velocity:
                v *= 0.5


            new_pos = [max(circle1.pos[0], circle2.pos[0]) - (circle1.pos[0] - circle2.pos[0]) / 2 + random.randint(0, int(max_radius) * 2),
                       max(circle1.pos[1], circle2.pos[1]) - (circle1.pos[1] - circle2.pos[1]) / 2 + random.randint(0, int(max_radius) * 2)]

            new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color
            new_name = circle1.name + circle2.name + "_new_" + str(_)
            new_circle = mass_model.Circle(new_name, new_pos, new_velocity, new_radius, new_mass, new_color)  # Assumes Circle constructor can handle these parameters
            circles.append(new_circle)

        for c in circles:
            print(c)

class GravityModel:
    def __int__(self, gravitation_constant):
        self.gravitation_constant = gravitation_constant

    def update_velocity_for_attraction(self, circle, other_circle):
        # g = 6.67430 * pow(10, -11)
        g = 6.67430 * pow(10, -6)

        # Calculate distance between circles
        dx = other_circle.pos[0] - circle.pos[0]
        dy = other_circle.pos[1] - circle.pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Avoid division by zero and self-interaction
        if distance == 0:
            return

        # Calculate force magnitude
        force = g * circle.mass * other_circle.mass / pow(distance, 2)

        # Calculate force direction
        Fx = force * (dx / distance)
        Fy = force * (dy / distance)

        # print(f"force: {Fx}, {Fy}")

        # Update velocities based on force direction
        circle.velocity[0] += Fx / circle.mass
        circle.velocity[1] += Fy / circle.mass

        # print(f"velocity: {circle.velocity}")

    def handle_circle_interaction(self, circles):
        for i, circle in enumerate(circles):
            for other_circle in circles[i + 1:]:
                self.update_velocity_for_attraction(circle, other_circle)
                self.update_velocity_for_attraction(other_circle, circle)





def two_val_average(val1, val2):
    return (val1 + val2)/2