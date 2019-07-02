from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from contacts.serializers import UserSerializer


class SignupView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """ Custom response for CreateApiView's class """
        serializer = self.get_serializer(data=request.data)
        username = serializer.initial_data.get('username')  # Get username before save user

        """ if user has already registered, redirect into signup """
        userObj = get_user_model().objects.filter(username=username).first()
        if userObj:
            return Response({'error': 'The user has already registered'}, status=status.HTTP_200_OK)  # Custom Response

        serializer.is_valid(raise_exception=True)  # Check Validation serializers
        self.perform_create(serializer)  # Save user with serializer
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.filter(user__username=username).first()  # Get token of username
        return Response({'token': str(token)}, headers=headers)

    def perform_create(self, serializer):
        """ Set token and save user """
        user = serializer.save()  # User save
        password = serializer.initial_data.get('password')
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)  # Create token


""" Signup With APIView """
# class SignupView(APIView):
#
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         username = data.get('username')
#         first_name = data.get('first_name')
#         last_name = data.get('last_name')
#         phone_number = data.get('phone_number')
#         password = data.get('password')
#
#         """ Check Json """
#         if not data:
#             return Response({'error': 'Json not found'}, status=400)
#
#         if not first_name:
#             return Response({'error': 'First_name not found in json'}, status=400)
#
#         if not last_name:
#             return Response({'error': 'Last_name not found in json'}, status=400)
#
#         if not phone_number:
#             return Response({'error': 'Phone_number not found in json'}, status=400)
#
#         if not username:
#             return Response({'error': 'username not found in json'}, status=400)
#
#         user = get_user_model().objects.filter(username=username).first()
#         if user:
#             return Response({'error': 'user is exist'}, status=status.HTTP_403_FORBIDDEN)
#
#         userObj = get_user_model().objects.create(username=username,
#                                                   first_name=first_name,
#                                                   last_name=last_name,
#                                                   phone_number=phone_number,
#                                                   password=password)
#
#         userSerializer = UserSerializer(data=request.data)
#         if userSerializer.is_valid():
#             userSerializer.save()
#
#         token = Token.objects.create(user=userObj)
#         return Response({'token': str(token)}, status=status.HTTP_201_CREATED)
