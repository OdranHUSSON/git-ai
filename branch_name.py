import asyncio
import subprocess
from async_openai_client import AsyncOpenAIClient 

async def generate_branch_name(user_input):
    client = AsyncOpenAIClient()
    while True:  
        prompt = "You're an expert developer, generate a good branch name (LOWERCASE) for the following task: \n\n" + user_input
        branch_name = await client.generate_response(prompt)
        print(branch_name)

        # Confirm the branch name
        confirm = input("\n\n Is this branch name okay? (Y/n): ")
        if confirm.lower() in ['y', 'yes']:
            # Execute Git command to checkout new branch
            subprocess.run(["git", "checkout", "-b", branch_name])
            break  # Exit loop after successful branch creation
        else:
            # Ask for user input again
            print("Please provide a new description for the branch.")
            user_input = input("Branch description: ")

if __name__ == "__main__":
    user_input = input("Please provide a description for the branch: ")
    asyncio.run(generate_branch_name(user_input))
