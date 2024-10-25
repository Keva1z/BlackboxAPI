import sys
sys.path.append('..')  # Add parent directory to module search path

from blackboxapi.client import AIClient
from blackboxapi.models import CLAUDE
from blackboxapi.agent import *
from colorama import init, Fore, Style

# Initialize colorama
init()

def print_colored(text, color):
    print(color + text + Style.RESET_ALL)

def main():
    client = AIClient(use_chat_history=True)
    
    # Set default model to Claude
    model = CLAUDE
    agent = None

    print_colored("Welcome to the Blackbox AI console interface!", Fore.YELLOW)
    print_colored(f"Default model: {model.name}", Fore.YELLOW)
    print_colored("Default agent: None", Fore.YELLOW)
    print_colored("Available commands:", Fore.YELLOW)
    print_colored("  /model <model_name> - change model (available: GPT4, CLAUDE, GEMINI, BLACKBOX)", Fore.YELLOW)
    print_colored("  /agent <agent_name> - change agent (available: CAN_CODER, RELATIONSHIP_COACH, MENTAL_ADVISOR, ALGORITHM_EXPLAINER, PROMPT_GENERATOR, None)", Fore.YELLOW)
    print_colored("  /clear - clear chat history", Fore.YELLOW)
    print_colored("  /exit - exit the program", Fore.YELLOW)
    print_colored("Enter your request or command:", Fore.YELLOW)

    while True:
        user_input = input(Fore.GREEN + ">> " + Style.RESET_ALL).strip()

        if user_input.lower() == "/exit":
            print_colored("Goodbye!", Fore.YELLOW)
            break

        elif user_input.lower() == "/clear":
            client.clear_chat_history(agent)
            print_colored("Chat history cleared.", Fore.YELLOW)

        elif user_input.lower().startswith("/model "):
            model_name = user_input.split(" ", 1)[1].upper()
            if model_name in ["GPT4", "CLAUDE", "GEMINI", "BLACKBOX"]:
                model = globals()[model_name]
                print_colored(f"Model changed to {model.name}", Fore.YELLOW)
            else:
                print_colored("Invalid model name. Please choose from available models.", Fore.YELLOW)

        elif user_input.lower().startswith("/agent "):
            agent_name = user_input.split(" ", 1)[1].upper()
            if agent_name == "NONE":
                agent = None
                print_colored("Agent disabled", Fore.YELLOW)
            elif agent_name in ["CAN_CODER", "RELATIONSHIP_COACH", "MENTAL_ADVISOR", "ALGORITHM_EXPLAINER", "PROMPT_GENERATOR"]:
                if agent_name == "PROMPT_GENERATOR":
                    agent = PROMPT_GENERATOR
                else:
                    agent = globals()[f"RU_{agent_name}"]
                print_colored(f"Agent changed to {agent.name}", Fore.YELLOW)
            else:
                print_colored("Invalid agent name. Please choose from available agents or None.", Fore.YELLOW)

        else:
            try:
                response = client.completions.create(user_input, agent=agent, model=model)
                print_colored("Assistant:", Fore.CYAN)
                print_colored(response, Fore.CYAN)
            except Exception as e:
                print_colored(f"An error occurred: {str(e)}", Fore.RED)

if __name__ == "__main__":
    main()
