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
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
         self.get_response = get_response
         self.request = {}

    def __call__(self, request):

        if request.method == 'POST':
            ip_address = request.META.get('REMOTE_ADDR')
            current_time = datetime.now().time()

            if ip_address in self.request:
                last_request_time, request_count = self.request[ip_address]
                if (current_time.hour - last_request_time.hour) * 60 + (current_time.minute - last_request_time.minute) < 1:
                    return HttpResponseForbidden("You are making requests too frequently.", status=429)
                else:
                    if request_count >= 5:
                        return HttpResponseForbidden("You have exceeded the request limit.", status=429)
                    self.request[ip_address] = (last_request_time, request_count + 1)
            else:
                self.request[ip_address] = (current_time, 1)

        response = self.get_response(request)

        return response
    
class RolepermissionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        
        if request.user.is_authenticated:
            if not (request.user.groups.filter(name='admin').exists() or request.user.groups.filter(name='moderator').exists()):
                return HttpResponseForbidden("You do not have permission to perform this action.")

        response = self.get_response(request)
        return response