from pydantic import Field, BaseModel
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001")

EMBEDDING_DIM = 3072

class Transcript(LanceModel):
    script_id: str = Field(description="unique ID of each record")
    source_name: str = Field(description="name of the original .md file")
    content: str = embedding_model.SourceField()
    embedding: Vector(EMBEDDING_DIM) = embedding_model.VectorField()

class Prompt(BaseModel):
    prompt: str = Field(description="Question or message provided from user.")

class RagResponse(BaseModel):
    answer: str = Field(description= "Answer returned to user.")