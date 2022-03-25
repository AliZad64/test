from typing import List
from ninja import  Field, Schema
from employee.models import Employee, FileGroup
#any class schema created in this file will change our outputs as json response
class FilesOut(Schema):
    name: str

class EmployeeOut(Schema):
    name: str
    # here we bring the files from FileGroup model and output it
    # as list(array) in json response
    files: List[FilesOut] = Field(None, alias="filess")

#this schema just for showing error messages
class MessageOut(Schema):
    message: str