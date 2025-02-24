from collections import Counter

ranks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

def has_pair(cards):
    rank_counts = {}
    for card in cards:
        rank = card[1]  # Assuming card is ('♠', 'A') where 'A' is the rank
        if rank in rank_counts:
            return True, [rank_counts[rank], card]  # Found a pair
        rank_counts[rank] = card  # Store the first occurrence
    return False, []

def has_two_pair(cards):
    rank_counts = {}
    collection = []
    
    for card in cards:
        rank = card[1]
        if rank in rank_counts:
            collection.append(rank_counts[rank])
            collection.append(card)
            if len(collection) == 4:
                return True, collection  # Found two pairs
        else:
            rank_counts[rank] = card  # Store first occurrence
    
    return False, []

def has_three_of_a_kind(cards):
    rank_counts = {}
    
    for card in cards:
        rank = card[1]
        if rank in rank_counts:
            rank_counts[rank].append(card)
            if len(rank_counts[rank]) == 3:
                return True, rank_counts[rank]  # Found three of a kind
        else:
            rank_counts[rank] = [card]  # Start tracking
    
    return False, []

def has_straight(cards):
    rank_list = sorted(set(ranks[card[1]] for card in cards))  # Remove duplicates, then sort

    # Standard Straight Check
    for i in range(len(rank_list) - 4):  # Ensure at least 5 ranks exist
        if all(rank_list[i + j] == rank_list[i] + j for j in range(5)):
            return True, rank_list[i:i + 5]  # Found a straight

    # Special Case: Ace-Low Straight (A-2-3-4-5)
    if {14, 2, 3, 4, 5}.issubset(set(rank_list)):  # Ace (14) + 2-3-4-5
        return True, [2, 3, 4, 5, 14]  # Ace is at the end to indicate Ace-low straight

    return False, []

def has_flush(cards):
    """Checks if there is a flush (5 cards of the same suit)."""
    suit_counts = Counter(card[0] for card in cards)  # Count suits
    for suit, count in suit_counts.items():
        if count >= 5:
            flush_cards = [card for card in cards if card[0] == suit]  # Get all cards of that suit
            return True, sorted(flush_cards, key=lambda x: ranks[x[1]], reverse=True)[:5]
    return False, []

def has_full_house(cards):
    """Checks if there is a Full House (Three of a Kind + One Pair)."""
    rank_counts = Counter(ranks[card[1]] for card in cards)
    three_of_a_kind = [rank for rank, count in rank_counts.items() if count >= 3]
    pair = [rank for rank, count in rank_counts.items() if count >= 2 and rank not in three_of_a_kind]

    if three_of_a_kind and pair:
        best_three = max(three_of_a_kind)
        best_pair = max(pair)
        full_house_cards = [card for card in cards if ranks[card[1]] in {best_three, best_pair}]
        return True, full_house_cards
    return False, []

def has_four_of_a_kind(cards):
    """Checks if there is Four of a Kind."""
    rank_counts = Counter(ranks[card[1]] for card in cards)
    four_of_a_kind = [rank for rank, count in rank_counts.items() if count == 4]
    
    if four_of_a_kind:
        best_four = max(four_of_a_kind)
        four_cards = [card for card in cards if ranks[card[1]] == best_four]
        kicker = max([card for card in cards if ranks[card[1]] != best_four], key=lambda x: ranks[x[1]], default=None)
        return True, four_cards + ([kicker] if kicker else [])
    return False, []

def has_straight_flush(cards):
    """Checks if there is a Straight Flush (Straight + Flush)."""
    is_flush, flush_cards = has_flush(cards)
    if not is_flush:
        return False, []
    
    flush_ranks = sorted(set(ranks[card[1]] for card in flush_cards))
    
    # Check for straight within flush cards
    for i in range(len(flush_ranks) - 4):
        if all(flush_ranks[i + j] == flush_ranks[i] + j for j in range(5)):
            straight_flush = [card for card in flush_cards if ranks[card[1]] in flush_ranks[i:i + 5]]
            return True, straight_flush
    
    # Ace-low straight flush
    if {14, 2, 3, 4, 5}.issubset(set(flush_ranks)):
        straight_flush = [card for card in flush_cards if ranks[card[1]] in {14, 2, 3, 4, 5}]
        return True, straight_flush

    return False, []

def has_royal_flush(cards):
    """Checks if there is a Royal Flush (10-J-Q-K-A in the same suit)."""
    is_flush, flush_cards = has_flush(cards)
    if not is_flush:
        return False, []
    
    flush_ranks = {ranks[card[1]] for card in flush_cards}
    
    if {10, 11, 12, 13, 14}.issubset(flush_ranks):
        royal_flush = [card for card in flush_cards if ranks[card[1]] in {10, 11, 12, 13, 14}]
        return True, royal_flush
    return False, []

def best_combination(cards):
    if has_royal_flush(cards)[0]:
        return 10, max(has_royal_flush(cards)[1])
    elif has_straight_flush(cards)[0]:
        return 9, max(has_straight_flush(cards)[1])
    elif has_four_of_a_kind(cards)[0]:
        return 8, max(has_four_of_a_kind(cards)[1])
    elif has_full_house(cards)[0]:
        return 7, max(has_full_house(cards)[1])
    elif has_flush(cards)[0]:
        return 6, max(has_flush(cards)[1])
    elif has_straight(cards)[0]:
        return 5, max(has_straight(cards)[1])
    elif has_three_of_a_kind(cards)[0]:
        return 4, max(has_three_of_a_kind(cards)[1])
    elif has_two_pair(cards)[0]:
        return 3, max(has_two_pair(cards)[1])
    elif has_pair(cards)[0]:
        return 2, max(has_pair(cards)[1])
    else:
        high_card_list = [ranks[card[1]] for card in cards]
        sorted(high_card_list, key=int, reverse=True)
        return 1, max(high_card_list)

def decide_winner(players):
    highest_combination = 0
    best_hands = {}

    # Step 1: Find the highest combination ranking
    for player in players:
        player_combination = best_combination(player.cards)  # (ranking, tiebreaker_values)
        best_hands[player] = player_combination  
        highest_combination = max(highest_combination, player_combination[0])

    # Step 2: Get all players with the highest ranking
    high_player_list = [p for p in players if best_hands[p][0] == highest_combination]

    # Step 3: Sort by tiebreaker values (e.g., for full house, check trips first, then pair)
    high_player_list.sort(key=lambda p: best_hands[p][1], reverse=True)

    # Step 4: Find the highest tiebreaker score
    top_score = best_hands[high_player_list[0]][1]

    # Step 5: Determine if there is a tie
    winners = [p for p in high_player_list if best_hands[p][1] == top_score]

    return winners, highest_combination  # Returns winners and their ranking (1-10)


