import asyncio

from fastapi import Response, Body

from apps.main.models import ModelOutput
from apps.run_main import app, model
from apps.model.cluster import Cluster

@app.get("/api/v1/main/")
async def index(data: Response):
    return {1: "Базовая страница"}


@app.get("/api/v1/get_model/")
async def get_model(data=Body()):
    output_info = []

    print(data)
    prompt = model.clust_model.recommend_product(data)
    for key, value in prompt.items():
        output_info.append({
            'id': key,
            'answer': await model.generate_result_text(text=value),
            'comment': value
        })
    # for client_data in data.body:
    #     # list_id, text_for_model = get_marketing_text(client_data)
    #     result_text = apps.model.main.model.generate_result_text(text_for_model)
    #     output_info.append(ModelOutput(
    #         id=1,
    #         communication_text=result_text,
    #         accuracy=90.1
    #     ))
    return output_info
