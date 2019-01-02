from urllib.parse import parse_qs
my_values = parse_qs('red=5&blue=0&green=', keep_blank_values = True)

print(my_values)

red = my_values.get('green', [''])[0] or 0

print(red)