from autogen_core import SingleThreadedAgentRuntime
import asyncio
from constants import Message, style_analyzer_topic
from autogen_core import TopicId
from agents import StyleAnalyzerAgent, ConceptGeneratorAgent, VerseComposerAgent, LyricEnhancerAgent, UserAgent
from constants import model_client, concept_generator_topic, verse_composer_topic, lyric_enhancer_topic, user_topic


async def main():
    runtime = SingleThreadedAgentRuntime()

    await StyleAnalyzerAgent.register(
        runtime, type=style_analyzer_topic, factory=lambda: StyleAnalyzerAgent(
            model_client=model_client)
    )

    await ConceptGeneratorAgent.register(runtime, type=concept_generator_topic, factory=lambda: ConceptGeneratorAgent(model_client=model_client))

    await VerseComposerAgent.register(runtime, type=verse_composer_topic, factory=lambda: VerseComposerAgent(model_client=model_client))

    await LyricEnhancerAgent.register(runtime, type=lyric_enhancer_topic, factory=lambda: LyricEnhancerAgent(model_client=model_client))

    await UserAgent.register(runtime, type=user_topic, factory=lambda: UserAgent())

    runtime.start()

    task1 = asyncio.create_task(runtime.publish_message(
        Message(
            content="Write a verse for Kendrick Lamar's album 'Good Kid M.A.A.D City'"),
        topic_id=TopicId(style_analyzer_topic, source="default"),
    ))

    task2 = asyncio.create_task(runtime.publish_message(
        Message(
            content="Write a verse for Drake's album 'Take Care'"),
        topic_id=TopicId(style_analyzer_topic, source="default"),
    ))

    await asyncio.gather(task1, task2)

    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
