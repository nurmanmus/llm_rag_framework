import os

from langchain.callbacks import MlflowCallbackHandler
from langchain.chains import LLMChain, RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser

from llm.chains.mesolitica.ingest import COLLECTION_NAME, VECTORSTORE_PATH
from llm.chains.mesolitica.prompts import rag_template, template
from llm.factory import LLMFactory, LLMType
from llm.schemas import HuggingFaceEndpointConfig, Question

HUGGINGFACEHUB_API_TOKEN = "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"

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EMBEDDING_MODEL = "mesolitica/mistral-embedding-191m-8k-contrastive"


# RAG IMPLEMENTATION - VectorDB putting the documents in the vectorDB
embeddings_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs={"device": "cpu"}, encode_kwargs={"normalize_embeddings": True})

# Add to vectorDB
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,  # Name of the collection you can change it
    embedding_function=embeddings_model,
    persist_directory=VECTORSTORE_PATH,  # Path to save the vectorstore
)

# you can import this retriever from anywhere and do semantic search
retriever = vectorstore.as_retriever()

hf_endpoint_config = HuggingFaceEndpointConfig(
    endpoint_url=os.getenv("HF_ENDPOINT_URL", ""),
    task="text-generation",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)


# make sure env variable HF_ENDPOINT_URL is set
mistral_llm_model = LLMFactory().create_factory(LLMType.HUGGINGFACE_ENDPOINT, hf_endpoint_config)

prompt = ChatPromptTemplate.from_template(template)
rag_prompt = ChatPromptTemplate.from_template(rag_template)

mistral_mlflow_callback = MlflowCallbackHandler(name="malaysian_mistral", experiment='malaysian_mistral', tracking_uri=MLFLOW_TRACKING_URI)

malaysian_mistral_chain = LLMChain(
    llm=mistral_llm_model,
    prompt=prompt,
    output_parser=StrOutputParser(),
    callbacks=[mistral_mlflow_callback],
)

malaysian_mistral_chain = malaysian_mistral_chain.with_types(input_type=Question)


# u can put any llm model here
malaysian_rag_chain = RetrievalQA.from_chain_type(
    llm=mistral_llm_model,  # malaysian mistral model that we created above
    retriever=retriever,
    chain_type='stuff',
    return_source_documents=True,  # return the source documents if you want to. you can change it
    callbacks=[MlflowCallbackHandler(name="rag_malaysian", experiment="rag_malaysian", tracking_uri=MLFLOW_TRACKING_URI)],
    chain_type_kwargs={'prompt': rag_prompt}
).with_types(input_type=Question)
