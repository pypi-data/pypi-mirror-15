A simple parser that will separate a string of would be arguments in the form of key:value
where key and value are strings separated by a colon.  This should work for any number of pairs.

Example:

$ example.py key1:value1 key2:value2 key3:this is value3

Would result in a dictionary of:

d { 'key1' : 'value1'
    'key2' : 'value2'
    'value3 : 'this is value3'
  }