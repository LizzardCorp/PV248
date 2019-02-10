import pygame
import math
from bar import Bar
from cube import Cube
from block import Block
import time

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)

def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    size = (1360, 780)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Breakout')
    font = pygame.font.Font(None, 36)
    block_count = 132
    over = pygame.mixer.Sound('game_over.wav')
    #winner = pygame.mixer.Sound('heureka.wav')

    all_sprites_list = pygame.sprite.Group()
    blocks = pygame.sprite.Group()

    bar = Bar(WHITE, 100, 10)
    bar.rect.x = 600
    bar.rect.y = 760

    cube = Cube(WHITE, 10, 10)
    cube.rect.x = 650
    cube.rect.y = 740

    for i in range(0,12):
        for j in range(1,12):
            block = Block(WHITE, 100, 20)
            block.rect.x = i*100+((i+1)*12)
            block.rect.y = j*20+(j*5)
            blocks.add(block)

    all_sprites_list.add(cube)
    all_sprites_list.add(bar)


    carryOn = True
    clock = pygame.time.Clock()

    game_over = False

    while carryOn:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
            elif event.type == pygame.MOUSEMOTION:
                mouse = pygame.mouse.get_pos()[0]
                if mouse > 1260:
                    bar.rect.x = 1260
                elif mouse < 0:
                    bar.rect.x = 0
                else:
                    bar.rect.x = mouse

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if bar.rect.x > 0:
                bar.moveLeft(10)
        if keys[pygame.K_RIGHT]:
            if bar.rect.x < 1260:
                bar.moveRight(10)

        if not game_over:
            game_over = cube.update()
        else:
            over.play()
            text = font.render("Game Over", True, WHITE)
            textpos = text.get_rect(centerx=1360/2)
            textpos.top = 300
            screen.blit(text, textpos)
            carryOn = False

        collision_bar = pygame.sprite.spritecollide(cube, [bar], False)
        if len(collision_bar) > 0:
            cube.bounce(0)

        for block in blocks:
            if cube.cube_collision(block):
                blocks.remove(block)

        if len(blocks) < 1:
            #winner.play()
            text = font.render("You win", True, WHITE)
            textpos = text.get_rect(centerx=1360/2)
            textpos.top = 300
            screen.blit(text, textpos)
            carryOn = False

        blocks.update()
        all_sprites_list.update()



        # --- Drawing code should go here

        all_sprites_list.draw(screen)
        blocks.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    time.sleep(5)
    pygame.quit()



if __name__ == '__main__':
    main()
