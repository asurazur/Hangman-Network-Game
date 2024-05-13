import pygame
import json
from src.hangman import Hangman
from src.request import Request

class StartState():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.loop = True

    def run(self, entity):
        entity.player.set_ready(True)
        while self.loop:
            self.clock.tick(60)
            self.handle_event(entity)

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
                self.loop=False
                entity.word = data.get_word()
                entity.category = data.get_category()
                entity.game_state.change_state(GameState())
                entity.run()

    def handle_event(self, entity):
        for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                    self.loop = False

class CountDownState():
    pass


class GameState():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.loop = True

    def run(self,entity):
        while self.loop:
            self.clock.tick(60)
            #handle input
            self.handle_event(entity)
            
            # Update Canvas
            entity.canvas.draw_background()
            Hangman.draw(entity.player.get_wrong(), entity.canvas.get_canvas())
            entity.canvas.draw_text(entity.hidden, 20, entity.width/2, entity.height/2)
            entity.canvas.update()
            
            # Network Stuff
            data:Request = entity.load_data(entity.send_data())
            entity.opponent = data.get_player()
            #Update Attributes
            print(entity.player)
            print(entity.opponent)
            print(set(entity.word))
            print(entity.player.get_correct_chars())

            #Player Wins if, word = correct_chars OR opponent Lose
            is_player_match = (set(entity.word) == entity.player.get_correct_chars())
            is_opp_match = (set(entity.word) == entity.opponent.get_correct_chars())
            if is_player_match or entity.opponent.is_lose():
                entity.player.set_finished(True)
                entity.game_state.change_state(EndState())
                entity.run()
            elif is_opp_match or entity.player.is_lose():
                entity.opponent.set_finished(True)
                entity.game_state.change_state(EndState())
                entity.run()
            else:
                continue

    def handle_event(self, entity):
         for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                    self.loop = False

                if event.type == pygame.KEYDOWN:
                    try:
                        char = chr(event.key).lower()
                        word = entity.word.lower()
                        if char in word:
                            entity.player.add_correct(char)
                        else:
                            entity.player.add_wrong(char)
                    except Exception as e:
                        print(str(e))

class EndState():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.loop = True

    def run(self,entity):
        while self.loop:
            self.clock.tick(60)
            #handle input
            self.handle_event(entity)
            if(entity.player.get_finished()):
                print("You Win")
            else:
                print("You Lose")
            # Update Canvas
            entity.canvas.draw_background()
            Hangman.draw(entity.player.get_wrong(), entity.canvas.get_canvas())
            entity.canvas.draw_text(entity.hidden, 20, entity.width/2, entity.height/2)
            entity.canvas.update()

    def handle_event(self, entity):
        for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                    self.loop = False