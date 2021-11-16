from os import get_exec_path
import shutil
from fastapi import UploadFile
import uuid


class UploadFileSteam:
    def __init__(self, file: UploadFile, generate_file_method = "UUID"):
        self.gen_method = generate_file_method
        self.file = file
        
    def upload(self):
        with open(f"{self.file.filename}", "wb") as buffer:
            shutil.copyfileobj(self.file.file, buffer)
            file_name_response = self.generateUniqueName() + "-" + self.file.filename
            shutil.move(self.file.filename, "static/" + file_name_response)
        return file_name_response

    def generateUniqueName(self):
        return self.uniqueIdGenerate()

    def uniqueIdGenerate(self):
        if self.gen_method  == "UUID":
            return str(uuid.uuid1())
        return self.file.filename