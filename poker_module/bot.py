from .bot_decide import decide, rate_hand

class Bot():
    def __init__(self, name: str, balance: int, configuration: dict):

        self.balance: int = balance
        self.name: str = name

        self.aggressiveness = configuration["aggressiveness"]
        self.bluff_frequency = configuration["bluff_frequency"]
        self.risk_tolerance = configuration["risk_tolerance"]

        self.round_stake: int = 0
        self.hand_stake: int = 0
        self.cards: int = []
        self.type = "bot"

        self.folded: bool = False
        self.all_in: bool = False

    def add_card(self, card: str):
        self.cards.append(card)

    def all_in(self):
        self.balance = 0
        self.all_in = True

    def bal(self, amount):
        self.balance += amount

    def add_stake(self, amount):
        self.round_stake += amount
        self.hand_stake += amount

    def round_reset(self):
        self.round_stake = 0

Bot.decide = decide
Bot.rate_hand = rate_hand
