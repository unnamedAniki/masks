from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.database.model import ModelLogs
from apps.run_main import query


class LogQueries:

    def get_logs(self):
        with Session(query) as session:
            logs = session.query(ModelLogs).all()
            print(logs)
            return logs

    def add_comment(self, model: ModelLogs):
        with Session(query) as session:
            session.add(model)
            session.commit()
            return

    def check_model_output(self, id: int, check: bool):
        with Session(query) as session:
            stmt = select(ModelLogs).where(id=id)
            message = session.scalars(stmt).one()
            print(message)
            message.is_right = check
            session.commit()
            return


logs_queries = LogQueries()