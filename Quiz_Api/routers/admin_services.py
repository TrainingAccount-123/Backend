from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import random

from dependency import get_question, get_user_status
from services.exception import InvalidInputError
from services.validators import validate_input_str_with_set, validate_input_str_without_strip
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])

class QuestionCreate(BaseModel):
    question: str
    correct_answer: str
    option1: str
    option2: str
    option3: str

class QuestionsPatch(BaseModel):
    id : int
    question: str = ""
    correct_answer: str = ""
    option1: str = ""
    option2: str = ""
    option3: str = ""

class QuestionsDelete(BaseModel):
    id : int

class QuestionsUpload(BaseModel):
    path : str

class QuestionsOrder(BaseModel):
    ids : list[str] = []
    num : int
    number_of_questions : int = 5


@router.post("/add_question")
async def add_question(
    payload : QuestionCreate,
    questions_obj = Depends(get_question),
    user_status = Depends(get_user_status)
    ):

    try:
        if user_status != "admin":
            raise HTTPException(status_code=401,detail="User must be admin to access this feature")
        
        logger.info("Starting addition of question")
        question = payload.question
        correct_answer = payload.correct_answer
        option1 = payload.option1
        option2 = payload.option2
        option3 = payload.option3

        await validate_input_str_with_set(question,{})
        await validate_input_str_with_set(correct_answer,{question})
        await validate_input_str_with_set(option1,{question,correct_answer})
        await validate_input_str_with_set(option2,{question,correct_answer,option1})
        await validate_input_str_with_set(option3,{question,correct_answer,option2,option1})
    except HTTPException as httpe:
        logger.warning(f"{httpe}")
        raise
    else:
        try:
            ques = await questions_obj.add_questions(question,correct_answer,option1,option2,option3)
            if isinstance(ques,dict):
                logger.info("Successfully Added Question")
                return {"added_question" : ques}
            else:
                raise HTTPException(status_code=406, detail=ques)

        except HTTPException as httpe:
            logger.warning(f"{httpe}")
            raise

        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=500, detail="Unexpected Error Occured while adding question")


@router.put("/edit_question")
async def edit_questions(
    payload: QuestionsPatch,
    questions_obj = Depends(get_question),
    user_status = Depends(get_user_status)
    ):

    try:
        if user_status != "admin":
            raise HTTPException(status_code=401,detail="User must be admin to access this feature")
        
        logger.info("starting editing of question")
        id = str(payload.id)
        question = payload.question
        correct_answer = payload.correct_answer
        option1 = payload.option1
        option2 = payload.option2
        option3 = payload.option3

        ids = await questions_obj.get_question_from_id(id)

    except InvalidInputError as iie:
        logger.warning(f"{iie}")
        raise HTTPException(status_code = 422, detail = f"{iie}")

    except HTTPException as httpe:
        logger.warning(f"{httpe}")
        raise

    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=500, detail="Unexpected Error Occured while editing question")

    else:
        try:
            await validate_input_str_without_strip(question,{})
            await validate_input_str_without_strip(correct_answer,{question})
            await validate_input_str_without_strip(option1,{question,correct_answer})
            await validate_input_str_without_strip(option2,{question,correct_answer,option1})
            await validate_input_str_without_strip(option3,{question,correct_answer,option2,option1})

        except HTTPException as httpe:
            logger.warning(f"{httpe}")
            raise

        else:
            try:
                ques = await questions_obj.edit_questions(id,question,correct_answer,option1,option2,option3)
                logger.info("Successfully Edited Question")
                return {"edited_question_to" : ques}

            except Exception as e:
                logger.error(f"{e}")
                raise HTTPException(status_code=500, detail="Unexpected Error Occured while editing question")

@router.delete("/remove_question")
async def remove_question(
    payload : QuestionsDelete,
    questions_obj = Depends(get_question),
    user_status = Depends(get_user_status)
    ):

    id = str(payload.id)

    try:
        if user_status != "admin":
            raise HTTPException(status_code=401,detail="User must be admin to access this feature")
        
        logger.info("Starting removal of question")
        removed = await questions_obj.remove_question(id)
        return {"removed_question" : removed}
        logger.info("Removal of question successfull")

    except HTTPException as httpe:
        logger.warning(f"{httpe}")
        raise
    
    except InvalidInputError as iie:
        logger.warning(f"{iie}")
        raise HTTPException(status_code = 400, detail = f"{iie}")

    except Exception as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=500, detail="Unexpected Error Occured while removing question")

@router.delete("/clear_questions")
async def clear_questions(
    questions_obj = Depends(get_question),
    user_status = Depends(get_user_status)
    ):

    try:
        if user_status != "admin":
            raise HTTPException(status_code=401,detail="User must be admin to access this feature")
        
        logger.info("starting clearing of all questions")
        await questions_obj.clear_questions()
        return {"status" : "cleared all questions"}
        logger.info("Clear all questions successfull")

    except HTTPException as httpe:
        logger.warning(f"{httpe}")
        raise

    except Exception as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=500, detail="Unexpected Error Occured while clearing question")

@router.get("/quiz")
async def give_quiz(
    questions_obj = Depends(get_question),
    user_status = Depends(get_user_status)
    ):

    try:
        if user_status != "admin":
            raise HTTPException(status_code=401,detail="User must be admin to access this feature")
        
        logger.info("Starting quiz")
        q_list = await questions_obj.give_quiz()

        return_randomised = {}

        for i in range(len(q_list)):
            options = random.sample([q_list[i]["correct_answer"],q_list[i]["option1"],q_list[i]["option2"],q_list[i]["option3"]],4)
            correct_answer_index = options.index(q_list[i]["correct_answer"])+1
            new_dict = {"question": q_list[i]["question"],
                        "options": options,
                        "correct_answer":correct_answer_index}

            return_randomised.update({f"question_number_{i+1}":new_dict})

        logger.info("Successfully finishing giving quiz")
        return return_randomised

    except HTTPException as httpe:
        logger.warning(f"{httpe}")
        raise

    except InvalidInputError as iie:
        logger.warning(f"{iie}")
        raise HTTPException(status_code = 400, detail = f"{iie}")

    except Exception as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=500, detail="Unexpected Error Occured while giving quiz")


@router.post("/upload_file")
async def upload_files_using_filepath(
    payload : QuestionsUpload,
    questions_obj = Depends(get_question),
    user_status = Depends(get_user_status)
    ):
    try:
        if user_status != "admin":
            raise HTTPException(status_code=401,detail="User must be admin to access this feature")
        
        logger.info("Starting upload of file")
        path = payload.path
        result = await questions_obj.take_json(path)

        return_dict = {}
        if isinstance(result,list):

            for i,item in enumerate(result):
                if isinstance(item,str):
                    return_dict.update({f"question{i+1}": f"Skipped question because {item}"})
                else:
                    return_dict.update({f"question{i+1}": item})

        elif isinstance(result,str):
            return_dict.update({"question1": f"Skipped question because {result}"})
            
        else:
            return_dict.update({"question1": {result}})
        
        return return_dict
        logger.info("Successfully completed upload of file")

    except HTTPException as httpe:
        logger.warning(f"{httpe}")
        raise

    except InvalidInputError as iie:
        logger.warning(f"{iie}")
        raise HTTPException(status_code = 400, detail = f"{iie}")

    except FileNotFoundError as fnfe:
        logger.warning(f"{fnfe}")
        raise HTTPException(status_code = 400, detail = f"{fnfe}")

    except Exception as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=500, detail="Unexpected Error Occured while Uploading file")

@router.get("/display_all")
async def display_all_questions(
    questions_obj = Depends(get_question),
    user_status = Depends(get_user_status)
    ):

    try:
        if user_status != "admin":
            raise HTTPException(status_code=401,detail="User must be admin to access this feature")
        
        logger.info("beginning display of all questions")
        questions = await questions_obj.get_question_from_id("all")
        if questions:
            return_dict = {
                f"question{i+1}" : questions[i]
                for i in range(len(questions))
            }
        
        else:
            return_dict = {"questions" : "No questions recorded yet"}
        
        logger.info("display successful")
        return return_dict

    except HTTPException as httpe:
        logger.warning(f"{httpe}")
        raise
    
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=500, detail="Unexpected Error Occured while displaying all questions")


@router.put("/question_order")
async def change_question_order(
    payload : QuestionsOrder,
    questions_obj = Depends(get_question),
    user_status = Depends(get_user_status)
    ):
    
    try:
        if user_status != "admin":
            raise HTTPException(status_code=401,detail="User must be admin to access this feature")
        
        logger.info("Beginning changing of question order")
        ids = payload.ids
        num = payload.num
        number_of_questions = payload.number_of_questions

        if num not in {1,2}:
            raise HTTPException(status_code=400, detail="Invalid Input for num, please provide either 1 or 2")
        else:
            questions = await questions_obj.get_question_from_id("all")
            id_list = [question["qid"] for question in questions]
            if num == 1:
                if number_of_questions>len(id_list):
                    raise HTTPException(status_code=400, detail="Invalid Input: number of questions given exceeds number of questions available. Reverting to previous or default settings")
                if number_of_questions<1:
                    raise HTTPException(status_code=400, detail="Invalid Input: number of questions given is too low. Reverting to previous or default settings")

                await questions_obj.change_number_of_questions(number_of_questions)
                return {"changed number_of_questions to" : number_of_questions}
            else:
                if ids:
                    for item in ids:
                        if item not in id_list:
                            raise InvalidInputError(f"Question ID {item} not found, reverting to previous or default settings")
                    await questions_obj.change_order_of_questions(ids,2)
                    return {
                        "changed number_of_questions to" : len(ids),
                        "ids_chosen" : ids
                    }
                else:
                    raise HTTPException(status_code=400, detail="Invalid Input: No ID's provided. Retaining randomization of questions")
        logger.info("change of question order Successful")

    except HTTPException as httpe:
        logger.warning(f"{httpe}")
        raise

    except InvalidInputError as iie:
        logger.warning(f"{iie}")
        raise HTTPException(status_code = 400, detail = f"{iie}")

    except Exception as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=500, detail="Unexpected Error Occured while changing question order")
