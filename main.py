import pygame
import random

pygame.init()

# Define screen dimensions
WIDTH = 1280
HEIGHT = 720

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geo Dash Clone")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define game objects
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
player_surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player_surface.fill(YELLOW)
player_mask = pygame.mask.from_surface(player_surface)

OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 150
obstacle_surface = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_surface.fill(GREEN)
obstacle_mask = pygame.mask.from_surface(obstacle_surface)

ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
enemy_surface = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
enemy_surface.fill(RED)
enemy_mask = pygame.mask.from_surface(enemy_surface)

# Define player object
player_x = 100
player_y = HEIGHT / 2 - PLAYER_HEIGHT / 2
player_vy = 0
player_gravity = 0.5
player_speed = 5
jump_speed = 7

# Define enemy object
enemy_x = 800
enemy_y = HEIGHT / 2 - ENEMY_HEIGHT / 2
enemy_vx = -5

# Define obstacles
obstacles = []

for i in range(5):
    obstacle_x = i*300 + random.randint(-150, 150)
    obstacle_y = player_y + PLAYER_HEIGHT
    obstacles.append((obstacle_x, obstacle_y))

# Define game state
score = 0
is_game_over = False

# Define game loop
clock = pygame.time.Clock()

while not is_game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_vy = -jump_speed
    
    # Update game state
    # Update player position
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed
    
    player_y += player_vy
    player_vy += player_gravity
    
    # Apply floor collider
    if player_y + PLAYER_HEIGHT > HEIGHT:
        player_y = HEIGHT - PLAYER_HEIGHT
        player_is_jumping = False
        player_vy = 0
        
    # Update obstacles
    for index, obstacle in enumerate(obstacles):
        obstacle_x, obstacle_y = obstacle
        obstacle_x -= 5
        obstacles[index] = (obstacle_x, obstacle_y)
        
        if obstacle_x < -OBSTACLE_WIDTH:
            obstacles.pop(index)
            obstacle_x = 500 + random.randint(100, 300)
            obstacle_y = player_y + PLAYER_HEIGHT
            obstacles.append((obstacle_x, obstacle_y))
        
        # Check for collision with obstacles
        if player_y + PLAYER_HEIGHT > obstacle_y and player_y < obstacle_y + OBSTACLE_HEIGHT:
            if player_x + PLAYER_WIDTH > obstacle_x and player_x < obstacle_x + OBSTACLE_WIDTH:
                is_game_over = True
        
    # Update enemy position
    enemy_x += enemy_vx
        
    # Check for collision with enemy
    if player_y + PLAYER_HEIGHT > enemy_y and player_y < enemy_y + ENEMY_HEIGHT:
        if player_x + PLAYER_WIDTH > enemy_x and player_x < enemy_x + ENEMY_WIDTH:
            is_game_over = True
        
    # Check for game over condition
    if player_y > HEIGHT or player_y < -PLAYER_HEIGHT:
        is_game_over = True
        
    # Update score if game is still running
    if not is_game_over:
        score += 1
        
    # Draw game objects
    screen.fill(BLACK)
        
    # Draw obstacles
    for obstacle in obstacles:
        screen.blit(obstacle_surface, obstacle)
            
    # Draw enemy
    screen.blit(enemy_surface, (enemy_x, enemy_y))
    
    # Draw player
    screen.blit(player_surface, (player_x, player_y))
    
    # Update screen
    pygame.display.flip()
        
    # Control frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()