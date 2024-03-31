import asyncio
import os
import sys  # Import sys to work with command-line arguments
from async_openai_client import AsyncOpenAIClient
import httpx
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables
load_dotenv()

# Assume the API token is stored in an environment variable named 'API_TOKEN'
API_TOKEN = os.getenv('API_TOKEN')

API_URL = "http://localhost:3000/api/version"

async def get_latest_version(token):
    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch the latest version, status code: {response.status_code}")

async def post_new_version(token, version, content):
    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"version": version, "content": content}
        response = await client.post(API_URL, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create a new version, status code: {response.status_code}")

async def generate_version_number(current_version, changelog):
    client = AsyncOpenAIClient()
    prompt = (
        f"Given the current version {current_version['version']} and the following changelog:\n{changelog}\n"
        "Determine the appropriate new version number. "
        "Remember, in Semantic Versioning (SemVer):"
        "\n- The MAJOR version increases with incompatible API changes,"
        "\n- The MINOR version increases with added functionality in a backwards compatible manner,"
        "\n- The PATCH version increases with backwards compatible bug fixes only."
        "\nWhat should be the new version number considering these guidelines? Output only the version number no additional text"
    )
    new_version = await client.generate_response(prompt)
    return new_version

async def main(branch_name):
    if API_TOKEN is None:
        print("API_TOKEN environment variable is not set. Exiting...")
        return

    current_version_info = await get_latest_version(API_TOKEN)
    
    # Execute the script with the branch name as an argument
    os.system(f"python3 git_jira_changelog_generator.py {branch_name}")
    
    with open('changelog.md', 'r') as file:
        changelog = file.read()
    new_version = await generate_version_number(current_version_info, changelog)
    print(f"Generated new version: {new_version}")
    await post_new_version(API_TOKEN, new_version, changelog)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <branch-name>")
        sys.exit(1)
    branch_name = sys.argv[1]
    asyncio.run(main(branch_name))
