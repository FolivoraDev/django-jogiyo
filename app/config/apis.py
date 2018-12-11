from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from members.tasks import my_send_email


class SendEmailView(APIView):

    def get(self, request):
        return Response('hi')

    def post(self, request, format=None):
        result = my_send_email.delay()
        print(result)
        return HttpResponse(result)
