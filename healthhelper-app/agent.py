from __future__ import annotations
import logging
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("my-worker")
logger.setLevel(logging.DEBUG)

# Global variables
user_questions = []
agent_responses = []
SPREADSHEET_ID = '1cQt9f5gbCgGAaPRfobbnoJRcVHxY9wZdFKUrP2MiLIU'
SERVICE_ACCOUNT_FILE = r'C:\Users\surej\Downloads\renamedrivefiles-de0b98892de2.json'

def init_sheets_service():
    """Initialize and return Google Sheets service"""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)

def write_to_sheet(service, user_input: str, agent_response: str):
    """Write a single conversation pair to the next available row"""
    try:
        # First, get the next empty row
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A:B'
        ).execute()
        
        next_row = len(result.get('values', [])) + 1
        range_name = f'Sheet1!A{next_row}:B{next_row}'
        
        body = {
            'values': [[user_input, agent_response]]
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        logger.info(f"Updated {result.get('updatedCells')} cells")
        return result
        
    except Exception as e:
        logger.error(f"Error writing to sheet: {str(e)}")
        return None

async def entrypoint(ctx: JobContext):
    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    participant = await ctx.wait_for_participant()
    
    # Initialize sheets service once
    sheets_service = init_sheets_service()
    run_multimodal_agent(ctx, participant, sheets_service)
    
    logger.info("agent started")
    
    # Keep the agent running
    while True:
        await ctx.wait_for_disconnection()

def run_multimodal_agent(ctx: JobContext, participant: rtc.RemoteParticipant, sheets_service):
    logger.info("starting multimodal agent")

    model = openai.realtime.RealtimeModel(
        instructions=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation. "
            "You were created as a demo to showcase the capabilities of LiveKit's agents framework."
        ),
        modalities=["audio", "text"],
    )
    agent = MultimodalAgent(model=model)

    # Create a conversation handler
    def handle_message(message: llm.ChatMessage):
        if message.role == "user":
            logger.info(f"User said: {message.content}")
            user_questions.append(message.content)
        elif message.role == "assistant":
            logger.info(f"Agent responded: {message.content}")
            agent_responses.append(message.content)
            # Only write to sheet when we have both a question and response
            if user_questions and agent_responses:
                write_to_sheet(sheets_service, user_questions[-1], message.content)

    # Set up the message handler
    agent.on_message = handle_message

    # Start the agent (non-async)
    agent.start(ctx.room, participant)

    # Create initial message through the model
    model.chat(
        messages=[
            llm.ChatMessage(
                role="assistant",
                content="Please begin the interaction with the user in a manner consistent with your instructions.",
            )
        ]
    )

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )