from file_handler import FileHandler
from questions import Questions
from exception import InvalidInputError

import asyncio
import sys
import re
import random

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
spamcheck_pattern = re.compile(r'(.)\1{3,}')

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

async def get_valid_input_int(msg):
    while True:
        inp = input(msg)
        try:
            a = int(inp)
            return a
        except ValueError:
            print("Invalid Input: Please enter a number\n")

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




    # print(f"Current number of questions: {questions_obj.NUMBER_OF_QUESTIONS_PER_QUIZ}")
    # ques = await questions_obj.get_question_from_id("all")
    # max_n = len(ques)
    # while True:
    #     new_number = await get_valid_input_int("Enter the new number of questions: ")
    #     if new_number>0:
    #         if new_number<=max_n:
    #             break
    #         print(f"Invalid Input: number of questions {new_number} exceeds available questions {max_n}")
    #     print("Invalid Input, please try again\n") 
        
    # try:
    #     await questions_obj.change_number_of_questions(new_number)
    #     print(f"Changed number of questions to {new_number}")

    # except InvalidInputError as iie:
    #     print(f"{iie}")

    # except Exception as e:
    #     print(f"{e}\nUnexpected Error Occurred while changing the number of questions per quiz")




    # ques = await questions_obj.get_question_from_id("all")
    # max_n = len(ques)
    # print(f"Current number of questions: {questions_obj.NUMBER_OF_QUESTIONS_PER_QUIZ}, maximum number of questions: {max_n}")
    
    # while True:
    #     new_number = await get_valid_input_int("Enter the new number of questions: ")
    #     if new_number>0:
    #         if new_number<=max_n:
    #             break
    #         print(f"Invalid Input: number of questions {new_number} exceeds available questions {max_n}")
    #         continue
    #     print("Invalid Input, please try again\n") 
        
    # try:
    #     await questions_obj.change_number_of_questions(new_number)
    #     print(f"Changed number of questions to {new_number}")

    # except InvalidInputError as iie:
    #     print(f"{iie}")

    # except Exception as e:
    #     print(f"{e}\nUnexpected Error Occurred while changing the number of questions per quiz")

    
    
    
    
    
    
    
    
    
    
    
#give_qiuz
    try:
        while True:
            randomization = await get_valid_input_int("Enter 1 for randomizing questions, or enter 2 for setting order of questions: ")
            if randomization in {1,2}:
                break
            print("Invalid Input: Please Enter 1 or 2\n")

        if randomization == 1:
            print("Questions set to randomize per quiz")
        
        else:
            print("Questions available:\n")
            try:
                questions = await questions_obj.get_question_from_id("all")
                if questions:
                    for dictionary in questions:
                        for key in dictionary:
                            print(f"{key} : {dictionary[key]}")
                        print("\n")
                else:
                    print("No questions recorded yet\n ")
            except Exception:
                print("Unexpected Error Occurred while displaying all questions")
                
            print("Input Question ID's in the order that is required\n")
            ids = []
            while True:
                id = await get_valid_input_str("Enter the id (enter -1 to exit): ")
                try:
                    if id == "-1":
                        break
                    ques = await questions_obj.get_question_from_id(id)
                    print(f"Question to be added at {len(ids)+1} position")
                    for key in ques:
                        print(f"{key} : {ques[key]}")
                    print("\n")
                    while True:
                        choice_msg = await get_valid_input_str(f"Do you wish to add the above question at {len(ids)+1} position (y/n):")
                        if choice_msg == 'y':
                            if id not in ids:
                                ids.append(id)
                            else:
                                print("ID already entered into ids")
                            break
                        elif choice_msg == 'n':
                            print("Cancelling addition of above question")
                        else:
                            print("Invalid Input, Please Enter (y/n)")
                    print("Current ID list:",end=" ")
                    for item in ids:
                        print(f"{item},",end=" ")
                    print("\n")

                except InvalidInputError as iie:
                    print(f"{iie}")
                    continue
                    
                except Exception:
                    print("Unexpected Error Occurred while setting question order")
                    continue
            
            if not ids:
                print("No questions entered to provide order, randomizing questions instead")
            else:
                try:                                        
                    await questions_obj.change_order_of_questions(ids,2)
                    print("Added questions with ids:",end=" ")
                    for item in ids:
                        print(f"{item}",end=" ")
                    print("\nin the above order to the quiz.\nThe quiz will take place only with the above questions\n")
                except Exception:
                    print("Unexpected Error Occurred while displaying questions")

    except Exception:
        print("Unexpected Error Occurred while displaying all questions")


    try:
        n = questions_obj.NUMBER_OF_QUESTIONS_PER_QUIZ
        q_dict = await questions_obj.give_quiz()

    except InvalidInputError as iie:
        print(f"Invalid Input: {iie}")

    except Exception:
        print("Unexpected Error Occurred while giving quiz")

    else:
        try:
            print("""Rules:
            Enter 1,2,3 or 4 to pick an option. Any other entry will be marked as an incorrect answer\n
            """)
            
            num_correct = 0
            for i in range(len(q_dict)):
                print(f"Q{i+1}) {q_dict[i]["question"]}\n")
                keylist = ["correct_answer","option1","option2","option3"]
                keylist = random.sample(keylist,4)
                index_correct = keylist.index("correct_answer")+1
                for j in range(len(keylist)):
                    print(f"{j+1}) {q_dict[i][keylist[j]]}\n")
                picked_ans = await get_valid_input_int("Please Enter an option(1,2,3 or 4): ")

                if picked_ans not in {1,2,3,4}:
                    print(f"{picked_ans} is not a valid input and will be marked as incorrect\n")
                elif picked_ans == -1:
                    print("Question timed out, Next question!!")
                elif picked_ans == index_correct:
                    num_correct+=1
            
            print(f"""Results: 
            Number of Questions:       {n}
            number of Correct Answers: {num_correct}
            Percentage Score:          {(num_correct*100)/n}%""")
        except InvalidInputError as iie:
            print(f"Invalid Input: {iie}")

        except Exception:
            print("Unexpected Error Occurred while giving quiz")




asyncio.run(main())