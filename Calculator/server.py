from fastapi import APIRouter, HTTPException
from arithmetic import Arithmetic
from pydantic import BaseModel


router = APIRouter()

class GetNumbers(BaseModel):
    lst : list(float)


@router.get("/add")
async def add(payload : GetNumbers):
    try:
        lst = payload.lst
        if not lst:
            raise HTTPException(status_code=400, detail="Invalid Input, No Numbers Entered")
        if len(lst) ==1:
            return {"result": lst[0]}
        for item in lst:
            if not isinstance(item,float):
                raise HTTPException(status_code=400, detail="Invalid Input, Enter only numbers")
        
        return {"result": await Arithmetic.add(lst)}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error Occurred while Adding Numbers")

@router.get("/subtract")
async def subtract(payload : GetNumbers):
    try:
        lst = payload.lst
        if not lst:
            raise HTTPException(status_code=400, detail="Invalid Input, No Numbers Entered")
        if len(lst) ==1:
            return {"result": lst[0]}
        for item in lst:
            if not isinstance(item,float):
                raise HTTPException(status_code=400, detail="Invalid Input, Enter only numbers")
        
        return {"result": await Arithmetic.subtract(lst)}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error Occurred while Subtracting Numbers")



@router.get("/multiply")
async def multiply(payload : GetNumbers):
    try:
        lst = payload.lst
        if not lst:
            raise HTTPException(status_code=400, detail="Invalid Input, No Numbers Entered")
        if len(lst) ==1:
            return {"result": lst[0]}
        for item in lst:
            if not isinstance(item,float):
                raise HTTPException(status_code=400, detail="Invalid Input, Enter only numbers")
        
        return {"result": await Arithmetic.multiply(lst)}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error Occurred while Multiplying Numbers")



@router.get("/divide")
async def divide(payload : GetNumbers):
    try:
        lst = payload.lst
        if not lst:
            raise HTTPException(status_code=400, detail="Invalid Input, No Numbers Entered")
        if len(lst) ==1:
            return {"result": lst[0]}
        for item in lst:
            if not isinstance(item,float):
                raise HTTPException(status_code=400, detail="Invalid Input, Enter only numbers")
        
        return {"result": await Arithmetic.add(lst)}
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error Occurred while Adding Numbers")

    except ZeroDivisionError:
        raise HTTPException(
            status_code=400,
            detail="Division by zero not allowed"
        )
