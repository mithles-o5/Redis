---
title: What is inside the worker.py
---
# Introduction

This document will walk you through the key components of the <SwmPath>[worker.py](/worker.py)</SwmPath> file. The purpose of this file is to manage tasks from a Redis queue and process them using Django models.

We will cover:

1. How tasks are retrieved from the Redis queue.
2. How tasks are processed using Django models.
3. Error handling for tasks with invalid data.

# Retrieving tasks from the Redis queue

<SwmSnippet path="/worker.py" line="25">

---

The worker function is designed to continuously retrieve tasks from a Redis queue. It uses the <SwmToken path="/worker.py" pos="27:7:7" line-data="        task_data = redis_client.blpop(&#39;task_queue&#39;) #blpop will blocks and waits until there is task in the task queue.">`blpop`</SwmToken> method to block and wait until a task is available in the queue. This ensures that the worker is always ready to process tasks as soon as they arrive.

```
def worker():
    while True:
        task_data = redis_client.blpop('task_queue') #blpop will blocks and waits until there is task in the task queue.
        print("Task data at position 0",task_data[0])
        print("Task data at position 1",task_data[1])
        task = ast.literal_eval(task_data[1].decode('utf-8')) #converts the string into the python object
        
        print(f"Processing task: {task}")
        process_queue_task(task)
```

---

</SwmSnippet>

# Processing tasks using Django models

<SwmSnippet path="/worker.py" line="10">

---

Once a task is retrieved, it is processed by extracting the <SwmToken path="/worker.py" pos="15:1:1" line-data="    recipe_id = task.get(&#39;recipe_id&#39;)">`recipe_id`</SwmToken> and fetching the corresponding <SwmToken path="/worker.py" pos="10:8:8" line-data="from recipe.models import Recipe">`Recipe`</SwmToken> object from the database. This is done using Django's ORM, which allows for efficient querying and manipulation of database records.

```
from recipe.models import Recipe

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=1) #StrictRedis - It validates and throws error, if something invalid.

def process_queue_task(task):
    recipe_id = task.get('recipe_id')
    try:
        recipe = Recipe.objects.get(id=recipe_id)
```

---

</SwmSnippet>

# Task processing details

<SwmSnippet path="/worker.py" line="19">

---

After fetching the <SwmToken path="/worker.py" pos="10:8:8" line-data="from recipe.models import Recipe">`Recipe`</SwmToken> object, the task is processed, and a message is printed to indicate the completion of the task for the specific recipe.

```
        name = f"Task for {recipe.name}"
        print(f"Task processesd for {recipe.name}")
```

---

</SwmSnippet>

# Error handling for invalid tasks

<SwmSnippet path="/worker.py" line="22">

---

If the <SwmToken path="/worker.py" pos="22:3:3" line-data="    except Recipe.DoesNotExist:">`Recipe`</SwmToken> object does not exist for the given <SwmToken path="/worker.py" pos="23:12:12" line-data="        print(f&quot;Recipe with ID {recipe_id} not found.&quot;)">`recipe_id`</SwmToken>, an error message is printed. This ensures that any invalid tasks are logged and can be addressed without causing the worker to crash.

```
    except Recipe.DoesNotExist:
        print(f"Recipe with ID {recipe_id} not found.")
```

---

</SwmSnippet>

# Worker execution

<SwmSnippet path="/worker.py" line="38">

---

The worker function is executed when the script is run directly. This setup allows the worker to start processing tasks immediately upon execution.

```
    worker()
```

---

</SwmSnippet>

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBUmVkaXMlM0ElM0FtaXRobGVzLW81" repo-name="Redis"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
