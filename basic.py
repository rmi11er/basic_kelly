from get_odds import get_odds
import json


K, B = 0.5, 5000

def decimal_to_american(decimal_odd):
    if decimal_odd > 2:
        return int((decimal_odd - 1) * 100)
    else:
        return int(-100 / (decimal_odd - 1))

def american_to_decimal(american_odd):
    if american_odd >= 100:
        return 1 + (american_odd / 100)
    else:
        return 1 + (100 / abs(american_odd))

def compute_arithmetic_mean(odds):
    decimal_odds = [american_to_decimal(odd) for odd in odds]
    return sum(decimal_odds) / len(decimal_odds)

def find_best_odds(odds):
    decimal_odds = [american_to_decimal(odd) for odd in odds]
    best_decimal_index = decimal_odds.index(max(decimal_odds))
    best_american_odd = odds[best_decimal_index]
    return best_american_odd

def compute_kelly_bet(odds, mean, K, B):
    p = 1 / mean
    q = 1 - p
    best_odds = find_best_odds(odds)
    best_decimal = american_to_decimal(best_odds) - 1
    kelly_fraction = (p * best_decimal - q) / best_decimal
    return kelly_fraction * B * K, best_odds

def main():
    use_custom_odds = input("Enter 1 for custom odds. Else will get recent online.")
    try:
        use_custom_odds = True if int(use_custom_odds) == 1 else False
    except Exception as e:
        use_custom_odds = False

    if use_custom_odds:
        odds = input("Enter the list of American odds separated by spaces: ")
        odds = list(map(float, odds.split()))

        mean_odds_decimal = compute_arithmetic_mean(odds)
        best_odds = find_best_odds(odds)
        kelly_bet = compute_kelly_bet(odds, mean_odds_decimal, K, B)

        print("Arithmetic Mean of Odds (Decimal):", mean_odds_decimal)
        print("Best Odds Relative to Mean (American):", best_odds)
        print("Kelly-sized Bet:", kelly_bet)
    else:
        data = get_odds()
        # with open("temp.json", "r") as file:
        #     data = json.load(file)

        games = [i for i in range(len(data))]

        for game_num in games:
            try:
                # Extract game information
                game = data[game_num]
                home_team = game["home_team"]
                away_team = game["away_team"]
                bookmakers = game["bookmakers"]

                home_odds = []
                away_odds = []

                for sportsbook_odds in bookmakers:
                    outcomes = sportsbook_odds['markets'][0]['outcomes']
                    if outcomes[0]['name'] == home_team:
                        home_odds.append(outcomes[0]['price'])
                        away_odds.append(outcomes[1]['price'])
                    else:
                        home_odds.append(outcomes[1]['price'])
                        away_odds.append(outcomes[0]['price'])

                home_mean = compute_arithmetic_mean(home_odds)
                away_mean = compute_arithmetic_mean(away_odds)

                kelly_bet_home, best_home_odds = compute_kelly_bet(home_odds, home_mean, K, B)
                kelly_bet_away, best_away_odds = compute_kelly_bet(away_odds, away_mean, K, B)

                if kelly_bet_away > 0.01 * B and kelly_bet_away > kelly_bet_home:
                    print(f"Kelly-sized Bet for {away_team}, odds {best_away_odds}:{kelly_bet_away}")
                elif kelly_bet_home > 0.01 * B and kelly_bet_home > kelly_bet_away:
                    print(f"Kelly-sized Bet for {home_team}, odds {best_home_odds}:{kelly_bet_home}")
                else:
                    print(f"No sizable bet for the game between {away_team} and {home_team}:")
            except Exception as e:
                print('exception encountered:', e)
                continue


if __name__ == "__main__":
    main()