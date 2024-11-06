from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.chains import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel
import uuid
import tqdm
from config import load_config
from chunking.recursive_token_chunker import RecursiveTokenChunker
import os
from  prompt import (
    AGENT_UPDATE_SUMMARY_CHUNK_PROMPT,
    AGENT_SUMMARY_CHUNK_PROMPT,
    AGENT_UPDATE_TITLE_CHUNK_PROMPT,
    AGENT_CREATE_TITLE_CHUNK_PROMPT,
    AGENT_GET_RELEVANT_CHUNK_PROMPT,
    AGENT_BASIC_CHUNKING_PROMPT,
) 
CONFIG = load_config()

def token_count(string: str) -> int:
    import tiktoken
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string, disallowed_special=()))
    return num_tokens

class AgenticChunkerGroq:
    def __init__(self):
        # Start Ollama server
        self.llama_model = ChatGroq(model=CONFIG['llm_groq']['model'],
                                    api_key = CONFIG['llm_groq']['api_key'])

        self.chunks = {}
        self.id_truncate_limit = 5
        self.generate_new_metadata_ind = True
        self.print_logging = True
        self.splitter = RecursiveTokenChunker(
            chunk_size=200,
            chunk_overlap=0
        )

    def add_propositions(self, propositions):
        for proposition in propositions:
            self.add_proposition(proposition)


    def add_proposition_to_chunk(self, chunk_id, proposition):
        # Add the new proposition to the existing chunk
        self.chunks[chunk_id]['propositions'].append(proposition)

        # Update the chunk's summary and title if needed
        if self.generate_new_metadata_ind:
            self.chunks[chunk_id]['summary'] = self._update_chunk_summary(self.chunks[chunk_id])
            self.chunks[chunk_id]['title'] = self._update_chunk_title(self.chunks[chunk_id])

    def _update_chunk_summary(self, chunk):
        prompt = AGENT_UPDATE_SUMMARY_CHUNK_PROMPT.format(
            current_chunks = chunk['summary'],
            adding_chunks = ', '.join(chunk['propositions'])
        )
        response = self.llama_model.invoke(prompt).content.strip()
        return response

    def _update_chunk_title(self, chunk):
        prompt = AGENT_UPDATE_TITLE_CHUNK_PROMPT.format(
            input = chunk['summary']
        )
        response = self.llama_model.invoke(prompt).content.strip()
        return response


    def add_proposition(self, proposition):
        if self.print_logging:
            print(f"\nAdding: '{proposition}'")

        if len(self.chunks) == 0:
            if self.print_logging:
                print("No chunks, creating a new one")
            self._create_new_chunk(proposition)
            return

        chunk_id = self._find_relevant_chunk(proposition)

        print('---chunk_id', chunk_id)

        if chunk_id:
            if self.print_logging:
                print(f"Chunk Found ({self.chunks[chunk_id]['chunk_id']}), adding to: {self.chunks[chunk_id]['title']}")
            self.add_proposition_to_chunk(chunk_id, proposition)
            return
        else:
            if self.print_logging:
                print("No chunks found")
            self._create_new_chunk(proposition)

    def _create_new_chunk(self, proposition):
        new_chunk_id = str(uuid.uuid4())[:self.id_truncate_limit]
        new_chunk_summary = self._get_new_chunk_summary(proposition)
        new_chunk_title = self._get_new_chunk_title(new_chunk_summary)

        self.chunks[new_chunk_id] = {
            'chunk_id': new_chunk_id,
            'propositions': [proposition],
            'title': new_chunk_title,
            'summary': new_chunk_summary,
            'chunk_index': len(self.chunks)
        }
        if self.print_logging:
            print(f"Created new chunk ({new_chunk_id}): {new_chunk_title}")

    def _get_new_chunk_summary(self, proposition):
        prompt = AGENT_SUMMARY_CHUNK_PROMPT.format(input = proposition)

        response = self.llama_model.invoke(prompt).content
        return response.strip()

    def _get_new_chunk_title(self, summary):
        prompt = AGENT_CREATE_TITLE_CHUNK_PROMPT.format(
            input = summary
        )

        response = self.llama_model.invoke(prompt).content
        return response.strip()

    def _find_relevant_chunk(self, proposition):
        current_chunk_outline = self.get_chunk_outline()
        prompt = AGENT_GET_RELEVANT_CHUNK_PROMPT.format(
            current_chunks = proposition,
            existed_chunks = current_chunk_outline
        )

        response = self.llama_model.invoke(prompt).content.strip()

        # Extract only the chunk ID
        if "No chunks" in response:
            return None
        else:
            # Use regex to find the chunk ID in the response
            import re
            match = re.search(r'\b\w{5}\b', response)  # Assuming the chunk ID is always 5 alphanumeric characters
            if match:
                return match.group(0)
            return None


    def get_chunk_outline(self):
        chunk_outline = []
        for chunk_id, chunk in self.chunks.items():
            chunk_outline.append(f"Chunk ID: {chunk['chunk_id']}\nChunk Title: {chunk['title']}\nSummary: {chunk['summary']}\n\n")
        return chunk_outline

    def pretty_print_chunks(self):
        print(f"\nYou have {len(self.chunks)} chunks\n")
        for chunk_id, chunk in self.chunks.items():
            print(f"Chunk #{chunk['chunk_index']}")
            print(f"Chunk ID: {chunk_id}")
            print(f"Summary: {chunk['summary']}")
            print("Propositions:")
            for prop in chunk['propositions']:
                print(f"    - {prop}")
            print("\n\n")
    def split_text(self, documents):
        chunks = self.splitter.split_text(documents)
        chunks_processed = []
        chunk_input = ''
        token_len = 0
        for i, chunk in enumerate(chunks):
            token_len += token_count(chunk)
            chunk_input += f'<|start_chunk_{i + 1}|>{chunk}<|end_chunk_{i+1}|>'
            if token_len > 800:
                chunks_processed.append(chunk_input)
                chunk_input  = ''
                token_len = 0
        new_chunks = []
        with tqdm.tqdm(total = len(chunks_processed)) as pbar:
            for i, chunk in enumerate(chunks_processed):
                prompt = AGENT_BASIC_CHUNKING_PROMPT.format(
                    input = chunk
                )
                response = self.llama_model.invoke(prompt).content.strip()
                import re
                numbers = re.findall(r'\d+', response)
                numbers = list(map(int, numbers))
                start_position = 0
                for index, n in enumerate(numbers):
                    index_split = f'<|end_chunk_{n}|>'
                    end_position = chunk.find(index_split)
                    if end_position != -1:
                        result = chunk[start_position : end_position]
                        start_position = end_position + len(index_split)
                    else:
                        result = chunk
                    chunk_clean = re.sub(r'<\|.*?\|>', ' ', result)
                    new_chunks.append(chunk_clean)
                pbar.update(1)
        return new_chunks



# # Instantiate your chunker using LLaMA 3
# llama_chunker = AgenticChunkerGroq()

# # Sample propositions
# propositions = [
#     "The only way to be successful is to get up at the crack of dawn – or so the story goes.",
#     "But early rising productivity is not a one-size-fits-all situation, Bryan Lufkin finds.",
#     "Being successful means waking up early – or so we’re constantly told."
# ]

# llama_chunker.add_propositions(propositions)
# llama_chunker.pretty_print_chunks()
