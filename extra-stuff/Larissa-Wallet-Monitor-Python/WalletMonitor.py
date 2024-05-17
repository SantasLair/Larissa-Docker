import aiohttp
import asyncio
import datetime
import os
import logging
import json
import sqlite3
from termcolor import colored

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WalletStat:
    def __init__(self, wallet_id):
        self.wallet_id = wallet_id
        self.current_earning = 0
        self.previous_earning = 0
        self.gain_amount = 0
        self.gain_is_old = False

    def update_earnings(self, new_earning):
        if new_earning == self.previous_earning:
            self.gain_is_old = True
            return
        
        if self.previous_earning > 0:
            self.gain_amount = new_earning - self.previous_earning
            self.gain_is_old = False
        
        self.previous_earning = self.current_earning
        self.current_earning = new_earning

    def display_earnings(self):
        if self.gain_amount == 0:
            print(f"WalletID {self.wallet_id}: {self.current_earning:.4f}")
        else:
            gain_str = f" (+{self.gain_amount:.4f})"
            if self.gain_is_old:
                print(f"WalletID {self.wallet_id}: {self.current_earning:.4f}" + colored(gain_str, "yellow"))
            else:
                print(f"WalletID {self.wallet_id}: {self.current_earning:.4f}{gain_str}")


class WalletStats:
    def __init__(self, config_file):
        self.wallets = {}
        self.load_config(config_file)
        self.conn = sqlite3.connect('earnings.db')
        self.create_table()

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
                self.token = config["bearer_token"]
                for wallet_id in config["wallet_ids"]:
                    self.wallets[wallet_id] = WalletStat(wallet_id)
            logging.info(f"Loaded {len(self.wallets)} wallet IDs from {config_file}")
        except FileNotFoundError:
            logging.error(f"Config file {config_file} not found")
        except json.JSONDecodeError:
            logging.error(f"Error parsing config file {config_file}")

    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS earnings
                                 (wallet_id TEXT, timestamp TEXT, earnings REAL)''')

    def save_earnings(self, wallet_id, earnings):
        with self.conn:
            self.conn.execute('INSERT INTO earnings (wallet_id, timestamp, earnings) VALUES (?, ?, ?)',
                              (wallet_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), earnings))

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    async def post_data(self, session, wallet_stat):
        url = "https://api.larissa.network/api/v1/key/keyUnclaimedEarning"
        headers = {"Authorization": f"Bearer {self.token}"}
        body = {"walletID": wallet_stat.wallet_id}

        try:
            async with session.post(url, headers=headers, json=body) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['status']:
                        return float(data['data'])
                    else:
                        logging.warning(f"Failed for walletID {wallet_stat.wallet_id}: {data['message']}")
                else:
                    logging.error(f"Failed for walletID {wallet_stat.wallet_id} with status code: {response.status}")
        except aiohttp.ClientError as e:
            logging.error(f"Network error for walletID {wallet_stat.wallet_id}: {e}")

        return None

    async def fetch_wallet_earnings(self, first_run):
        async with aiohttp.ClientSession() as session:
            tasks = [self.post_data(session, wallet_stat) for wallet_stat in self.wallets.values()]
            results = await asyncio.gather(*tasks)

            total = 0
            self.clear_screen()
            print(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            for wallet_stat, current_earning in zip(self.wallets.values(), results):
                if current_earning is not None:
                    wallet_stat.update_earnings(current_earning)
                    wallet_stat.display_earnings()
                    self.save_earnings(wallet_stat.wallet_id, current_earning)
                    total += current_
