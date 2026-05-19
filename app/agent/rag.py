from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

PERSIST_DIR = "vector_store"
PDF_DIR = "uploads/pdfs"

embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")


def indexar_pdfs():
    documentos = []
    for arquivo in os.listdir(PDF_DIR):
        if arquivo.endswith(".pdf"):
            caminho = os.path.join(PDF_DIR, arquivo)
            loader = PyPDFLoader(caminho)
            documentos.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documentos)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    print(f"{len(chunks)} chunks indexados com sucesso!")
    return vectorstore


def consultar(pergunta, k=3):
    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )
    resultados = vectorstore.similarity_search(pergunta, k=k)
    contexto = "\n\n".join([doc.page_content for doc in resultados])
    return contexto


if __name__ == "__main__":
    indexar_pdfs()