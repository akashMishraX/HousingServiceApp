class ApiResponse:
    def __init__(self,statusCode,responseMessage,responseData=None) -> None:
        self.statusCode = statusCode
        self.responseMessage = responseMessage
        self.responseData = responseData

    def to_dict(self):
        response_dict = {
            'status_code': self.status_code,
            'response_message': self.response_message
        }
        if self.responseData is not None:
            response_dict['response_data'] = self.responseData
        return response_dict


    # Class modified methods which implites in class instead of instance of class
    @classmethod
    def success(cls, message="Success", data=None):
        return cls(200, message, data)
    
    @classmethod
    def created(cls, message="Created", data=None):
        return cls(201, message, data)
  
    @classmethod
    def no_content(cls,message='"No Content"'):
        return cls(204, message)