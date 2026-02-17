from file_handler import FileHandler
from questions import Questions
from exception import InvalidInputError

import asyncio
import sys
import re

pattern = re.compile(r'[^A-Za-z0-9\s]{2,}')
spamcheck_pattern = re.compile(r'(.)\1{3,}')

async def get_valid_input_str(msg):
    while True:
        inp = input(msg)
        if inp.strip():
            return inp
        else:
            print("Invalid Input, Please try again\n")

pattern = re.compile(r'[^A-Za-z0-9\s]{2,}')
spamcheck_pattern = re.compile(r'(.)\1{2,}')
async def get_valid_input_str_with_set(msg,set):

    while True:
        inp = input(msg)
        checker = inp.strip()
        if checker:
            if not spamcheck_pattern.search(checker):
                if not pattern.search(checker):
                    if checker not in set:
                        return inp

        print("Invalid Input, Please try again\n")

async def get_valid_input_str_without_strip(msg,set):

    while True:
        inp = input(msg)
        if inp:
            checker = inp.strip()
            if checker:
                if not spamcheck_pattern.search(checker):
                    if not pattern.search(checker):
                        if checker not in set:
                            return inp

            print("Invalid Input, Please try again\n")

        else:
            return inp

async def main():
    try:
        fh_obj = FileHandler()
        questions_obj = await Questions.create(fh_obj)

    except FileNotFoundError:
        print("Error Occurred on startup: users.csv or question_bank.json was not found")
        sys.exit()

    except Exception:
        print("Unexpected Error Occurred on startup, shutting down system")
        sys.exit()




















    # try:
    #     questions = await questions_obj.get_question_from_id("all")
    #     if questions:
            
    #         for dictionary in questions:
    #             for key in dictionary:
    #                 print(f"{key} : {dictionary[key]}")
    #             print("\n")
    #     else:
    #         print("No questions recorded yet\n ")

    # except Exception:
    #     print("Unexpected Error Occurred while displaying all questions")

    # id = input("Enter the question id: ")
    # print("\n")
    # try:
    #     ques = await questions_obj.get_question_from_id(id)
    #     print("Chosen Question to edit")
    #     for key in ques:
    #         print(f"{key} : {ques[key]}")
    #     print("\n")
    #     confirm_remove = await get_valid_input_str("Do you really wish to edit the question (y/n): ")
    #     while True:
    #         if confirm_remove == 'y':
    #             print("Press the Enter key if you do not want to edit field")
    #             while True:
    #                 question = await get_valid_input_str_without_strip("Enter the question: ",{})
    #                 if len(question)>9:
    #                     break
    #                 elif len(question) == 0:
    #                     break
    #                 print("Invalid Input, Please Try Again\n")
    #             correct_answer = await get_valid_input_str_without_strip("Enter the correct answer: ",{question})
    #             option1 = await get_valid_input_str_without_strip("Enter the first incorrect option: ",{question,correct_answer})
    #             option2 = await get_valid_input_str_without_strip("Enter the second incorrect option: ",{question,correct_answer,option1})
    #             option3 = await get_valid_input_str_without_strip("Enter the third incorrect option: ",{question,correct_answer,option2})
    #             try:
    #                 ques = await questions_obj.edit_questions(id,question,correct_answer,option1,option2,option3)
    #                 print("Finished editing question to:\n")
    #                 for key in ques:
    #                     print(f"{key} : {ques[key]}")
    #                 print("\n")
    #                 break

    #             except InvalidInputError as iie:
    #                 print(f"{iie}")
    #                 break

    #             except Exception:
    #                 print("Unexpected Error Occurred while editing the question")
    #                 break

    #         elif confirm_remove == "n":
    #             print("Cancelling edit of question")
    #             break
    #         else:
    #             print("Invalid Input, Please Try again")
    # except InvalidInputError as iie:
    #     print(f"{iie}")
    # except Exception:
    #     print("Unexpected Error Occurred while editing the question")


    path = await get_valid_input_str("Enter the path to the json file: ")
    try:
        result = await questions_obj.take_json(path)
        if isinstance(result,list):
            for item in result:
                if isinstance(item,str):
                    print(item)
                else:
                    for key in item:
                        print(f"{key} : {item[key]}")
        elif isinstance(result,str):
            print(result)
        else:
            print(result)

    except FileNotFoundError as fnfe:
        print(f"{fnfe}")

    except InvalidInputError as iie:
        print(f"{iie}")

    # except Exception:
    #     print("Unexpected Error Occurred while taking json")




    






asyncio.run(main())