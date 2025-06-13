"""Create a ChatVectorDBChain for question/answering."""
from langchain.chains import ConversationChain
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableSequence

def get_chain(stream_handler, tracing: bool = False):
    """Create a conversation chain for question/answering using Gemini."""

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )
    manager = AsyncCallbackManager([])
    stream_manager = AsyncCallbackManager([stream_handler])
    if tracing:
        tracer = LangChainTracer()
        manager.add_handler(tracer)
        stream_manager.add_handler(tracer)

    streaming_llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-001",
        client_options=None,
        transport=None,
        additional_headers=None,
        client=None,
        async_client=None,
        callback_manager=manager,
    )

    memory = ConversationBufferMemory(return_messages=True, memory_key="history")

    # Define a function to load memory and format input for the prompt
    def with_memory(inputs):
        history = memory.load_memory_variables(inputs).get("history", [])
        return {"input": inputs["input"], "history": history}

    # Compose the chain using the pipe syntax
    chain = with_memory | prompt | streaming_llm

    return chain
