import requests
from dotenv import load_dotenv
import os
from os.path import join, dirname
from agents import function_tool
from typing import Dict
from pydantic import BaseModel

class ScamInput(BaseModel):
    address: str

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

@function_tool
def check_scam_address(wallet_info: ScamInput) -> Dict[str, bool]:
    """
    Check if crypto address is scam or not
    
    """
    scam_db_url = os.environ.get("SCAM_DATABASE_URL")
    if not scam_db_url:
        raise ValueError("SCAM_DATABASE_URL is not set in environment variables.")

    response = requests.get(scam_db_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch scam database: {response.status_code}")

    scam_data = response.json()
    scam_addresses = {addr.lower() for addr in scam_data.get("address", [])}

    return {"is_scam": wallet_info.address.lower() in scam_addresses}


