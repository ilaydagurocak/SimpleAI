from sympy import simplify
from googletrans import Translator

class SimpleAI:
    def __init__(self):
        self.knowledge = {
            "hello": "Hello! How can I assist you today?",
            "how are you": "I'm great, thank you. What about you?",
            "what's your name": "My name is Lina.",
            "what's your mother's name": "I was created by code, so I don't have a mother. But you can think of the programmer as my creator!",
            "goodbye": "Goodbye! Have a nice day!",
            "can you solve mathematical problems": "Yes, absolutely! I can. I'm quite skilled at math.",
            "can you hear me": "Yes, I can hear you.",
            "can you help me": "Yes, how can I help you?",
            "you look great": "Thank you! Though, I don't have a physical appearance, I appreciate the sentiment.",
            "quit": "Okay, goodbye!"
        }
        self.default_response = "I'm sorry, I don't understand that."

    def get_response(self, user_input):
        user_input = user_input.lower()

        if "translate" in user_input:
            user_input = user_input.replace("translate", "").strip()
            lang, text_to_translate = user_input.split(' ', 1)
            translator = Translator()

            try:
                # Try to get a translation. If it fails, retry up to 3 times.
                for _ in range(3):
                    try:
                        translation = translator.translate(text_to_translate, dest=lang).text
                        return translation
                    except Exception as e:
                        print(f"Translation failed with error: {e}, retrying...")
                return "I'm sorry, translation failed after several attempts."
            except Exception as e:
                print(f"Translation failed with error: {e}")
                return self.default_response

        elif user_input in self.knowledge:
            return self.knowledge[user_input]

        else:
            try:
                # If the input is not in knowledge, try to evaluate it as a mathematical expression
                result = str(simplify(user_input))
                return result
            except:
                # If it can't be evaluated, return the default response
                return self.default_response
