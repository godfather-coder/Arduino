import pygame
import serial

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Control Two Balls with Joysticks")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Ball properties
ball_radius = 20
ball1_position = [screen_width // 4, screen_height // 2]
ball2_position = [3 * screen_width // 4, screen_height // 2]
ball_speed = 20

# Initialize serial communication
serial_port = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino port

# Load font
font = pygame.font.Font(None, 36)

# Game variables
player1_score = 0
player2_score = 0
player1_wolf = True
player2_wolf = False
wolf_title_1 = "Wolf is Player 1 !!!"
wolf_title_2 = "Wolf is Player 2 !!!"
game_over = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if the game is over
    if not game_over:
        # Read data from the serial port
        if serial_port.in_waiting > 0:
            try:
                data = serial_port.readline().decode('utf-8').strip()
                x1, y1, _, x2, y2, _ = map(int, data.split(','))

                # Update ball 1 position
                ball1_position[0] += x1 * ball_speed
                ball1_position[1] += y1 * ball_speed

                # Ensure ball 1 stays within window boundaries
                ball1_position[0] = max(ball_radius, min(screen_width - ball_radius, ball1_position[0]))
                ball1_position[1] = max(ball_radius, min(screen_height - ball_radius, ball1_position[1]))

                # Update ball 2 position
                ball2_position[0] += x2 * ball_speed
                ball2_position[1] += y2 * ball_speed

                # Ensure ball 2 stays within window boundaries
                ball2_position[0] = max(ball_radius, min(screen_width - ball_radius, ball2_position[0]))
                ball2_position[1] = max(ball_radius, min(screen_height - ball_radius, ball2_position[1]))

                # Check for collision and update scores
                if ball1_position[1] == ball2_position[1] and ball1_position[0] == ball2_position[0] and player1_wolf:
                    player1_score += 1
                    player2_wolf = not player2_wolf
                    player1_wolf = not player1_wolf
                    ball1_position = [screen_width // 4, screen_height // 2]
                    ball2_position = [3 * screen_width // 4, screen_height // 2]
                elif ball1_position[1] == ball2_position[1] and ball1_position[0] == ball2_position[0] and player2_wolf:
                    player2_score += 1
                    player2_wolf = not player2_wolf
                    player1_wolf = not player1_wolf
                    ball1_position = [screen_width // 4, screen_height // 2]
                    ball2_position = [3 * screen_width // 4, screen_height // 2]

                # Check for win condition
                if player1_score >= 3 or player2_score >= 3:
                    game_over = True

            except:
                continue

    # Clear the screen
    screen.fill(WHITE)

    # Draw balls
    pygame.draw.circle(screen, RED, ball1_position, ball_radius)
    pygame.draw.circle(screen, BLUE, ball2_position, ball_radius)

    # Draw text
    text1 = font.render("Player 1 Score: " + str(player1_score), True, BLACK)
    text2 = font.render("Player 2 Score: " + str(player2_score), True, BLACK)
    if player1_wolf:
        wolf_text = font.render(wolf_title_1, True, RED)
    else:
        wolf_text = font.render(wolf_title_2, True, BLUE)
    if game_over:
        if player1_score >= 3:
            winner_text = font.render("Player 1 Wins!", True, RED)
        else:
            winner_text = font.render("Player 2 Wins!", True, BLUE)
        screen.blit(winner_text, ((screen_width - winner_text.get_width()) // 2, screen_height // 2))

    screen.blit(text1, (10, 10))
    screen.blit(text2, (screen_width - text2.get_width() - 10, 10))
    screen.blit(wolf_text, ((screen_width - wolf_text.get_width()) // 2, 10 + text1.get_height()))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
serial_port.close()
