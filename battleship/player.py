class Player:
    def __init__(self):
        self.players = []

    def asking_name(self):
        player1 = input("Player 1, please enter your name: ")
        player2 = input("Player 2, please enter your name: ")
        self.players = [player1, player2]
        return self.players
