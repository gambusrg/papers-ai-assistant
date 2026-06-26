from pydantic import Field

from pydantic import BaseModel


class ExtractorLLM(BaseModel):
    technologies: list[str] = Field(description="Technologies mentioned in the paper")
    user_interest_points: list[str] = Field(
        description="User interest points in the paper"
    )
    project_interest_points: list[str] = Field(
        description="Project interest points in the paper"
    )
    user_content_points: str = Field(description="User content interest")
    project_content_points: str = Field(description="Project content points")
