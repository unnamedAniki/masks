from fastapi import APIRouter, status


def init(app):
    from .api import get_model, index
    router = APIRouter(tags=['Site'])

    # ROUTES
    # -------------------------------------------
    router.add_api_route(
        '/',
        methods=['GET'],
        status_code=status.HTTP_200_OK,
        endpoint=index
    )
    router.add_api_route(
        '/get_model',
        methods=['POST'],
        status_code=status.HTTP_200_OK,
        endpoint=get_model
    )

    # INCLUDE ROUTER
    # -------------------------------------------
    app.include_router(router)