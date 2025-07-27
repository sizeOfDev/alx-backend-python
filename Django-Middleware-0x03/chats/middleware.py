from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'

        with open('./chats/requests.log', 'a') as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
            
        # print(f"{datetime.now()} - User: {user} - Path: {request.path}")
    
        resposnse = self.get_response(request)

        return resposnse