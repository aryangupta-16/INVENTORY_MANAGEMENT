# tests/test_validator_agent.py
from app.agents.validator_agent import CommandValidatorAgent

def test_validator_agent():
    """
    Test CommandValidatorAgent LLM structured output for missing parameters
    """
    print("Starting Validator Agent Test...")
    
    agent = CommandValidatorAgent()
    
    # Example: user wants to record a payment, but customer name is missing
    action = "record_payment"
    target_agent = "finance"
    user_input = "John Doe paid 200$"
    
    # Run the validator agent
    output = agent.validate(action, target_agent, user_input)
    
    print("Validator Agent Output:", output)

if __name__ == "__main__":
    test_validator_agent()