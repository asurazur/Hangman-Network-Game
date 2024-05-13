import pygame

class Player():
    def __init__(self):
        self.correct_chars = set()
        self.wrong_chars = set()
        self.ready = False
        self.finished = False

    def set_ready(self, isReady):
        self.ready = isReady

    def get_ready(self):
        return self.ready

    def set_finished(self, finished):
        self.finished = finished
    
    def get_finished(self):
        return self.finished
    
    def add_correct(self, char):
        self.correct_chars.add(char)

    def get_correct_chars(self):
        return self.correct_chars

    def add_wrong(self, char):
        self.wrong_chars.add(char)

    def get_wrong_chars(self):
        return self.wrong_chars

    def get_correct(self):
        return len(self.correct_chars)

    def get_wrong(self):
        return len(self.wrong_chars)

    def is_lose(self):
        return True if len(self.wrong_chars) >= 11 else False

    def __str__(self):
        return f"Ready: {self.get_ready()} | Finished: {self.get_finished()} | Correct: {self.get_correct()} | Wrong: {self.get_wrong()}"
