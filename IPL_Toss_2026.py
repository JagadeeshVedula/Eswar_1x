import random
from datetime import datetime
import os
import requests

try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf not found. Manual input will be used.")
    PdfReader = None

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "8656246989:AAEv4COi8EL-AfaMCv76eOVsRydqaVsVsSo"
TELEGRAM_CHAT_ID = "7723525044"

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

def send_telegram_message(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(RED + f"Telegram Error: {e}" + RESET)
        return False

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

def get_team_code(full_name):
    full_name_lower = full_name.lower()
    if "mumbai" in full_name_lower: return "MI"
    if "chennai" in full_name_lower: return "CSK"
    if "royal challengers" in full_name_lower: return "RCB"
    if "kolkata" in full_name_lower: return "KKR"
    if "sunrisers" in full_name_lower: return "SRH"
    if "delhi" in full_name_lower: return "DC"
    if "lucknow" in full_name_lower: return "LSG"
    if "gujarat" in full_name_lower: return "GT"
    if "rajasthan" in full_name_lower: return "RR"
    if "punjab" in full_name_lower: return "PBKS"
    return None

def get_matches_from_pdf(pdf_path):
    if not PdfReader or not os.path.exists(pdf_path):
        return []
    
    try:
        reader = PdfReader(pdf_path)
        today_str = datetime.now().strftime("%d-%b-%y").upper()
        
        matches = []
        for page in reader.pages:
            text = page.extract_text()
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            
            match_start_idx = -1
            for i in range(len(lines) - 34):
                if all(lines[i+j].isdigit() for j in range(35)):
                    match_start_idx = i
                    break
            
            if match_start_idx != -1:
                date_start = match_start_idx - 35
                away_start = match_start_idx - 140
                home_start = match_start_idx - 210
                
                for k in range(35):
                    if lines[date_start + k] == today_str:
                        home_team_name = lines[home_start + k]
                        away_team_name = lines[away_start + k]
                        
                        home_code = get_team_code(home_team_name)
                        away_code = get_team_code(away_team_name)
                        
                        if home_code and away_code:
                            matches.append((home_code, away_code))
        return matches
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []

def run_toss(team1, team2, auto_send=False):
    team1_full, captain1 = teams[team1]
    team2_full, captain2 = teams[team2]
    
    total1 = name_value(captain1)
    total2 = name_value(captain2)
    
    digit1 = single_digit(total1)
    digit2 = single_digit(total2)
    
    print("\n" + CYAN + f"--- Toss: {team1_full} vs {team2_full} ---" + RESET)
    print(CYAN + "Captains:" + RESET)
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

    if auto_send:
        tg_message = (
            f"<b>🏆 IPL 2026 Toss Prediction</b>\n\n"
            f"🏏 <b>Match:</b> {team1_full} vs {team2_full}\n"
            f"---------------------------\n"
            f"👤 {captain1}: {total1} → <b>{digit1}</b>\n"
            f"👤 {captain2}: {total2} → <b>{digit2}</b>\n\n"
            f"🎯 <b>Toss Winner Prediction:</b>\n"
            f"✨ <b>{result[0].upper()}</b> ✨\n"
            f"---------------------------"
        )
        if send_telegram_message(tg_message):
            print(GREEN + "Result sent to Telegram! [OK]" + RESET)
        else:
            if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
                print(YELLOW + "Telegram credentials not found. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars." + RESET)
            else:
                print(RED + "Failed to send result to Telegram! [ERROR]" + RESET)

def main():
    print(CYAN + "IPL 2026 Toss Predictor" + RESET)
    
    # Try to get matches from PDF
    pdf_matches = get_matches_from_pdf("schedule.pdf")
    
    if pdf_matches:
        print(f"\nFound {len(pdf_matches)} match(es) for today ({datetime.now().strftime('%d-%b-%y').upper()}):")
        for m1, m2 in pdf_matches:
            run_toss(m1, m2, auto_send=True)
    else:
        print("\nNo matches found for today in schedule.pdf or error reading file.")
        
    # Exit automatically if running in GitHub Actions or CI environment
    if os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CI") == "true":
        print("\nAutomated run complete. Exiting.")
        return

    while True:
        cont = input("\nDo you want to run a manual toss? (y/n): ")
        if cont.lower() == 'y':
            print("\n" + CYAN + "Available Teams:" + RESET, ", ".join(teams.keys()))
            team1 = input("Enter first team: ").upper()
            team2 = input("Enter second team: ").upper()
            
            if team1 == team2:
                print(RED + "Both teams cannot be the same." + RESET)
                continue
            if team1 not in teams or team2 not in teams:
                print(RED + "Invalid team name." + RESET)
                continue
            
            run_toss(team1, team2, auto_send=True)
        else:
            break

if __name__ == "__main__":
    main()
