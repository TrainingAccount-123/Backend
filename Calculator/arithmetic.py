from functools import reduce
class Arithmetic:

    @staticmethod
    async def add(nums):

        try:
            sum = reduce(lambda acc, x: acc + x, nums, 0.0)
        except Exception as e:
            raise Exception(f"arithmetic.py : {e}") from e
        else:
            return sum

    @staticmethod
    async def subtract(nums):

        try:
            difference = reduce(lambda acc, x: acc - x, nums, 0.0)
        except Exception as e:
            raise Exception(f"arithmetic.py : {e}") from e
        else:
            return difference
    
    @staticmethod
    async def multiply(nums):

        try:
            product = reduce(lambda acc, x: acc * x, nums, 0.0)
        except Exception as e:
            raise Exception(f"arithmetic.py : {e}") from e
        else:
            return product

    @staticmethod
    async def divide(nums):
        
        try:
            quotient = reduce(lambda acc, x: acc/x, nums, 0.0)
        except ZeroDivisionError as zde:
            raise ZeroDivisionError(f"Error: Division by 0 is not allowed {zde}") from zde
        except Exception as e:
            raise Exception(f"arithmetic.py : {e}") from e
        else:
            return quotient