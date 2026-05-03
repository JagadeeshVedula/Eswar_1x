import random

# Color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Teams: short code -> (full name, captain)
teams = {
    "MI": ("Mumbai Indians", "Hardik Pandya"),
    "CSK": ("Chennai Super Kings", "Ruturaj Gaikwad"),
    "RCB": ("Royal Challengers Bangalore", "Rajat Patidar"),
    "KKR": ("Kolkata Knight Riders", "Ajinkya Rahane"),
    "SRH": ("Sunrisers Hyderabad", "Pat Cummins"),
    "DC": ("Delhi Capitals", "Axar Patel"),
    "LSG": ("Lucknow Super Giants", "Rishabh Pant"),
    "GT": ("Gujarat Titans", "Shubman Gill"),
    "RR": ("Rajasthan Royals", "Riyan Parag"),
    "PBKS": ("Punjab Kings", "Shreyas Iyer")
}

def name_value(name):
    total = 0
    for ch in name.upper():
        if ch.isalpha():
            total += ord(ch) - 64
    return total

def single_digit(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

while True:
    print("\n" + CYAN + "Available Teams:" + RESET, ", ".join(teams.keys()))
    print(CYAN + "--- New Match Toss ---" + RESET)
    
    team1 = input("Enter first team: ").upper()
    team2 = input("Enter second team: ").upper()
    
    # Prevent same team selection
    if team1 == team2:
        print(RED + "Both teams cannot be the same. Try again." + RESET)
        continue
    
    # Validate teams
    if team1 not in teams or team2 not in teams:
        print(RED + "Invalid team name. Try again." + RESET)
        continue
    
    team1_full, captain1 = teams[team1]
    team2_full, captain2 = teams[team2]
    
    total1 = name_value(captain1)
    total2 = name_value(captain2)
    
    digit1 = single_digit(total1)
    digit2 = single_digit(total2)
    
    print("\n" + CYAN + "Captains:" + RESET)
    print(team1_full, "Captain:", captain1)
    print(team2_full, "Captain:", captain2)
    
    print("\n" + CYAN + "Results:" + RESET)
    print(captain1, "=", total1, "->", digit1)
    print(captain2, "=", total2, "->", digit2)
    
    # Random toss
    result = random.choice([
        (team1_full, captain1, digit1),
        (team2_full, captain2, digit2)
    ])
    
    print("\n" + CYAN + "Toss Result:" + RESET)
    print(GREEN + "Selected Team:" + RESET, result[0])
    print(YELLOW + "Captain:" + RESET, result[1], "(" + str(result[2]) + ")")
    
    cont = input("\nDo you want to try again? (y/n): ")
    if cont.lower() != 'y':
        break