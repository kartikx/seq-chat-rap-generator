from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
import asyncio

from constants import model_client
from agents import VerseComposerAgent


async def main():
    runtime = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    runtime.start()
    await VerseComposerAgent.register(runtime, "verse_composer_agent", lambda: VerseComposerAgent(model_client=model_client))
    print("Verse Composer Agent started")

    await runtime.stop_when_signal()

if __name__ == "__main__":
    asyncio.run(main())
