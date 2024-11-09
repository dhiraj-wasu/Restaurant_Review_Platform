
from django.http import HttpResponse, JsonResponse
import csv
from rest_framework import generics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from backend.serializers import CommentSerializer, CustomerSerializer, ResSerializer
# from .serializers import *
from .models import *
# Create your views here.
from  backend.tasks.task import predictor
from  backend.tasks.task2 import export_comments_to_csv
from django.db import transaction
from rest_framework.decorators import api_view
from .RestaurantLeaderboard import Leaderboard

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
    def post(self, request, *args, **kwargs):
           user=int(request.data["user"])
           res_id=int(request.data["restaurant_id"])
           comment=request.data["comment"]
           data = comments.objects.create(
                                       user_id=customer.objects.get(id=user), 
                                       restaurant_id=restaurant.objects.get(id=res_id),
                                       Review=comment
               )
           export_comments_to_csv(res_id)
           result=predictor.delay(res_id)
           serializer = CommentSerializer(data)
           data.save()
           return JsonResponse({
                    "comment":serializer.data
                         }
                 )
    def get(self, request, *args, **kwargs):
         data= comments.objects.filter( user_id=self.request.user)
         serializer = CommentSerializer(data, many=True)
         return JsonResponse({
                    "comment":serializer.data
                         }
                 )
    
    


class adduser(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
             user_name=request.data["name"]
             user_email=request.data["email"]
             user_password=request.data["pass"]
             data=customer.objects.create(
                             user_name=user_name,
                             user_email=user_email,
                             user_password= user_password,
             ) 
             data.save()
             serializer =CustomerSerializer(data)
             
             return JsonResponse({
                    "comment":serializer.data
                            }
                 )
 #########################################################################
 # restro###############################################   
class addRestro(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
              restaurant_name=request.data["name"]
              restaurant_owner=request.data["owner"]
              owner_number=request.data["phone"]
              owner_email=request.data["email"]
              data=restaurant.objects.create(
                            restaurant_name=restaurant_name,
                            restaurant_owner=restaurant_owner,
                            owner_number=owner_number,
                            owner_email= owner_email,
              ) 
              data.save()
              serializer =  ResSerializer(data)
              return JsonResponse({
                    "comment":serializer.data
                            }
                 )

class GetRestro(generics.ListCreateAPIView):
      serializer_class =  ResSerializer
      def get(self, request, *args, **kwargs):
             

           return super().get(request, *args, **kwargs)
    
    
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
