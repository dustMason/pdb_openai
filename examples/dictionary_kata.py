# https://www.codewars.com/kata/57a93f93bb9944516d0000c1
from pdb_openai import debug


class Dictionary:
    def __init__(self):
        self.entries = {}

    def newentry(self, key: str, value: str) -> None:
        self.entries[key] = value

    def look(self, key: str) -> str:
        return self.entries[key]


try:
    d = Dictionary()
    d.newentry("Apple", "Hello")
    print(d.look("Apple"))
    print(d.look("Nope"))
except:
    debug.post_mortem(wtf=True)

# python examples/dictionary_kata.py

# Hello
#
# > /Users/jordan/src/pdb_openai/examples/dictionary_kata.py(13)look()
# -> return self.entries[key]
#
# The program is executing a method called `look` inside a class named `Dictionary`. The method is meant to return a
# value from `self.entries` dictionary using a provided `key`. When executing the line `return self.entries[key]`,
# the program ran into an issue because the key `'Nope'` did not exist in the `self.entries` dictionary, leading to a
# KeyError being raised.
#
# This KeyError triggered an exception block in the script, causing the program to enter a post-mortem debugging
# session initiated by `debug.post_mortem(wtf=True)`. Specifically, the error occurred while trying to print the
# result of `d.look("Nope")`, where `d` is an instance of the `Dictionary` class. This instance is situated at memory
# address `0x102ba8d60`, and the method `look` was called with `"Nope"` as its argument, which does not exist in the
# dictionary's entries, hence the error.
