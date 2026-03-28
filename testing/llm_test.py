from llm_models.groq_client import GroqClient
from llm_models.prompt_builder import PromptBuilder
from llm_models.config import LLMConfig

def run_test():
    query = "Who is in HR? and what is his age of priya singh?"
    context_docs = [
        "_id: 2 | name: Neha Verma | department: HR | email: neha@company.com | salary: 60000 | description: Manages recruitment and employee engagement.", 
        
        "_id: 4 | name: Priya Singh | department: Engineering | email: priya@company.com | salary: 70000 | age : 28 | description: Software Engineer."
    ]

    config = LLMConfig(
        temperature=0.1,   # easy to tweak
        max_tokens=300
    )

    prompt_builder = PromptBuilder()
    groq_client = GroqClient(config)

    prompt = prompt_builder.build(query, context_docs)

    print("\n🧠 Prompt:\n", prompt)

    response = groq_client.generate(prompt)

    print("\n🤖 Response:\n", response)


if __name__ == "__main__":
    run_test()