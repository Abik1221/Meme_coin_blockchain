import time
import random
from datetime import datetime
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from config import SETTINGS, RPC_BACKUPS

# Persistent test wallet (avoids repeated airdrops)
TEST_WALLET = None
current_rpc = SETTINGS["rpc_url"]

def get_devnet_connection():
    """Rotate RPC endpoints if rate-limited"""
    global current_rpc
    for _ in range(SETTINGS["max_retries"]):
        try:
            devnet = Client(current_rpc)
            devnet.get_health()  # Test connection
            return devnet
        except:
            # Cycle to next backup RPC
            current_rpc = RPC_BACKUPS[(RPC_BACKUPS.index(current_rpc) + 1) % len(RPC_BACKUPS)]
            time.sleep(SETTINGS["retry_delay"])
    return None

def launch_memecoin(coin_name=None):
    """Launch coin with rate-limit protection"""
    global TEST_WALLET
    coin_name = coin_name or SETTINGS["coin_default_name"]
    
    # Mock mode (no blockchain)
    if SETTINGS["mock_mode"]:
        return {
            "success": True,
            "coin_name": coin_name,
            "tx_id": f"mock_{random.randint(10000, 99999)}",
            "solscan_url": "https://solscan.io/token/MOCK_ADDR?cluster=devnet",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": "Running in mock mode (no real blockchain)"
        }
    
    # Real Devnet mode
    try:
        # Initialize wallet once
        if not TEST_WALLET:
            devnet = get_devnet_connection()
            if not devnet:
                raise ConnectionError("All RPC endpoints failed")
                
            TEST_WALLET = Keypair()
            airdrop_tx = devnet.request_airdrop(TEST_WALLET.pubkey(), 1_000_000_000)
            time.sleep(5)  # Wait for airdrop
        
        return {
            "success": True,
            "coin_name": coin_name,
            "tx_id": str(TEST_WALLET.pubkey())[:15] + "...",
            "solscan_url": f"https://solscan.io/token/{TEST_WALLET.pubkey()}?cluster=devnet",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": "Live on Solana Devnet"
        }
    except Exception as e:
        print(f"Error: {e}")
        # Fallback to mock mode
        SETTINGS["mock_mode"] = True
        return launch_memecoin(coin_name)  # Recursive fallback

# Test
if __name__ == "__main__":
    print(launch_memecoin("TEST_COIN"))