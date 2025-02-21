from random import random

class Bot():
    def __init__(self, name: str, balance: int, configuration: dict):

        self.balance: int = balance
        self.name: str = name

        self.aggressiveness = configuration["aggressiveness"]
        self.bluff_frequency = configuration["bluff_frequency"]
        self.risk_tolerance = configuration["risk_tolerance"]

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

    def rate_hand(self):
        if len(self.cards) == 2: # Preflop Hand
            cards = self.cards

            ranks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

            rank1, rank2 = ranks[cards[0][1]], ranks[cards[1][1]]
            suit1, suit2 = cards[0][0], cards[1][0]

            is_suited = suit1 == suit2
            is_pair = rank1 == rank2
            diff = abs(rank1-rank2)

            if is_pair:
                if rank1 >= 10:
                    return 10
                elif rank1 >= 7:
                    return 8
                elif rank1 >= 4:
                    return 6
                else: return 4

            elif is_suited:
                if (rank1, rank2) in [(14,13), (14,12)]:
                    return 9
                elif (rank1, rank2) in [(14,11), (13,12)]:
                    return 8
                elif (rank1, rank2) in [(14,10), (13,11)]:
                    return 7
                elif diff == 1 and max(rank1, rank2) >= 9:
                    return 6
                elif diff == 2 and max(rank1, rank2) >= 10:
                    return 5
                elif diff == 1 and max(rank1, rank2) >= 7:
                    return 5
                else:
                    return 4
                
            else:
                if (rank1, rank2) in [(14,13), (14,12)]:
                    return 8
                elif (rank1, rank2) in [(14,11), (13,12)]:
                    return 7
                elif diff == 1 and max(rank1, rank2) >= 10:
                    return 6
                elif diff == 2 and max(rank1, rank2) >= 11:
                    return 5
                elif diff == 3 and max(rank1, rank2) >= 11:
                    return 4
                elif max(rank1, rank2) >= 10:
                    return 3
                else:
                    return 2
                
    def decide(self, bet, blind):
        rand = random()
        rating = self.rate_hand()
        aggressiveness = self.aggressiveness >= rand
        bluff_frequency = self.bluff_frequency >= rand
        risk_tolerance = self.risk_tolerance >= rand

        if bet == 0:
            return f"bet {blind}" if (rating <= 4) and (aggressiveness or bluff_frequency) else "check"
        elif bet >= self.balance:
            return f"all-in {self.balance}" if rating >= 7 or risk_tolerance else "fold"
        else:
            if rating >= 7 or risk_tolerance:
                if aggressiveness:
                    return f"raise {2*bet}" if 2*bet < self.balance else f"call {bet}"
                else:
                    return f"call {bet}"
            elif rating <= 3 and not bluff_frequency:
                return "fold"
            else:
                return f"call {bet}"