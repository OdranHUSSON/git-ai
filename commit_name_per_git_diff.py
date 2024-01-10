import asyncio
import subprocess
from async_openai_client import AsyncOpenAIClient 

async def generate_commit_message(changes):
    client = AsyncOpenAIClient()
    while True:  # Loop to allow for repeated attempts
        prompt = "You're an expert developer, generate a short commit message with one emoji at the beginning for the following changes: \n\n ```" + changes + "```"
        commit_message = await client.generate_response(prompt)
        print(commit_message)

        # Confirm the commit message
        confirm = input("\n\n Is this commit message okay? (Y/n): ")
        if confirm.lower() in ['y', 'yes']:
            # Execute Git commands
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", commit_message])
            break  # Exit loop after successful commit
        else:
            # Ask for user input and use it as the new changes description
            print("Please provide a custom commit description.")
            changes = input("Commit description: ")

if __name__ == "__main__":
    try:
        # Execute git diff and capture its output
        git_diff_output = subprocess.check_output(["git", "diff"], text=True)
        if git_diff_output:
            asyncio.run(generate_commit_message(git_diff_output))
        else:
            print("No changes detected.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while trying to get git diff:", e)
