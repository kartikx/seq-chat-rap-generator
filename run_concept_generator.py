from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
import asyncio

from constants import model_client
from agents import ConceptGeneratorAgent


async def main():
    runtime = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    runtime.start()
    await ConceptGeneratorAgent.register(runtime, "concept_generator_agent", lambda: ConceptGeneratorAgent(model_client=model_client))
    print("Concept Generator Agent started")
    await runtime.stop_when_signal()

if __name__ == "__main__":
    asyncio.run(main())
