from constants import Message, style_analyzer_topic, concept_generator_topic, model_client, verse_composer_topic, lyric_enhancer_topic, user_topic, simulate_network_delay
from dataclasses import dataclass
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

from autogen_core import (
    MessageContext,
    RoutedAgent,
    TopicId,
    message_handler,
    type_subscription,
)
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage
import time
import logging
import random


@type_subscription(topic_type=style_analyzer_topic)
class StyleAnalyzerAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A Style Analyzer")
        self._system_message = SystemMessage(
            content=(
                """
               You are a hip-hop lyric analyst. Given an artist and an album or song name, analyze their lyrics to extract their signature style.
               Focus on rhyme schemes, flow, recurring themes, vocabulary, and tone.
               Output a detailed style profile highlighting these elements in a structured format.

                Example Output:

                Rhyme Scheme: Complex multisyllabic rhymes with internal rhyming.
                Flow: Fast-paced with syncopated rhythms.
                Themes: Success, struggle, street life.
                Tone: Confident and aggressive.
                Common Vocabulary: Hustle, grind, money, loyalty.
               """
            )
        )
        self._model_client = model_client

    @message_handler
    async def handle_user_description(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"Hip hop artist with an Album or Song name: {
            message.content}"

        start_time = time.time()
        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(
                content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )
        end_time = time.time()
        elapsed_time = end_time - start_time

        log_entry = f"{message.session_id} {self.id.type}: {elapsed_time}"
        # logging.info(log_entry)

        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-'*80}\n{self.id.type} {message.session_id}:\n{response}")

        if simulate_network_delay:
            delay = random.uniform(0.01, 0.1)
            time.sleep(delay)

        await self.publish_message(Message(response, message.session_id), topic_id=TopicId(concept_generator_topic, source=self.id.key))


@type_subscription(topic_type=concept_generator_topic)
class ConceptGeneratorAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A concept generator")
        self._system_message = SystemMessage(
            content=(
                """
                "You are a creative hip-hop concept generator. Using the provided style profile and an optional user-provided topic or mood, brainstorm core ideas and themes for a rap verse.
                Ensure these ideas align with the artist’s style and tone. Present 2-3 compelling concepts to inspire the verse."

                Example Output:

                Theme 1: Overcoming obstacles in the music industry.
                Theme 2: Celebrating success and wealth.
                Mood: Confident, energetic.
                Imagery Suggestions: Diamond chains, late-night studio sessions, city skylines.
                """
            )
        )

        self._model_client = model_client

    @message_handler
    async def handle_artist_analysis(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"Here is the artist's style profile: {
            message.content}. Use an optional topic or mood to generate concepts."

        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(
                content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )

        response = llm_result.content
        assert (isinstance(response, str))

        print(f"{'-'*80}\n{self.id.type} {message.session_id}:\n{response}")

        response = message.content + "\n" + response

        if simulate_network_delay:
            delay = random.uniform(0.01, 0.1)
            time.sleep(delay)

        await self.publish_message(Message(response, message.session_id), topic_id=TopicId(verse_composer_topic, source=self.id.key))


@type_subscription(topic_type=verse_composer_topic)
class VerseComposerAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A verse composer")
        self._system_message = SystemMessage(
            content=(
                """
                "You are a skilled hip-hop lyricist. Using the artist’s style profile and the generated concepts, craft an 8 line rap verse.
                The verse must reflect the artist's signature flow, rhyme patterns, and lyrical themes.
                Maintain authenticity to the artist’s tone while making it creative and engaging."

                Only return the verse.

                Example Output:
                Cold nights turned me savage, now I’m burnin’ through the ceiling,
                Every loss was a lesson, now I’m stackin’ while I’m healin’.
                Studio locked, pen bleeds—visions vivid when I’m schemin’,
                Wrote my future in the dark, now my diamonds steady gleamin’.

                Talkin’ hustle, talkin’ pain, every scar became a medal,
                Pedal heavy, no brakes, foot’s welded to the metal.
                Voices doubted every step, now they echo when I’m risin’,
                Built this throne from the struggle—now I’m king without disguises
                """
            )
        )

        self._model_client = model_client

    @message_handler
    async def handle_artist_style_and_concepts(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"Here is the artist's style profile and possible themes you could use: {
            message.content}."

        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(
                content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )

        response = llm_result.content
        assert (isinstance(response, str))

        print(f"{'-'*80}\n{self.id.type} {message.session_id}:\n{response}")

        if simulate_network_delay:
            delay = random.uniform(0.01, 0.1)
            time.sleep(delay)

        await self.publish_message(Message(response, message.session_id), topic_id=TopicId(lyric_enhancer_topic, source=self.id.key))


@type_subscription(topic_type=lyric_enhancer_topic)
class LyricEnhancerAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A lyric enhancer")
        self._system_message = SystemMessage(
            content=(
                """
                You are a professional hip-hop editor. Refine the draft rap verse by enhancing wordplay, tightening the flow, and ensuring rhythmic balance.
                Make the lyrics more impactful while staying true to the artist's style. Focus on improving rhyme density, cadence, and vivid imagery.

                Only return the enhanced verse.

                Example Output (Enhanced):

                Cold nights forged a king, now I’m scorched in the skyline,
                Losses flipped to lessons, turned my pain into a gold mine.
                Locked in the booth, ink spills—every thought is a landmine,
                Lit the dark with my verses, now my diamonds outshine time.

                Talk struggle, talk hustle—every scar’s a war story,
                Foot heavy on the pedal, breakin’ lanes in full glory.
                Echoes of doubt fade out while I’m risin’ in the static,
                Built a throne from the ashes—now my reign is cinematic."
            """
            )
        )

        self._model_client = model_client

    @message_handler
    async def handle_artist_style_and_concepts(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"Here is a draft of the rap verse: {
            message.content}. Enhance the verse to make it more engaging and authentic to the artist's style."

        llm_result = await self._model_client.create(
            messages=[self._system_message, UserMessage(
                content=prompt, source=self.id.key)],
            cancellation_token=ctx.cancellation_token,
        )

        response = llm_result.content
        assert (isinstance(response, str))

        print(f"{'-'*80}\n{self.id.type} {message.session_id}:\n{response}")

        if simulate_network_delay:
            delay = random.uniform(0.01, 0.1)
            time.sleep(delay)

        await self.publish_message(Message(response, message.session_id), topic_id=TopicId(user_topic, source=self.id.key))


@type_subscription(topic_type=user_topic)
class UserAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("A user agent that simply outputs the generated verse.")

    @message_handler
    async def handle_final_output(self, message: Message, ctx: MessageContext) -> None:
        log_entry = f"{message.session_id} end: {time.time()}"
        logging.info(log_entry)
        print(f"{'-'*80}\n{self.id.type} {message.session_id}:\n{message.content}")
