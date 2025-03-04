import pygame as pg
import random as rn

# Initialize the game
pg.init()
# Set display surface
window_width = 1000
window_height = 400
display_surface = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Feed the dragon")
# Set FPS and clock
FPS = 60
clock = pg.time.Clock()
# Set game values
player_starting_lives = 5 #Don't change these, they might ruin your gameplay
player_velocity = 5
coin_starting_velocity = 10
coin_acceleration = 0.5
player_acceleration = 0.5 
buffer_distance = 100
score = 0
player_lives = player_starting_lives
coin_velocity = coin_starting_velocity
linex = 64
liney = 0
# Set color
green = (0, 255, 0)
dark_green = (10, 50, 10)
white = (255, 255, 255)
black = (0, 0, 0)

# Set font
font = pg.font.Font("graffiti.ttf", 32)
# Set text
score_text = font.render("Score: " + str(score), True, green, dark_green)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render("Feed the Dragon", True, green, black)
title_rect = title_text.get_rect()
title_rect.centerx = window_width // 2
title_rect.y = 10

lives_text = font.render("Lives: " + str(player_lives), True, green, dark_green)
lives_rect = lives_text.get_rect()
lives_rect.topright = (window_width - 10, 10)

game_over_text = font.render("Game over!", True, green, dark_green)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (window_width // 2, window_height // 2)

continue_text = font.render("Press any key to play again", True, green, dark_green)
continue_rect = continue_text.get_rect()
continue_rect.center = (window_width // 2, window_height // 2 + 32)

# Set sounds and music
coin_sound = pg.mixer.Sound("coin_sound.wav")
miss_sound = pg.mixer.Sound("miss_sound.wav")
miss_sound.set_volume(0.1)
pg.mixer.music.load("ftd_background_music.wav")
# Set images
player_image = pg.image.load("dragon_right.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = window_height // 2
coin_image = pg.image.load("coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = window_width + buffer_distance
coin_rect.y = rn.randint(64, window_height - 32)
# Main game loop:
pg.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    #keys code
    keys = pg.key.get_pressed()
    # Move the dragon (up and down)
    if (keys[pg.K_w] or keys[pg.K_UP]) and player_rect.top > 64:
        player_rect.y -= player_velocity
    if (keys[pg.K_s] or keys[pg.K_DOWN]) and player_rect.bottom < window_height:
        player_rect.y += player_velocity
    #move the coin
    if coin_rect.x < 0:
        #player missed the coin
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = window_width + buffer_distance
        coin_rect.y = rn.randint(64, window_height - 32)
    else:
        #move the coin
        coin_rect.x -= coin_velocity
    #Check if you touched the coin
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += coin_acceleration
        player_velocity += player_acceleration
        coin_rect.x = window_width + buffer_distance
        coin_rect.y = rn.randint(64, window_height)
    #Update the HUD
    score_text = font.render("Score: " + str(score), True, green, dark_green)
    lives_text = font.render("Lives: " + str(player_lives), True, green, dark_green)
    #Game over condition!
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pg.display.update()
        #Pause the game until the user presses a key
        pg.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_paused = False
                    running = False
                if event.type == pg.KEYDOWN:
                    score = 0
                    player_lives = player_starting_lives
                    player_rect.y = window_height//2
                    coin_velocity = coin_starting_velocity
                    pg.mixer.music.play(-1, 0.0)
                    is_paused = False
    #Fill the display surface
    display_surface.fill(black)
    # Blit the assets
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)
    pg.draw.line(display_surface, white, (liney, linex), (window_width, linex), 2)
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)
   
    # Update the display surface
    pg.display.update()
    # Tick the clock
    clock.tick(FPS)

# End the game
pg.quit()