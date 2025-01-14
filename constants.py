from autogen_core import TopicId
import logging
from autogen_ext.models.openai import OpenAIChatCompletionClient

from dataclasses import dataclass

import asyncio
import time
import logging
import uuid
import numpy as np

lambda_rate = 0.15
total_requests = 25


@dataclass
class Message:
    content: str
    session_id: str


simulate_network_delay = True

style_analyzer_topic = "style_analyzer"
concept_generator_topic = "concept_generator"
verse_composer_topic = "verse_composer"
lyric_enhancer_topic = "lyric_enhancer"
user_topic = "user"

# model_client = OpenAIChatCompletionClient(
#     model="gpt-4o-mini",
#     api_key=os.environ["OPENAI_API_KEY"],
# )

model_client = OpenAIChatCompletionClient(
    model="llama3.2",
    base_url="http://127.0.0.1:11434/v1",
    api_key="placeholder",
    model_capabilities={
        "vision": False,
        "function_calling": True,
        "json_output": True,
    },
)

logging.basicConfig(filename='request_times.log', level=logging.INFO)

rappers_albums = [
    ("Kendrick Lamar", "To Pimp a Butterfly"),
    ("J. Cole", "2014 Forest Hills Drive"),
    ("Drake", "Take Care"),
    ("Nas", "Illmatic"),
    ("Jay-Z", "The Blueprint"),
    ("Eminem", "The Marshall Mathers LP"),
    ("Kanye West", "My Beautiful Dark Twisted Fantasy"),
    ("Travis Scott", "ASTROWORLD"),
    ("Lil Wayne", "Tha Carter III"),
    # ("Tyler, The Creator", "IGOR"),
    # ("Pusha T", "DAYTONA"),
    # ("Future", "DS2"),
    # ("Joey Bada$$", "B4.DA.$$"),
    # ("Mac Miller", "Swimming"),
    # ("Nicki Minaj", "Pink Friday"),
    # ("Logic", "Under Pressure"),
    # ("A$AP Rocky", "LONG.LIVE.A$AP"),
    # ("Childish Gambino", "Because the Internet"),
    # ("MF DOOM", "Madvillainy"),
    # ("Lil Uzi Vert", "Eternal Atake")
]


async def run_test(runtime):
    task_list = []

    for rapper, album in rappers_albums:
        id = uuid.uuid4().__str__()
        start_time = time.time()
        logging.info(f"{id} start: {start_time}")
        logging.info(f"{id} rapper: {rapper} album: {album}")
        # print("Making request at: ",  time.strftime(
        #     "%Y-%m-%d %H:%M:%S", time.localtime()))

        task = asyncio.create_task(runtime.publish_message(
            Message(
                content=f"Write a verse for {rapper}'s album '{album}'",
                session_id=id),
            topic_id=TopicId(style_analyzer_topic, source="default"),
        ))

        task_list.append(task)

        inter_arrival_time = np.random.exponential(1 / lambda_rate)
        time.sleep(inter_arrival_time)

    await asyncio.gather(*task_list)
