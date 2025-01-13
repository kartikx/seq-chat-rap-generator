from constants import model_client
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

import asyncio
from agents import StyleAnalyzerAgent


async def main():
    runtime = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    runtime.start()
    await StyleAnalyzerAgent.register(runtime, "style_analyzer_agent", lambda: StyleAnalyzerAgent(model_client=model_client))
    print("Style Analyzer Agent started")

    await runtime.stop_when_signal()

if __name__ == "__main__":
    asyncio.run(main())
