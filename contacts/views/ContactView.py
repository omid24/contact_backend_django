from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from contacts.models import Contact
from contacts.serializers import ContactSerializer


class ContactView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)


class UserContactView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.method == 'GET':
            user = get_user_model().objects.get(pk=request.user.pk)
            queryset = user.contacts.all()
            return Response(ContactSerializer(queryset, many=True, context={'request': request}).data)
