import os
from typing import Dict

import pymongo
from dotenv import load_dotenv
from pinecone import Pinecone
from pydantic import BaseModel, Field

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# On langchain >= 1.0 these legacy chains live in `langchain_classic.chains`
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

load_dotenv(dotenv_path=".env")

# ---------------------------------------------------------------------------
# 1. Models + vector store
# ---------------------------------------------------------------------------
# Check Google's current model list: older Gemini / embedding models get retired.
# The embedding model's output dimension MUST match your Pinecone index dimension.
embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("gramaphone-index")
vector_store = PineconeVectorStore(index=index, embedding=embedding)
# vector_store = PineconeVectorStore(index=index, embedding=embedding, namespace="panchayat")

# ---------------------------------------------------------------------------
# 2. Retriever: the bridge between Pinecone and the LLM
# ---------------------------------------------------------------------------
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4},  # number of chunks passed to the LLM
)

# Rewrites follow-ups ("what about the fee?") into standalone queries
# using chat history, so the vector search gets a meaningful query.
contextualize_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given the chat history and the latest user message, rewrite the latest "
            "message as a standalone question that can be understood without the "
            "history. Do NOT answer it. If it is already standalone, return it unchanged.",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_prompt
)

# ---------------------------------------------------------------------------
# 3. Answer chain: retrieved docs are injected into {context}
# ---------------------------------------------------------------------------
system_prompt = (
    "You are a realtime AI assistant for complaint registration for a single "
    "Gramapanchayath. Collect the user's name, age, DOB, Aadhaar number, location "
    "and their complaint. "
    "Use the context below to answer questions about the panchayat's services, "
    "schemes and procedures. If the context does not contain the answer, say you "
    "don't know instead of inventing details. "
    "Always answer in one or two sentences. Don't repeat questions. "
    "At the end of the conversation, thank the user and assure them you will "
    "forward their complaint shortly.\n\n"
    "Context:\n{context}"  # required by create_stuff_documents_chain
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# ---------------------------------------------------------------------------
# 4. Per-session state (instead of one global chat_history for every user)
# ---------------------------------------------------------------------------
sessions: Dict[str, dict] = {}


def get_session(session_id: str) -> dict:
    return sessions.setdefault(session_id, {"history": [], "user_messages": []})


# ---------------------------------------------------------------------------
# 5. Database
# ---------------------------------------------------------------------------
class ComplaintExtractor(BaseModel):
    """Extract the complaint details from the user"""

    name: str = Field(description="Extract the name from the user")
    age: str = Field(description="Extract the age of the user")
    dob: str = Field(description="Extract the date of birth of the user")
    aadharnumber: str = Field(description="Extract the Aadhar number of the user")
    location: str = Field(description="Extract the location (city) of the user")
    complaint_summary: str = Field(description="Extract the complaint summary from the user")
    complaint_title: str = Field(description="Title of the complaint")


client = pymongo.MongoClient(os.getenv("MONGODB"))
db = client["web-app"]
collection = db["Works"]


def update_database(user_messages: list) -> str:
    combined_complaint = " ".join(user_messages)

    extraction_prompt = (
        ChatPromptTemplate.from_template(
            """
            Using the following combined complaint text, extract the details as follows:
            - Name
            - Age
            - Date of Birth (DOB)
            - Aadhaar Number
            - Location (city)
            - Complaint Title
            - Complaint Summary

            Input: {context}
            """
        )
        | llm.with_structured_output(schema=ComplaintExtractor)
    )
    complaint_data = extraction_prompt.invoke({"context": combined_complaint})

    # Your original built `insert_data` but inserted `complaint_json` instead.
    # Pick whichever shape the "Works" collection is supposed to have.
    complaint_json = complaint_data.model_dump()
    collection.insert_one(complaint_json)

    print("Complaint saved to database:", complaint_json)
    return "Complaint registered successfully. Thank you for reaching out!"


# ---------------------------------------------------------------------------
# 6. Entry point
# ---------------------------------------------------------------------------
def converse_ai(message: dict) -> str:
    """
    message = {"prompt": str, "disconnected": bool, "session_id": str (optional)}
    """
    session_id = message.get("session_id", "default")

    if message.get("disconnected"):
        session = sessions.pop(session_id, None)
        if session and session["user_messages"]:
            return update_database(session["user_messages"])
        return "No complaint to register."

    session = get_session(session_id)

    result = rag_chain.invoke(
        {"input": message["prompt"], "chat_history": session["history"]}
    )
    answer = result["answer"]  # result["context"] holds the retrieved Documents

    session["user_messages"].append(message["prompt"])
    session["history"].extend(
        [HumanMessage(content=message["prompt"]), AIMessage(content=answer)]
    )
    return answer


# ---------------------------------------------------------------------------
# Optional: load documents into Pinecone (run once if the index is empty)
# ---------------------------------------------------------------------------
def ingest_text(text: str, source: str = "manual") -> None:
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = splitter.create_documents([text], metadatas=[{"source": source}])
    vector_store.add_documents(docs)


if __name__ == "__main__":
    print(converse_ai({"prompt": "What documents do I need for a birth certificate?", "disconnected": False}))
