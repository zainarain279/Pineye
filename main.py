import requests
import json
import time
from datetime import datetime
import sys
from urllib.parse import parse_qs, urlparse
import os
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def key_bot():
    api = "https://raw.githubusercontent.com/zainarain279/APIs-checking/refs/heads/main/my.json"
    try:
        response = requests.get(api)
        response.raise_for_status()
        try:
            data = response.json()
            header = data['header']
            print('\033[96m' + header + '\033[0m')
        except json.JSONDecodeError:
            print('\033[96m' + response.text + '\033[0m')
    except requests.RequestException as e:
        print('\033[96m' + f"Failed to load header: {e}" + '\033[0m')

class PinEyeBot:
    def __init__(self):
        self.base_url = "https://api2.pineye.io/api"
        self.token = None
        self.chat_id = "5373988314"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

    def countdown(self, seconds, prefix=""):
        for remaining in range(seconds, 0, -1):
            sys.stdout.write(f"\r{prefix}Wait: {remaining:3d} seconds")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r" + " " * 50 + "\r")  # Clear the line
        sys.stdout.flush()

    def print_separator(self):
        print("\n" + "="*50 + "\n")

    def print_header(self, text):
        self.print_separator()
        print(f"🔵 {text}")
        print("-"*50)

    def login(self, query_data):
        self.print_header("LOGIN")
        url = f"{self.base_url}/v2/Login"
        payload = {"userinfo": query_data}
        
        self.headers["chatid"] = self.chat_id
        
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.token = data["data"]["token"]
            self.headers["authorization"] = f"Bearer {self.token}"
            self.headers["x-chat-id"] = self.chat_id
            print("✅ Login successful!")
            return True
        print("❌ Login failed!")
        return False
    def auto_tap(self):
        count = random.randint(100, 1000)
        url = f"{self.base_url}/v1/Tap?count={count}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            print(f"💫 Tap successful! Energy: {data['data']['energy']['currentEnergy']} | Balance: {data['data']['balance']}")
            return data['data']
        return None

    def claim_daily(self):
        self.print_header("CLAIM DAILY REWARD")
        url = f"{self.base_url}/v1/DailyReward/claim"
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            print(f"🎁 Daily reward claimed! Balance: {data['data']['balance']}")
            return True
        print("❌ Failed to claim daily reward")
        return False

    def get_tasks(self):
        url = f"{self.base_url}/v1/Social"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()["data"]
        return []

    def claim_task(self, task_id):
        url = f"{self.base_url}/v1/SocialFollower/claim?socialId={task_id}"
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Task {task_id} claimed! Balance: {data['data']['balance']}")
            return True
        return False

    def get_practices(self):
        url = f"{self.base_url}/v1/PranaGame/GetAllPractices"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()["data"]["practiceList"]
            current_timestamp = int(time.time())
            available_practices = []
            for practice in data:
                if practice["nextPracticeTime"] <= current_timestamp:
                    available_practices.append(practice)
                else:
                    next_time = datetime.fromtimestamp(practice["nextPracticeTime"])
                    print(f"⏳ {practice['title']} available on: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")
            return available_practices
        return []

    def get_practice_details(self, practice_id):
        url = f"{self.base_url}/v1/PranaGame/GetPracticeDetails"
        params = {"practiceId": practice_id}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        return None

    def claim_practice(self, practice_id):
        url = f"{self.base_url}/v1/PranaGame/ClaimPractice"
        params = {"practiceId": practice_id}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()["data"]
            print(f"✨ Practice finished! Profit: {data['profit']} | Balance: {data['balance']}")
            return True
        return False

    def complete_practices(self):
        self.print_header("SOLVE PRACTICES")
        available_practices = self.get_practices()
        
        if not available_practices:
            print("❌ There are no practices currently available")
            next_available = None
            current_timestamp = int(time.time())
            
            response = requests.get(f"{self.base_url}/v1/PranaGame/GetAllPractices", headers=self.headers)
            if response.status_code == 200:
                practices = response.json()["data"]["practiceList"]
                next_time = min([p["nextPracticeTime"] for p in practices if p["nextPracticeTime"] > current_timestamp], default=None)
                if next_time:
                    next_datetime = datetime.fromtimestamp(next_time)
                    print(f"\n⏰ Practice berikutnya tersedia pada: {next_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            return
            
        print(f"📝 Menemukan {len(available_practices)} practices that can be completed")
        
        for practice in available_practices:
            print(f"\n🎯 Solve practice: {practice['title']}")
            details = self.get_practice_details(practice["id"])
            if details:
                practice_time = details["practiceTime"]
                print(f"⏳ Practice time: {practice_time} second")
                self.countdown(practice_time, f"[{practice['title']}] ")
                self.claim_practice(practice["id"])
                time.sleep(2)

    def get_marketplace(self):
        url = f"{self.base_url}/v1/PranaGame/Marketplace"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()["data"]
        return None

    def purchase_card(self, card_id, level):
        url = f"{self.base_url}/v1/PranaGame/Purch"
        params = {
            "cardId": card_id,
            "level": level
        }
        response = requests.post(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()["data"]
            print(f"💎 Successfully upgraded card ID {card_id} to level {level}! Balance: {data['balance']}")
            return data
        return None

    def get_fastest_cooldown(self, marketplace_data):
        min_cooldown = float('inf')
        for category in marketplace_data["categories"]:
            for card in category["cards"]:
                if card["cooldownTime"] > 0 and card["cooldownTime"] < min_cooldown:
                    min_cooldown = card["cooldownTime"]
        return min_cooldown if min_cooldown != float('inf') else 0

    def auto_buy_cards(self, wait_cooldown=False):
        self.print_header("AUTO BUY CARDS")
        tap_data = self.auto_tap()
        if not tap_data:
            return False
        
        current_balance = tap_data['balance']
        
        while True:
            marketplace = self.get_marketplace()
            if not marketplace:
                return False
                
            cheapest_card = None
            min_cost = float('inf')
            
            for category in marketplace["categories"]:
                for card in category["cards"]:
                    if (card["cooldownTime"] == 0 and 
                        card["cost"] < min_cost and 
                        not card["hasStartDependency"]):
                        print(f"💡 Eligible card - ID: {card['id']}, {card['title']}, Cost: {card['cost']}, Level: {card['currentLevel']}")
                        cheapest_card = card
                        min_cost = card["cost"]
            
            if not cheapest_card:
                fastest_cooldown = self.get_fastest_cooldown(marketplace)
                if fastest_cooldown > 0 and wait_cooldown:
                    print(f"\n⏳ All cards are in cooldown. Fastest cooldown: {fastest_cooldown} seconds")
                    print(f"⌛ Waiting for cooldown to finish...")
                    self.countdown(fastest_cooldown)
                    continue
                else:
                    print("❌ No cards available to buy")
                    break
            
            if min_cost > current_balance:
                print(f"💰 Insufficient balance (Balance: {current_balance}, Cost: {min_cost})")
                break
            
            result = self.purchase_card(cheapest_card["id"], cheapest_card["currentLevel"] + 1)
            if not result:
                break
            
            current_balance = result['balance']
            time.sleep(1)

def main():
    clear()
    key_bot()
    try:
        with open("query.txt", "r") as f:
            queries = [line.strip() for line in f.readlines() if line.strip()]
        
        while True:
            # Jalankan semua akun
            for index, query_data in enumerate(queries, 1):
                print(f"\n{'='*20} ACCOUNT #{index} {'='*20}\n")
                
                bot = PinEyeBot()
                if not bot.login(query_data):
                    print(f"⚠️ Bypassing account #{index} due to failure login")
                    continue

                # 1. Auto tap
                bot.print_header("AUTO TAP")
                for i in range(5):
                    print(f"\nTap #{i+1}")
                    bot.auto_tap()
                    if i < 4:
                        bot.countdown(2)
                
                # 2. Claim daily reward
                bot.claim_daily()
                
                # 3. Claim tasks
                bot.print_header("CLAIMING TASKS")
                tasks = bot.get_tasks()
                unclaimed_tasks = [t for t in tasks if not t["isClaimed"]]
                if unclaimed_tasks:
                    print(f"📋 Found {len(unclaimed_tasks)} unclaimed task")
                    for task in unclaimed_tasks:
                        bot.claim_task(task["id"])
                        time.sleep(1)
                else:
                    print("✅ All tasks have been claimed")
                
                # 4. Complete practices
                bot.complete_practices()
                
                # 5. Auto buy cards
                bot.auto_buy_cards(wait_cooldown=False)
                
                bot.print_separator()
                print(f"✨ Account #{index} finished! ✨")
                
                if index < len(queries):
                    print("\nMove to the next account in:")
                    bot.countdown(5, "⏳ ")

            # Istirahat 10 menit sebelum memulai ulang
            print("\n\n🕐 Rest for 10 minutes before restarting...")
            for remaining in range(600, 0, -1):
                minutes = remaining // 60
                seconds = remaining % 60
                sys.stdout.write(f"\r⏳ Time remaining: {minutes:02d}:{seconds:02d}")
                sys.stdout.flush()
                time.sleep(1)
            print("\n\n🔄 Restart the program...\n")

    except Exception as e:
        print(f"\n❌ There is an error: {str(e)}")

if __name__ == "__main__":
    main()
