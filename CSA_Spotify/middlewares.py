from django.contrib.auth.middleware import get_user
from django.http import response
from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

EXCLUDE_FROM_MIDDLEWARE = []

class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print(request.META['HTTP_AUTHORIZATION'])
        request.user = SimpleLazyObject(lambda:self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JSONWebTokenAuthentication()
        if jwt_authentication.get_jwt_value(request):
            user, jwt = jwt_authentication.authenticate(request)
        return user

class AuthorizationMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = '.'.join((view_func.__module__, view_func.__name__))
        if view_name in EXCLUDE_FROM_MIDDLEWARE:
            return None
    
    def __call__(self, request):
        token = request.COOKIES.get('Orgasmic_Rays')
        # print("token" , token)
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        return self.get_response(request)
