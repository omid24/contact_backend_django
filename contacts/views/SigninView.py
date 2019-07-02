from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView


class SigninView(APIView):

    def post(self, request, format=None):
        data = request.data
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            return Response(status=200)
        else:
            return Response(status=401)
