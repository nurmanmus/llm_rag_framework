from fastapi import APIRouter, Request
from langserve import add_routes  # type: ignore

from llm.chains import malaysian_mistral_chain, malaysian_rag_chain, mistral_chain, mixtral_chain, rag_chain
from llm.chains.hf_chain.chain import retriever as myth_retriever
from llm.chains.mesolitica.chain import retriever as malaysian_retriever
from llm.schemas import LLMInput, LLMOutput

# This router will handle all the API routes.
router = APIRouter()

# Add routes to the router.
# The `add_routes` function from langserve is used to dynamically add routes
add_routes(router, mistral_chain, path="/mistral")
add_routes(router, mixtral_chain, path="/mixtral")
add_routes(router, rag_chain, path="/rag_mixtral")
add_routes(router, malaysian_mistral_chain, path="/malaysian_mistral")
add_routes(router, malaysian_rag_chain, path="/malaysian_rag")


@router.post("/mythology_semantic_search")
def sem_search(schema: LLMInput):
    response = myth_retriever.get_relevant_documents(schema.query)
    return response


@router.post("/malaysian_semantic_search")
def malaysian_sem_search(schema: LLMInput):
    response = malaysian_retriever.get_relevant_documents(schema.query)
    return response


@router.post("/mistral-api", response_model=LLMOutput)
def mistral_api(schema: LLMInput, request: Request):
    return mistral_chain.invoke(schema.query)


@router.post("/mixtral-api", response_model=LLMOutput)
def mixtral_api(schema: LLMInput, request: Request):
    return mixtral_chain.invoke(schema.query)


@router.post("/malaysian_mistral-api", response_model=LLMOutput)
def malaysian_mistral(schema: LLMInput, request: Request):
    return malaysian_mistral_chain.invoke(schema.query)


@router.post("/rag_mixtral-api")
def rag_mixtral_api(schema: LLMInput, request: Request):
    return rag_chain.invoke(schema.query)


@router.post("/malaysian_rag-api")
def malaysian_rag_api(schema: LLMInput, request: Request):
    return malaysian_rag_chain.invoke(schema.query)
