class UserNotFondError (Exception):
    pass

class EmployeeNotFoundError (Exception):
    pass

class DeleteError(Exception):
    def __init__(self):
        return 'error the employee could not be deleted' 
       
    