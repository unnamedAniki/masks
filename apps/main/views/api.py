import asyncio
import json

from fastapi import Response, Body
from fastapi.encoders import jsonable_encoder

from apps.main.models import ModelOutput
from apps.run_main import app, model
from apps.model.cluster import Cluster

@app.get("/api/v1/main/")
async def index(data: Response):
    return {1: "Базовая страница"}


@app.get("/api/v1/get_model/")
async def get_model(data=Body()):
    output_info = []
    print(jsonable_encoder(data.decode("utf-8")))
    prompt = model.clust_model.generatePrompt(jsonable_encoder(data.decode("utf-8")))
    user_prompt = {}
    for key, value in prompt.items():
        user_prompt['id'] = key
        user_prompt['comment']: str = ""
        for text in value:
            output_text = await model.generate_result_text(text=text)
            user_prompt['comment'] = output_text
            break
        output_info.append(user_prompt)
    return output_info
    # for client_data in data.body:
    #     # list_id, text_for_model = get_marketing_text(client_data)
    #     result_text = apps.model.main.model.generate_result_text(text_for_model)
    #     output_info.append(ModelOutput(
    #         id=1,
    #         communication_text=result_text,
    #         accuracy=90.1
    #     # ))
    return output_info
