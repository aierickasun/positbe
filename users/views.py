from django.shortcuts import render
#import the rest_framework class/methods
from users.serializers import UsersSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class TokenGenerator:
    def token_payload_generator(current_username_id):
        token_payload = { "user_id":current_username_id}
        token, _ = Token.objects.get_or_create(token_payload)
        token_response = {"token":token.key}
        return token_response

class UserLogin(APIView):
    def post(self,request,format = None):
        try:
            serializer = UsersSerializer(data=request.data)
            username, password = serializer.initial_data["username"], serializer.initial_data["password"]
        except:
            invalid_response = {"response":"invalid payload type"}
            return Response(invalid_response,status=status.HTTP_400_BAD_REQUEST)

        valid_user = User.objects.filter(username=username,password=password).exists()
        if valid_user:
            valid_user_id = User.objects.filter(username=username,password=password)[0].id
            token_generated = TokenGenerator.token_payload_generator(valid_user_id)
            return Response(token_generated,status=status.HTTP_201_CREATED)
        else:
            invalid_response = {"response":"username or password is incorrect or does not exist"}
            return Response(invalid_response,status=status.HTTP_400_BAD_REQUEST)

class UserRegistration(APIView):
    def post(self,request,format = None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.data["username"]
            current_username = User.objects.filter(username=username)
            current_username_id = current_username[0].id
            token_generated = TokenGenerator.token_payload_generator(current_username_id)
            return Response(token_generated, status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
# Create your views here.
