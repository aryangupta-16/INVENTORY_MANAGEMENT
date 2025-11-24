# tests/test_llm_agents.py
# import pytest
from app.agents.command_output import CommandInterpreterAgent
# from app.llm.ollama_llm import llm  # your LLM definition file

def test_command_interpreter_llm():
    """
    Test CommandInterpreterAgent LLM structured output
    """
    
    print("starttt")
    agent = CommandInterpreterAgent()
    
    user_input = "how are you?"
    print("startingg agentt")
    output = agent.parse(user_input)
    
    
    print("LLM Output:", output)
    
if __name__ == "__main__":
    test_command_interpreter_llm()