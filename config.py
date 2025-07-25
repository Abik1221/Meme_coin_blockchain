# Central configuration with fail-safes
SETTINGS = {
    "network": "devnet",  # "devnet" | "mainnet" (future)
    "rpc_url": "https://api.devnet.solana.com",  # Free tier
    "mock_mode": False,  # Toggle fake data when rate-limited
    "coin_default_name": "MEME_COIN",
    "max_retries": 3,  # Auto-retry if API fails
    "retry_delay": 5  # Seconds between retries
}

# Alternative free RPC endpoints (fallback if primary fails)
RPC_BACKUPS = [
    "https://solana-devnet.rpcpool.com",
    "https://devnet.helius-rpc.com/?api-key=free"
]