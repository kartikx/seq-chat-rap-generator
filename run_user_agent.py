from autogen_core import (
    TopicId
)
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
import asyncio

from constants import Message, style_analyzer_topic

from agents import UserAgent


async def main():
    runtime = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    runtime.start()
    await UserAgent.register(runtime, "user_agent", lambda: UserAgent())
    print("User Agent started")

    # await asyncio.sleep(5)

    # await runtime.publish_message(
    #     Message(
    #         content="Write a verse for Kendrick Lamar's album 'To Pimp a Butterfly'"),
    #     topic_id=TopicId(style_analyzer_topic, source="default"),
    # )

    await runtime.stop_when_signal()

if __name__ == "__main__":
    asyncio.run(main())
