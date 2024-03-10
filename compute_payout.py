"""
This file contains helper functions to calculate the payout of American odds bets
"""
def calc_payout_american(bet_string: str):
    bets = bet_string.split()
    overall_payout = 0.
    
    for bet in bets:
        odds, amount_bet = bet.split(":")
        odds = int(odds)
        amount_bet = float(amount_bet) if amount_bet else 0  # Convert to integer only if not empty
        
        if odds > 0:  # Positive odds, indicating underdog
            payout = amount_bet * (odds / 100.)
            overall_payout += payout + amount_bet
        else:  # Negative odds, indicating favorite
            payout = amount_bet / (-odds / 100.)
            overall_payout += payout + amount_bet
        
    print(overall_payout)
    return overall_payout


def parse_and_calculate(text):
    lines = text.strip().split('\n')
    bets = []
    total_wagered = 0
    num_lines = 0
    
    for line in lines:
        print(line)
        if ':' in line:
            num_lines += 1
            parts = line.split(', odds ')
            if len(parts) == 2:
                bet_info = parts[1].split(':')
                if len(bet_info) == 2:
                    amount_bet = float(bet_info[1])
                    total_wagered += amount_bet
        
        if line.startswith('+') or line.startswith('Y'):
            parts = line.split(', odds ')
            if len(parts) == 2:
                bet_info = parts[1].split(':')
                if len(bet_info) == 2:
                    odds = int(bet_info[0])
                    amount_bet = float(bet_info[1])
                    bets.append(f"{odds}:{amount_bet}")
    
    if bets:
        bet_data = ' '.join(bets)
        overall_payout = calc_payout_american(bet_data)
        return num_lines, overall_payout, total_wagered, overall_payout - total_wagered
    else:
        return num_lines, 0, total_wagered


# def parse_and_calculate(text):
#     lines = text.strip().split('\n')
#     bets = []
    
#     for line in lines:
#         line = line.replace(': ', ':')
#         if line.startswith('Y'):
#             parts = line.split(', odds ')
#             if len(parts) == 2:
#                 bet_info = parts[1].split(': ')
#                 if len(bet_info) != 2:
#                     bet_info = parts[1].split(':')
#                 if len(bet_info) == 2:
#                     odds = int(bet_info[0])
#                     amount_bet = float(bet_info[1])
#                     bets.append(f"{odds}:{amount_bet}")
    
#     if bets:
#         print(bets)
#         bet_data = ' '.join(bets)
#         overall_payout = calc_payout_american(bet_data)
#         return overall_payout
#     else:
#         return 0


if __name__ == "__main__":
    with open('bets.dump', 'r') as bets_file:
        bets_string = bets_file.read()

    print('num bets, winnings, amount wagered, profits:', parse_and_calculate(bets_string))