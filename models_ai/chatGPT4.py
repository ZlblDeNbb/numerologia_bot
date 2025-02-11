import openai
from models_ai.prompts_ai import TokenAPI
import environ

env = environ.Env()
environ.Env.read_env()

class ChatGPT4Model:
    def __init__(self):
        self.api_key = env('OPENAI_TOKEN_API')  # Чтение ключа API
        self.base_url = env('BASE_OPENAI_URL')
        self.max_input_tokens = TokenAPI.INPUTSTOKENS # Максимум токенов для входного сообщения
        self.max_response_tokens = TokenAPI.OUTPUTSTOKENS  # Максимум токенов для ответа

    def count_tokens(self, messages):
        tokens = sum(len(message["content"].split()) for message in messages)
        return tokens

    def get_response(self, message, prompt):
        messages = [
            {"role": "system", "content": f"{prompt}"},
            {"role": "user", "content": message}
        ]

        total_tokens = self.count_tokens(messages)
        if total_tokens > self.max_input_tokens:
            return "Ваш вопрос слишком длинный. Пожалуйста, сократите его."

        client = openai.Client(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=self.max_response_tokens,
        )

        return response.choices[0].message.content

__all__ = ()
