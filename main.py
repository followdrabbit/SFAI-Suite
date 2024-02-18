import asyncio
import os
import argparse
from dotenv import load_dotenv
import openai
from utils.assistant_manager import OpenAIAssistantManager
from src.baseline.V4FinalJudge import create_baseline

async def main():

    # Setup argparse for command line arguments
    parser = argparse.ArgumentParser(description='Calls controls_creator with technology and ticket parameters.')
    parser.add_argument('-tec', '--technology', type=str, required=True, help='The new technology name')
    parser.add_argument('-tic', '--ticket', type=str, required=True, help='The ticket associated with the change')
    
    # Parse the provided arguments
    args = parser.parse_args()

    # Call the controls_creator function with the technology and the assistant ID
    await create_baseline(technology=args.technology, ticket=args.ticket)



if __name__ == "__main__":
    asyncio.run(main())
