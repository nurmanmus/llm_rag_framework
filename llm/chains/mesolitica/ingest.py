import os
import shutil
from argparse import ArgumentParser

from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

load_dotenv()


CHUNK_SIZE = 400  # you can increase token size in HuggingFaceEndpoint settings in HuggingFace then you can increase chunk size
CHUNK_OVERLAP = 30

# IMPORTANT make sure paths are correct
EMBEDDING_MODEL = "mesolitica/mistral-embedding-191m-8k-contrastive"

DATA_PATH = "llm/chains/mesolitica/data"
VECTORSTORE_PATH = "llm/chains/mesolitica/vectorstore"
COLLECTION_NAME = "malaysian"
PROCESSED_PATH = "llm/chains/mesolitica/processed"
loaded_files = set()
embeddings_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs={"device": "cpu"}, encode_kwargs={"normalize_embeddings": True})


vectorstore = Chroma(
    collection_name=COLLECTION_NAME,  # Name of the collection you can change it
    embedding_function=embeddings_model,
    persist_directory=VECTORSTORE_PATH,  # Path to save the vectorstore
)

# Ensure processed directory exists
if not os.path.exists(PROCESSED_PATH):
    os.makedirs(PROCESSED_PATH)

def move_to_processed(file_path):
    dest_path = os.path.join(PROCESSED_PATH, os.path.basename(file_path))
    try:
        shutil.move(file_path, dest_path)
    except FileNotFoundError:
        print(f"File {file_path} not found but thats ok it already moved to processed")


def delete_file_from_vectorstore(source_doc, chroma_instance):
    try:
        ids = chroma_instance.get(where = {'source': source_doc})['ids']
        chroma_instance.delete(ids = ids)
        print(f"Deleted {source_doc} from vectorstore")

    except Exception as e:
        print(f"Error deleting {source_doc} from vectorstore: {e}")


def ingest():
    global loaded_files
    # RAG IMPLEMENTATION - VectorDB putting the documents in the vectorDB
    # pdf loader
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    for doc in documents:
        filename = doc.metadata['source'].split('/')[-1]
         # if filename in processed folder selede old one from vectorstore
        if os.path.exists(os.path.join(PROCESSED_PATH, filename)):
            delete_file_from_vectorstore(filename, vectorstore)
        loaded_files.add(doc.metadata.get('source'))
        doc.metadata['source'] = filename

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)
    # txt loader
    loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    for doc in documents:
        doc.metadata['page'] = 1
        filename = doc.metadata['source'].split('/')[-1]
        # if filename in processed folder selede old one from vectorstore
        if os.path.exists(os.path.join(PROCESSED_PATH, filename)):
            delete_file_from_vectorstore(filename, vectorstore)
        loaded_files.add(doc.metadata.get('source'))
        doc.metadata['source'] = filename

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    texts += text_splitter.split_documents(documents)
    # IMPORTANT: This is a destructive operation. It will remove the existing vectorstore.
    if len(texts):
        print(f"Loaded {len(texts)} splits")
        # Add documents to vectorstore
        Chroma.from_documents(
            documents=texts,
            collection_name=COLLECTION_NAME,  # Name of the collection you can change it
            embedding=embeddings_model,
            persist_directory=VECTORSTORE_PATH,  # Path to save the vectorstore
        )
    else:
        print("No documents found to ingest in data directory")



if __name__ == "__main__":

    parser = ArgumentParser()
    # --delete filename to delete from vectorstore 
    parser.add_argument("--delete", help="delete file from vectorstore")
    # reset chroma db 
    parser.add_argument("--reset", help="reset chroma db", action="store_true")
    args = parser.parse_args()
    if args.delete:
        delete_file_from_vectorstore(args.delete, vectorstore)
        shutil.move(os.path.join(PROCESSED_PATH, args.delete), os.path.join(DATA_PATH, args.delete))
    elif args.reset:
        # delete vectorestore path and move processed files to data
        shutil.rmtree(VECTORSTORE_PATH)
        # move all processed files to data move just the files
        for file in os.listdir(PROCESSED_PATH):
            shutil.move(os.path.join(PROCESSED_PATH, file), os.path.join(DATA_PATH, file))
        print("Reset vectorstore and moved processed files to data")

    else:
        ingest()
        for file in loaded_files:
            move_to_processed(file)
        print("Ingested and moved to processed")

