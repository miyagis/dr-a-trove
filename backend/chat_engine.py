from langchain_chroma import Chroma
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import Document, SystemMessage, HumanMessage, AIMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List
from config import set_env_variables, logging_setup
from typing import List, Dict

import untappd

import sys
from inspect import getmembers, isfunction, getdoc

chat_history = {}
logger = logging_setup()
set_env_variables()
web_search_tool = TavilySearchResults(max_results=2)

# TODO: Return answer{"to_user": "", "sources": ["source1": "", "source2": ""]}
# TODO
# TODO
# TODO

# chat_history = {
#     "1": {
#         "user": "What Eastern European wheat beers are there?",
#         "assistant": "Wheat beers aren't typical Eastern European styles. However, German and Czech wheat beers have become more popular in Eastern Europe."
#     }
# } # for test purpose
chat_history = {
    "1": {
        "user": "Hi",
        "assistant": "Hello."
    }
}

vector_db = Chroma(persist_directory="backend\\chroma_db", embedding_function=OpenAIEmbeddings())

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.4,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def translate(question):
    # prompt = ChatPromptTemplate.from_messages([
    #     SystemMessagePromptTemplate.from_template("You are a language and websearch expert."),
    #     HumanMessagePromptTemplate.from_template("""
    #     Which languages (max 2) could this question be translated in to get better websearch results:
    #     Question: {question}
    #     Provide a JSON with zero or more keys of the language in string and the translation as the value. 
    #                                              No premable or explanation. For example:
    #                                              {example}

    #     """)
    # ])
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a language and websearch expert."),
        HumanMessagePromptTemplate.from_template("""
        Which languages (up to 3) could this question be translated into to significantly improve web search results:
        Question: {question}
        
        Only select a language if you are confident that searching in that language will provide better or more relevant results. If no translation is likely to improve results, return an empty JSON. 
        Provide the output as a JSON with zero or more keys of the language in string and the translation as the value. No preamble or explanation. For example:
                                                 {example}

        """)
    ])
    chain = prompt | llm | JsonOutputParser()
    
    example = """
        "Dutch": "Hoe gaat het?",
        "English": "How are you?"
    """
    translations = chain.invoke({"question": question, "example": example})
    logger.info(translations)
    # languages = ", ".join(translations.keys())
    # logger.info(f"translations (number): {len(translations)}: {languages}")
    return translations

def web_search(question, rephrased_questions_translated):
    """
    Web search based on the re-phrased question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with appended web results
    """
    documents = []
    web_results = web_search_tool.invoke({"query": question})
    documents.extend(
        [
            Document(page_content=d["content"], metadata={"url": d["url"]})
            for d in web_results
        ]
    )

    for language in rephrased_questions_translated:
        web_results = web_search_tool.invoke({"query": rephrased_questions_translated[language]})
        documents.extend(
            [
                Document(page_content=d["content"], metadata={"url": d["url"]})
                for d in web_results
            ]
        )
    return documents

def rephrase_question_with_chat_history(question: str, chat_history: Dict[str, Dict[str, str]]) -> str:
    # Construct the conversation history as messages
    # messages = [
    #     SystemMessage(content="""
    #         You are a question re-writer that converts an input question to a better version optimized for vectorstore retrieval.
    #         Your goal is to focus on the current question and ensure that it is clear, concise, and semantically rich for retrieval, without altering its original intent.
    #         The chat history is provided only for minimal context and should not overly influence the rephrasing.
    #         """)
    # ]
    messages = [
        SystemMessage(content="""
            You are a question re-writer that converts an input question to a better version optimized for vectorstore retrieval.
            Focus on the core intent of the question and ignore previous answers unless directly relevant to understanding the question.
            """)
    ]
    for key, value in chat_history.items():
        if key == 'user':
            messages.append(HumanMessage(content=value))
        if key == 'assistant':  
            messages.append(AIMessage(content=value))
    
    # Add the current question as the final message
    messages.append(HumanMessage(content=question))
    
    # Run the chat model with the structured messages
    response = llm.invoke(messages)
    rephrased_question = response.content.strip()
    logger.info(f"rephrased_question: {rephrased_question}")
    return rephrased_question

def retrieve_with_chat_history(rephrased_question: str, k: int = 5) -> List[Document]: # is chat history included here?
    documents = vector_db.similarity_search(query=rephrased_question, k=k)
    logger.info(f"documents (number): {len(documents)}")
    return documents

def grade_documents(documents: List[Document], question: str) -> List[Document]:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are an expert in document relevance."),
        HumanMessagePromptTemplate.from_template("""
        Grade the relevance of the following document with respect to the question:
        Question: {question}
        Document: {document}
        Provide a grade between 1 (low relevance) and 10 (high relevance) as a JSON with a single key 'score' 
                                                 and no premable or explanation.
        """)
    ])
    # chain = LLMChain(llm=llm, prompt=prompt)
    chain = prompt | llm | JsonOutputParser()
    
    graded_documents = []
    for doc in documents:
        grade = chain.invoke({"question": question, "document": doc.page_content})
        if "source" in doc.metadata:
            logger.info(f"grade: {grade}; source: {doc.metadata['source']}; doc.page_content: {doc.page_content}")
        elif "url" in doc.metadata:
            logger.info(f"grade: {grade}; url: {doc.metadata['url']}; doc.page_content: {doc.page_content}")
        else:
            logger.error("Unknown document structure")

        if int(grade['score']) > 5:
            graded_documents.append(doc)
        # else:
        #     logger.info(f"doc.page_content: low score: {doc.page_content}")
    
    return graded_documents

def generate_answer(documents: List[Document], question: str, chat_history: Dict[str, str], max_response_size_in_sentences: int = 5) -> str:
    history_str = "\n".join([f"User: {entry['user']}\nAssistant: {entry['assistant']}" for entry in chat_history.values()])
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant for question-answering tasks related to beers and ales. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Keep the answer extremely concise"),
        HumanMessagePromptTemplate.from_template("""
        Based on the following documents and conversation history, generate a CONCISE answer to the question:
        Question: {question}
        Documents: {documents}
        History: {history_str}
        Limit the response to {max_response_size} sentences.
        """)
    ])
    chain = prompt | llm
    documents_content = " ".join([doc.page_content for doc in documents]) # TODO this is just combining all sources so we don't know what source exactly was used
    answer = chain.invoke({"question": question, "documents": documents_content, "history_str": history_str, "max_response_size": max_response_size_in_sentences})
    answer= answer.content.strip()

    complete_answer = {
        "answer": answer,
        "sources": {}
    }
    for document in documents:
        if "source" in document.metadata:
            complete_answer["sources"][document.metadata['source']] = document.page_content
        elif "url" in document.metadata:
            complete_answer["sources"][document.metadata['url']] = document.page_content
        else:
            logger.error("Unknown document structure")

    logger.info("complete_answer: %s", complete_answer)
    return complete_answer

def grade_answer(question: str, answer: str) -> int:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are an expert grader."),
        HumanMessagePromptTemplate.from_template("""
        Grade the following answer based on how well it addresses the question:
        Question: {question}
        Answer: {answer}
        Provide a grade between 1 (poor) and 10 (excellent) as a JSON with a single key 'score' 
                                                 and no premable or explanation.
        """)
    ])
    chain = prompt | llm | JsonOutputParser()
    grade = chain.invoke({"question": question, "answer": answer})
    grade = grade['score']
    logger.info(f"answer grade: {grade}")
    return grade

def get_current_module_functions():
    # Get the current module using sys
    current_module = sys.modules[__name__]
    
    functions = {}
    for name, obj in getmembers(current_module, isfunction):
        docstring = getdoc(obj)
        functions[name] = docstring
    
    return functions

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

def determine_tool_order(tools_dict: dict, task_description: str) -> List[str]:
    # Format the dictionary into a readable string
    formatted_tools = "\n".join([f"{key}: {value}" for key, value in tools_dict.items()])

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are an expert in task planning and tool selection."),
        HumanMessagePromptTemplate.from_template(f"""
        You are given a set of tools that may be used to complete a task. 
        Your task is to select ONLY the relevant tools and arrange them in the correct execution order.
        
        Task Description: {{task_description}}
        Available Tools: 
        {formatted_tools}
        
        Please provide the correct order of the tools as a JSON array with the key 'ordered_tools'. 
        If a tool is not needed, do not include it in the list. 
        The JSON should contain only the ordered list and no additional text or explanation.
        """)
    ])

    # chain = LLMChain(llm=llm, prompt=prompt)
    chain = prompt | llm | JsonOutputParser()
    
    response = chain.invoke({"task_description": task_description})
    logger.info(f"Ordered Tools: {response}")
    
    return response['ordered_tools']

def tool_retrieve_book_knowledge(rephrased_question):
    """
    This function searches in books and returns highly trusted information but is limited for very recent issues.
    """
    retrieved_documents = retrieve_with_chat_history(rephrased_question)
    return retrieved_documents

def tool_web_search(rephrased_question):
    """
    This function searches the web to resolve questions on recent topics that are unlikely to be found in books.
    """
    rephrased_questions_translated = translate(rephrased_question)
    web_results = web_search(rephrased_question, rephrased_questions_translated)
    return web_results

def tool_get_local_beer(location):
    """
    This function searches the specialized websites for top breweries and beers to provide drinking suggestions.
    """
    breweries_response = untappd.get_breweries(search_query=location, search_type="brewery", search_sort="distance")
    beers = []
    return beers


def front_end_integration(question: str, chat_history: dict):
    logger.info(f"Input: {question}")
    max_response_size_in_sentences = 3
    functions = get_current_module_functions()
    tool_functions = {key: value for key, value in functions.items() if key.startswith("tool")}

    if len(chat_history) > 0:
        rephrased_question = rephrase_question_with_chat_history(question, chat_history)
    else:
        rephrased_question = question
    
    counter = 0
    answer_grade = -1
    task_description = f"Respond to this user input: {rephrased_question}"
    selection_of_tools = determine_tool_order(tool_functions, task_description)
    while answer_grade <= 5 or counter >=3:
        documents_to_answer_question = []
        for selected_tool in selection_of_tools: 
            if selected_tool == 'tool_web_search':
                print("dr. A. Trove: Searching the web...")
                web_documents = tool_web_search(rephrased_question)
                web_documents_graded = grade_documents(web_documents, rephrased_question)
                # TODO get more info from the website
                documents_to_answer_question.extend(web_documents_graded)
            elif selected_tool == 'tool_retrieve_book_knowledge':
                curated_documents = tool_retrieve_book_knowledge(rephrased_question)
                curated_documents_graded = grade_documents(curated_documents, rephrased_question)
                documents_to_answer_question.extend(curated_documents_graded)
            else:
                logger.error(f"Unknown tool selected: {selected_tool}")

        answer = generate_answer(documents_to_answer_question, rephrased_question,chat_history, max_response_size_in_sentences)
        if answer['answer'] != "I don't know.":
            answer_grade = grade_answer(question, answer['answer'])
        else:
            answer_grade = 11
        counter+=1

    return answer

def mini_main():
    logger.info(f"==========START========")
    chat_counter = 2
    while True:
        question = input("You: ")
        answer = front_end_integration(question, chat_history)
        print("dr. A. Trove: " + str(answer['answer']))
        chat_history[str(chat_counter)] = {"user": question, "assistant": answer['answer']}
        chat_counter+=1

if __name__ == '__main__':
    tool_get_local_beer('Aalst')
    mini_main()