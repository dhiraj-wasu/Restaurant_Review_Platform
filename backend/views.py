
from django.http import HttpResponse, JsonResponse
import csv
from rest_framework import generics
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from backend.serializers import CommentSerializer, CustomerSerializer, ResSerializer,updateCommentSerializer
# from .serializers import *
from .models import *
# Create your views here.
from  backend.tasks.task import predictor
from  backend.tasks.task2 import export_comments_to_csv
from django.db import transaction
from rest_framework.decorators import api_view
from .RestaurantLeaderboard import Leaderboard
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db import transaction

class analysis(generics.ListCreateAPIView):
     def post(self, request, *args, **kwargs):
            res_id=int(request.data["restaurant_id"])
            if(predictor(res_id) == 1):
             return JsonResponse({
              "result":"done"
             })
            else:
               return JsonResponse({
              "result":"error"
             })
     


class addcomment(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    # def post(self, request, *args, **kwargs):
    #        user=int(request.data["user"])
    #        print(user)
    #        res_id=int(request.data["restaurant_id"])
    #        comment=request.data["comment"]
    #        data = comments.objects.create(
    #                                    user_id=M_User.objects.get(id=user),
    #                                    restaurant_id=restaurant.objects.get(id=res_id),
    #                                    Review=comment 
    #            )
    #        export_comments_to_csv(res_id)
    #        result=predictor.delay(res_id)
    #        serializer = CommentSerializer(data)
    #        data.save()
    #        return JsonResponse({
    #                 "comment":serializer.data
    #                      }
    #              )
    def post(self, request, *args, **kwargs):
        user = int(request.data["user_id"])
        res_id = int(request.data["restaurant_id"])
        comment = request.data["Review"]
    
        try:
        # Wrap the entire process in an atomic transaction block
          with transaction.atomic():
            # Create the comment record
            data = comments.objects.create(
                user_id=M_User.objects.get(id=user),
                restaurant_id=restaurant.objects.get(id=res_id),
                Review=comment
            )
            
            # Export comments to CSV (optional, depending on its purpose)
            export_comments_to_csv(res_id)
            
            # Call the async function with Celery
            result = predictor.delay(res_id)
            if result==1:
                raise Exception("Testing rollback - intentional error")
            # Serialize the comment object to return it as a response
            serializer = CommentSerializer(data)
            
            return JsonResponse({
                "comment": serializer.data
            })
    
    # Handle any exceptions that may occur, and automatically roll back
        except Exception as e:
        # Log or print the error for debugging if needed
            print("An error occurred:", e)
        
        # Return an error response
        return JsonResponse({
            "error": "An error occurred while processing your request."
        }, status=500)
    

    def get(self, request, *args, **kwargs):
         data= comments.objects.filter(user_id=self.request.user)
         serializer = CommentSerializer(data, many=True)
         return JsonResponse({
                    "comment":serializer.data
                        }
                 )
class Update_delete_comment(generics.RetrieveUpdateDestroyAPIView):
       queryset = comments.objects.all()
       serializer_class = updateCommentSerializer


# from rest_framework_simplejwt.tokens import RefreshToken

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }





class adduser(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
             user_name=request.data["name"]
             user_email=request.data["email"]
             user_password=request.data["pass"]
             usertype=request.data["type"]
             username=request.data["username"]
             if M_User.objects.filter(email=user_email).exists():
                user=M_User.objects.get(email=user_email)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
               'user':{
               'token': token.key,
               'user_id': user.pk,
               'username':user.full_name,
               'usertype':user.usertype,
               'email':user.email,
               'password':user.password
               }
              })
             else:
                 data=M_User.objects.create(
                             full_name=user_name,
                             usertype= usertype,
                             email=user_email,
                             password= user_password,
                             username=username,
                             
                    ) 
                 user=M_User.objects.get(email=user_email)
                 token, created = Token.objects.get_or_create(user=user)
                 data.save()
                 return Response({
               'user':{
               'token': token.key,
               'user_id': user.pk,
               'full_name':user.full_name,
               'User_name':user.username,
               'usertype':user.usertype,
               'email':user.email,
               'password':user.password
               }
              })
             

class login(generics.ListCreateAPIView): 
      def post(self, request, *args, **kwargs):
            user_email=request.data["email"]
            user_password=request.data["pass"]
            if M_User.objects.filter(email=user_email,password=user_password).exists():
                user=M_User.objects.get(email=user_email,password=user_password)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
               'user':{
               'token': token.key,
               'user_id': user.pk,
               'full_name':user.full_name,
               'User_name':user.username,
               'usertype':user.usertype,
               'email':user.email,
               'password':user.password
               }
              })
            else:
                return JsonResponse({
                    "comment":"Wrong Password"
                            }
                 )

 #########################################################################restro#
 ######################################################################################################################  

class addRestro(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    def post(self, request, *args, **kwargs):
              user=request.data["user"]
              restaurant_name=request.data["name"]
              restaurant_owner=request.data["owner"]
              owner_number=request.data["phone"]
              owner_email=request.data["email"]
              address=request.data["address"]
              desc=request.data["desc"]
              data=restaurant.objects.create(
                            user=M_User.objects.get(id=user),
                            restaurant_name=restaurant_name,
                            restaurant_owner=restaurant_owner,
                            owner_number=owner_number,
                            owner_email= owner_email,
                            restaurant_desc=desc,
                            restaurant_address=address,
              ) 
              data.save()
              serializer =  ResSerializer(data)
              return JsonResponse({
                    "comment":serializer.data
                            }
                 )

    def get(self, request):
        queryset = restaurant.objects.filter(user=self.request.user)
        serializer = ResSerializer(queryset, many=True)
        return JsonResponse({"Restaurant":serializer.data}, safe=False) 


class allRestro(generics.ListCreateAPIView):
      serializer_class =  ResSerializer
      def get(self, request, *args, **kwargs):
          queryset = restaurant.objects.all()
          serializer = ResSerializer(queryset, many=True)
          return JsonResponse({"Restaurant":serializer.data}, safe=False) 
    
    
def leaderboard_view(request):
    leaderboard = Leaderboard()
    
    # Fetch the top 10 restaurants
    top_restaurants = leaderboard.get_all_scores()
    print(top_restaurants)
    # Prepare the leaderboard data for the JSON response
    leaderboard_data = [
         {"restaurant_id": restaurant_id.decode('utf-8'), "score": score}
        for restaurant_id, score in  top_restaurants
    ]
   
    return JsonResponse({
        "leaderboard":  leaderboard_data
    }, status=200)
