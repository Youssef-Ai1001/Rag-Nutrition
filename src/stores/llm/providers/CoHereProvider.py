from ...LLMInterface import LLMInterface
from ...LLMEnums import CoHereEnums, DocumentTypeEnum
import cohere
import logging

class CoHereProvider(LLMInterface):

    def __init__(
        self,
        api_key: str,
        api_url: str = None,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int=1000,
        default_generation_temperature: float = 0.5
    ):
        self.api_key = api_key
        self.api_url = api_url
        
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        
        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_size = None
        
        self.client = cohere.Client(api_key = self.api_key)
        
        self.logger = logging.getLogger(__name__)
        
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id
        self.logger.info(f"Generation model set to {model_id}") 
    
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        self.logger.info(f"Embedding model set to {model_id} and embedding size set to {embedding_size}")
  
    def process_prompt(self, prompt: str):
        return prompt[:self.default_input_max_characters].strip()

    def generate_text(self, prompt:str, chat_history:list=[], max_output_tokens:int=None, temperature:float=None):
        
        if not self.client:
            self.logger.error(f"CoHere client is not initialized.")
            return None
        
        if not self.generation_model_id:
            self.logger.error(f"Generation model is not set.")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens is not None else self.default_generation_max_output_tokens       
        temperature = temperature if temperature is not None else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt, role=CoHereEnums.USER.value)
        )
        
        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message=self.process_prompt(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens
        )
        
        if not response or not hasattr(response, "text"):
            self.logger.error("Error while generating text with CoHere.")
            return None

        return response.text
       
    def embed_text(self, prompt: str, document_type: str=None):
        
        if not self.client:
            self.logger.error(f"CoHere client is not initialized.")
            return None

        if not self.embedding_model_id:
            self.logger.error(f"Embedding model is not set.")
            return None
        
        input_type = CoHereEnums.DOCUMENT.value
        
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = CoHereEnums.QUERY.value
            
        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_prompt(prompt)],
            input_type=input_type,
            embedding_types=["float"]
        )
        
        if not response or not hasattr(response, 'embeddings') or len(response.embeddings) == 0:
            self.logger.error("Error while generating embedding with CoHere.")
            return None
        
        return response.embeddings[0]
        
    def construct_prompt(self, prompt:str, role:str):
        return{
            "role": role,
            "text": self.process_prompt(prompt)
        }