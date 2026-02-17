import random
import os

from services.exception import InvalidInputError

class Questions:

    __PERSISTANCE_PATH = "C:/Users/SkandaSankarRaman/OneDrive - GapBlue Software Labs Pvt Ltd/Work/live_coding/Quiz_Api/databases/question_bank.json"
    NUMBER_OF_QUESTIONS_PER_QUIZ = 5
    RANDOMIZE = []

    def __init__(self,question_bank,fh):
        self.__question_bank = question_bank
        self.fh_obj = fh


    @classmethod
    async def create(cls,fh):

        qb = await fh.file_read_to_thread(cls.__PERSISTANCE_PATH,"json")
        return cls(qb,fh)
    
    async def add_questions(self,question,correct_answer,option1,option2,option3):
        
        try:
            question = question[0].upper() + question[1:].lower()
            if question[-1] not in {".","?"}:
                question += "?"
            q_list = [x["question"].lower() for x in self.__question_bank]
            if question.lower() in q_list:
                return f"The Question: {question} Already Exists"
            if self.__question_bank:
                id = str(max(int(t["qid"]) for t in self.__question_bank)+1)
            else:
                id = "1"
            self.__question_bank.append({"qid":id,"question":question, "correct_answer":correct_answer, "option1":option1, "option2":option2, "option3":option3})
            await self.fh_obj.file_write_to_thread(self.__PERSISTANCE_PATH,self.__question_bank,"json")
            return self.__question_bank[-1]
        except Exception:
            raise Exception("Unexpected Error occurred while adding question")

    async def edit_questions(self,id,question,correct_answer,option1,option2,option3):

        try:
            if question:
                question = question[0].upper() + question[1:].lower()
                if question[-1] not in {".","?"}:
                    question += "?"
            
            element = list(filter(lambda x:x["qid"] == id,self.__question_bank))
            if element:
                index = self.__question_bank.index(element[0])
                edit_list = [question,correct_answer,option1,option2,option3]
                key_list = list(element[0].keys())[1:]
                for i in range(len(edit_list)):
                    if edit_list[i].strip():
                        element[0][key_list[i]]=edit_list[i]
                self.__question_bank[index] = element[0]
                await self.fh_obj.file_write_to_thread(self.__PERSISTANCE_PATH,self.__question_bank,"json")
                return element[0]
            else:
                raise InvalidInputError("Question ID not found")

        except InvalidInputError:
            raise

        except Exception as e:
            raise Exception(f"Unexpected Error Occurred while editing question: {e}")

    async def remove_question(self,id):

        try:
            element = list(filter(lambda x:x["qid"] == id,self.__question_bank))
            if element:
                self.__question_bank.remove(element[0])
                await self.fh_obj.file_write_to_thread(self.__PERSISTANCE_PATH,self.__question_bank,"json")
                return element[0]

            else:
                raise InvalidInputError("Question ID not found")

        except InvalidInputError:
            raise

        except Exception as e:
            raise Exception(f"Unexpected Error Occurred while removing question: {e}")

    async def clear_questions(self):

        try:
            self.__question_bank = []
            await self.fh_obj.file_write_to_thread(self.__PERSISTANCE_PATH,self.__question_bank,"json")

        except Exception as e:
            raise Exception(f"Unexpected Error Occurred while clearing question bank: {e}")

    async def give_quiz(self):

        try:
            if not self.RANDOMIZE:
                if self.NUMBER_OF_QUESTIONS_PER_QUIZ>=len(self.__question_bank):
                    raise InvalidInputError("The number of questions to be asked exceeds the number of questions available")
                else:
                    return random.sample(self.__question_bank,self.NUMBER_OF_QUESTIONS_PER_QUIZ)

            else:
                elements = [await self.get_question_from_id(id) for id in self.RANDOMIZE]
                return elements

        except InvalidInputError:
            raise

        except Exception as e:
            raise Exception(f"Unexpected Error Occurred while giving quiz: {e}")

    async def _validate_json_keys(self,file_content):

        try:
            _REQUIRED_KEYS = {"question","correct_answer","option1","option2","option3"}
            if not isinstance(file_content,list):

                if not isinstance(file_content,dict):
                    return ("The given JSON File does not contain the correct format",False)
                else:
                    missing = _REQUIRED_KEYS - set(file_content.keys())

                    if missing:
                        return (f"Required keys missing in json file: {missing}",False)
                    else:
                        return ("dict",True)

            else:
                missing_string = ""

                for i in range(len(file_content)):
                    if isinstance(file_content[i],dict):
                        missing = _REQUIRED_KEYS - set(file_content[i].keys())
                        if missing:
                            for item in missing:
                                missing_string += f"Question {i+1} is missing {item} keys\n"
                        else:
                            for item in file_content[i]:
                                if isinstance(file_content[i][item],str):
                                    continue
                                else:
                                    missing_string += f"Question {i+1} has wrong datatype in {item} key\n"
                            
                    else:
                        missing_string += f"Question {i+1} is missing {_REQUIRED_KEYS}"

                if not missing_string:
                    return ("list",True)
                else:
                    return (f"Required keys missing:\n{missing_string}",False)

        except Exception as e:
            raise Exception(f"Unexpected Error Occurred while validating JSON file: {e}")              

    async def take_json(self,path):

        try:
            if not os.path.isfile(path):
                raise InvalidInputError("Given path does not exist")

            else:
                file_content = await self.fh_obj.file_read_to_thread(path,"json")
                validation_result = await self._validate_json_keys(file_content)

                if not validation_result[1]:
                    raise InvalidInputError(validation_result[0])
                else:
                    if validation_result[0] == "dict":
                        return await self.add_questions(file_content["question"],file_content["correct_answer"],file_content["option1"],file_content["option2"],file_content["option3"])

                    else:
                        result = []
                        for item in file_content:
                            result.append(await self.add_questions(item["question"],item["correct_answer"],item["option1"],item["option2"],item["option3"]))
                            # list = [item["question"],item["correct_answer"],item["option1"],item["option2"],item["option3"]]
                            # for item in list:
                            #     print(item)
                            # print("\n")
                        return result
        except FileNotFoundError:
            raise

        except InvalidInputError:
            raise

        except Exception as e:
            raise Exception(f"Unexpected Error Occurred while taking json: {e}")

    async def get_question_from_id(self,id):
        
        if id.lower() == "all":
            return self.__question_bank
        else:
            try:
                element = list(filter(lambda x:x["qid"] == id,self.__question_bank))
                if element:
                    return element[0]
                else:
                    raise InvalidInputError(f"No question found with ID: {id}")

            except InvalidInputError:
                raise

            except Exception as e:
                raise Exception(f"Unexpected Error Occurred while taking json: {e}")

    @classmethod      
    async def change_number_of_questions(cls,num):
        try:
            cls.NUMBER_OF_QUESTIONS_PER_QUIZ = num

        except Exception as e:
            raise Exception(f"Unexpected Error Occurred: {e}")


    @classmethod
    async def change_order_of_questions(cls,ids,num=1):
        try:
            if num == 1:
                cls.RANDOMIZE = []
            else:
                cls.RANDOMIZE = ids
                cls.NUMBER_OF_QUESTIONS_PER_QUIZ = len(ids)

        except InvalidInputError:
            raise

        except Exception as e:
            raise Exception(f"Unexpected Error Occurred: {e}")
        
