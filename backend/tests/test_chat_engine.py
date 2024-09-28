import sys
import os
import csv
import json

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend import chat_engine, config

config.set_env_variables()

questions = [
    "What beer styles are typical to Malopolska?",
    "What are the historical roots of Wit Bier?",
    "Was there already hopped beer in Belgium in the 11th century?",
    "When did hop get introduced in the UK?",
    "Are there conflicting views on the role of beer and ale to replace polluted water?",
    "Can you give examples of ales that are top fermented but don't have refermentation on the bottle? Include brewery.",
    "What are the key ingredients used in brewing beer, and how do they affect the flavor?",
    "Can you explain the difference between ales and lagers in terms of fermentation?",
    "What is the significance of the IBU (International Bitterness Units) in beer?",
    "How does the water chemistry in this region influence the beers produced here?",
    "What are some historical brewing methods that are still used today?",
    "Can you recommend a beer that pairs well with spicy food?",
    "What is the role of hops in beer, and how do different varieties impact the taste?",
    "Are there any local breweries you would recommend that focus on traditional brewing techniques?",
    "What is the process of barrel aging, and how does it affect the final product?",
    "Can you suggest a beer that showcases unique yeast characteristics?",
    "What are the main ingredients used in brewing beer?",
    "Can you explain the difference between ales and lagers?",
    "How does the fermentation process affect the flavor of the beer?",
    "What types of hops do you use in your beers, and how do they impact the taste?",
    "What is the history behind the brewing traditions in this region?",
    "How do different yeast strains influence the characteristics of beer?",
    "What are some common off-flavors in beer, and what causes them?",
    "Can you tell me about any seasonal or limited-edition brews you have available?",
    "What beer styles do you think are currently trending?",
    "How do you determine the optimal serving temperature for different types of beer?",
    "What is the process of dry hopping, and how does it affect aroma?",
    "Can you suggest a beer that has a strong malt profile?",
    "What role does water chemistry play in the brewing process?",
    "How do you recommend tasting beer to fully appreciate its flavors?",
    "What are some classic beer styles that every enthusiast should try?",
    "Can you explain the difference between bottle conditioning and keg conditioning?",
    "What are some unique or unusual ingredients you've seen used in craft beers?",
    "How do you think the craft beer movement has changed the beer landscape?",
    "What are the main ingredients in beer, and how do they affect flavor?",
    "What is the significance of the beer's ABV (alcohol by volume)?",
    "How does the brewing process influence the final taste of the beer?",
    "What are the most common beer styles, and how do they differ?",
    "Can you recommend a good beer for someone who usually drinks light lagers?",
    "What is the role of hops in beer, and how do different varieties impact flavor?",
    "How does the fermentation temperature affect the beer's profile?",
    "What are some historical styles of beer that are less common today?",
    "Can you explain what 'IBU' means and why it's important?",
    "What is the difference between a stout and a porter?",
    "How do you properly taste and evaluate a beer?",
    "What are some food pairings you recommend for this beer?",
    "Can you tell me about the origin of this brewery?",
    "What is the difference between bottle conditioning and keg conditioning?",
    "What are some local breweries you would recommend?",
    "How do different yeast strains affect the flavor and aroma of beer?",
    "What is the history behind the beer styles popular in this region?",
    "How do you determine the freshness of a beer?",
    "What is the process of dry hopping, and how does it affect the beer?",
    "Can you recommend a sour beer for someone new to the style?",
    "What are some common off-flavors in beer and their causes?",
    "How does aging beer in barrels change its characteristics?",
    "What is a 'session beer,' and what makes it different?",
    "Can you explain the significance of the beer's color?",
    "What are some unique or experimental beers you have on tap?",
    "How do you clean and maintain the draft system to ensure quality?",
    "What is the difference between a craft beer and a mass-produced beer?",
    "Can you recommend a beer that showcases local ingredients?",
    "What is the role of carbonation in beer, and how is it achieved?",
    "What are some classic beer styles from Belgium?",
    "How does the water profile affect the brewing process?",
    "What are some seasonal beers that you have available?",
    "Can you explain the term 'beer flight' and how it works?",
    "What is the importance of the beer's aroma in the tasting experience?",
    "What are some common myths about beer that you'd like to debunk?",
    "How do you select the beers that you have on tap?",
    "What is the difference between a lager and a pilsner?",
    "Can you recommend a beer that has a strong malt profile?",
    "What are the trends in the craft beer industry right now?",
    "How does the brewing process differ between commercial and home brewing?",
    "What is the significance of the beer's head and how should it look?",
    "Can you tell me about any beer festivals or events happening soon?",
    "What are some popular beer cocktails or mixed drinks?",
    "How do you store beer properly to maintain its quality?",
    "What are some of the most unusual ingredients you've seen in beer?",
    "Can you explain the difference between a wheat beer and a hefeweizen?",
    "What is the history of the beer style known as IPA?",
    "How do you feel about beer trends like non-alcoholic and low-calorie options?",
    "What is your personal favorite beer, and why do you like it?"
]

chat_history = {
    "1": {
        "user": "Hi",
        "assistant": "Hello."
    }
}

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.4,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def generate_questions(number_of_questions):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a beer and ale enthousiast asking questions."),
        HumanMessagePromptTemplate.from_template("""
        Return {number_of_questions} questions that a beer enthousiast would ask a bartender about beer. This can be related to the chemistry and history of the beer. But also about specific recommendations.
        Combine common questions from pub drinkers with hobbyists. 
        Provide the output as a JSON with "question01" to "question{number_of_questions}" as the keys and the questions as the values. No preamble or explanation.
        """)
    ])
    chain = prompt | llm | JsonOutputParser()
    
    questions_dict = chain.invoke({"number_of_questions": number_of_questions})
    
    questions = list(questions_dict.values())

    return questions


def rag_compare_original_with_rephrased_question(questions):
    # List to store the final combined data
    combined_results = [["Original_question", "Rephrased_quesiton", "source", "page_content", "Original_score", "Rephrased_score"]]
    
    for question in questions:
        # Step 1: Retrieve and grade for rephrased question
        rephrased_question = chat_engine.rephrase_question_with_chat_history(question, chat_history)
        rephrased_curated_documents = chat_engine.tool_retrieve_book_knowledge(rephrased_question)
        rephrased_curated_documents_graded = chat_engine.grade_documents(rephrased_curated_documents, rephrased_question)
        
        # Step 2: Retrieve and grade for original question
        original_curated_documents = chat_engine.tool_retrieve_book_knowledge(question)
        original_curated_documents_graded = chat_engine.grade_documents(original_curated_documents, question)
        
        for doc in original_curated_documents_graded:
            combined_results.append([question, 
                                     rephrased_question,
                                     doc[0].metadata['source'], 
                                     doc[0].page_content, 
                                     int(doc[1]['score']), 
                                     -1])

        for doc in rephrased_curated_documents_graded:
            found = False
            for c_r in combined_results[1:]:
                if question == c_r[0]:
                    if doc[0].metadata['source'] == c_r[2]:
                        if doc[0].page_content == c_r[3]:
                            c_r[5] = int(doc[1]['score'])
                            # c_r[1] = rephrased_question
                            found = True
                            break
            if not found:
                combined_results.append([question, 
                            rephrased_question,
                            doc[0].metadata['source'], 
                            doc[0].page_content, 
                            -1, 
                            int(doc[1]['score'])])
    
    with open('test_chat_engine_rag_compare_original_with_rephrased_question_03.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(combined_results)
    return combined_results  

def question_answer_evaluation(questions):
    question_answer = [["question", "answer", "grade"]]
    for index, question in enumerate(questions):
        print(index)
        answer = chat_engine.front_end_integration(question, chat_history, question_style="original")
        question_answer.append([question, answer['answer'], answer['grade']])
    
    with open('test_question_answer_evaluation_original_01.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(question_answer)
    return question_answer

if __name__ == '__main__':
    # questions = generate_questions(90)

    question_answer_evaluation(questions[20:])

    # combined_results= rag_compare_original_with_rephrased_question(questions)

