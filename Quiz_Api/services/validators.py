import re
from fastapi import HTTPException

pattern = re.compile(r'[^A-Za-z0-9\s]{2,}')
spamcheck_pattern = re.compile(r'(.)\1{3,}')

async def validate_input_str(inp: str, field_name: str = "Input"):
    if not inp or not inp.strip():
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}, Please try again"
        )
    return inp

async def validate_input_str_with_set(inp: str, existing_set: set, field_name: str = "Input"):
    checker = inp.strip()
    if not checker:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}, Please try again"
        )
    if spamcheck_pattern.search(checker):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}, Please try again"
        )
    if pattern.search(checker):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}, Please try again"
        )
    if checker in existing_set:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}: The option has already been entered, Please try again"
        )
    return inp

async def validate_input_str_without_strip(inp: str, existing_set: set, field_name: str = "Input"):
    if not inp:
        return inp
    checker = inp.strip()
    if not checker:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}, Please try again"
        )
    if spamcheck_pattern.search(checker):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}, Please try again"
        )
    if pattern.search(checker):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}, Please try again"
        )
    if checker in existing_set:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}: The option has already been entered, Please try again"
        )
    return inp

async def validate_input_int(inp, field_name: str = "Input"):
    try:
        return int(inp)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}: Please enter a number"
        )
