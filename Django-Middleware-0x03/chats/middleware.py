from datetime import datetime

from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'

        with open('requests.log', 'a') as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
            
        # print(f"{datetime.now()} - User: {user} - Path: {request.path}")
    
        resposnse = self.get_response(request)

        return resposnse
    
class RestrictAccessByTimeMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        user = request.user if request.user.is_authenticated else 'Anonymous'
        
        current_time = datetime.now().time()


        start_time = datetime.strptime("06:00", "%H:%M").time()
        end_time = datetime.strptime("21:00", "%H:%M").time()

        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access restricted ( 6PM - 9PM)", status=403)

        response = self.get_response(request)
        
        return response