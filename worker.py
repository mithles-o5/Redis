import os
import django
import redis #allows to import redis-client library
import time
import ast #ast - Abstract Syntax Tree module.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoredis.settings')  
django.setup() #initialize the django env, loads all the settings,databases,models etc.

from recipe.models import Recipe

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=1) #StrictRedis - It validates and throws error, if something invalid.

def process_queue_task(task):
    recipe_id = task.get('recipe_id')
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        
        name = f"Task for {recipe.name}"
        print(f"Task processesd for {recipe.name}")
        
    except Recipe.DoesNotExist:
        print(f"Recipe with ID {recipe_id} not found.")

def worker():
    while True:
        task_data = redis_client.blpop('task_queue') #blpop will blocks and waits until there is task in the task queue.
        print("Task data at position 0",task_data[0])
        print("Task data at position 1",task_data[1])
        task = ast.literal_eval(task_data[1].decode('utf-8')) #converts the string into the python object
        
        print(f"Processing task: {task}")
        process_queue_task(task)
        
        time.sleep(1)

if __name__ == '__main__':
    worker()