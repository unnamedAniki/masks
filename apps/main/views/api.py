import asyncio

from fastapi import Response

from apps.main.models import ModelOutput
from apps.run_main import app, model


@app.get("/api/v1/main/")
async def index(data: Response):
    return {1: "Базовая страница"}


@app.get("/api/v1/get_model/")
async def get_model(data: Response):
    output_info = []
    output = await model.generate_result_text(
        text="Краткий маркетинговый текст потребительский кредит женщина средних лет")
    # for client_data in data.body:
    #     # list_id, text_for_model = get_marketing_text(client_data)
    #     result_text = apps.model.main.model.generate_result_text(text_for_model)
    #     output_info.append(ModelOutput(
    #         id=1,
    #         communication_text=result_text,
    #         accuracy=90.1
    #     ))
    return {'id': 1, 'answer': output, 'comment': data.body}
