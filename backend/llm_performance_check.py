# https://blog.langchain.dev/evaluating-rag-pipelines-with-ragas-langsmith/
# https://docs.ragas.io/en/stable/getstarted/index.html#get-started

# check: performance of original question vs rephrased question
#  - Perform RAG
#  - Grade returned fragments (context_relevancy and context_recall)
#  - Rate final generated answer (faithfulness and answer_relevancy)


from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# generator with openai models
generator_llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
critic_llm = ChatOpenAI(model="gpt-4")
embeddings = OpenAIEmbeddings()

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings
)

# generate testset
testset = generator.generate_with_langchain_docs(documents, test_size=10, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25})