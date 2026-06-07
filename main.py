from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage

loader = PyPDFLoader("./story.pdf")

docs = loader.load()

load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings ,ChatGoogleGenerativeAI

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001") #y model text embedding generate kerta hai

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index('py-index')
vector_store = PineconeVectorStore(embedding=embeddings, index=index) #yaha hamne vector store kiya

@tool
def getContext(query:str):
  """Use this tool get more information for fulfiling the user demand 
  Provide the query parameter for what you are looking for."""
  result = vector_store.similarity_search(query=query,k=2)
  return  str(result)



model = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

agent = create_agent(model=model,tools=[getContext])

response = agent.invoke({
  'messages':[HumanMessage("What was the first chapter of the Harsh's story ? and summarise it")]
})


print(response["messages"][-1].text)

# print(vector_store.add_texts(["ring"])) #jaha vector store uski id return kerta hai

# print(vector_store.add_documents(documents=docs)) #pdf store vector form me

# results = vector_store.similarity_search( #specific world data deti query search
#     query="Interview Preparation",
#     k=1
# )

# print(results)