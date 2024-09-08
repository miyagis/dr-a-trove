import bs4
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredEPubLoader
import os
import nltk
from nltk.data import find
from nltk import download
from config import set_env_variables

def ensure_resource(resource_name):
    try:
        find(f'taggers/{resource_name}')
    except LookupError:
        download(resource_name)

def create_vectorstore():
    print("START create_vectorstore")
    set_env_variables()
    # Load, chunk and index the contents of the blog to create a retriever.
    data_directory = "data"
    all_docs = []

    for filename in os.listdir(data_directory):
        print(str(filename))
        if filename.endswith(".epub"):
            file_path = os.path.join(data_directory, filename)
            
            loader = UnstructuredEPubLoader(file_path)
            docs = loader.load()
            
            all_docs.extend(docs)
        else:
            print(f"File not recognized as epub: {filename}")

    web_loader = WebBaseLoader(web_paths=['https://www.hobbybrouwen.nl/artikel/koolzuur.html',
                                          'https://www.hobbybrouwen.nl/artikel/Zink_in_de_brouwketel.html',
                                          'https://brouw-bier.nl/theorie/grondstoffen/gist/gistcel.aspx', 
                                          'https://brouw-bier.nl/theorie/grondstoffen/gist/groeifasen.aspx', 
                                          'https://brouw-bier.nl/theorie/grondstoffen/gist/stofwisseling.aspx', 
                                          'https://oudbier.blogspot.com/', 
                                          'http://www.oldandinteresting.com/ale-warmers.aspx', 
                                          'https://brewingclassical.wordpress.com/timeline/', 
                                          'https://historia.org.pl/2020/02/10/piwo-w-sredniowiecznym-i-renesansowym-krakowie-gdzie-co-i-za-ile-pito/', 
                                          'https://braciatrix.com/2017/05/24/featured-content-3/', 
                                          'https://braciatrix.com/2017/10/27/nope-medieval-alewives-arent-the-archetype-for-the-modern-pop-culture-witch/#comments', 
                                          'https://onlinelibrary.wiley.com/doi/10.1002/jib.49'])
    web_docs = web_loader.load()
    all_docs.extend(web_docs)

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=180)
    splits = text_splitter.split_documents(all_docs)

    # Initialize the embedding function
    embedding = OpenAIEmbeddings()

    # Initialize the vectorstore and process in batches
    persist_directory = "./chroma_db"
    batch_size = 166  # Adjust the batch size as necessary

    # Create the initial Chroma vectorstore with the first batch
    initial_batch = splits[:batch_size]
    vectorstore = Chroma.from_documents(documents=initial_batch, embedding=embedding, persist_directory=persist_directory)

    # Process the remaining splits in smaller batches
    for i in range(batch_size, len(splits), batch_size):
        batch = splits[i:i+batch_size]
        vectorstore.add_documents(documents=batch, embedding=embedding)

    # vectorstore.persist()  # Save the vectorstore to disk

    return vectorstore

def create_retriever(recreate_vectorstore=False):
    if recreate_vectorstore:
        vectorstore = create_vectorstore()
    else:
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    return retriever


def main():
    print("sd")

if __name__ == '__main__':
    main()
