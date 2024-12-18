class ApiError :
    def __init__(self,statusCode,errorMessage) -> None:
        self.statusCode = statusCode
        self.errorMessage = errorMessage
    def to_dict(self):
        return {
            'status_code': self.statusCode,
            'error_message': self.errorMessage
        }

    # Class modified methods which implites in class instead of instance of class
    @classmethod
    def bad_request(cls, message="Bad Request"):
        return cls(400, message).to_dict()
    
    @classmethod
    def internal_server_error(cls,message="Internal Server Error"):
        return cls(500,message).to_dict()
    
    def not_found(cls, message="Not Found"):
        return cls(404, message).to_dict()