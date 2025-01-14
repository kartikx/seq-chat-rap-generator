from autogen_core import SingleThreadedAgentRuntime
import asyncio
from agents import StyleAnalyzerAgent, ConceptGeneratorAgent, VerseComposerAgent, LyricEnhancerAgent, UserAgent
from constants import model_client, style_analyzer_topic, concept_generator_topic, verse_composer_topic, lyric_enhancer_topic, user_topic, run_test


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

    await run_test(runtime)

    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
