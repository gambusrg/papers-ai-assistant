import datetime
import uuid

from src.domain.state import State

TEST_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
TEST_PAPER_ID = uuid.UUID("00000000-0000-0000-0000-000000000002")

from src.domain.conversation_state import ConversationState

TEST_CONVERSATION_STATE: ConversationState = {
    "user_id": TEST_USER_ID,
    "paper_id": TEST_PAPER_ID,
    "query": "What does this paper say about attention mechanisms?",
    "response": "",
    "conversation_context": [],
}

TEST_STATE: State = {
    "user_id": TEST_USER_ID,
    "id": TEST_PAPER_ID,
    "source": "https://arxiv.org/pdf/1706.03762",
    "title": "Attention is All You Need",
    "technologies": ["transformers", "attention", "nlp"],
    "content": "We propose a new simple network architecture, the Transformer...",
    "headers": ["Abstract", "Introduction", "Model Architecture"],
    "pages": 15,
    "timestamp": datetime.datetime(2024, 1, 1, 0, 0, 0),
    "project_interest_points": [],
    "user_interest_points": [],
    "project_content_points": "",
    "user_content_points": "",
    "related_papers": [],
    "previous_user_interests": ["deep learning", "nlp"],
    "previous_project_interests": ["python", "pytorch"],
    "user_interests": ["deep learning", "nlp", "transformers"],
    "project_interests": ["python", "pytorch", "llms"],
}
