import aiohttp
import asyncio
import datetime
import os
from termcolor import colored

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
    def __init__(self, filename, token):
        self.wallets = {}
        self.load_wallets(filename)
        self.token = token

    def load_wallets(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    self.wallets[line.strip()] = WalletStat(line.strip())

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    async def post_data(self, session, wallet_stat):
        url = "https://api.larissa.network/api/v1/key/keyUnclaimedEarning"
        headers = {"Authorization": f"Bearer {self.token}"}
        body = {"walletID": wallet_stat.wallet_id}

        async with session.post(url, headers=headers, json=body) as response:
            if response.status == 200:
                data = await response.json()
                if data['status']:
                    return float(data['data'])
                else:
                    print(f"Failed for walletID {wallet_stat.wallet_id}: {data['message']}")
            else:
                print(f"Failed for walletID {wallet_stat.wallet_id} with status code:", response.status)
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
                    total += current_earning

            print(f"Total unclaimed earnings: {total:.4f}\n")
            return first_run

    async def run(self):
        first_run = True
        while True:
            first_run = await self.fetch_wallet_earnings(first_run)
            first_run = False

            # tweak this as you like... 2 minutes is default (a safe value).  Making this number too small may risk a ban.
            await asyncio.sleep(600) # wait for 2 minutes, then update again

if __name__ == "__main__":
    token = "Your Bearer Token goes HERE"  # Replace with your actual token
    stats = WalletStats('wallet_ids.csv', token)
    asyncio.run(stats.run())
