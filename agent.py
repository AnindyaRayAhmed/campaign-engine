"""Main ADK multi-agent workflow for the hackathon project.

Pipeline:
User Input -> Idea Agent -> Copy Agent -> Planner Agent -> Save to SQLite
"""

from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.apps import App

from sub_agents import MODEL, copy_agent, idea_agent, planner_agent
from tools import save_campaign

# Load .env values for local runs.
load_dotenv()

save_and_format_agent = LlmAgent(
    name="SaveAndFormatAgent",
    model=MODEL,
    description="Saves campaign in DB and returns final structured response.",
    tools=[save_campaign],
    instruction=(
        "You are the final step in a campaign pipeline.\n"
        "Input state:\n"
        "idea_result: {idea_result}\n"
        "copy_result: {copy_result}\n"
        "planner_result: {planner_result}\n\n"
        "Tasks:\n"
        "1) Parse these JSON values.\n"
        "2) Call tool save_campaign exactly once with payload:\n"
        "   {\"product\": idea_result.product, \"idea\": idea_result, \"copy\": copy_result, \"plan\": planner_result.plan}\n"
        "3) Return final plain-text output in EXACT format:\n\n"
        "Campaign Idea:\n"
        "...\n\n"
        "Ad Copy:\n"
        "* Headline: ...\n"
        "* Description: ...\n"
        "* CTA: ...\n\n"
        "Posting Plan:\n"
        "* Platform: ...\n"
        "* Schedule: ...\n\n"
        "Saved Campaign ID: ...\n"
    ),
)

root_agent = SequentialAgent(
    name="CampaignManager",
    description="Coordinates idea, copy, planning, and storage for campaigns.",
    sub_agents=[idea_agent, copy_agent, planner_agent, save_and_format_agent],
)

# ADK CLI compatibility (recommended object name: app)
app = App(name="campaign_engine", root_agent=root_agent)
