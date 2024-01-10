import asyncio
import subprocess
import sys
from async_openai_client import AsyncOpenAIClient 

async def generate_markdown_description(diff_output):
    client = AsyncOpenAIClient()
    prompt = "As a senior tech lead, generate a markdown description of the changes in this PR from this git diff:\n\n" + diff_output
    markdown_description = await client.generate_response(prompt)
    return markdown_description

async def main(base_branch):
    try:
        # Current branch is assumed as the target branch
        target_branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
        diff_cmd = ["git", "diff", base_branch, target_branch]
        diff_output = subprocess.check_output(diff_cmd, text=True)

        markdown_changes = await generate_markdown_description(diff_output)
        print(markdown_changes)
    except subprocess.CalledProcessError as e:
        print("An error occurred while trying to get git diff:", e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_branch = sys.argv[1]  # The branch to compare with
        asyncio.run(main(base_branch))
    else:
        print("Please provide the base branch name for comparison.")
