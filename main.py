from poker_module import Game, Player, Bot
from time import time

# git push -u origin main
#c:/Users/abiel/Documents/PokerProject/main.py

# ---------- VARIABLES And INPUTS ---------- #
start_balance = 10000
bots_amount = 1 #int(input("Bots amount: "))
players_amount = 1 #int(input("Players amount: "))
default_configuration = {
        "aggressiveness": 0.51,
        "bluff_frequency": 0.91,
        "risk_tolerance": 0.61
        }
# ---------- FUNCTIONS ---------- #

def create_players(bots_amount, players_amount):
    players = []
    for i in range (players_amount):
        players.append(Player(f"Player{i+1}", start_balance))
    for i in range (bots_amount):
        players.append(Bot(f"Bob{i+1}", start_balance, default_configuration))
        

    return players

players = create_players(bots_amount, players_amount)
game = Game(100, players)
for p in players:
    game.win_count[p.name] = 0


#start = time()
while True:
    if input("Enter 'start' to start: ") == "start":
        game.start()
    else:
        break
print(game.win_count)
#end = time()
#print(f"1000 games took {end-start} seconds")

