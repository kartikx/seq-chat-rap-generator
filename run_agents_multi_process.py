from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
import asyncio
from constants import Message, run_test
from autogen_core import try_get_known_serializers_for_type


async def main():
    runtime = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    runtime.add_message_serializer(try_get_known_serializers_for_type(Message))
    runtime.start()

    await run_test(runtime)

    await runtime.stop_when_signal()


if __name__ == "__main__":
    asyncio.run(main())
