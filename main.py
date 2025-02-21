from poker_module import Game, Player, Bot

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
def create_players(bots_amount, players_amount):
    global players
    players = []
    for i in range (bots_amount):
        players.append(Bot(f"Bob{i+1}", start_balance, default_configuration))
    for i in range (players_amount):
        players.append(Player(f"Player{i+1}", start_balance))

num_players = len(players)
game = Game(100, players)




# GAME #
game.give_cards()
process_blind = game.process_blind()

print("POKER GAME")
print(f"BTN: {players[process_blind].name}")
print(f"SB: {players[(process_blind+1) % num_players].name}")
print(f"BB: {players[(process_blind+2) % num_players].name}")

game.round(game.blind *2)
