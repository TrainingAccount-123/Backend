from fastapi import Request, HTTPException
from services.exception import InvalidInputError

def get_question(request: Request):
    return request.app.state.questions_obj

def get_user(request : Request):
    return request.app.state.user_obj

async def get_user_status(request : Request, username : str):
    try:
        return await request.app.state.user_obj.get_user_status(username)
    except InvalidInputError as iie:
        raise HTTPException(status_code=403,detail=f"{iie}")

def get_logger(request : Request):
    return request.app.state.logger

