# Jinja2-Clone (Rubic2)
This project is not intended to be used but tot be a demonstration project. I wrote this as a challenge to see if I could acomplish a clone of a library I have used before making Flask applications

[Jinja 2 Documentation](http://jinja.pocoo.org/docs/2.10/templates/)

## Features
- {{ VariableName }} 
  - expression that replaces with the local variables value
  - Works with multiple data types like strings, bool, int, dict, list, and even classes!
  - Examples:
  - `employee = {'Name': {'First': Nick, 'Last': 'Wayne'}, 'Age': 21}`
  - `myCar = car()`
  - `{{ myCar.Make }}`
  - `{{ myCar.Model }}`
  - `{{ myCar.toString() }}`
  - ^^Functions can also take paramaters :)
  - `{{ employee.Name['First'] }}`
  - ^^Intermix dot and bracket notation
  - `{{ employee.Name.Last }}`
  - `{{ employee['Age'] }}`
- {{ VariableName | PIPES }}
  - Pipes are defined in [Pipes.py](/pipes.py)
  - Currently parameters do not work
  - Examples:
  - ` ages = ['21', '18'] `
  - `{{ ages[0] | int }}`
  - `{{ ages | max }}`
  - `{{ ages | length }}`
- {% if CONDTIONAL %} {% endif %} 
  - everything between the if statment and the endif will be conditionally rendered based on the evaluation of the ocnditional
  - Example: ` {% if 3 < 5 %} <p>3 is less than 5</p> {% endif %}`
- {% for VAR in range(start, stop, step) %} {% endfor %} 
  - This operates like a standard for range loop and the range operates the same. this repeats everything in between the start and end
  - Example: ` {% for i in range(0,11,2) %} <p>{{ i }}</p> {% endif %} `
- {% for VAR in LIST %} {% endfor %}
  - This will assign the current element in the list to var, can be a class, dict. Can't be another list until I add a call stack for lists
  - Example: ` {% for line in ["Line 1", "Line 2", "Line 3"] %} <p>{{ line }}</p> {% endif %} `
  
## Limitations

## Bugs

## Changelog