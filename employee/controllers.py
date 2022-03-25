from encodings import utf_8
from ninja import File, Router, UploadedFile
from employee.models import Employee, FileGroup
from employee.schemas import EmployeeOut, MessageOut
from typing import List
import json
import os
files_controller = Router(tags=['files'])


# we create the endpoint for the api here where first line will be output response thats taken from schemas file (check schemas file)
# second line is the input where we are going to input text file inside the function parameter
@files_controller.post('post_file', response= {
    201: List[EmployeeOut], 
    400: MessageOut})
def post_file(request,file: UploadedFile = File(...)):
    try:
        #first change the text file to JSON format but since the text type is from word document then it will be problem because we will need
        #to encode the text file as utf-8 to get rid of annoying word doc symbols
        raw_data = str(file.read(), 'utf-8')
        raw_data = raw_data.replace('“', '"')
        raw_data = raw_data.replace('”', '"')

        #now we can change text file to JSON format as a list of dict in python
        json_data = json.loads(raw_data)

        
        # iterate the list to input the info in database
        for info in json_data:
            file_name = list(info.keys())[0]
            employee_name = list(info.values())[0]
            
            # we check if there is employee with that name already made in the database so we don't end up making duplicate employees
            employee = Employee.objects.filter(name = employee_name).values()
            print(employee)
            if not employee and employee != "":
                # this creates us new employee in the database
                employee = Employee.objects.create(name = employee_name)
            employee = Employee.objects.get(name = employee_name)
            
            # we also check if there is file with the same title in the database, i would like to update the file but right now there is no info
            # to add to the file and its just a name
            file_check = FileGroup.objects.filter(name = file_name, employee_id = employee.id).select_related('employee')
            if not file_check and file_check != "":
                file_create = FileGroup.objects.create(name = file_name, employee_id = employee.id)
        
        all_employee = Employee.objects.all()
        return 201, all_employee
    except:
        return 400, {"message": "enter text file or enter text file that has an array of objects"}
    

@files_controller.get("all_employees", response= {
    200: List[EmployeeOut],
    404: MessageOut
})
def all_employees(request):
    all_employee = Employee.objects.all()
    if all_employee:
        return 200, all_employee
    return 404, {"message": "there are no employees"}
