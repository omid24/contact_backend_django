from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets, serializers
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contacts.models import Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'username', 'phone_number', 'image',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'image',)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('image',)


class AddContactForUser(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')

        """ Check Json """
        if not data:
            return Response({'error': 'Json not found'}, status=400)

        if not first_name:
            return Response({'error': 'First_name not found in json'}, status=400)

        if not last_name:
            return Response({'error': 'Last_name not found in json'}, status=400)

        if not phone_number:
            return Response({'error': 'Phone_number not found in json'}, status=400)

        user = get_user_model().objects.filter(pk=request.user.pk).first()
        if not user:
            return Response({'error': 'user not found in json'}, status=404)

        contactObj = Contact.objects.filter(phone_number=phone_number).first()
        if not contactObj:
            contactObj = Contact.objects.create(first_name=first_name, last_name=last_name, phone_number=phone_number)
        # contactObj =Contact.objects.filter(id=contactObj.pk).first()
        # print(contactObj)

        """ Save Image for contact """
        contactImageSerializer = ContactSerializer(contactObj, data=request.data)
        if contactImageSerializer.is_valid():
            contactImageSerializer.save()

        user.contacts.add(contactObj)
        user.save()
        return Response(status=201)


class UserContactView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.method == 'GET':
            user = get_user_model().objects.get(pk=request.user.pk)
            queryset = user.contacts.all()
            print(queryset)
            return Response(ContactSerializer(queryset, many=True, context={'request': request}).data)


class SignupView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')
        password = data.get('password')

        """ Check Json """
        if not data:
            return Response({'error': 'Json not found'}, status=400)

        if not first_name:
            return Response({'error': 'First_name not found in json'}, status=400)

        if not last_name:
            return Response({'error': 'Last_name not found in json'}, status=400)

        if not phone_number:
            return Response({'error': 'Phone_number not found in json'}, status=400)

        if not username:
            return Response({'error': 'username not found in json'}, status=400)

        user = get_user_model().objects.filter(username=username).first()
        if user:
            return Response({'error': 'user is exist'}, status=status.HTTP_403_FORBIDDEN)

        userObj = get_user_model().objects.create(username=username,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  phone_number=phone_number,
                                                  password=password)

        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid():
            userSerializer.save()

        token = Token.objects.create(user=userObj)
        return Response({'token': str(token)}, status=status.HTTP_201_CREATED)


class SignupView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    # permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """ Set token and save user """
        user = serializer.save()
        token = Token.objects.create(user=user)

    def create(self, request, *args, **kwargs):
        """ Custom response for CreateApiView's class """
        serializer = self.get_serializer(data=request.data)
        username = serializer.initial_data.get('username')

        """ if user has already registered, redirect into signup """
        userObj = get_user_model().objects.filter(username=username).first()
        if userObj:
            return Response({'error': 'The user has already registered'}, status=status.HTTP_200_OK)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # if serializer.is_valid():
        #     user = serializer.save()
        token = Token.objects.filter(user__username=username).first()

        return Response({'token': str(token)}, headers=headers)

        # return Response({'error': 'UserSerializer is not valid'}, status=400)
