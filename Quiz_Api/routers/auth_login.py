from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import logging

from dependency import get_user
from services.exception import InvalidInputError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/login",tags=["login"])

class LoginResult(BaseModel):
    username : str
    password : str

class UserStatus(BaseModel):
    username : str

@router.get("/login_result")
async def login_reult(
    payload : LoginResult,
    user_obj = Depends(get_user)
    ):

    try:
        
        username = payload.username
        password = payload.password
        logger.info(f"attempting login for {username}")
        login = await user_obj.login(username,password)
        return {"status":login}
        logger.info("Login Successful")

    except Exception as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=500, detail="Unexpected Error Occurred while attempting to login")

@router.get("/get_user_status")
async def get_user_status(
    payload : UserStatus,
    user_obj = Depends(get_user)
    ):

    try:
        username = payload.username
        user_status = await user_obj.get_user_status(username)
        return {"user_status": user_status}
        
    except InvalidInputError as iie:
        logger.warning(f"{iie}")
        raise HTTPException(status_code = 400, detail = f"{iie}")

    except Exception as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=500, detail="Unexpected Error Occurred while attempting to get user status")

