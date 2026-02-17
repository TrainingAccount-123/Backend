from fastapi import APIRouter, HTTPException, Depends
import random
import logging

from services.exception import InvalidInputError
from dependency import get_question, get_user_status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/quiz")
async def give_quiz(
    questions_obj = Depends(get_question),
    user_status = Depends(get_user_status)
    ):

    try:
        logger.info("starting quizzing process")
        if user_status != "user":
            raise HTTPException(status_code=401,detail="User must be user to access this feature")
        q_list = await questions_obj.give_quiz()

        return_randomised = {}

        for i in range(len(q_list)):
            options = random.sample([q_list[i]["correct_answer"],q_list[i]["option1"],q_list[i]["option2"],q_list[i]["option3"]],4)
            correct_answer_index = options.index(q_list[i]["correct_answer"])+1
            new_dict = {"question": q_list[i]["question"],
                        "options": options,
                        "correct_answer":correct_answer_index}

            return_randomised.update({f"question_number_{i+1}":new_dict})

        logger.info("Successfully completed quizzing process")
        return return_randomised

    except HTTPException as httpe:
        logger.warning(f"{httpe}")
        raise

    except InvalidInputError as iie:
        logger.warning(f"{iie}")
        raise HTTPException(status_code = 422, detail = f"{iie}")

    except Exception as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=400, detail="Unexpected Error Occured while removing question")

