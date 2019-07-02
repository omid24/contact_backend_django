from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contacts.models import Contact
from contacts.serializers import ContactSerializer, UserSerializer


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
            """ Create new contact """
            contactSerializer = ContactSerializer(data=request.data)
            if contactSerializer.is_valid():
                contactSerializer.save()
        else:
            """ Update contact """
            contactSerializer = ContactSerializer(contactObj, data=request.data)
            if contactSerializer.is_valid():
                contactSerializer.save()

            user.contacts.add(contactObj)
            user.save()
            return Response(status=201)


# class AddContactForUser(CreateAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = ContactSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def create(self, request, *args, **kwargs):
#
#         serializer = self.get_serializer(data=request.data)
#         phone_number = serializer.initial_data.get('phone_number')
#
#         contactObj = Contact.objects.filter(phone_number=phone_number).first()
#         if not contactObj:
#             """ Create new contact """
#             # contactSerializer = ContactSerializer(data=request.data)
#             # if contactSerializer.is_valid():
#             #     contactSerializer.save()
#             serializer.is_valid(raise_exception=True)  # Check Validation serializers
#             self.perform_create(serializer)
#         else:
#             """ Update contact """
#             contactSerializer = ContactSerializer(contactObj, data=request.data)
#             if contactSerializer.is_valid():
#                 contactSerializer.save()
#
#         """ Add contact for user """
#         user = get_user_model().objects.filter(pk=request.user.pk).first()
#         print(user)
#         user.contacts.add(contactObj)
#         user.save()
#
#         serializer.is_valid(raise_exception=True)  # Check Validation serializers
#         headers = self.get_success_headers(serializer.data)
#         return Response(headers=headers)
#
#     def perform_create(self, serializer):
#         serializer.save()
