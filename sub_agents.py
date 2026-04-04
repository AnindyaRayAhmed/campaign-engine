"""Sub-agent definitions for the campaign pipeline."""

from google.adk.agents.llm_agent import LlmAgent

MODEL = "gemini-2.5-flash"

idea_agent = LlmAgent(
    name="IdeaAgent",
    model=MODEL,
    description="Generates campaign concept, audience, and hook.",
    instruction=(
        "You are the Idea Agent for a marketing team. "
        "The user message will look like: 'Create a campaign for [product]'. "
        "Extract product name and create a simple, creative campaign concept including an emotional hook and the main problem it solves. "
        "Return ONLY valid JSON with this exact schema: "
        '{"product":"...","concept":"...","target_audience":"...","hook":"..."}'
    ),
    output_key="idea_result",
)

copy_agent = LlmAgent(
    name="CopyAgent",
    model=MODEL,
    description="Creates ad headline, description, and CTA.",
    instruction=(
        "You are the Copy Agent. Use the campaign idea below to generate ad copy.\n"
        "Idea JSON:\n{idea_result}\n"
        "Return ONLY valid JSON with this exact schema: "
        '{"headline":"...","description":"...","cta":"..."}'
    ),
    output_key="copy_result",
)

planner_agent = LlmAgent(
    name="PlannerAgent",
    model=MODEL,
    description="Builds posting platform + schedule and final structured output.",
    instruction=(
    "You are the Planner Agent. Use idea and copy to create a simple posting plan.\n"
    "Idea JSON:\n{idea_result}\n"
    "Copy JSON:\n{copy_result}\n"
    "Return ONLY valid JSON like this:\n"
    '{"plan":{"platform":"Instagram","schedule":"Post at 7 PM for 3 days"}}'
),
    output_key="planner_result",
)
