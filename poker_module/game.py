from random import randint
from prettytable import PrettyTable
from .game_winner import decide_winner

class Game():
    def __init__(self, blind: int, players: list):
        self.blind: int = blind
        self.players: list = players
        self.btn: int = None

        self.cards: list = []
        self.community_cards: list = []
        self.pot: int = 0
        self.deck = [ # ♠♥♣♦
            "♠2", "♠3", "♠4", "♠5", "♠6", "♠7", "♠8", "♠9", "♠T", "♠J", "♠Q", "♠K", "♠A",
            "♣2", "♣3", "♣4", "♣5", "♣6", "♣7", "♣8", "♣9", "♣T", "♣J", "♣Q", "♣K", "♣A",
            "♥2", "♥3", "♥4", "♥5", "♥6", "♥7", "♥8", "♥9", "♥T", "♥J", "♥Q", "♥K", "♥A",
            "♦2", "♦3", "♦4", "♦5", "♦6", "♦7", "♦8", "♦9", "♦T", "♦J", "♦Q", "♦K", "♦A",
        ]


    # Basic Functions #
    def add_card(self, card: str):
        self.cards.append(card)

    def add_pot(self, amount: int):
        self.pot += amount

    def new_card(self):
        card = self.deck[randint(0, 51)]
        while card in self.cards:
            card = self.deck[randint(0, 51)]
        self.add_card(card)
        return card 

    def give_first_hand(self):
        for p in self.players:
            for i in range(2):
                card = self.new_card()
                p.add_card(card)
    
    def give_com_card(self, amount):
        for i in range (amount):
            card = self.new_card()
            self.community_cards.append(card)
            for p in self.players:
                p.add_card(card)

    def print_current(self):
        table = PrettyTable()
        table.field_names = ["Name", "Balance", "Folded"]
        for player in self.players:
            table.add_row([player.name, player.balance, player.folded])
        print(f"Pot: {self.pot}")
        print(table)

    def process_blind(self):
        num_players = len(self.players)
        players = self.players
        BTN = randint(0, num_players-1)
        self.btn = BTN
        if num_players <= 2:
            SB = BTN
            BB = (BTN + 1) % num_players
        else:
            SB = (BTN + 1) % num_players
            BB = (BTN + 2) % num_players

        small_blind = players[SB]
        big_blind = players[BB]
        if small_blind.balance <= self.blind:
            self.add_pot(small_blind.balance)
            small_blind.all_in()
        if big_blind.balance <= self.blind * 2:
            self.add_pot(big_blind.balance)
            big_blind.all_in()
        else:
            small_blind.bal(- self.blind)
            small_blind.add_stake(self.blind)
            big_blind.bal(- self.blind *2)
            big_blind.add_stake(self.blind * 2)

            self.add_pot(self.blind *3)

        return BTN

    # Game mechanic Functions #
    def start(self):
        def br():
            print("="*60)
        def reset():
            for p in players:
                p.round_reset()
        players = self.players
        num_players = len(players)
        player = next((p for p in self.players if p.name == "Player1"), None)

        self.give_first_hand()
        dealer_button = self.process_blind()

        br()

        print("POKER GAME")
        print(f"BTN: {players[dealer_button].name}")
        print(f"SB: {players[(dealer_button+1) % num_players].name}")
        print(f"BB: {players[(dealer_button+2) % num_players].name}")
        if player is not None:
            print(f"Balance: {player.balance}")
            print(f"Cards: {player.cards}")

        br()

        self.round(3, self.blind *2)

        br()

        self.print_current()
        reset()

        self.give_com_card(3)
        print(f"Community cards: {self.community_cards}")
        if player is not None:
            print(f"Balance: {player.balance}")
            print(f"Cards: {player.cards[:2]}")
        self.round()

        br()

        self.print_current()
        reset()

        self.give_com_card(1)
        print(f"Community cards: {self.community_cards}")
        if player is not None:
            print(f"Balance: {player.balance}")
            print(f"Cards: {player.cards[:2]}")
        self.round()

        br()

        self.print_current()
        reset()

        self.give_com_card(1)
        print(f"Community cards: {self.community_cards}")
        if player is not None:
            print(f"Balance: {player.balance}")
            print(f"Cards: {player.cards[:2]}")
        self.round()

        winners = decide_winner([p for p in self.players if not p.folded])
        hand_rankings = {1: "High Card", 2: "Pair", 3: "Two Pair", 4: "Three of a Kind", 5: "Straight", 6: "Flush", 7: "Full House", 8: "Four of a Kind", 9: "Straight Flush", 10: "Royal Flush", }
        print(f"{[winner.name for winner in winners[0]]} won the hand with {hand_rankings[winners[1]]}!")

    def take_action(self, player, action, bet): # actions: check, call, bet, raise, all-in
        action = action.split()
        action_type = action[0]
        all_in_value = 0
        if len(action) == 2:
            bet_amount = int(action[1])

            if action_type == "bet":
                player.bal(-bet_amount)
                self.add_pot(bet_amount)
                print(f"{player.name} ({player.balance}) bets {action[1]}.")
                player.add_stake(bet_amount)

            elif action_type == "raise":
                player.bal(-(bet_amount-player.round_stake))
                self.add_pot(bet_amount-player.round_stake)
                print(f"{player.name} ({player.balance}) raises to {action[1]} (+{bet_amount-player.round_stake}).")
                player.add_stake(bet_amount - player.round_stake)

            elif action_type == "all_in":
                self.add_pot(player.balance)
                all_in_value = player.balance
                player.add_stake(player.balance)
                player.all_in()
                print(f"{player.name} ({player.balance}) goes all in with {all_in_value}.")
        else:
            if action_type == "call":
                player.bal(-(bet-player.round_stake))
                self.add_pot(bet-player.round_stake)
                
                print(f"{player.name} ({player.balance}) calls {bet} (+{bet-player.round_stake}).")
                player.add_stake(bet - player.round_stake)

            elif action_type == "fold":
                player.folded = True
                print(f"{player.name} ({player.balance}) folds.")

            elif action_type == "check":
                print(f"{player.name} ({player.balance}) checks.")


    def round(self, pos = 1, bet = 0):
        num_player = len(self.players)
        i = self.btn + pos
        count = 0
        last_raiser: int = None
        bet = bet
        

        while count < num_player:

            turn = self.players[i % num_player]

            if turn.folded: # when the turn is folded, ignore and skip
                i += 1
                count += 1
                continue

            if turn.all_in: # when the turn is folded, ignore and skip
                i += 1
                count += 1
                continue

            if last_raiser is not None and i%num_player == last_raiser: # if the turn is the last raiser with no new raises, end the round
                print("last raiser is turn")
                break

            print(f"{turn.name}s turn:")
            action = turn.decide(bet, self.blind)

            if len(action.split()) == 2:
                if int(action.split()[1]) > bet: # when new bet is higher than current bet
                    last_raiser = i % num_player
                    if action.split()[0] == "all_in":
                        bet = turn.balance
                    else:
                        bet = int(action.split()[1])
                    count = 0  # Reset count only if a new bet is made
                else:
                    count += 1  # Increase count only if no new bet is made
            else:
                count += 1  # Increase count if it's a simple action like "check" or "call"

            i += 1

            self.take_action(turn, action, bet)
            print("-"*10)