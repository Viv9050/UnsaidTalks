
import re
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools

def analyze_prompt(prompt: str) -> str:
    tags = []
    if "vegan" in prompt.lower(): tags.append("🌿 Vegan")
    if "vegetarian" in prompt.lower(): tags.append("🌱 Vegetarian")
    if "gluten-free" in prompt.lower(): tags.append("🌾 Gluten-Free")
    if "under 30" in prompt.lower() or "less than 30" in prompt.lower(): tags.append("⏱️ Quick")
    if "allergic to nuts" in prompt.lower(): tags.append("⚠️ Nut-Free")
    if "beginner" in prompt.lower(): tags.append("👨‍🍳 Beginner")

    tag_line = " | ".join(tags) if tags else "General Recipe"
    return f"{prompt.strip()}\n\n[Tags: {tag_line}]"

recipe_agent = Agent(
    name="ChefGenius",
    tools=[ExaTools()],
    model=OpenAIChat(id="gpt-4o"),
    description="ChefGenius helps you cook delicious recipes with your ingredients, time, and skill level.",
    instructions=dedent("""
        Read the user's ingredients, dietary needs, and time limit.
        Search for a fitting recipe and return:
        - Recipe title + cuisine
        - Prep & cook time
        - Skill level + emoji tags
        - Ingredients list
        - Step-by-step instructions
        - Nutritional info (if known)
        - Substitutions and storage tips
    """),
    markdown=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
)

if __name__ == "__main__":
    user_prompt = "I'm a beginner. I have tofu, garlic, and broccoli. I need a vegan dinner under 30 minutes. I'm allergic to nuts."
    final_prompt = analyze_prompt(user_prompt)
    recipe_agent.print_response(final_prompt, stream=True)
