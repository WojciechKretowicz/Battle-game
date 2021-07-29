from player import Player
import random


class Battle:
    def __init__(self, n_colors=4, n_cards=52, record_history=True, random_state=None):
        if n_cards % n_colors != 0:
            raise ValueError("n_cards % n_colors != 0")

        random.seed(random_state)

        self.n_colors = n_colors
        self.n_cards = n_cards
        self.player1 = Player(random.randint(1, 1e9))
        self.player2 = Player(random.randint(1, 1e9))

        self.random_state = random_state

        self.cards = [(h, c) for h in range(self.n_cards // n_colors) for c in range(n_colors)]
        self.player1.cards = random.sample(self.cards, self.n_cards // 2)
        self.player2.cards = list(set(self.cards).difference(self.player1.cards))
        random.shuffle(self.player2.cards)

        self.history = [] if record_history else None

    def play(self, verbose=True):
        state = 0
        while state == 0:
            state = self.battle()

        if verbose:
            if state == 1:
                print("Player 1 won")
            else:
                print("Player 2 won")

        return state

    def battle(self):
        cards = []
        hist = []
        while True:

            state = self.is_the_end()
            if state != 0:
                break
            card1 = self.player1.play_card()
            card2 = self.player2.play_card()

            if self.history:
                hist.append({'cards': (card1, card2)})

            cards.append(card1)
            cards.append(card2)

            if card1[0] > card2[0]:
                self.player1.take_cards(cards)
                if self.history:
                    hist[-1]['winner'] = 1
                break
            elif card1[0] < card2[0]:
                self.player2.take_cards(cards)
                if self.history:
                    hist[-1]['winner'] = 2
                break
            else:
                state = self.is_the_end()
                if self.history:
                    hist[-1]['winner'] = 0
                if state != 0:
                    break

                card1 = self.player1.play_card()
                card2 = self.player2.play_card()
                if self.history:
                    hist[-1]['hidden'] = (card1, card2)

                cards.append(card1)
                cards.append(card2)

        self.history.append(hist)
        return state

    def is_the_end(self):
        p1 = self.player1.is_able_to_play()
        p2 = self.player2.is_able_to_play()

        if not p1:
            return 2
        if not p2:
            return 1
        return 0
