#Feed the dragon
import pygame
import random

pygame.init()

GAME_FOLDER = "D:/batches/Python Ground Up/Video Games/feed_the_dragon/"

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#music
pygame.mixer.music.load(GAME_FOLDER + "background_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#sounds
loss = pygame.mixer.Sound(GAME_FOLDER + "loss.wav")
loss.set_volume(0.5)

pickup = pygame.mixer.Sound(GAME_FOLDER + "pickup.wav")
pickup.set_volume(0.5)

#background image
background_image = pygame.image.load(GAME_FOLDER + "dragon_night.jpg")
background_image = pygame.transform.scale(background_image,(WINDOW_WIDTH,WINDOW_HEIGHT))

#fonts
game_font_big = pygame.font.Font(GAME_FOLDER + "AttackGraffiti.ttf",60)
game_font_small = pygame.font.Font(GAME_FOLDER + "AttackGraffiti.ttf",30)

#Colors
GREEN = pygame.Color(34, 177,76)
RED = pygame.Color(237, 18, 36)
ORANGE = pygame.Color(255, 127, 0)

#HUD
title = game_font_big.render("Feed The Dragon", True, GREEN)
title_rect = title.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.top = 10

game_score = 0
score = game_font_small.render("Score: " + str(game_score), True, GREEN)
score_rect = score.get_rect()
score_rect.left = 50
score_rect.top = 10

game_lives = 3
lives = game_font_small.render("Lives: " + str(game_lives), True, GREEN)
lives_rect = lives.get_rect()
lives_rect.right = WINDOW_WIDTH-50
lives_rect.top = 10

#Extra Texts
game_over = game_font_big.render("Game Over!!!", True, ORANGE)
game_over_rect = game_over.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50)

what_next = game_font_small.render("Press R to Restart, Any other key to Quit!!!", True, ORANGE)
what_next_rect = what_next.get_rect()
what_next_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)

#game Actors
#dragon
dragon = pygame.image.load(GAME_FOLDER + "dragon.png")
DRAGON_VELOCITY = 5
dragon_rect = dragon.get_rect()
dragon_rect.right = WINDOW_WIDTH - 10
dragon_rect.centery = WINDOW_HEIGHT//2

#coins (dragon food)
coin_velocity = 5
all_coins = []
for i in range(6):
    coin = pygame.image.load(GAME_FOLDER + "coin" + str(i) + ".png")
    all_coins.append(pygame.transform.scale(coin, (48,48)))
coin_rect = all_coins[0].get_rect()
coin_rect.left = 0
coin_rect.centery = random.randint(100,WINDOW_HEIGHT-100)
coin_index = 0

#main game loop
clock = pygame.time.Clock()
FPS = 60
running = True
game_status = 1

while running:
    events = pygame.event.get()
    for ev in events:
        if ev. type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN and game_status == 0:
            if ev.key  == pygame.K_r:
                #reset the game values
                game_lives = 3
                game_score = 0
                coin_velocity = 5
                #render the reset values
                score = game_font_small.render("Score: " + str(game_score), True, GREEN)
                lives = game_font_small.render("Lives: " + str(game_lives), True, GREEN)
                #reposition the dragon
                dragon_rect.right = WINDOW_WIDTH - 10
                dragon_rect.centery = WINDOW_HEIGHT // 2
                # reposition the coin
                coin_rect.left = 0
                coin_rect.centery = random.randint(100, WINDOW_HEIGHT - 100)
                coin_index = 0
                #play the music
                pygame.mixer.music.play(-1)
                #restart
                game_status = 1

            else:
                running = False

    #background
    window.blit(background_image,(0,0))

    #HUD
    window.blit(title, title_rect)
    window.blit(lives, lives_rect)
    window.blit(score, score_rect)



    if game_status == 1:
        #dragon movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and dragon_rect.top > 0:
            dragon_rect.top -= DRAGON_VELOCITY
        elif keys[pygame.K_DOWN] and dragon_rect.bottom < WINDOW_HEIGHT:
            dragon_rect.top += DRAGON_VELOCITY

        # dragon
        window.blit(dragon, dragon_rect)

        #coin animation
        window.blit(all_coins[int(coin_index)], coin_rect)
        coin_index+=0.1
        if coin_index >= len(all_coins):
            coin_index = 0

        #coin movement
        coin_rect.right+= coin_velocity

        #coin pick
        if dragon_rect.colliderect(coin_rect):
            pickup.play()
            coin_rect.left = 0
            coin_rect.centery = random.randint(100, WINDOW_HEIGHT - 100)
            coin_velocity+=1
            game_score +=1
            score = game_font_small.render("Score: " + str(game_score), True, GREEN)

        #coin loss
        elif coin_rect.right > WINDOW_WIDTH:
            loss.play()
            coin_rect.left = 0
            coin_rect.centery = random.randint(100, WINDOW_HEIGHT - 100)
            coin_velocity = 5
            game_lives -= 1
            if game_lives > 0:
                lives = game_font_small.render("Lives: " + str(game_lives), True, GREEN)
            elif game_lives == 0:
                #game over
                lives = game_font_small.render("Lives: " + str(game_lives), True, RED)
                pygame.mixer.music.stop()
                game_status = 0

    elif game_status == 0:
        #game over
        window.blit(game_over, game_over_rect)
        window.blit(what_next, what_next_rect)


    pygame.display.update()
    clock.tick(FPS)

pygame.mixer.music.stop()
pygame.quit()