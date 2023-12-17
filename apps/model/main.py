import asyncio
import os.path
import time
from concurrent.futures import ProcessPoolExecutor
from threading import Thread
from apps.model.cluster import Cluster
from llama_cpp import Llama

from apps.model.settings import model_settings


class Model:
    def __init__(self):
        self.model = Llama(
            model_path=model_settings.PATH,
            n_ctx=1536,
            n_parts=1,
            n_threads=16,
            n_gpu_layers=33,
        )
        #path_data - Путь к файле с информацией о пользователях EXCEL
        self.clust_model = Cluster(path_data=path_data, path_cluster=model_settings.PATH_cluster)

    def get_prompt(self):
        predict = self.clust_model.predictClust()
        products = self.clust_model.recommend_product(predict)
        return products

    def get_message_tokens(self, role, content):

        message_tokens = self.model.tokenize(content.encode("utf-8"))
        message_tokens.insert(1, model_settings.ROLE_TOKENS[role])
        message_tokens.insert(2, model_settings.LINEBREAK_TOKEN)
        message_tokens.append(self.model.token_eos())
        return message_tokens

    def get_system_tokens(self):
        system_message = {
            "role": "system",
            "content": model_settings.SYSTEM_PROMPT
        }
        return self.get_message_tokens(**system_message)

    async def generate_result_text(self, top_k: int = 30,
                                   top_p: float = 0.9,
                                   temperature: float = 0.2,
                                   repeat_penalty: float = 1.09,
                                   text: str = ""):
        print("current_time")
        current_time = time.time()
        ai_model = self.model
        print("ai_model")
        tokens = self.get_system_tokens()
        ai_model.eval(tokens)
        print("get_system_tokens")
        message_tokens = self.get_message_tokens(role="user", content=text)
        role_tokens = [ai_model.token_bos(), model_settings.BOT_TOKEN, model_settings.LINEBREAK_TOKEN]
        tokens += message_tokens + role_tokens
        print("preform_generate")
        generator = ai_model.generate(
            tokens,
            top_k=top_k,
            top_p=top_p,
            temp=temperature,
            mirostat_tau=5,
            mirostat_eta=0.04,
            repeat_penalty=repeat_penalty
        )
        token_str = ""
        before_detokenize = time.time()
        for token in generator:
            if token == ai_model.token_eos():
                break
            token_str += ai_model.detokenize([token]).decode("utf-8", errors="ignore")

        print(f'Затрачено на детокенизацию: {time.time() - before_detokenize} сек.')
        print(f'Общее время выполнения: {time.time() - current_time} сек.')
        return token_str



