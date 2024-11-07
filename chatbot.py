from prompt import LLM_QUERY_PROMPT
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from config import load_config
from hybrid_search import HybridSearch


CONFIG = load_config()

class ChatbotAssistant:
    def __init__(self):
        self.llm = ChatGroq(
            model= CONFIG['llm_groq']['model'],
            api_key= CONFIG['llm_groq']['api_key'],
            temperature= 0.0,
            streaming=True
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.prompt = self.get_prompt()
        self.search = HybridSearch()
        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )
    def get_prompt(self):
        return ChatPromptTemplate.from_messages(
            LLM_QUERY_PROMPT
        )
    def invoke(self, query):
        docs = self.search.query_docs(query_text=query)
        response = self.chain.invoke(
            {'context': docs, 'humman_input': query, 'chat_history': self.memory.load_memory_variables({})["chat_history"]}
        )
        return response
