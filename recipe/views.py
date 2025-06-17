from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.core.cache import cache 
# Create your views here.
from .models import *
import redis
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def recipeview(request):
    queryset = Recipe.objects.all()
    
    return render(request,'home.html',{'recipes':queryset})

def recipe_view(request, pk):
    recipe = cache.get(pk) #gets the recipe id from cache if no id is present, returns none
    print(recipe)
    if not recipe:
        try:
            recipe = get_object_or_404(Recipe, pk=pk) #if there is no recipe in cache(for that pk), it gets the object from the database 
            cache.set(pk, recipe,timeout=10) #sets the key(pk) and value(recipe) in cache and removes it automatically from cache after 10s
            print("hit the db")
        except Recipe.DoesNotExist:
            return HttpResponse("This Recipe Doesnot Exists")
              
    else:
        print("hit the cache")
    
    context = {"recipe":recipe}
    
    return render(request,"recipe.html",context)


redis_client = redis.Redis(host='127.0.0.1', port=6379, db=1)  #creates a connection to the redis (Here redis - py package and Redis is the class in it)
@api_view(['POST'])
def push_task_to_queue(request):
    serializer = TaskSerializer(data=request.data)
    
    if serializer.is_valid():
        
        recipe_id = serializer.validated_data['recipe_id']
        
        task = {'recipe_id': recipe_id}
        redis_client.rpush('task_queue', str(task))  #here the task is pushed at the right end of the queue. Here we are converting it to string because,Redis can't handle python dictionary(So we are serializing it)
        
        return Response({"message": "Task added to queue"}, status=status.HTTP_201_CREATED)
    
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)