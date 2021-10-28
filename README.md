# Code Convention
* For class names use `PascalCase`
* For data members `lower_case_with_underscores`
```python
class MyClass:
  def __init__(self):
    self.object_number_one = 0
    self.object_number_two = 0
```
# Project Setup
## Utility Classes
* Five categories:
  1. Registration and De-Registration
  2. Publishing
  3. Retrieving Information
  4. File Transfer between Peers
  5. Update Information
* Each category will have its own file, and then sub classes for each data type

## Server Database
* When server registers new clients, needs to add clients to a database
  * We will be using a CSV to manage clients and store their info
  * We need a utility file to receive connections & store their info in a CSV

# References Section
* [JSON Deserialization in Python](https://stackoverflow.com/questions/42397511/python-how-to-get-json-object-from-a-udp-received-packet)
* [Infinite UDP Loop to Receive JSON Objects](https://stackoverflow.com/questions/28072914/data-structure-for-udp-server-parsing-json-objects-in-python)
