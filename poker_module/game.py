from random import randint

class Game():
    def __init__(self, blind: int, players: list):
        self.blind: int = blind
        self.players: list = players
        self.btn: int = None

        self.cards: list = []
        self.table: list = []
        self.pot: int = 0
        self.deck = [ # ♠♥♣♦
            "♠2", "♠3", "♠4", "♠5", "♠6", "♠7", "♠8", "♠9", "♠T", "♠J", "♠Q", "♠K", "♠A",
            "♣2", "♣3", "♣4", "♣5", "♣6", "♣7", "♣8", "♣9", "♣T", "♣J", "♣Q", "♣K", "♣A",
            "♥2", "♥3", "♥4", "♥5", "♥6", "♥7", "♥8", "♥9", "♥T", "♥J", "♥Q", "♥K", "♥A",
            "♦2", "♦3", "♦4", "♦5", "♦6", "♦7", "♦8", "♦9", "♦T", "♦J", "♦Q", "♦K", "♦A",
        ]



    def add_card(self, card: str):
        self.cards.append(card)

    def add_pot(self, amount: int):
        self.pot += amount

    def give_cards(self):
        for p in self.players:
            for i in range(2):
                card = self.deck[randint(0, 51)]
                while card in self.cards:
                    card = self.deck[randint(0, 51)]
                self.add_card(card)
                p.add_card(card)

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
            big_blind.bal(- self.blind *2)

            self.add_pot(self.blind *3)

        return BTN
    
    def take_action(self, player, action, bet): # actions: check, call, bet, raise, all-in
        action = action.split()
        action_type = action[0]
        all_in_value = 0
        if len(action) == 2:
            bet_amount = int(action[1])
            if action_type == "call":
                player.bal(-bet)
                self.add_pot(bet)
            elif action_type == "bet":
                player.bal(-bet_amount)
                self.add_pot(bet_amount)
            elif action_type == "raise":
                player.bal(-bet_amount)
                self.add_pot(bet_amount)
            elif action_type == "all_in":
                self.add_pot(player.balance)
                all_in_value = player.balance
                player.all_in()
        else:
            if action_type == "fold":
                player.folded = True

        if action == "all_in":
            print(f"{player.name} ({player.balance}) goes all in with {all_in_value}.")
        if len(action) == 2:
            print(f"{player.name} ({player.balance}) {action[0]}s {action[1]}.")
        else:
            print(f"{player.name} ({player.balance}) {action[0]}s.")

    
    def round(self, bet = 0):
        num_player = len(self.players)
        i = self.btn + 3
        count = 0
        last_raiser: int = None
        bet = bet
        

        while count < num_player:

            turn = self.players[i % num_player]
            if turn.folded: # when the turn is folded, ignore and skip
                i += 1
                continue

            if turn.all_in: # when the turn is folded, ignore and skip
                i += 1
                continue

            print(f"{turn.name}s turn:")

            if last_raiser is not None and i%num_player == last_raiser: # if the turn is the last raiser with no new raises, end the round
                print("last raiser is turn")
                break
            
            action = turn.decide(bet, self.blind)

            if len(action.split()) == 2:
                if int(action.split()[1]) > bet: # when new bet is higher than current bet
                    last_raiser = i%num_player
                    if action.split()[0] == "all_in":
                        bet = turn.balance
                    bet = int(action.split()[1])
                    count = 0
            else:
                count += 1

            i += 1

            self.take_action(turn, action, bet)
        print("round ended")


                
