import pygame, sys

# --- 1. GENERAL SETUP ---
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong - Retro Neon Style')

# Colors (RETRO NEON STYLE)
neon_green = (65, 255, 150)
bg_color = (15, 15, 15) # Dark Black/Grey Background

# Game Rectangles (x, y, width, height)
# Paddles are now wider (20) for a chunkier look
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 30, screen_height/2 - 70, 20, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 20, 140)

# Variables
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7

# Score Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None, 64) 

# --- 2. FUNCTIONS ---
def ball_restart():
    """Resets the ball to the center and sends it in a random direction"""
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_y *= -1 
    ball_speed_x *= -1 

# --- 3. THE GAME LOOP ---
while True:
    # A. Input Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Player Movement Key Checks
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # B. Game Logic
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    player.y += player_speed

    # Opponent AI 
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    # Bouncing Logic (Top and Bottom Walls)
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Collision Logic (Player & Opponent Paddles)
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    # Score Logic
    if ball.left <= 0:
        player_score += 1
        ball_restart()
        
    if ball.right >= screen_width:
        opponent_score += 1
        ball_restart()

    # Boundary Logic (Keep paddles on screen)
    if player.top <= 0: player.top = 0
    if player.bottom >= screen_height: player.bottom = screen_height
    if opponent.top <= 0: opponent.top = 0
    if opponent.bottom >= screen_height: opponent.bottom = screen_height

    # C. Drawing on Screen (STYLED SECTION)
    screen.fill(bg_color)
    
    # Draw Paddles
    pygame.draw.rect(screen, neon_green, player)
    pygame.draw.rect(screen, neon_green, opponent)
    
    # Draw Ball 
    pygame.draw.ellipse(screen, neon_green, ball)
    
    # Draw Center Line (Dashed effect)
    for i in range(0, screen_height, 20): 
        pygame.draw.rect(screen, neon_green, [screen_width/2 - 2, i, 4, 10])

    # Draw Scores
    player_text = game_font.render(f"{player_score}", False, neon_green)
    screen.blit(player_text, (660, 470))

    opponent_text = game_font.render(f"{opponent_score}", False, neon_green)
    screen.blit(opponent_text, (600, 470))

    # Update Display
    pygame.display.flip()
    
    # Limit Frames Per Second (FPS)
    clock.tick(60)