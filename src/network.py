import socket
import pickle
import json
import random
import time
import os
from .request import Request
from .player import Player


class Network:
    random.seed(time.time())
    currentId = "0"
    generate_word = True
    states = [Request(0, '', '', Player()), Request(1, '', '', Player())]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "words.json")
    with open(json_file_path, "r") as f:
        words = json.load(f)


    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = port
        self.addr = (self.host, self.port)
        self.id = self.connect() 


    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        """
        :param data: bytes
        :return: bytes
        """
        try:
            self.client.send(data)
            reply = self.client.recv(2048)
            return reply
        except socket.error as e:
            return str(e)
        
    @staticmethod
    def threaded_client(conn):
        conn.send(str.encode(Network.currentId))
        Network.currentId = "1"
        while True:
            try:
                if Network.generate_word:
                    word, category = Network.generate_word()
                    Network.states[0].set_guess(word, category)
                    Network.states[1].set_guess(word, category)
                    Network.generate_word = False
                    print(word, category)
                    print(set(word.upper()))
                data = conn.recv(2048)
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    request:Request = pickle.loads(data)
                    player:Player = request.get_player()
                    id:int = request.get_net_id()
                    Network.states[id].set_player(player)
                    if id == 0: nid = 1
                    if id == 1: nid = 0
                    reply = pickle.dumps(Network.states[nid])
                    conn.sendall(reply)
            except:
                print("An Error has Occurred")
                break

        print("Connection Closed")
        conn.close()
    
    @staticmethod
    def generate_word() -> tuple[str, str]:
        """
        Returns a random word with its category
        :return: tuple[str, str]
        """
        
        categories = list(Network.words.keys())
        category = random.choice(categories)
        words = list(Network.words[category])
        word = random.choice(words)
        return (word, category)
