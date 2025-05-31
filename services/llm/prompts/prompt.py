import os


def get_llm_prompt(question: str) -> str:
    """
    Generates a prompt for the LLMs to answer a question
    :param question: The question to be answered
    :return: prompt
    """

    # Load prompt template once at startup
    with open("services/llm/prompts/prompt_template.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = prompt_template.replace("{user_input}", question)
    return prompt
