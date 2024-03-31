import asyncio
import openai
from dotenv import load_dotenv
import os

load_dotenv()

class AsyncOpenAIClient:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = api_key 
        self.client = openai.AsyncOpenAI() 
 
    async def generate_response(self, prompt):
        try:
            stream = await self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            response_text = ""
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content
            return response_text.strip() 
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""