import random


class Player:
    def __init__(self, random_state=None):
        self.cards = []
        self.discarded = []
        self.random_state = random_state

    def play_card(self):
        if len(self.cards) == 0:
            self.shuffle()

        card = self.cards.pop()
        return card

    def shuffle(self, randomization=False):
        if len(self.cards):
            raise ValueError("You still have some cards in your hand!")

        self.cards = self.discarded
        self.discarded = []

        if randomization:
            if self.random_state is not None:
                random.seed(self.random_state)

            random.shuffle(self.cards)

    def is_able_to_play(self):
        return True if len(self.cards) + len(self.discarded) != 0 else False

    def take_cards(self, *cards):
        for c in cards:
            self.discarded += c
