import json
import re

import yaml

from src.domain.lllm_moldes import ExtractorLLM
from src.domain.ports import LLMPort, VectorStorePort
from src.domain.state import State

import logging

logger = logging.getLogger(__name__)
with open("resources/prompts/extractor.yaml") as f:
    EXTRACTOR_PROMPT = yaml.safe_load(f)


def extractor_agent(state: State, llm: LLMPort, vector_store: VectorStorePort) -> dict:
    """From the content received in the state, makes a llm call to extract interest user and project points and content.

    Args:
        state (State): current graph state

    Returns:
        dict: extracted interest points
    """
    query = (
        f"{' '.join(state['user_interests'])} {' '.join(state['project_interests'])}"
    )
    chunks = vector_store.search_similar_chunks(
        query=query, user_id=str(state["user_id"]), paper_id=str(state["id"])
    )
    paper_content = "\n\n".join(chunks)

    system_prompt = EXTRACTOR_PROMPT["extractor"]["system"].format(
        user_interest_points=state["user_interests"],
        project_interest_points=state["project_interests"],
    )
    user_prompt = EXTRACTOR_PROMPT["extractor"]["user"].format(
        paper_content=paper_content
    )
    raw_response = llm.complete(
        prompt=user_prompt, model="llama-3.3-70b-versatile", system_prompt=system_prompt
    )

    matches = re.findall(r"\{[^{}]+\}", raw_response, re.DOTALL)
    if not matches:
        raise ValueError(f"No JSON found in LLM response: {raw_response[:200]}")

    try:
        interest_content = json.loads(matches[-1])

        logger.info(f"EXTRACTOR AGENT | Extracted content: {interest_content}")
        ExtractorLLM(**interest_content)
    except Exception as e:
        raise e

    return interest_content
