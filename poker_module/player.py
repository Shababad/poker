class Player():
    def __init__(self, name: str, balance: int):

        self.balance: int = balance
        self.name: str = name

        self.cards: list = []
        self.type = "human"

        self.round_stake: int = 0
        self.folded: bool = False
        self.all_in: bool = False

    def add_card(self, card: str):
        self.cards.append(card)

    def all_in(self):
        self.balance = 0
        self.all_in = True

    def bal(self, amount):
        self.balance += amount

    def decide(self, bet, blind):
        possible_actions = ["all_in", "raise"]
        if bet > 0:
            possible_actions.append("call")
        elif bet == 0:
            possible_actions.append("check")
            possible_actions.append("bet")
        action = input(f"Your turn, {possible_actions}: ")

        if action == "call":
            action = f"call {bet}"
        elif action == "all-in":
            action = f"call {self.balance}" 

        return action
