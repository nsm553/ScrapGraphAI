from langchain_community.document_loaders import DirectoryLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import ollama
from langchain_community.vectorstores import Chroma

# load documents
loader = DirectoryLoader('./docs', glob="**/*.md", loader_cls=UnstructuredWordDocumentLoader)
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# Initialize llama 3.2
llm = ollama(model="llama3.2", base_url="http://localhost:11434")

#  search and respond
query = "What is the purpose of diffusion in LLM"
similar_docs = vectorstore.similarity_search(query)
context = "\n".join([doc.page_content for doc in similar_docs])
resp = llm(f"Context: {context}\nQuestion: {query}\nAnswer: ")
print(resp)
