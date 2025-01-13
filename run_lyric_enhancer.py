from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
import asyncio

from constants import model_client
from agents import LyricEnhancerAgent


async def main():
    runtime = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    runtime.start()
    await LyricEnhancerAgent.register(runtime, "lyric_enhancer_agent", lambda: LyricEnhancerAgent(model_client=model_client))
    print("Lyric Enhancer Agent started")

    await runtime.stop_when_signal()

if __name__ == "__main__":
    asyncio.run(main())
