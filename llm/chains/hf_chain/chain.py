import os

from langchain.callbacks import MlflowCallbackHandler
from langchain.chains import LLMChain, RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser

from llm.chains.hf_chain.config import mistral_config, mixtral_config
from llm.chains.hf_chain.ingest import COLLECTION_NAME, VECTORSTORE_PATH
from llm.chains.hf_chain.prompts import rag_template, template
from llm.factory import LLMFactory, LLMType
from llm.schemas import Question

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

EMBEDDING_MODEL= "BAAI/bge-base-en-v1.5"


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


mistral_llm_model = LLMFactory().create_factory(LLMType.HUGGINGFACE_API, mistral_config)
mixtral_llm_model = LLMFactory().create_factory(LLMType.HUGGINGFACE_API, mixtral_config)

prompt = ChatPromptTemplate.from_template(template)
rag_prompt = ChatPromptTemplate.from_template(rag_template)

mistral_mlflow_callback = MlflowCallbackHandler(name="mistral", experiment="mistral", tracking_uri=MLFLOW_TRACKING_URI)
mixtral_mlflow_callback = MlflowCallbackHandler(name="mixtral", experiment="mixtral", tracking_uri=MLFLOW_TRACKING_URI)


mistral_chain = LLMChain(
    llm=mistral_llm_model,
    prompt=prompt,
    output_parser=StrOutputParser(),
    callbacks=[mistral_mlflow_callback],
)

mixtral_chain = LLMChain(
    llm=mixtral_llm_model,
    prompt=prompt,
    output_parser=StrOutputParser(),
    callbacks=[mixtral_mlflow_callback],
)


mistral_chain = mistral_chain.with_types(input_type=Question)
mixtral_chain = mixtral_chain.with_types(input_type=Question)


# u can put any llm model here
rag_chain = RetrievalQA.from_chain_type(
    llm=mixtral_llm_model,
    retriever=retriever,
    chain_type='stuff',
    return_source_documents=True,  # return the source documents if you want to. you can change it
    callbacks=[MlflowCallbackHandler(name="rag", experiment="rag", tracking_uri=MLFLOW_TRACKING_URI)],
    chain_type_kwargs={'prompt': rag_prompt}
).with_types(input_type=Question)
