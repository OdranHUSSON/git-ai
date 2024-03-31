import requests
import os
import re
import csv
from dotenv import load_dotenv
import logging
import base64
import asyncio
from async_openai_client import AsyncOpenAIClient

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# GitHub credentials and repo details
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')  # 'username/repo'

# Jira credentials
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_TOKEN = os.getenv('JIRA_TOKEN')
JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')  # 'yourdomain.atlassian.net'

# Headers for GitHub and Jira API requests
github_headers = {'Authorization': f'token {GITHUB_TOKEN}'}
jira_headers = {'Authorization': f'Basic {base64.b64encode(f"{JIRA_EMAIL}:{JIRA_TOKEN}".encode()).decode()}', 'Content-Type': 'application/json'}

def get_github_data(repo, branch):
    prs, commits = [], []
    try:
        prs_url = f'https://api.github.com/repos/{repo}/pulls?state=open&base=main&head={branch}'
        commits_url = f'https://api.github.com/repos/{repo}/commits?sha={branch}'

        prs_response = requests.get(prs_url, headers=github_headers)
        commits_response = requests.get(commits_url, headers=github_headers)

        prs = prs_response.json() if prs_response.status_code == 200 else []
        commits = commits_response.json() if commits_response.status_code == 200 else []
        
        logging.info(f"Fetched {len(prs)} PRs and {len(commits)} commits from GitHub for branch '{branch}'.")
    except Exception as e:
        logging.error(f"Error fetching GitHub data for branch '{branch}': {e}")
    return prs, commits

def extract_jira_keys(prs, commits):
    keys = set()
    for pr in prs:
        matches = re.findall(r'[A-Z]+-\d+', pr['title'])
        keys.update(matches)
    for commit in commits:
        matches = re.findall(r'[A-Z]+-\d+', commit['commit']['message'])
        keys.update(matches)
    logging.info(f"Extracted {len(keys)} unique Jira keys.")
    logging.info(f"Jira keys: {keys}")
    return list(keys)

def get_jira_authorization_header(email, token):
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return {'Authorization': f'Basic {encoded_credentials}', 'Content-Type': 'application/json'}

def adf_to_plain_text(adf):
    """
    Convert Atlassian Document Format (ADF) to plain text.
    
    :param adf: The ADF content as a dictionary.
    :return: A plain text representation of the ADF content.
    """
    plain_text = ""
    
    # For now we'll only handle paragraphs this should be suficient to generate propper changelogs via a LLM
    if not isinstance(adf, dict) or 'content' not in adf:
        return plain_text
    
    for content_block in adf.get('content', []):
        if content_block.get('type') == 'paragraph':
            for text_block in content_block.get('content', []):
                if text_block.get('type') == 'text':
                    plain_text += text_block.get('text', '') + "\n"
    
    return plain_text.strip()

def get_jira_issue_details(keys):
    details = {}
    jira_headers = get_jira_authorization_header(JIRA_EMAIL, JIRA_TOKEN)
    for key in keys:
        try:
            url = f'https://{JIRA_DOMAIN}/rest/api/3/issue/{key}'
            response = requests.get(url, headers=jira_headers)
            if response.status_code == 200:
                data = response.json()
                # Extract the issue type name from the issue details
                issue_type = data['fields']['issuetype']['name'] if 'issuetype' in data['fields'] and 'name' in data['fields']['issuetype'] else 'Unknown'
                
                # Convert ADF description to plain text
                description_adf = data['fields'].get('description', {})
                description_text = adf_to_plain_text(description_adf)
                
                details[key] = {
                    'title': data['fields']['summary'],
                    'description': description_text,
                    'type': issue_type 
                }
            else:
                logging.warning(f"Failed to fetch details for Jira issue {key}. HTTP status code: {response.status_code}")
                logging.warning(f"Response: {response.text}")
        except Exception as e:
            logging.error(f"Error fetching Jira issue details for {key}: {e}")
    return details


def read_csv_to_string(csv_filepath):
    """
    Reads a CSV file and converts it to a string format that can be used as input for AI.
    """
    rows = []
    with open(csv_filepath, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Format each row as a string, you might adjust the formatting to your needs
            row_str = ' | '.join(row)
            rows.append(row_str)
    return '\n'.join(rows)

async def generate_changelog_by_ai(csv_content):
    client = AsyncOpenAIClient()
    prompt = "As an expert product manager, convert the following changelog entries from a CSV into a readable changelog.md we'll include in this release ( as this is displayed to end users reformulate in business terms if possible and dont include card ids, start by headder 2 focus on the added / fixed part of the changelog as the version and title will be added by a script in the deployment process) Dont forget to reformulate for the end clients, this changelog is for external usage :\n\n" + csv_content
    
    changelog = await client.generate_response(prompt)
    print(changelog)
    with open('changelog.md', 'w', encoding='utf-8') as file:
        file.write(changelog)


def write_to_csv(prs, commits, issue_details):
    with open('changelog.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Jira Issue Key', 'Issue Type', 'Title', 'Description'])  # Add 'Issue Type' column
        
        for pr in prs:
            key = next((k for k in issue_details if k in pr['title']), None)
            if key:
                writer.writerow(['PR', key, issue_details[key]['type'], issue_details[key]['title'], issue_details[key]['description']])
                logging.info(f"Logged PR: {key}")
        
        for commit in commits:
            key = next((k for k in issue_details if k in commit['commit']['message']), None)
            if key:
                writer.writerow(['Commit', key, issue_details[key]['type'], issue_details[key]['title'], issue_details[key]['description']])
                logging.info(f"Logged commit: {key}")

# Execute
async def main(branch):
    prs, commits = get_github_data(GITHUB_REPO, branch)
    jira_keys = extract_jira_keys(prs, commits)
    issue_details = get_jira_issue_details(jira_keys)
    write_to_csv(prs, commits, issue_details)
    
    csv_content = read_csv_to_string('changelog.csv')
    await generate_changelog_by_ai(csv_content)

    logging.info("AI-generated changelog has been created.")
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: script.py <branch-name>")
    else:
        branch = sys.argv[1]
        asyncio.run(main(branch))