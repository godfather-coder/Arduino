import pygame
import sys
import math
import serial

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
speed =2
# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Arm")
serial_port = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino port

# Define ArmPart class
class ArmPart:
    def __init__(self, length, angle, pivot, min_angle, max_angle):
        self.length = length
        self.angle = angle
        self.pivot = pivot
        self.min_angle = min_angle
        self.max_angle = max_angle

    def rotate(self, angle):
        new_angle = self.angle + angle
        if self.min_angle <= new_angle <= self.max_angle:
            self.angle = new_angle

    def get_end_point(self):
        end_x = self.pivot[0] + self.length * math.cos(math.radians(self.angle))
        end_y = self.pivot[1] - self.length * math.sin(math.radians(self.angle))  # Note the negative sign
        return int(end_x), int(end_y)

# Create instances of ArmPart for upper arm, forearm, and hand
upper_arm = ArmPart(150, 147, (WIDTH // 2, HEIGHT // 2), 120, 170)
forearm = ArmPart(120, 195, (0, 0), 174, 280)
hand = ArmPart(30, -81, (0, 0), -90, 2)

# Create font for displaying angles
font = pygame.font.Font(None, 24)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate the arm parts (change the rotation angle)
    if serial_port.in_waiting > 0:
        try:
            data = serial_port.readline().decode('utf-8').strip()
            x1, y1, _, x2, y2, _ = map(int, data.split(','))
            upper_arm.rotate(speed * y1)
            forearm.rotate(speed * y2)
            hand.rotate(speed * x2)

            # Update forearm pivot point to the end point of upper arm
            forearm.pivot = upper_arm.get_end_point()

            # Update hand pivot point to the end point of forearm
            hand.pivot = forearm.get_end_point()

            # Clear the screen
            screen.fill(WHITE)

            # Draw the arm parts
            pygame.draw.line(screen, BLACK, upper_arm.pivot, upper_arm.get_end_point(), 15)
            pygame.draw.line(screen, BLACK, forearm.pivot, forearm.get_end_point(), 15)
            pygame.draw.line(screen, BLACK, hand.pivot, hand.get_end_point(), 15)

            # Display angles of arm parts
            upper_arm_angle_text = font.render(f"Upper Arm Angle: {upper_arm.angle:.2f}", True, RED)
            forearm_angle_text = font.render(f"Forearm Angle: {forearm.angle:.2f}", True, RED)
            hand_angle_text = font.render(f"Hand Angle: {hand.angle:.2f}", True, RED)
            screen.blit(upper_arm_angle_text, (10, 10))
            screen.blit(forearm_angle_text, (230, 10))
            screen.blit(hand_angle_text, (450, 10))

            # Update the display
            pygame.display.flip()

            # Limit the frame rate
            pygame.time.Clock().tick(60)

        except:
            continue

# Quit Pygame
pygame.quit()
sys.exit()
