import pygame
import random
import os
import json
import math
import sys

# Debug flag to print more info
DEBUG = True

def debug_print(message):
    if DEBUG:
        print(message)

# Initialize Pygame
debug_print("Initializing Pygame...")
try:
    pygame.init()
    pygame.mixer.init()
except Exception as e:
    debug_print(f"Error initializing Pygame: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

# Set up the display
WIDTH = 800
HEIGHT = 600
debug_print("Setting up display...")
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")
except Exception as e:
    debug_print(f"Error setting up display: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Load images with explicit fallbacks
debug_print("Loading images...")
try:
    background = pygame.image.load("background.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    debug_print(f"Failed to load background.png: {e}")
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BLACK)

try:
    player_img = pygame.image.load("player.png").convert_alpha()
except Exception as e:
    debug_print(f"Failed to load player.png: {e}")
    player_img = pygame.Surface((50, 40))
    player_img.fill(WHITE)

try:
    enemy_img = pygame.image.load("enemy.png").convert_alpha()
except Exception as e:
    debug_print(f"Failed to load enemy.png: {e}")
    enemy_img = pygame.Surface((40, 30))
    enemy_img.fill(RED)

try:
    bomber_img = pygame.image.load("bomber.png").convert_alpha()
except Exception as e:
    debug_print(f"Failed to load bomber.png: {e}")
    bomber_img = pygame.Surface((40, 30))
    bomber_img.fill(YELLOW)

try:
    elite_img = pygame.image.load("elite.png").convert_alpha()
except Exception as e:
    debug_print(f"Failed to load elite.png: {e}")
    elite_img = pygame.Surface((40, 30))
    elite_img.fill((0, 255, 0))

try:
    mega_img = pygame.image.load("mega.png").convert_alpha()
except Exception as e:
    debug_print(f"Failed to load mega.png: {e}")
    mega_img = pygame.Surface((200, 150))
    mega_img.fill((255, 0, 255))

try:
    bullet_img = pygame.image.load("bullet.png").convert_alpha()
except Exception as e:
    debug_print(f"Failed to load bullet.png: {e}")
    bullet_img = pygame.Surface((5, 15))
    bullet_img.fill(WHITE)

try:
    bomb_img = pygame.image.load("bomb.png").convert_alpha()
except Exception as e:
    debug_print(f"Failed to load bomb.png: {e}")
    bomb_img = pygame.Surface((5, 15))
    bomb_img.fill(YELLOW)

try:
    explosion_img = pygame.image.load("explosion.png").convert_alpha()
except Exception as e:
    debug_print(f"Failed to load explosion.png: {e}")
    explosion_img = pygame.Surface((40, 40))
    explosion_img.fill(RED)

try:
    title_img = pygame.image.load("title.png").convert_alpha()
except Exception as e:
    debug_print(f"Failed to load title.png: {e}")
    title_img = pygame.Surface((450, 200))
    title_img.fill(WHITE)

# Load sounds
debug_print("Loading sounds...")
try:
    bullet_sound = pygame.mixer.Sound("bullet.wav")
except Exception as e:
    debug_print(f"Failed to load bullet.wav: {e}")
    bullet_sound = None

try:
    explosion_sound = pygame.mixer.Sound("explosion.wav")
except Exception as e:
    debug_print(f"Failed to load explosion.wav: {e}")
    explosion_sound = None

try:
    bomb_drop_sound = pygame.mixer.Sound("bomb_drop.wav")
except Exception as e:
    debug_print(f"Failed to load bomb_drop.wav: {e}")
    bomb_drop_sound = None

try:
    dive_sound = pygame.mixer.Sound("dive.wav")
except Exception as e:
    debug_print(f"Failed to load dive.wav: {e}")
    dive_sound = None

# Load background music
debug_print("Loading background music...")
try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.75)
except Exception as e:
    debug_print(f"Failed to load background_music.mp3: {e}")

# Scale sprite images
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 40
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 30
BOMBER_WIDTH, BOMBER_HEIGHT = 40, 30
ELITE_WIDTH, ELITE_HEIGHT = 40, 30
MEGA_WIDTH, MEGA_HEIGHT = 200, 150
BULLET_WIDTH, BULLET_HEIGHT = 5, 15
BOMB_WIDTH, BOMB_HEIGHT = 5, 15
EXPLOSION_WIDTH, EXPLOSION_HEIGHT = 40, 40
TITLE_WIDTH, TITLE_HEIGHT = 450, 200

debug_print("Scaling images...")
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
bomber_img = pygame.transform.scale(bomber_img, (BOMBER_WIDTH, BOMBER_HEIGHT))
elite_img = pygame.transform.scale(elite_img, (ELITE_WIDTH, ELITE_HEIGHT))
mega_img = pygame.transform.scale(mega_img, (MEGA_WIDTH, MEGA_HEIGHT))
bullet_img = pygame.transform.scale(bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))
bomb_img = pygame.transform.scale(bomb_img, (BOMB_WIDTH, BOMB_HEIGHT))
explosion_img = pygame.transform.scale(explosion_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))
title_img = pygame.transform.scale(title_img, (TITLE_WIDTH, TITLE_HEIGHT))

# Scale player image for lives display
LIVES_ICON_WIDTH, LIVES_ICON_HEIGHT = 25, 20
lives_icon = pygame.transform.scale(player_img, (LIVES_ICON_WIDTH, LIVES_ICON_HEIGHT))

# High score handling
HIGH_SCORE_FILE = "high_scores.json"
def load_high_scores():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_high_scores(scores):
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump(scores, f)

def update_high_scores(score, initials):
    scores = load_high_scores()
    scores.append({"initials": initials, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:5]

# Display start screen with high scores
def show_start_screen(high_scores):
    debug_print("Showing start screen...")
    clock = pygame.time.Clock()
    screen.blit(background, (0, 0))
    
    screen.blit(title_img, (WIDTH//2 - TITLE_WIDTH//2, HEIGHT//2 - 250))
    
    font = pygame.font.SysFont('Arial', 25, bold=True)
    high_score_title = font.render("High Scores", True, LIGHT_BLUE)
    screen.blit(high_score_title, (WIDTH//2 - high_score_title.get_width()//2, HEIGHT//2 - 20))
    
    for i, entry in enumerate(high_scores[:5]):
        score_text = font.render(f"{entry['initials']} - {entry['score']}", True, LIGHT_BLUE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 10 + i * 30))
    
    start_font = pygame.font.SysFont('Arial', 30, bold=True)
    start_text = start_font.render("Press S to Start", True, YELLOW)
    start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 200))
    
    waiting = True
    while waiting:
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0:
            screen.blit(start_text, start_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    debug_print("S pressed, exiting start screen...")
                    waiting = False
        
        screen.blit(background, (0, 0))
        screen.blit(title_img, (WIDTH//2 - TITLE_WIDTH//2, HEIGHT//2 - 250))
        screen.blit(high_score_title, (WIDTH//2 - high_score_title.get_width()//2, HEIGHT//2 - 20))
        for i, entry in enumerate(high_scores[:5]):
            score_text = font.render(f"{entry['initials']} - {entry['score']}", True, LIGHT_BLUE)
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 10 + i * 30))
        
        clock.tick(60)

# Display enter initials screen
def show_enter_initials_screen(score):
    debug_print("Showing enter initials screen...")
    screen.blit(background, (0, 0))
    font = pygame.font.SysFont('Arial', 48, bold=True)
    prompt_text = font.render(f"New High Score: {score}", True, WHITE)
    instruction_text = font.render("Enter 3 initials:", True, WHITE)
    initials = ""
    
    waiting = True
    while waiting:
        screen.blit(background, (0, 0))
        screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))
        initials_text = font.render(initials, True, WHITE)
        screen.blit(initials_text, (WIDTH//2 - initials_text.get_width()//2, HEIGHT//2 + 80))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) == 3:
                    waiting = False
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]
                elif len(initials) < 3 and event.key >= pygame.K_a and event.key <= pygame.K_z:
                    initials += chr(event.key).upper()
    
    return initials

# Display game over screen with play again option
def show_game_over_screen(score):
    debug_print("Showing game over screen...")
    screen.blit(background, (0, 0))
    font = pygame.font.SysFont('Arial', 48, bold=True)
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    play_again_text = font.render("Play Again? (Y/N)", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 30))
    screen.blit(play_again_text, (WIDTH//2 - play_again_text.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                if event.key == pygame.K_n:
                    return False
    return False

# Display end credits screen
def show_end_credits():
    debug_print("Showing end credits screen...")
    screen.blit(background, (0, 0))
    font = pygame.font.SysFont('Arial', 36, bold=True)
    
    credits_line1 = font.render("Programming and graphics by", True, WHITE)
    credits_line2 = font.render("Brian Zimmerman using Grok", True, WHITE)
    credits_line3 = font.render("Music arranged by", True, WHITE)
    credits_line4 = font.render("Brian Zimmerman 2025", True, WHITE)
    
    screen.blit(credits_line1, (WIDTH//2 - credits_line1.get_width()//2, HEIGHT//2 - 100))
    screen.blit(credits_line2, (WIDTH//2 - credits_line2.get_width()//2, HEIGHT//2 - 50))
    screen.blit(credits_line3, (WIDTH//2 - credits_line3.get_width()//2, HEIGHT//2 + 20))
    screen.blit(credits_line4, (WIDTH//2 - credits_line4.get_width()//2, HEIGHT//2 + 60))
    
    pygame.display.flip()
    pygame.time.wait(5000)  # Display for 5 seconds before exiting

# Main game function
def play_game():
    debug_print("Entering play_game()...")
    try:
        # Player properties
        debug_print("Setting player properties...")
        player_x = WIDTH // 2 - PLAYER_WIDTH // 2
        player_y = HEIGHT - 100
        player_speed = 10
        lives = 3
        player_explosion = None

        # Bullet properties
        debug_print("Setting bullet properties...")
        bullet_speed = 7
        bullets = []

        # Bomb properties
        debug_print("Setting bomb properties...")
        bomb_speed = 5
        bombs = []
        BOMB_DROP_CHANCE = 0.0025
        bombs_enabled = True

        # Elite dive properties
        debug_print("Setting elite dive properties...")
        DIVE_CHANCE = 0.000625
        DIVE_SPEED = 5

        # Mega alien properties
        debug_print("Setting mega alien properties...")
        MEGA_BOMB_CHANCE = 0.01

        # Explosion properties
        debug_print("Setting explosion properties...")
        explosions = []
        EXPLOSION_DURATION = 30

        # Enemy properties
        debug_print("Setting enemy properties...")
        BASE_ENEMY_SPEED = 2
        enemy_speed = BASE_ENEMY_SPEED
        SPEED_INCREASE = 0.2
        enemies = []
        ENEMY_ROWS = 3
        ENEMY_COLS = 10
        level = 1

        # Game state
        debug_print("Setting game state...")
        paused = False
        score = 0
        clock = pygame.time.Clock()

        # Create enemies
        def create_enemies(level):
            nonlocal enemies, enemy_speed
            debug_print(f"Creating enemies for level {level}...")
            enemies = []
            if level == 10:
                enemies.append({
                    'x': WIDTH // 2 - MEGA_WIDTH // 2,
                    'y': HEIGHT // 2 - MEGA_HEIGHT // 2,  # Mid-screen
                    'type': "mega",
                    'health': 20,
                    'time': 0
                })
            else:
                rows = min(5, ENEMY_ROWS + (level - 1) // 3)
                for row in range(rows):
                    for col in range(ENEMY_COLS):
                        if level >= 7 and row == 0:
                            enemy_type = "elite"
                        elif level >= 4 and row == 0:
                            enemy_type = "bomber"
                        else:
                            enemy_type = "normal"
                        enemy = {
                            'x': 75 + col * (ENEMY_WIDTH + 20),
                            'y': 50 + row * (ENEMY_HEIGHT + 20),
                            'direction': 1,
                            'type': enemy_type,
                            'diving': False,
                            'original_x': 75 + col * (ENEMY_WIDTH + 20),
                            'original_y': 50 + row * (ENEMY_HEIGHT + 20)
                        }
                        enemies.append(enemy)
            enemy_speed = BASE_ENEMY_SPEED + (level - 1) * 0.1
            debug_print(f"Enemies created: {len(enemies)}")

        # Display level transition
        def show_level_transition(level):
            debug_print(f"Showing level transition for level {level}...")
            screen.blit(background, (0, 0))
            font = pygame.font.SysFont('Arial', 48, bold=True)
            level_text = font.render(f"Level {level}", True, WHITE)
            screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT//2 - 24))
            pygame.display.flip()
            pygame.time.wait(2000)

        # Display pause screen
        def show_pause_screen():
            debug_print("Showing pause screen...")
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            font = pygame.font.SysFont('Arial', 48, bold=True)
            pause_text = font.render("PAUSED", True, WHITE)
            instruction_text = font.render("Press P to continue", True, WHITE)
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 20))
            pygame.display.flip()

        # Initial enemy creation
        debug_print("Creating initial enemies...")
        try:
            create_enemies(level)
            debug_print("Starting background music...")
            if pygame.mixer.get_init():
                pygame.mixer.music.play(-1)
            else:
                debug_print("Mixer not initialized, skipping music...")
        except Exception as e:
            debug_print(f"Error initializing game state: {e}")
            pygame.quit()
            input("Press Enter to exit...")
            sys.exit(1)

        # Game loop
        debug_print("Entering game loop...")
        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and not paused and not player_explosion:
                            bullet = {
                                'x': player_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2,
                                'y': player_y
                            }
                            bullets.append(bullet)
                            if bullet_sound:
                                bullet_sound.play()
                        if event.key == pygame.K_p:
                            paused = not paused
                            if paused:
                                if pygame.mixer.get_init():
                                    pygame.mixer.music.pause()
                                show_pause_screen()
                            else:
                                if pygame.mixer.get_init():
                                    pygame.mixer.music.unpause()
                        if event.key == pygame.K_b:
                            bombs_enabled = not bombs_enabled
                            debug_print(f"Bombs {'enabled' if bombs_enabled else 'disabled'}")

                if paused:
                    continue

                # Player movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player_x > 0 and not player_explosion:
                    player_x -= player_speed
                if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_WIDTH and not player_explosion:
                    player_x += player_speed

                # Update bullets
                for bullet in bullets[:]:
                    bullet['y'] -= bullet_speed
                    if bullet['y'] < 0:
                        bullets.remove(bullet)

                # Update bombs
                for bomb in bombs[:]:
                    bomb['y'] += bomb_speed
                    if bomb['y'] > HEIGHT:
                        bombs.remove(bomb)
                    if (not player_explosion and 
                        bomb['x'] >= player_x and 
                        bomb['x'] <= player_x + PLAYER_WIDTH and
                        bomb['y'] >= player_y and 
                        bomb['y'] <= player_y + PLAYER_HEIGHT):
                        lives -= 1
                        player_explosion = {
                            'x': player_x,
                            'y': player_y,
                            'timer': EXPLOSION_DURATION
                        }
                        if explosion_sound:
                            explosion_sound.play()
                        bombs.remove(bomb)
                        break

                # Update explosions
                for explosion in explosions[:]:
                    explosion['timer'] -= 1
                    if explosion['timer'] <= 0:
                        explosions.remove(explosion)

                # Update player explosion
                if player_explosion:
                    player_explosion['timer'] -= 1
                    if player_explosion['timer'] <= 0:
                        player_explosion = None
                        player_x = WIDTH // 2 - PLAYER_WIDTH // 2
                        if lives > 0:
                            create_enemies(level)
                            bullets.clear()
                            bombs.clear()
                        if lives <= 0:
                            running = False

                # Update enemies
                for enemy in enemies[:]:
                    if enemy['type'] == "mega":
                        enemy['time'] += 0.05
                        enemy['x'] = WIDTH // 2 + 350 * math.sin(enemy['time']) - MEGA_WIDTH // 2  # Side-to-side, centered
                        # y stays fixed at HEIGHT // 2 - MEGA_HEIGHT // 2 from creation
                        
                        if random.random() < MEGA_BOMB_CHANCE and bombs_enabled:
                            bomb = {
                                'x': enemy['x'] + MEGA_WIDTH // 2 - BOMB_WIDTH // 2,
                                'y': enemy['y'] + MEGA_HEIGHT
                            }
                            bombs.append(bomb)
                            if bomb_drop_sound:
                                bomb_drop_sound.play()

                    elif enemy['type'] == "elite" and not enemy['diving'] and random.random() < DIVE_CHANCE:
                        enemy['diving'] = True
                        if dive_sound:
                            dive_sound.play()

                    if enemy.get('diving', False):
                        enemy['y'] += DIVE_SPEED
                        if (not player_explosion and 
                            enemy['x'] >= player_x and 
                            enemy['x'] <= player_x + PLAYER_WIDTH and
                            enemy['y'] >= player_y and 
                            enemy['y'] <= player_y + PLAYER_HEIGHT):
                            lives -= 1
                            player_explosion = {
                                'x': player_x,
                                'y': player_y,
                                'timer': EXPLOSION_DURATION
                            }
                            if explosion_sound:
                                explosion_sound.play()
                            enemy['diving'] = False
                            enemy['x'] = enemy['original_x']
                            enemy['y'] = enemy['original_y']
                            continue
                        if enemy['y'] > HEIGHT:
                            enemy['diving'] = False
                            enemy['x'] = enemy['original_x']
                            enemy['y'] = enemy['original_y']
                    else:
                        if enemy['type'] != "mega":
                            enemy['x'] += enemy_speed * enemy['direction']
                            if enemy['x'] <= 0 or enemy['x'] >= WIDTH - ENEMY_WIDTH:
                                for e in enemies:
                                    if not e.get('diving', False) and e['type'] != "mega":
                                        e['direction'] *= -1
                                        e['y'] += 20
                                enemy_speed += SPEED_INCREASE

                    if enemy['type'] == "bomber" and bombs_enabled and random.random() < BOMB_DROP_CHANCE:
                        bomb = {
                            'x': enemy['x'] + BOMBER_WIDTH // 2 - BOMB_WIDTH // 2,
                            'y': enemy['y'] + BOMBER_HEIGHT
                        }
                        bombs.append(bomb)
                        if bomb_drop_sound:
                            bomb_drop_sound.play()

                    for bullet in bullets[:]:
                        if enemy['type'] == "mega":
                            if (bullet['x'] >= enemy['x'] and 
                                bullet['x'] <= enemy['x'] + MEGA_WIDTH and
                                bullet['y'] >= enemy['y'] and 
                                bullet['y'] <= enemy['y'] + MEGA_HEIGHT):
                                enemy['health'] -= 1
                                bullets.remove(bullet)
                                # Add explosion on hit
                                explosions.append({
                                    'x': bullet['x'] - EXPLOSION_WIDTH // 2,
                                    'y': bullet['y'] - EXPLOSION_HEIGHT // 2,
                                    'timer': EXPLOSION_DURATION
                                })
                                if explosion_sound:
                                    explosion_sound.play()
                                if enemy['health'] <= 0:
                                    explosions.append({
                                        'x': enemy['x'] + MEGA_WIDTH // 2 - EXPLOSION_WIDTH // 2,
                                        'y': enemy['y'] + MEGA_HEIGHT // 2 - EXPLOSION_HEIGHT // 2,
                                        'timer': EXPLOSION_DURATION
                                    })
                                    if explosion_sound:
                                        explosion_sound.play()
                                    enemies.remove(enemy)
                                    score += 100
                                break
                        else:
                            if (bullet['x'] >= enemy['x'] and 
                                bullet['x'] <= enemy['x'] + ENEMY_WIDTH and
                                bullet['y'] >= enemy['y'] and 
                                bullet['y'] <= enemy['y'] + ENEMY_HEIGHT):
                                explosions.append({
                                    'x': enemy['x'],
                                    'y': enemy['y'],
                                    'timer': EXPLOSION_DURATION
                                })
                                if explosion_sound:
                                    explosion_sound.play()
                                enemies.remove(enemy)
                                bullets.remove(bullet)
                                if enemy['type'] == "elite":
                                    score += 20
                                else:
                                    score += 10
                                break

                if not enemies and not player_explosion:
                    level += 1
                    show_level_transition(level)
                    create_enemies(level)
                    bullets.clear()
                    bombs.clear()

                for enemy in enemies[:]:
                    if not enemy.get('diving', False) and enemy['type'] != "mega" and enemy['y'] > HEIGHT - 100 and not player_explosion:
                        lives -= 1
                        player_explosion = {
                            'x': player_x,
                            'y': player_y,
                            'timer': EXPLOSION_DURATION
                        }
                        if explosion_sound:
                            explosion_sound.play()
                        break

                screen.blit(background, (0, 0))
                
                for explosion in explosions:
                    screen.blit(explosion_img, (explosion['x'], explosion['y']))
                
                if not player_explosion:
                    screen.blit(player_img, (player_x, player_y))
                elif player_explosion:
                    screen.blit(explosion_img, (player_explosion['x'], player_explosion['y']))
                
                for bullet in bullets:
                    screen.blit(bullet_img, (bullet['x'], bullet['y']))
                
                for bomb in bombs:
                    screen.blit(bomb_img, (bomb['x'], bomb['y']))
                
                for enemy in enemies:
                    if enemy['type'] == "bomber":
                        screen.blit(bomber_img, (enemy['x'], enemy['y']))
                    elif enemy['type'] == "elite":
                        screen.blit(elite_img, (enemy['x'], enemy['y']))
                    elif enemy['type'] == "mega":
                        screen.blit(mega_img, (enemy['x'], enemy['y']))
                    else:
                        screen.blit(enemy_img, (enemy['x'], enemy['y']))

                font = pygame.font.SysFont('Arial', 36, bold=True)
                status_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
                status_rect = status_text.get_rect(center=(WIDTH//2, HEIGHT - 20))
                screen.blit(status_text, status_rect)

                for i in range(lives):
                    screen.blit(lives_icon, (WIDTH - (LIVES_ICON_WIDTH + 10) * (i + 1), HEIGHT - LIVES_ICON_HEIGHT - 10))

                pygame.display.flip()
                
                clock.tick(60)

            except Exception as e:
                debug_print(f"Error in game loop: {e}")
                running = False

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        debug_print("Exiting play_game()...")
        return score
    except Exception as e:
        debug_print(f"Error in play_game(): {e}")
        input("Press Enter to exit...")
        sys.exit(1)

# Main game loop with high scores and end credits
debug_print("Starting main loop...")
try:
    high_scores = load_high_scores()
    while True:
        show_start_screen(high_scores)
        final_score = play_game()
        
        if not high_scores or final_score > min([entry['score'] for entry in high_scores]) or len(high_scores) < 5:
            initials = show_enter_initials_screen(final_score)
            high_scores = update_high_scores(final_score, initials)
            save_high_scores(high_scores)
        
        if not show_game_over_screen(final_score):
            show_end_credits()  # Show credits before exiting
            break
except Exception as e:
    debug_print(f"Error in main loop: {e}")
    input("Press Enter to exit...")
finally:
    pygame.quit()
    debug_print(f"Game Over! Final Score: {final_score if 'final_score' in locals() else 'N/A'}")
    input("Press Enter to exit...")