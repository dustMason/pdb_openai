# Pdb + GPT-4

A wrapper around the standard Python debugger `Pdb` that adds 3 special commands for interacting with OpenAI's models.

## Installation

```
pip install pdb_openai
```

## Configuration

Your OpenAI API key should be available in the `OPENAI_API_KEY` env var. Alternatively, you can pass an api key as an
argument to the `stop` function which triggers a breakpoint in your code.

## Usage

Use this debugger similar to how you would invoke pdb:

```
from pdb_openai import debug; debug.stop()
```

Once in the session, you can use 3 new commands in addition to the standard pdb workflow. As you interact with the
debugger, the session history including input, output and errors are stored in memory. When any of the commands below
are invoked, the model gets a transcript of the session in addition to your prompt.

## gen

```
(Pdb OpenAI) gen a 5 line greeter function with randomness
import random
def greet():
    names = ["Alice", "Bob", "Charlie", "Diana", "Edward"]
    greeting = ["Hello", "Hi", "Hey", "Greetings", "What's up"]
    print(f"{random.choice(greeting)}, {random.choice(names)}!")

Run it? (y/n) y

(Pdb OpenAI) greet()
Hello, Bob!
```

## ask

```
(Pdb OpenAI) ask what happened
When the `greet()` function was called, the following occurred:
1. The function selected a random name from the list `names`, which contains five different names: "Alice", "Bob", "Charlie", "Diana", and "Edward".
2. It also selected a random greeting from the list `greeting`, which includes five different greetings: "Hello", "Hi", "Hey", "Greetings", and "What's up".
3. It combined the selected greeting and name with a formatted string to create a message.
4. Finally, the function printed this message to the console.
Since the selections are random, the exact output can vary with each call to `greet()`, displaying a greeting and a name randomly chosen from the lists provided.
```

## wtf

This is an alias for `ask` with this prompt: `Explain how the program arrived at this state, including the cause of any
errors. Be concise.` Add one or more `?` chars to the command to provide more context to the model.