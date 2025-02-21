from poker_module import Game, Player, Bot
# git push -u origin main


# ---------- VARIABLES And INPUTS ---------- #
start_balance = 10000
bots_amount = 4 #int(input("Bots amount: "))
players_amount = 1 #int(input("Players amount: "))
default_configuration = {
        "aggressiveness": 0.5,
        "bluff_frequency": 0.7,
        "risk_tolerance": 0.5
        }

# ---------- FUNCTIONS ---------- #
def br():
    print("="*60)

def create_players(bots_amount, players_amount):
    players = []
    for i in range (players_amount):
        players.append(Player(f"Player{i+1}", start_balance))
    for i in range (bots_amount):
        players.append(Bot(f"Bob{i+1}", start_balance, default_configuration))

    return players

players = create_players(bots_amount, players_amount)
game = Game(100, players)

def hand_round():
    global players, game
    num_players = len(players)
    game.give_cards()
    dealer_button = game.process_blind()

    br()
    print("POKER GAME")
    print([p.name for p in players])
    print(f"BTN: {players[dealer_button].name}")
    print(f"SB: {players[(dealer_button+1) % num_players].name}")
    print(f"BB: {players[(dealer_button+2) % num_players].name}")
    br()

    game.round(game.blind *2)

hand_round()
