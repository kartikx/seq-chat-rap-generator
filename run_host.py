from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
import asyncio


async def main():
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start()

    await host.stop_when_signal()


if __name__ == "__main__":
    asyncio.run(main())
