# from https://www.tjelvarolsson.com/blog/five-exercises-to-master-the-python-debugger/
from pdb_openai import debug


def subtractor(a, b):
    """Return a minus b."""
    # time.sleep(5)
    return a - b


some = subtractor(12, 8)
crazy = subtractor(12, 78)
scientific = subtractor(56, 31)
experiment = subtractor(101, 64)

total = some + crazy + scientific + experiment

try:
    experimental_fraction = experiment / total
except:
    debug.post_mortem(wtf=True)

# python examples/subtractor.py

# > /Users/jordan/src/pdb_openai/examples/subtractor.py(19)<module>()
# -> experimental_fraction = experiment / total
#
# The program reached the current state, executing the line `experimental_fraction = experiment / total`,
# due to an attempt to perform division with `total` being `0`. This line of code is problematic because dividing by
# zero is not allowed in Python (or in general arithmetic), and it raises a `ZeroDivisionError`.
#
# From the provided debug info, we can observe the following key points:
#
# - The division happens within a `try` block, and upon encountering the error, the code is set to jump into a custom
# exception handling routine involving a `debug.post_mortem(wtf=True)` call. This suggests that the error handling is
# intentionally catching all exceptions (indicated by a bare `except:`) and is possibly meant for extensive debugging
# or logging purposes, especially with the included argument `wtf=True` which is likely a custom flag for detailed
# error reporting.
#
# - The variables involved in the operation are `experiment` with a value of `37` and `total` with a value of `0`.
# The attempt to divide `37` by `0` is what triggers the error.
#
# - There does not appear to be other relevant local or global variable manipulations between the instantiation of
# these variables and the division operation that might have prevented this error.
#
# In conclusion, the program arrived at this state due to attempting a division operation where the denominator (
# `total`) is zero, which is a direct cause of a `ZeroDivisionError`. The error handling mechanism has captured this
# exception and initiated a custom debugging procedure. To resolve this issue, ensuring `total` is not zero before
# performing the division or implementing more precise error handling for `ZeroDivisionError` could be considered.

# (Pdb OpenAI) ask suggest a fix

# ```python
# # Check if total is zero before dividing
# if total != 0:
#     experimental_fraction = experiment / total
# else:
#     # Handle the case when total is zero, possibly setting a default value or raise a more informative error
#     experimental_fraction = 0  # or any other appropriate action
# ```
