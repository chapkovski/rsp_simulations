# RoShamBo simulation (Fictitious play)  vs (WSLS from Chernov&Susin18)
import random
from collections import Counter

result_descriptor = {0: 'Lose', 1: 'Tie', 2: 'Win'}
beta = .4


class Move:
    descriptor = {0: 'Rock', 1: 'Scissors', 2: 'Paper'}
    base = 3

    def __init__(self, value, ):
        self.value = value % self.base

    def __gt__(self, other):
        return self.value % self.base > other.value % self.base

    def __lt__(self, other):
        return self.value % self.base < other.value % self.base

    def __add__(self, other):
        if isinstance(other, int):
            return Move(self.value + other)
        if isinstance(other, Move):
            return Move(self.value + other.value)

    def __sub__(self, other):
        if isinstance(other, int):
            return Move(self.value - other)
        if isinstance(other, Move):
            return Move(self.value - other.value)

    def __str__(self):
        return self.descriptor[self.value % self.base]

    def __eq__(self, other):
        return self.value == (other.value % self.base)

    def __hash__(self):
        return hash(str(self.value))

    def __int__(self):
        return int(self.value)

    def __repr__(self):
        return str(self.value)

    @classmethod
    def random_move(cls):
        return cls(random.randint(0, cls.base))


class Player:
    def get_other(self):
        return [i for i in self.game.get_players() if i != self][0]

    def __init__(self, game):
        self.history = []  # history of moves
        self.result_history = []  # history of outcomes
        self.game = game

    def __setattr__(self, key, value):
        if key == 'move':
            super().__setattr__(key, value)
            self.history.append(self.move)
            return
        super().__setattr__(key, value)

    def register_result(self):
        self.result_history.append(int(self.move - self.get_other().move + 1))


class Human(Player):
    optimal_strategy = {2: -1, 1: 1, 0: 0}

    def __init__(self, game):
        self.optimal_history = list()
        super().__init__(game)

    def check_for_optimal_strategy(self):
        prev_outcome = self.result_history[-1]
        move_vs_prev = self.move - self.history[-1]
        self.optimal_history.append(self.optimal_strategy[prev_outcome] == int(move_vs_prev))

    def make_move(self):
        if self.game.round > 1:
            other_history = self.get_other().history
            other_history_freq = Counter(other_history)
            most_pop = max([i for i in other_history_freq.values()])
            candidates = [i for i, j in other_history_freq.items() if j == most_pop]
            self.move = random.choice(candidates) + 1
            self.check_for_optimal_strategy()
        else:
            self.move = Move.random_move()


class Bot(Player):
    strategy = {2: -1, 1: 1, 0: 0}

    def make_move(self):
        if self.game.round >= 2:
            x = random.uniform(0, 1)
            if x >= beta:
                # the rule is following: if you won, you move left; if there was a tie, you move right,
                # if you lost you repeat
                self.move = Move(int(self.history[-1]) + self.strategy[self.result_history[-1]])
            else:
                self.move = Move.random_move()
        else:
            self.move = Move.random_move()


class Game:
    history = list()
    round = 0

    def __init__(self, rounds):
        self.max_age = rounds
        self.bot = Bot(self)
        self.human = Human(self)

    def get_players(self):
        return [self.bot, self.human]

    def run_game(self):
        for i in range(self.max_age):
            self.round += 1
            for p in self.get_players():
                p.make_move()
            for p in self.get_players():
                p.register_result()


for j in range(100):
    game = Game(100)
    game.run_game()
    print('Iteration {0}: Optimal decisions share by human: {1:.0%}'.format(j, sum(
        game.human.optimal_history) / game.max_age))
