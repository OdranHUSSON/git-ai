import asyncio
import os
from async_openai_client import AsyncOpenAIClient
import httpx

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

async def main():
    access_token = "merguezboudinnoir"
    current_version_info = await get_latest_version(access_token)
    os.system("python3 git_jira_changelog_generator.py")
    with open('changelog.md', 'r') as file:
        changelog = file.read()
        new_version = await generate_version_number(current_version_info, changelog)
        print(f"Generated new version: {new_version}")
        await post_new_version(access_token, new_version, changelog)

if __name__ == "__main__":
    asyncio.run(main())
