from web3 import Web3
from agents import function_tool
from dotenv import load_dotenv
import os
from typing import Dict, List
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

@function_tool
def fetch_aave_info() -> Dict[str, float]:
    """
    Fetch Aave V3 user account data from Base chain
    """
    web3 = Web3(Web3.HTTPProvider(os.environ.get("BASE_RPC_URL")))
    if not web3.is_connected(): 
        raise Exception("Web3 is not connected")
    
    wallet_address = Web3.to_checksum_address(os.environ.get("WALLET_ADDRESS"))
    POOL_ADDRESS = Web3.to_checksum_address(os.environ.get("POOL_ADDRESS"))
    POOL_ABI = [ 
    { 
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}], 
        "name": "getUserAccountData", 
        "outputs": [
            {"internalType": "uint256", "name": "totalCollateralBase", "type": "uint256"}, 
            {"internalType": "uint256", "name": "totalDebtBase", "type": "uint256"}, 
            {"internalType": "uint256", "name": "availableBorrowsBase", "type": "uint256"}, 
            {"internalType": "uint256", "name": "currentLiquidationThreshold", "type": "uint256"}, 
            {"internalType": "uint256", "name": "ltv", "type": "uint256"}, 
            {"internalType": "uint256", "name": "healthFactor", "type": "uint256"}
        ],
        "stateMutability": "view", 
        "type": "function"
    }
    ]

    pool_contract = web3.eth.contract(address=POOL_ADDRESS, abi=POOL_ABI)
    data = pool_contract.functions.getUserAccountData(wallet_address).call()
    asset_breakdown = fetch_user_assets(wallet_address)

    return {
        "collateral_usd": round(data[0] / 1e8, 4),
        "debt_usd": round(data[1] / 1e8, 4),
        "available_borrow_usd": round(data[2] / 1e8, 4),
        "health_factor": round(data[5] / 1e18, 4),
        "wallet_asset_breakdown": asset_breakdown
    }

def fetch_user_assets(wallet_address: str) -> List[Dict[str, any]]:
    """
    Fetch user's per-asset balances and approximate USD values.
    """

    # Simulated: in real use, you'd get the token contracts dynamically
    token_addresses = {
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "WBTC": "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
        "WETH": "0x4200000000000000000000000000000000000006"
    }

    # ERC20 minimal ABI
    erc20_abi = [
        {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
        {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},
        {"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"}
    ]

    web3 = Web3(Web3.HTTPProvider(os.environ.get("BASE_RPC_URL")))
    assets = []

    for symbol, address in token_addresses.items():
        contract = web3.eth.contract(address=Web3.to_checksum_address(address), abi=erc20_abi)

        try:
            balance = contract.functions.balanceOf(wallet_address).call()
            decimals = contract.functions.decimals().call()
            human_balance = balance / (10 ** decimals)

            assets.append({
                "symbol": symbol,
                "balance": round(human_balance, 6),
            })

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    return assets
    







