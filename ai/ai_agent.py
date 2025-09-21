# ai/ai_agent.py
import google.generativeai as genai

class CommandInterpreter:
    def __init__(self):
        # Hardcoded API key (works in exe)
        api_key = "enter-your-api-key-here"
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def interpret(self, user_input: str) -> str:
        prompt = (
            f"Interpret the following user instruction as a single, executable terminal command. "
            f"Do not include any additional text, explanations, or code blocks. Just the command.\n"
            f"Do not include symbols like ``,`$` or `>` before the command.\n"
            f"User Instruction: {user_input}\nTerminal Command:"
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Error: Could not interpret command."

# Wrapper function
_interpreter = CommandInterpreter()
def interpret_natural_command(instruction: str) -> str:
    return _interpreter.interpret(instruction)
