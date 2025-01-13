from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost, GrpcWorkerAgentRuntime
import asyncio
from constants import Message, style_analyzer_topic
from autogen_core import try_get_known_serializers_for_type, TopicId


async def main():
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start()

    runtime = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    runtime.add_message_serializer(try_get_known_serializers_for_type(Message))
    runtime.start()

    # TODO Add this in a separate file that can make multiple requests.
    await asyncio.sleep(10)

    await runtime.publish_message(
        Message(
            content="Write a verse for Kendrick Lamar's album 'To Pimp a Butterfly'"),
        topic_id=TopicId(style_analyzer_topic, source="default"),
    )

    await host.stop_when_signal()


if __name__ == "__main__":
    asyncio.run(main())
