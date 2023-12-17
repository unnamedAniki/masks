import asyncio
import json

from fastapi import Response, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from apps.database.db_connect import engine
from apps.database.model import ModelLogs
from apps.database.queries import log_queries
from apps.database.queries.log_queries import logs_queries
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
        model_log = ModelLogs(
            user_prompt=user_prompt['comment'],
            user_id=user_prompt['id']
        )
        logs_queries.add_comment(model_log)
        output_info.append(user_prompt)

    return output_info


@app.get("/api/v1/get_logs/")
async def get_logs():
    logs = logs_queries.get_logs()
    return logs


@app.post("/api/v1/check_log")
async def check_log(comment_id: int, check: bool):
    logs_queries.check_model_output(check=check, id=comment_id)