import asyncio
import sys
import subprocess
from async_openai_client import AsyncOpenAIClient 

async def generate_commit_message(changes):
    client = AsyncOpenAIClient()
    prompt = "You're an expert developer, generate a short commit message with one emoji at the beginning for the following changes: \n\n ```" + changes + "```"
    commit_message = await client.generate_response(prompt)
    print(commit_message)

    # Confirm the commit message
    confirm = input("\n\n Is this commit message okay? (Y/n): ")
    if confirm.lower() in ['y', 'yes']:
        # Execute Git commands
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", commit_message])
    else:
        print("Commit aborted.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        changes = " ".join(sys.argv[1:])
        asyncio.run(generate_commit_message(changes))
    else:
        print("Please provide a description of the changes.")
