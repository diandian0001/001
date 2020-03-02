from django.db import models

# Create your models here.
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class MyMiddleWare(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    @staticmethod
    def process_request(request):
        if 'indent' in request.path:
            session = request.session
            if session.get('account'):
                # money = session.get('addr')
                # # print(money)
                # if money:
                #     pass
                # else:
                pass
                # return redirect('dang:show_index')
            else:
                return redirect('dang:login')