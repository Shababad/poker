class Player():
    def __init__(self, name: str, balance: int):

        self.balance: int = balance
        self.name: str = name

        self.cards: list = []
        self.type = "human"

        self.round_stake: int = 0
        self.hand_stake: int = 0
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

    def decide(self, bet, blind):
        possible_actions = ["all_in", "raise", "fold"]
        if bet > 0:
            possible_actions.append("call")
        elif bet == 0:
            possible_actions.append("check")
            possible_actions.append("bet")
        action = input(f"Your action: {possible_actions}: ")
        while action.split()[0] not in possible_actions:
            action = input(f"Invalid action,  try again: {possible_actions}: ")

        return action
