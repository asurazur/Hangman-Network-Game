class Request:
    def __init__(self, id, word, category, player):
        self.id = id
        self.word = word
        self.category = category
        self.player = player

    def get_net_id(self):
        return int(self.id)
    
    def get_player(self):
        return self.player
    
    def get_word(self):
        return self.word
    
    def get_category(self):
        return self.category
    
    def set_player(self, player):
        self.player = player

    def set_guess(self, word, category):
        self.word = word
        self.category = category