from langchain_openai import AzureChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, AgentHistoryList
import asyncio
import json
import print_object
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

    config = BrowserConfig(
        headless=False,
    )
    
    browser = Browser(config=config)

    agent = Agent(
        task="搜索azure ai foundry doc主页, 并抓取左侧树桩导航栏所有link",
        llm=llm,
        browser=browser,
    )
    result = await agent.run()
    # print(result)
    print_object.save_as_json(result, "result.json", excluded_fields=['screenshot'])

asyncio.run(main())