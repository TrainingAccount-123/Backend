import csv
import json
import asyncio
from pathlib import Path


class FileHandler:

    def __init__(self):
        self._lock = asyncio.Lock()

    
    async def _validate_extension(self,path, expected):
        p = Path(path)

        if not p.suffix:
            raise FileNotFoundError(f"No file extension provided for path: {path}")

        if p.suffix.lower() != f".{expected.lower()}":
            raise FileNotFoundError(
                f"Invalid file extension. Expected .{expected}, got {p.suffix}"
            )


    def load_json(self, path_to_json):
        
        try:

            with open(path_to_json, "r") as f:
                content = json.load(f)
                if content:
                    return content
                else:
                    return []
        
        except FileNotFoundError as fnfe:
            raise FileNotFoundError(f"JSON File was not found while reading : {fnfe}")
        
        except Exception as e:
            raise Exception(f"Unexpected Error Occurred while reading JSON: {e}")

    def load_csv(self, path_to_csv):

        if path_to_csv[-4:] != ".csv":
                raise FileNotFoundError("File has wrong extension")
                
        try:
            with open(path_to_csv, "r", newline="") as f:
                loaded = csv.DictReader(f)
                rows = list(loaded)
                return rows
   
        except FileNotFoundError as fnfe:
            raise FileNotFoundError(f"CSV File was not found while reading : {fnfe}")
   
        except Exception as e:
            raise Exception(f"Unexpected Error Occurred while reading CSV: {e}")

    def write_to_csv(self, path_to_csv, data):
   
        if data != []:
            headers = data[0].keys()
            try:
                with open(path_to_csv,"w",newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
   
                    for row in data:
                        writer.writerow(row)
   
            except FileNotFoundError as fnfe:
                raise FileNotFoundError(f"CSV File was not found while writing : {fnfe}")
   
            except Exception as e:
                raise Exception(f"Unexpected Error Occurred while writing CSV: {e}")

        else:
            try:
                with open(path_to_csv,"w",newline="") as f:
                    pass
   
            except FileNotFoundError as fnfe:
                raise FileNotFoundError(f"CSV File was not found while writing : {fnfe}")

            except Exception as e:
                raise Exception(f"Unexpected Error Occurred while writing CSV: {e}")

    def write_to_json(self, path_to_json, data):

        try:
            if data:
                with open(path_to_json,"w") as f:
                    json.dump(data,f,indent=4)
            
            else:
                with open(path_to_json,"w") as f:
                    json.dump([],f,indent=4)

        except FileNotFoundError as fnfe:
            raise FileNotFoundError(f"JSON File was not found while writing : {fnfe}")

        except Exception as e:
                raise Exception(f"Unexpected Error Occurred while writing JSON: {e}")

    async def file_read_to_thread(self, path_to_file, filetype):
        try:

            try:
                await self._validate_extension(path_to_file,filetype)
            except FileNotFoundError:
                raise

            async with self._lock:
                if filetype.lower() == "json":
                    return await asyncio.to_thread(self.load_json,path_to_file)
                elif filetype.lower() == "csv":
                    return await asyncio.to_thread(self.load_csv,path_to_file)
                else:
                    raise ValueError
        
        except FileNotFoundError:
            raise

        except Exception:
            raise 

    async def file_write_to_thread(self, path_to_file, data, filetype):
        try:

            try:
                await self._validate_extension(path_to_file,filetype)
            except FileNotFoundError:
                raise

            async with self._lock:
                if filetype.lower() == "json":
                    await asyncio.to_thread(self.write_to_json,path_to_file,data)
                elif filetype.lower() == "csv":
                    await asyncio.to_thread(self.write_to_csv,path_to_file,data)
                else:
                    raise ValueError

        except FileNotFoundError:
            raise

        except Exception:
            raise
