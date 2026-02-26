import pygame
import math

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "MOVE_FORWARD"
        self.velocity = 0
        self.max_speed = 3
        self.acceleration = 0.05
        self.path = []
        self.target_index = 0
        self.theta = -math.pi / 2
        self.rot_angle = 5
        self.sensor_length = 80
        self.sensor_offsets = [0, math.radians(30), math.radians(-30)]

        self.image_original = pygame.image.load("assets/mouse.png").convert_alpha()
        self.image_original = pygame.transform.scale(self.image_original, (40, 40))
        self.image_original = pygame.transform.rotate(self.image_original, -90)

    def update(self,obstacle_rect):
        print(self.velocity)
        sensor_hits = self.detect_sensors(obstacle_rect)
        if self.state == "MOVE_FORWARD":
            if any(sensor_hits):
                
                self.velocity = 0
                self.state = "BACK_UP"
                self.state_start_time = pygame.time.get_ticks()
            else:
                self.apply_throttle(1)

        elif self.state == "BACK_UP":
            self.apply_throttle(-1)
            if pygame.time.get_ticks() - self.state_start_time > 2000:
                self.velocity = 0
                self.state = "MOVE_FORWARD"
                self.state_start_time = pygame.time.get_ticks()
    #movement
    def apply_throttle(self, direction):
    # direction = 1 forward, -1 backward, 0 stop

        if direction != 0:
            self.velocity += direction * self.acceleration

            # Clamp velocity
            if self.velocity > self.max_speed:
                self.velocity = self.max_speed
            if self.velocity < -self.max_speed:
                self.velocity = -self.max_speed
        else:
            # rolling stop (friction)
            self.velocity *= 0.9

        self.x += self.velocity * math.cos(self.theta)
        self.y += self.velocity * math.sin(self.theta)

    def rotate(self):
        self.theta += math.radians(self.rot_angle)

    #render in pygame
    def draw(self, screen):
        rotated = pygame.transform.rotate(
            self.image_original,
            -math.degrees(self.theta)
        )
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)

    def get_sensor_rays(self):
        rays = []
        for offset in self.sensor_offsets:
            angle = self.theta + offset
            end_x = self.x + self.sensor_length * math.cos(angle)
            end_y = self.y + self.sensor_length * math.sin(angle)
            rays.append(((self.x, self.y), (end_x, end_y)))
        return rays

    def detect_sensors(self, obstacle_rect):
        hits = []

        for start, end in self.get_sensor_rays():
            hit = obstacle_rect.clipline(start, end)
            hits.append(bool(hit))

        return hits  


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "MOVE_FORWARD"
        self.speed = 2
        self.path = []
        self.target_index = 0
        self.theta = -math.pi / 2
        self.rot_angle = 5
        self.sensor_length = 80
        self.sensor_offsets = [0, math.radians(30), math.radians(-30)]

        self.image_original = pygame.image.load("assets/cat.png").convert_alpha()
        self.image_original = pygame.transform.scale(self.image_original, (60, 60))
        self.image_original = pygame.transform.rotate(self.image_original, -90)

    def update(self):
        pass

    #render in pygame
    def draw(self, screen):
        rotated = pygame.transform.rotate(
            self.image_original,
            -math.degrees(self.theta)
        )
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)
    
    def get_rect(self):
        rotated = pygame.transform.rotate(
            self.image_original,
            -math.degrees(self.theta)
        )
        return rotated.get_rect(center=(self.x, self.y))


#pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

robot = Robot(400, 600)
cat = Obstacle(400,300)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    robot.update(cat.get_rect())
    robot.draw(screen)

    cat.draw(screen)

    # Draw sensors
    for start, end in robot.get_sensor_rays():
        pygame.draw.line(screen, (0, 255, 0), start, end, 2)

    pygame.display.flip()

pygame.quit()