from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
import config
from config import set_env_variables

def response_check(response):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", convert_system_message_to_human=True)
    result = llm(
        [
            SystemMessage(content="You are a helpful assistant that evaluates responses to users. Are there logical mistakes (Yes or No)? Are there chronological mistakes (Yes or No)? Answer only with: Logical_mistakes: Yes/No; Chronological_mistakes: Yes/No."),
            HumanMessage(content=response),
        ]
    )
    # result = llm.invoke("Write a ballad about LangChain")
    return str(result.content)


if __name__ == '__main__':
    set_env_variables()
    response = "Yes, hopped beer was present in Belgium by the 11th century. Hops were introduced to Flanders through imported beer from Hamburg and Amsterdam, and local brewers began using hops by the 14th century. The use of hops in brewing became more widespread, leading to the development of various beer styles, including those that would eventually influence Witbier. "
    response = response_check(response=response)
    print(response)
