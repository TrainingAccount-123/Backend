from services.exception import InvalidInputError

class Users:
    """
    Class should only be initialized with the following step to preserve async:
    class_obj = await Users.create(file_handler_obj)
    """

    __DB_PATH = "C:/Users/SkandaSankarRaman/OneDrive - GapBlue Software Labs Pvt Ltd/Work/live_coding/Quiz_Api/databases/users.csv"
    
    def __init__(self,database,fh_obj):
        self.__database = database
        self._fh_obj = fh_obj

    @classmethod
    async def create(cls,fh):
        db = await fh.file_read_to_thread(cls.__DB_PATH,"csv")
        return cls(db,fh)

    async def add_user(self,username,password,status):
        try:
            self.__database.append({"username":username,"password":password,"status":status})
            await self._fh_obj.file_write_to_thread(self.__DB_PATH,self.__database,"csv")
        except Exception as e:
            raise Exception(f"Unexpected error occurred while adding user: {e}")
        

    async def remove_user(self,username):
        try:
            element = list(filter(lambda x:x["username"].lower() == username.lower(),self.__database))
            if element:
                self.__database.remove(element[0])
                await self._fh_obj.file_write_to_thread(self.__DB_PATH,self.__database,"csv")
            else:
                raise InvalidInputError("Username Does Not Exist")

        except InvalidInputError:
            raise

        except Exception as e:
            raise Exception(f"Unexpected error occurred while removing user: {e}")

    async def change_password(self,username,new_password):
        try:
            element = list(filter(lambda x:x["username"].lower() == username.lower(),self.__database))
            if element:
                index = self.__database.index(element[0])
                self.__database[index]["password"] = new_password
                await self._fh_obj.file_write_to_thread(self.__DB_PATH,self.__database,"csv")
            else:
                raise InvalidInputError("Username Does Not Exist")

        except InvalidInputError:
            raise

        except Exception as e:
            raise Exception(f"Unexpected error occurred while changing password: {e}")

    async def get_user_status(self,username):
        try:
            element = list(filter(lambda x:x["username"].lower() == username.lower(),self.__database))
            if element:
                return element[0]["status"]
            else:
                raise InvalidInputError("Username Does Not Exist")

        except InvalidInputError:
            raise

        except Exception as e:
            raise Exception(f"Unexpected error occurred while getting user status: {e}")

    async def login(self,username,password):
        try:
            element = list(filter(lambda x:x["username"].lower() == username.lower(),self.__database))
            if element:
                if element[0]["password"] == password:
                    return f"Login Successful, Welcome {username}"
                else:
                    return "Invalid username or password entered"
            else:
                return "Invalid username or password entered"

        except Exception as e:
            raise Exception(f"Unexpected error occurred while logging in: {e}")
