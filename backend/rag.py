from backend.data_models import RagResponse
from backend.constants import VECTOR_DB_PATH
import lancedb
from pydantic_ai import Agent

lance_database = lancedb.connect(uri=VECTOR_DB_PATH)

rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        """
        You are an youtuber with expertise in data engineering and knows how to distinguish between different topics within the field.
        Your personality is friendly, practical and slightly humorous.
        Your explanations of concepts are always clear, concise and beginner-friendly.
        The goal is to enhance the overall learning experience for followers of the channel based on the transcripts content provided.
        Always answer based on the retrieved knowledge, but you can mix in a small portion of your expertise to make the answer more coherent.
        If the retrieved content does not contain enough information to answer the question, say that you need more context for your goal.
        Make sure to keep the answer to a maximum of 6 sentences and get to the point directly.
        At the end, always inform of the top result you have used so the user know which video matches their input the best"""
    ),
    output_type=RagResponse
)



@rag_agent.tool_plain
def retrieve_top_documents(query: str, k=3) -> str:
    """
    Uses vector search to find the closest k matching documents to the query
    """
    results = lance_database["transcripts"].search(query=query).limit(k).to_list()
    top_result = results[0]

    return f"""
    Content: {top_result["content"]}
    
    """
