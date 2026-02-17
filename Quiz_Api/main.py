import asyncio
import sys
import random
import re

from exception import InvalidInputError
from users import Users
from file_handler import FileHandler
from questions import Questions


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
                    else:
                        print("Invalid Input: The option has already been entered, Please try again\n")
                    
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
                        else:
                            print("Invalid Input: The option has already been entered, Please try again\n")

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
        user_obj = await Users.create(fh_obj)
        questions_obj = await Questions.create(fh_obj)

    except FileNotFoundError:
        print("Error Occurred on startup: users.csv or question_bank.json was not found")
        sys.exit()

    except Exception:
        print("Unexpected Error Occurred on startup, shutting down system")
        sys.exit()

    for i in range(5):
        username = await get_valid_input_str("Enter your username: ")
        password = await get_valid_input_str("Enter your password: ")
        try:
            login_result = await user_obj.login(username,password)
            print(login_result)
        except Exception:
            print("Unexpected Error Occurred while attempting to login")
        else:
            if login_result == f"Login Successful, Welcome {username}":
                break
            else:
                print(f"You have {4-i} more attempts")

        if i == 4:
            print("5 incorrect attempts were made to log in. Shutting down system.")
            sys.exit()

    user_status = await user_obj.get_user_status(username)

    if user_status == "user":
        while True:
            choice = await get_valid_input_int("""Available choices:
                1. Start Quiz
                2. Logout and Close system
                Please Enter your choice: """)
            try:
                match choice:

                    case 1:
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

                    case 2:
                        print("Closing system, thank you!!")
                        sys.exit()
                    
                    case _:
                        print("Invalid Input. Try again\n")
                        continue
            except Exception:
                print("Unexpected Error Occurred while executing choice")

    else:
        while True:
            choice = await get_valid_input_int("""Available Choices:
                1. Add Question  
                2. Edit Question  
                3. Remove Question  
                4. Clear Questions
                5. Start Quiz 
                6. Upload Questions File using Filepath
                7. Display All Questions
                8. Set number of random questions or provide order for the quiz (5 randomized questions given by default)
                9. Logout and close system 
                Please Confirm your choice: """)
            try:
                match choice:

                    case 1:
                        while True:
                            question = await get_valid_input_str_with_set("Enter the question: ",{})
                            if len(question)>9:
                                break
                            print("Invalid Input, Length of question is lesser than 10, Please Try again\n")
                        correct_answer = await get_valid_input_str_with_set("Enter the correct answer: ",{question})
                        option1 = await get_valid_input_str_with_set("Enter the first incorrect option: ",{question,correct_answer})
                        option2 = await get_valid_input_str_with_set("Enter the second incorrect option: ",{question,correct_answer,option1})
                        option3 = await get_valid_input_str_with_set("Enter the third incorrect option: ",{question,correct_answer,option1,option2})
                        try:
                            print("\n")
                            ques = await questions_obj.add_questions(question,correct_answer,option1,option2,option3)
                            if isinstance(ques,dict):
                                print("Added question")
                                for key in ques:
                                    print(f"{key} : {ques[key]}")
                            else:
                                print(ques)

                        except Exception:
                            print("Unexpected Error Occuured while adding question")
                    
                    case 2:
                        try:
                            questions = await questions_obj.get_question_from_id("all")
                            if questions:
                                
                                for dictionary in questions:
                                    for key in dictionary:
                                        print(f"{key} : {dictionary[key]}")
                                    print("\n")
                            else:
                                print("No questions recorded yet\n ")
                                continue

                        except Exception:
                            print("Unexpected Error Occurred while displaying all questions")
                        
                        else:
                            id = input("Enter the question id: ")
                            
                            try:
                                ques = await questions_obj.get_question_from_id(id)
                            except InvalidInputError as iie:
                                print(f"{iie}")
                            except Exception:
                                print("Unexpected Error Occurred while editing the question")

                            else:
                                try:
                                    print("Chosen Question to edit")

                                    for key in ques:
                                        print(f"{key} : {ques[key]}")
                                    print("\n")

                                    while True:
                                        confirm_edit = await get_valid_input_str("Do you really wish to edit the question (y/n): ")
                                        
                                        if confirm_edit == 'y':
                                            print("Press the Enter key if you do not want to edit field")
                                            
                                            while True:
                                                question = await get_valid_input_str_without_strip("Enter the question: ",{})
                                                if len(question)>9:
                                                    break
                                                elif len(question) == 0:
                                                    break
                                                print("Invalid Input, Please Try Again\n")
                                            
                                            correct_answer = await get_valid_input_str_without_strip("Enter the correct answer: ",{question})
                                            option1 = await get_valid_input_str_without_strip("Enter the first incorrect option: ",{question,correct_answer})
                                            option2 = await get_valid_input_str_without_strip("Enter the second incorrect option: ",{question,correct_answer,option1})
                                            option3 = await get_valid_input_str_without_strip("Enter the third incorrect option: ",{question,correct_answer,option2})
                                            
                                            try:
                                                ques = await questions_obj.edit_questions(id,question,correct_answer,option1,option2,option3)
                                                print("Finished editing question to:\n")
                                                for key in ques:
                                                    print(f"{key} : {ques[key]}")
                                                print("\n")
                                                break

                                            except InvalidInputError as iie:
                                                print(f"{iie}")
                                                break

                                            except Exception:
                                                print("Unexpected Error Occurred while editing the question")
                                                break

                                        elif confirm_edit == "n":
                                            print("Cancelling edit of question")
                                            break
                                        
                                        else:
                                            print("Invalid Input, Please Enter (y/n)")

                                except InvalidInputError as iie:
                                    print(f"{iie}")
                                    
                                except Exception:
                                    print("Unexpected Error Occurred while editing the question")

                    case 3:
                        try:
                            questions = await questions_obj.get_question_from_id("all")
                            if questions:
                                
                                for dictionary in questions:
                                    for key in dictionary:
                                        print(f"{key} : {dictionary[key]}")
                                    print("\n")
                            else:
                                print("No questions recorded yet\n ")
                                continue

                        except Exception:
                            print("Unexpected Error Occurred while displaying all questions")
                        
                        else:
                            id = await get_valid_input_str("Enter the question id:")
                            try:
                                ques = await questions_obj.get_question_from_id(id)
                                print("Chosen Question to remove")
                                for key in ques:
                                    print(f"{key} : {ques[key]}")
                                print("\n")
                            except InvalidInputError as iie:
                                print(f"{iie}")
                            except Exception:
                                print("Unexpected Error Occurred while displaying the questions\n")
                            else:
                                while True:
                                    confirm_remove = await get_valid_input_str("Do you really wish to remove the question (y/n)")
                                
                                    if confirm_remove == 'y':
                                        try:
                                            await questions_obj.remove_question(id)
                                            print(f"Removed question with id {id}")
                                            break
                                        except Exception:
                                            print("Unexpected Error Occurred while removing the question\n")
                                    elif confirm_remove == "n":
                                        print("Cancelling removal of question\n")
                                        break
                                    else:
                                        print("Invalid Input, Please enter (y/n)\n")
                            
                    case 4:
                        while True:
                            confirm_remove = await get_valid_input_str("Do you really wish to clear all the questions (y/n)")
                        
                            if confirm_remove == 'y':
                                try:
                                    await questions_obj.clear_questions()
                                    print("Cleared all questions")
                                    break
                                except Exception:
                                    print("Unexpected Error Occurred while clearing all questions")
                            elif confirm_remove == "n":
                                print("Cancelling clearing of all questions")
                                break
                            else:
                                print("Invalid Input, Please enter either y or n")

                    # case 5:
                    #     ques = await questions_obj.get_question_from_id("all")
                    #     max_n = len(ques)
                    #     print(f"Current number of questions: {questions_obj.NUMBER_OF_QUESTIONS_PER_QUIZ}, maximum number of questions: {max_n}")
                        
                    #     while True:
                    #         new_number = await get_valid_input_int("Enter the new number of questions: ")
                    #         if new_number>0:
                    #             if new_number<=max_n:
                    #                 break
                    #             print(f"Invalid Input: number of questions {new_number} exceeds available questions {max_n}")
                    #             continue
                    #         print("Invalid Input, please try again\n") 
                            
                    #     try:
                    #         await questions_obj.change_number_of_questions(new_number)
                    #         print(f"Changed number of questions to {new_number}")

                    #     except InvalidInputError as iie:
                    #         print(f"{iie}")

                    #     except Exception as e:
                    #         print(f"{e}\nUnexpected Error Occurred while changing the number of questions per quiz")
                            
                    case 5:
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
                    
                    case 6:
                        path = await get_valid_input_str("Enter the path to the json file: ")
                        try:
                            result = await questions_obj.take_json(path)

                            if isinstance(result,list):

                                for item in result:
                                    if isinstance(item,str):
                                        print(f"Skipped question because {item}")
                                    else:
                                        print("Added question: ")
                                        for key in item:
                                            print(f"{key} : {item[key]}")

                            elif isinstance(result,str):
                                print(f"Skipped question because {result}")
                                
                            else:
                                print("Added question: ")
                                for key in item:
                                    print(f"{key} : {item[key]}")

                        except FileNotFoundError as fnfe:
                            print(f"{fnfe} or is not json")

                        except InvalidInputError as iie:
                            print(f"{iie}")

                        except Exception:
                            print("JSON provided has errors")

                    case 7:
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

                    case 8:
                        try:
                            while True:
                                randomization = await get_valid_input_int("Enter 1 for setting number of random questions in the quiz, or enter 2 for setting order of questions: ")
                                if randomization in {1,2}:
                                    break
                                print("Invalid Input: Please Enter 1 or 2\n")

                            if randomization == 1:
                                ques = await questions_obj.get_question_from_id("all")
                                max_n = len(ques)
                                print(f"Current number of questions: {questions_obj.NUMBER_OF_QUESTIONS_PER_QUIZ}, maximum number of questions: {max_n}")
                                
                                while True:
                                    new_number = await get_valid_input_int("Enter the new number of questions: ")
                                    if new_number>0:
                                        if new_number<=max_n:
                                            break
                                        print(f"Invalid Input: number of questions {new_number} exceeds available questions {max_n}\n")
                                        continue
                                    print("Invalid Input, please try again\n") 
                                    
                                try:
                                    await questions_obj.change_number_of_questions(new_number)
                                    print(f"Changed number of questions to {new_number}")

                                except InvalidInputError as iie:
                                    print(f"{iie}")

                                except Exception as e:
                                    print(f"{e}\nUnexpected Error Occurred while changing the number of questions per quiz")
                            
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
                                                break
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
                                        continue

                        except Exception:
                            print("Unexpected Error Occurred while displaying all questions")
                        
                    case 9:
                        print("\nClosing System, Thank you!")
                        sys.exit()

                    case _:
                        print("Invaid Input: Please Enter one of the above choices")

                while True:
                    exit_choice = await get_valid_input_str("Do you wish to continue with the application (y/n): ")
                    if exit_choice == 'y': 
                        break
                    elif exit_choice == 'n':
                        sys.exit()
                    else:
                        print("Invalid Input: Please Input (y/n)") 

            except Exception:
                print("Unexpected Error Occurred while executing choice")

if __name__ == "__main__":
    asyncio.run(main())