import json

import yaml

from src.domain.ports import LLMPort
from src.domain.state import State

import logging

logger = logging.getLogger(__name__)
with open("resources/prompts/extractor.yaml") as f:
    EXTRACTOR_PROMPT = yaml.safe_load(f)


def extractor_agent(state: State, llm: LLMPort) -> dict:
    """From the content received in the state, makes a llm call to extract interest user and project points and content.

    Args:
        state (State): current graph state

    Returns:
        dict: extracted interest points
    """
    extractor_prompt = EXTRACTOR_PROMPT["extractor"]["system"].format(
        paper_content=state["content"],
        user_interest_points=state["user_interests"],
        project_interest_points=state["project_interests"],
    )
    raw_response = llm.complete(
        prompt=extractor_prompt, model="llama-3.3-70b-versatile"
    )
    logger.info(f"LLM Extractor response: {raw_response}")
    json_start = raw_response.find("{")
    json_end = raw_response.rfind("}") + 1
    interest_content = json.loads(raw_response[json_start:json_end])

    return interest_content
