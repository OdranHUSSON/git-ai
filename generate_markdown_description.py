import asyncio
import subprocess
import pyperclip
from async_openai_client import AsyncOpenAIClient 

async def generate_markdown_description(diff_output):
    client = AsyncOpenAIClient()
    prompt = "As a senior tech lead, generate a markdown description of the changes in this PR from this git diff (output the markdown directly without markdown tilds):\n\n" + diff_output
    markdown_description = await client.generate_response(prompt)
    return markdown_description

async def main():
    try:
        # Prompt the user for the base branch name
        base_branch = input("Please enter the base branch name for comparison: ")
        # Current branch is assumed as the target branch
        target_branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
        diff_cmd = ["git", "diff", base_branch, target_branch]
        diff_output = subprocess.check_output(diff_cmd, text=True)
        
        markdown_changes = await generate_markdown_description(diff_output)
        print(markdown_changes)

        # Confirm and copy to clipboard
        confirm = input("\n\nCopy this markdown to clipboard? (Y/n): ")
        if confirm.lower() in ['y', 'yes']:
            pyperclip.copy(markdown_changes)
            print("Markdown copied to clipboard.")
        else:
            print("Operation cancelled.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while trying to get git diff:", e)

if __name__ == "__main__":
    asyncio.run(main())
