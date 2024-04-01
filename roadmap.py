import requests
import os
from dotenv import load_dotenv
import logging

# Setup logging and environment variables
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

# JIRA credentials and domain
JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')  # Example: 'yourdomain.atlassian.net'
JIRA_ACCESS_TOKEN = os.getenv('JIRA_ACCESS_TOKEN')  # Ensure this is set in your .env file or environment

def get_jira_epics(board_id):
    """
    Fetches epics from a specified JIRA board.

    :param board_id: The ID of the JIRA board from which to fetch epics.
    :return: A list of epics, or an empty list in case of failure.
    """
    url = f'https://{JIRA_DOMAIN}/rest/agile/1.0/board/{board_id}/epic'
    headers = {
        'Authorization': f'Bearer {JIRA_ACCESS_TOKEN}',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        epics = response.json()
        logging.info(f"Successfully fetched {len(epics.get('values', []))} epics from JIRA board {board_id}.")
        return epics.get('values', [])
    except requests.RequestException as e:
        logging.error(f"Error fetching epics from JIRA board {board_id}: {e}")
        return []

# Example usage
if __name__ == "__main__":
    board_id = '1' 
    epics = get_jira_epics(board_id)
    print(epics)
