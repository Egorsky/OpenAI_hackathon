from web3 import Web3
from agents import function_tool
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

@function_tool
def fetch_aave_info():
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

    return {
        "collateral_usd": round(data[0] / 1e8, 4),
        "debt_usd": round(data[1] / 1e8, 4),
        "available_borrow_usd": round(data[2] / 1e8, 4),
        "health_factor": round(data[5] / 1e18, 4)
    }

    







