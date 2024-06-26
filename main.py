import pandas as pd
import random

# Load Pokémon data
pokemon_data = pd.read_csv('pokemon_data.csv')
pokemon_data['Type'] = pokemon_data['Type 1'] + ', ' + pokemon_data['Type 2']

# Function to deal 6 Pokémon to each player
def deal_pokemon(data):
    return data.sample(6).reset_index(drop=True)

# Initialize players
player_pokemon = deal_pokemon(pokemon_data)
computer_pokemon = deal_pokemon(pokemon_data)

# Load strengths and weaknesses of each type
pokemon_type_data = pd.read_csv('pokemon_type_table.csv')

def get_type_effectiveness(pokemon_type, effectiveness_data):
    row = effectiveness_data[effectiveness_data['Type'] == pokemon_type].iloc[0]
    return {
        'Strong Against': row['Strong Against'].split(', '),
        'Weak Against': row['Weak Against'].split(', '),
        'Resistant To': row['Resistant To'].split(', '),
        'Vulnerable To': row['Vulnerable To'].split(', ')
    }

def calculate_score(player_types, computer_types, effectiveness_data):
    def score_effectiveness(player_type, computer_type):
        score = 0
        effectiveness = get_type_effectiveness(player_type, effectiveness_data)

        if computer_type in effectiveness['Strong Against']:
            score += 1.5
        elif computer_type in effectiveness['Weak Against']:
            score += 0.5
        else:
            score += 1

        if computer_type in effectiveness['Resistant To']:
            score -= 0.5
        elif computer_type in effectiveness['Vulnerable To']:
            score -= 1.5
        else:
            score -= 1

        return score

    score = 0
    for pt in player_types:
        for ct in computer_types:
            score += score_effectiveness(pt, ct)
            score -= score_effectiveness(ct, pt)

    return 1 if score > 0 else 2 if score < 0 else 0

def determine_winner(player_pokemon, computer_pokemon, chosen_attribute):
    if chosen_attribute in ['Power', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def']:
        if player_pokemon[chosen_attribute] > computer_pokemon[chosen_attribute]:
            return 1
        elif player_pokemon[chosen_attribute] < computer_pokemon[chosen_attribute]:
            return 2
        else:
            return 0
    elif chosen_attribute == 'Legendary':
        if player_pokemon[chosen_attribute] == True and computer_pokemon[chosen_attribute] == False:
            return 1
        elif player_pokemon[chosen_attribute] == False and computer_pokemon[chosen_attribute] == True:
            return 2
        else:
            return 0
    elif chosen_attribute == 'Type':
        player_types = [player_pokemon['Type 1'], player_pokemon['Type 2']]
        computer_types = [computer_pokemon['Type 1'], computer_pokemon['Type 2']]
        return calculate_score(player_types, computer_types, pokemon_type_data)

# Game loop
player_remaining = player_pokemon.copy()
computer_remaining = computer_pokemon.copy()
turn = 0

while len(player_remaining) > 0 and len(computer_remaining) > 0:
    print(f"Turn {turn + 1}")
    # Each player places a Pokémon onto the battleground
    while True:
        print("Player remaining Pokémon:", player_remaining['Name'].values)
        player_active_name = input("Choose a Pokémon to place on the battleground: ")
        if player_active_name not in player_remaining['Name'].values:
            print("You don't have that Pokémon. Please choose one of your Pokémon.")
            continue
        else:
            break

    player_active = player_remaining[player_remaining['Name'] == player_active_name].iloc[0]
    computer_active = computer_remaining.sample(1).iloc[0]

    print("Player Active Pokémon:", player_active['Name'])
    print("Computer Active Pokémon:", computer_active['Name'])

    # Player with the highest speed chooses the attribute
    if player_active['Speed'] > computer_active['Speed']:
        choosing_player = 'Player'
    else:
        choosing_player = 'Computer'

    print(f"{choosing_player} chooses the attribute to compare.")

    # For simplicity, let's assume they always choose 'Attack'
    if choosing_player == 'Player':
        while True:
            chosen_attribute = input("Choose an attribute to compare (HP, Attack, Defense, Sp. Atk, Sp. Def, Legendary, Type): ")
            if chosen_attribute in ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Legendary', 'Type']:
                break
            else:
                print("Invalid attribute. Please choose again.")
    else:
        chosen_attribute = random.choice(['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Legendary', 'Type'])

    print(f"Chosen Attribute: {chosen_attribute}")

    winner = determine_winner(player_active, computer_active, chosen_attribute)

    if winner == 1:
        print("Player wins the round.")
        computer_remaining = computer_remaining.drop(computer_remaining.index[0]).reset_index(drop=True)
    elif winner == 2:
        print("Computer wins the round.")
        player_remaining = player_remaining.drop(player_remaining[player_remaining['Name'] == player_active_name].index).reset_index(drop=True)
    else:
        print("It's a tie.")

    print(f"Player remaining Pokémon: {len(player_remaining)}")
    print(f"Computer remaining Pokémon: {len(computer_remaining)}")

    turn += 1
    print("\n")

# Determine the final winner
if len(player_remaining) == 0 and len(computer_remaining) != 0:
    print("Computer wins the game!")
elif len(computer_remaining) == 0 and len(player_remaining) != 0:
    print("Player wins the game!")
else:
    print("The game is a draw.")
