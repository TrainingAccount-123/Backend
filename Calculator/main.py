from arithmetic import Arithmetic
import asyncio

import sys

async def valid_input(nth):
    while True:
        try:
            inp = float(input(f"Enter the {nth} number:"))
        except ValueError as ve:
            print(f"Invalid Input: Provided value is not a number. Please Try Again\n.{ve}")
        except Exception as e:
            print(f"Unexpected Error Occured: {e}")
        else:
            return inp
        

async def main():
    arithmetic_obj = Arithmetic()
    while True:
        choice = input("""
            Available Choices:
            1 - Addition
            2 - Subtraction
            3 - Multiplication
            4 - Division
            5 - Exit
            Enter one of the above choices: """)
        print("\n")

        try:
            match choice:

                case "1":
                    num1 = await valid_input("first")
                    num2 = await valid_input("second")
                    print(f"{num1} + {num2} = {await arithmetic_obj.add([num1,num2])}")

                case "2":
                    num1 = await valid_input("first")
                    num2 = await valid_input("second")
                    print(f"{num1} - {num2} = {await arithmetic_obj.subtract([num1,num2])}")

                case "3":
                    num1 = await valid_input("first")
                    num2 = await valid_input("second")
                    print(f"{num1} * {num2} = {await arithmetic_obj.multiply([num1,num2])}")

                case "4":
                    num1 = await valid_input("first")
                    num2 = await valid_input("second")
                    print(f"{num1} / {num2} = {await arithmetic_obj.divide([num1,num2])}")
                
                case "5":
                    print("Closing System, Thank You")
                    break

                case _ :
                    print("Invalid Input: Enter one of the choices.")

        except ZeroDivisionError as zde:
            print(f"Invalid Input: Denominator cannot be zero {zde}\n")

        except Exception as e:
            print(f"Unexpected Error Occured: {e}")
        
        while True:
            exit_choice = input("Do you wish to continue? (y/n): ")
            if exit_choice.lower() == "y":
                break
            elif exit_choice.lower() == "n":
                print("Closing System, Thank You")
                sys.exit()
            else:
                print("Invalid Input, Please Enter (y/n)")
                continue

if __name__ == "__main__":
    asyncio.run(main())
