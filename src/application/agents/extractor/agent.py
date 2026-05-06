import json

import yaml

from src.domain.models import Paper, Profile
from src.domain.ports import LLMPort
from src.domain.state import State

with open("resources/prompts/extractor.yaml") as f:
    EXTRACTOR_PROMPT = yaml.safe_load(f)


async def extractor_agent(state: State, llm: LLMPort, profile: Profile) -> dict:
    """From the content received in the state, makes a llm call to extract interest user and project points and content.

    Args:
        state (State): _description_

    Returns:
        dict: _description_
    """
    technologies = [
        tech for project in profile.projects for tech in project.technologies
    ]

    extractor_prompt = EXTRACTOR_PROMPT.format(
        paper_content=state["content"],
        user_interest_points=profile.explicit_interests + profile.implicit_interests,
        project_interest_points=technologies,
    )
    interest_content = json.loads(
        llm.complete(prompt=extractor_prompt, model="google-ai-studio")
    )

    return interest_content
