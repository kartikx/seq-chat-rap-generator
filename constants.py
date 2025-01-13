from autogen_ext.models.openai import OpenAIChatCompletionClient

from dataclasses import dataclass

import os


@dataclass
class Message:
    content: str


style_analyzer_topic = "style_analyzer"
concept_generator_topic = "concept_generator"
verse_composer_topic = "verse_composer"
lyric_enhancer_topic = "lyric_enhancer"
user_topic = "user"

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.environ["OPENAI_API_KEY"],
)
