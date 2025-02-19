from langchain_openai import AzureChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os 
from pydantic import SecretStr
load_dotenv()

endpoint = os.getenv("ENDPOINT_URL")
api_key = os.getenv("AZURE_OPENAI_API_KEY") 

llm = AzureChatOpenAI(
    model_name="gpt-4o",
    api_version='2024-02-15-preview',
    azure_endpoint=endpoint,
    api_key=SecretStr(api_key),
)

async def main():
    agent = Agent(
        task="找到kong这家公司的主页，然后找到他们的公司简介下载到txt文件中",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())