from holdem_calc import holdem_calc

def simulate_all_possible(bot):
    hole_cards = []
    for card in bot.playerCards:
        hole_cards.append(str(card).replace("10", "T"))

    board_cards = []
    for card in bot.tableCards:
        board_cards.append(str(card).replace("10", "T"))

    if len(hole_cards) < 2:
        return "Folded"
    
    elif len(board_cards) < 3:
        return "Waiting for flop"

    else:
        probabilities = holdem_calc.calculate_odds_villan(
            board=board_cards,
            exact=False,
            num = 1,
            input_file= None,
            hero_cards=hole_cards,
            villan_cards=None,
            verbose=False
        )

        probabilities = {"Tie" : probabilities[0], "Win": probabilities[1], "Lose" : probabilities[2]}

        return probabilities

def calculate_ev(bot):
    monte_carlo_probabilities = simulate_all_possible(bot)

    if type(monte_carlo_probabilities) == dict:
        call = (float(monte_carlo_probabilities['Lose'])) / (float(monte_carlo_probabilities['Win']) * float(bot.potSize))
        
        if int(call) > 0:
            return f"Call/Raise over {call}"
        else:
            return "Check/Fold"
    else:
        return monte_carlo_probabilities