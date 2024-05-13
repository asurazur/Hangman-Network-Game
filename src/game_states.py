import pygame
import json
from src.hangman import Hangman
from src.request import Request

class StartState():
    def run(self, entity):
        clock = pygame.time.Clock()
        run = True
        entity.player.set_ready(True)
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                    run = False

            #Display
            entity.canvas.draw_background()
            Hangman.prehangman(entity.canvas.get_canvas())
            message="waiting for opponent"
            entity.canvas.draw_text(message, 20, entity.width/2, entity.height/2)
            entity.canvas.update()

            #Network Stuff
            data:Request = entity.load_data(entity.send_data())
            entity.opponent = data.get_player()
            opponentReady = entity.opponent.get_ready()
            playerReady = entity.player.get_ready()

            #Change Game State
            if (opponentReady and playerReady):
                run=False
                entity.word = data.get_word()
                entity.category = data.get_category()
                print(entity.word)
                print(entity.category)
                entity.game_state.change_state(GameState())
                entity.run()

class CountDownState():
    pass


class GameState():
    def run(self,entity):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                    run = False

            keys = pygame.key.get_pressed()

            #handle input



            # Update Canvas
            entity.canvas.draw_background()
            Hangman.draw(entity.player.get_wrong(), entity.canvas.get_canvas())
            entity.canvas.draw_text("In Game", 20, entity.width/2, entity.height/2)
            entity.canvas.update()
            
            # Network Stuff
            # data = entity.load_data(entity.send_data())
            #Update Attributes
        

class EndState():
    pass