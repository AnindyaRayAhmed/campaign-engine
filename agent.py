"""Main ADK multi-agent workflow for the hackathon project."""

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.apps import App

from .sub_agents import MODEL, idea_agent, copy_agent, planner_agent
from .tools import save_campaign, get_campaigns_tool, save_brand_tool

save_and_format_agent = Agent(
    name="SaveAndFormatAgent",
    model=MODEL,
    description="Saves campaign in DB and returns final structured response.",
    tools=[save_campaign],
    output_key="final_output",
    instruction="""
        You are the final response generator.

        Look at the conversation history above to find the raw JSON outputs for the Idea, Copy, and Plan.

        IMPORTANT:
        First, parse the JSON strings from the history and call the save_campaign tool. 

        Then, format a human-readable response exactly like this:

        🎯 Campaign Idea:
        [Extract and insert the concept here]

        👥 Target Audience:
        [Extract and insert the target_audience here]

        🔥 Hook:
        [Extract and insert the hook here]

        🧾 Ad Copy:
        Headline: [Extract and insert the headline here]
        Description: [Extract and insert the description here]
        CTA: [Extract and insert the cta here]

        📅 Posting Plan:
        Platform: [Extract and insert the platform here]
        Schedule: [Extract and insert the schedule here]

        Saved Campaign ID: [Extract and insert the campaign ID returned by the tool here]

        Rules:
        - Do NOT output JSON.
        - Only output the formatted response.
    """
)

campaign_workflow = SequentialAgent(
    name="CampaignWorkflow",
    sub_agents=[idea_agent, copy_agent, planner_agent, save_and_format_agent]
)

root_agent = Agent(
    name="CampaignAssistant",
    model=MODEL,
    instruction=(
        "You are a marketing assistant.\n\n"
        "CRITICAL:\n"
        "If the user message is about creating a campaign, "
        "you MUST delegate to the CampaignWorkflow sub-agent.\n"
        "Do NOT respond yourself in that case.\n\n"
        "If the user message is casual (hi, hello), respond normally.\n\n"
        "If user provides brand details:\n"
        "- Extract brand, tone, colors.\n"
        "- Call save_brand_tool.\n\n"
        "If user asks to see past campaigns:\n"
        "- Call get_campaigns_tool\n"
        "- Summarize results\n"
    ),
    tools=[save_brand_tool, get_campaigns_tool],
    sub_agents=[campaign_workflow]
)

app = App(
    name="campaign_engine",
    root_agent=root_agent
)
