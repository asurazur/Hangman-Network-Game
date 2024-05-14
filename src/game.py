import pygame
import pickle
from src.network import Network
from src.player import Player
from src.canvas import Canvas
from src.game_states import *
from src.state_manager import StateManager
from src.request import Request

class Game:
    def __init__(self, w, h, host, port):
        pygame.mixer.init()
        self.net = Network(host, port)
        self.width = w
        self.height = h
        self.word = ''
        self.category = ''
        self.hidden = ''
        self.player = Player()
        self.opponent = Player()
        self.canvas = Canvas(self.width, self.height, "Guess Word")
        self.game_state = StateManager(StartState())

    def run(self):
        self.game_state.run(self)

    def send_data(self):
        """
        Send game state to server
        :return: str
        """
        request = Request(self.net.id, None, None, self.player)
        data = pickle.dumps(request)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def load_data(data) -> Request:
        """
        :param data: str
        :return: Request
        """
        try:
            return pickle.loads(data)
        except:
            pass