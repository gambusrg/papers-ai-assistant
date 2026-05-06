import json

import yaml

from src.domain.ports import LLMPort
from src.domain.state import State

with open("resources/prompts/extractor.yaml") as f:
    EXTRACTOR_PROMPT = yaml.safe_load(f)


async def extractor_agent(state: State, llm: LLMPort) -> dict:
    """From the content received in the state, makes a llm call to extract interest user and project points and content.

    Args:
        state (State): current graph state

    Returns:
        dict: extracted interest points
    """
    extractor_prompt = EXTRACTOR_PROMPT.format(
        paper_content=state["content"],
        user_interest_points=state["user_interests"],
        project_interest_points=state["project_interests"],
    )
    interest_content = json.loads(
        llm.complete(prompt=extractor_prompt, model="gemini-2.0-flash")
    )

    return interest_content
