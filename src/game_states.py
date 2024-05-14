import pygame
import json
from src.hangman import *
from src.request import Request

class StartState():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.loop = True

    def run(self, entity):
        pygame.mixer.music.load('src/Music/KM/Two Finger Johnny.mp3')
        pygame.mixer.music.play()
        entity.player.set_ready(True)
        while self.loop:
            self.clock.tick(60)
            self.handle_event(entity)

            #Network Stuff
            data = entity.load_data(entity.send_data())
            entity.opponent = data.get_player()
            opponentReady = entity.opponent.get_ready()
            playerReady = entity.player.get_ready()

            #Display
            entity.canvas.draw_background()
            Hangman.prehangman(entity.canvas.get_canvas())
            message="waiting for opponent"
            entity.canvas.draw_text(message, 30, entity.width/2 -25, entity.height/2)
            entity.canvas.update()

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


class GameState():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.loop = True

    def run(self,entity):
        while self.loop:
            self.clock.tick(60)
            #handle input
            self.handle_event(entity)
            
            #Validate
            is_player_match = (len(set(entity.word)) == entity.player.get_correct())
            is_opp_match = (len(set(entity.word)) == entity.player.get_correct())
            opponent_lose = entity.opponent.is_lose()
            player_lose = entity.player.is_lose()
            if is_player_match or opponent_lose:
                entity.player.set_finished(True)
            elif is_opp_match or player_lose:
                entity.opponent.set_finished(True)
            # Network Stuff
            data = entity.load_data(entity.send_data())
            entity.opponent = data.get_player()

            #Log
            print("You:", str(entity.player))
            print("Enemy:", str(entity.opponent))

            # Update Canvas
            entity.canvas.draw_background()
            Hangman.draw(entity.player.get_wrong(), entity.canvas.get_canvas())
            entity.hidden = GameState.parse_hidden(entity.word, entity.player.get_correct_chars())
            entity.canvas.draw_text(entity.hidden.upper(), 50, entity.width/2 + 75 , entity.height/2)
            entity.canvas.draw_text(entity.category, 38, entity.width/2 + 75, entity.height/2 + 50)
            entity.canvas.update()

            #Update Attributes
            #Player Wins if, word = correct_chars OR opponent Lose
            if entity.player.get_finished() or entity.opponent.get_finished():
                self.loop = False
                entity.game_state.change_state(EndState())
                entity.run()
                    
    @staticmethod
    def parse_hidden(word: str, chars: set) -> str:
        """
        example:
            hidden = ''
            word = 'pizza'
            chars = ('p', 'z')
        
        """
        hidden = [i if i in chars  else '-' for i in word]
        return ''.join(hidden)



    def handle_event(self, entity):
         for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                    self.loop = False

                if event.type == pygame.KEYDOWN:
                    pygame.mixer.Sound('src/Music/Keyboard.wav').play()
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
        pygame.mixer.music.stop()
        pygame.mixer.Sound('src/Music/KM/Loping Sting.mp3').play()
        while self.loop:
            self.clock.tick(60)
            #handle input
            self.handle_event(entity)

            # Network Stuff
            data = entity.load_data(entity.send_data())
            entity.opponent = data.get_player()

            # Update Canvas
            entity.canvas.draw_background()
            if entity.player.get_finished():
                entity.canvas.draw_text("You Win", 50, entity.width/2 -60, entity.height/2 -70, GREEN)
            else:
                entity.canvas.draw_text("You Lose", 50, entity.width/2 -60, entity.height/2 -70, RED)

            entity.canvas.draw_text("The Word Is", 50, entity.width/2 -75, entity.height/2 -35)
            entity.canvas.draw_text("\""+ entity.word.upper() + "\"", 50, entity.width/2 -69, entity.height/2)
            entity.canvas.update()


    def handle_event(self, entity):
        for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                    self.loop = False