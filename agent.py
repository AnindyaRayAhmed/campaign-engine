"""Main ADK multi-agent workflow for the hackathon project.

Pipeline:
User Input -> Idea Agent -> Copy Agent -> Planner Agent -> Save to SQLite
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.apps import App

from sub_agents import MODEL, copy_agent, idea_agent, planner_agent
from tools import save_campaign


save_and_format_agent = LlmAgent(
    name="SaveAndFormatAgent",
    model=MODEL,
    description="Saves campaign in DB and returns final structured response.",
    tools=[save_campaign],
    instruction=(
    "You are the final step in a campaign pipeline.\n\n"
    "You will receive outputs from previous agents:\n"
    "- idea_result\n"
    "- copy_result\n"
    "- planner_result\n\n"
    "Extract the key information and call the save_campaign tool.\n\n"
    "If any field is missing, infer reasonable values instead of failing.\n\n"
    "Call save_campaign tool EXACTLY like this:\n"
    "{\n"
    '  "product": idea_result["product"],\n'
    '  "idea": idea_result,\n'
    '  "copy": copy_result,\n'
    '  "plan": planner_result["plan"]\n'
    "}\n\n"
    "Then return output in this format:\n\n"
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
