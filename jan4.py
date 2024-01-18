import re

text = "select a, b,c from $$emp database.employee aa"

# Create a regex object.
pattern = re.compile(r"from\s+(?:`|\w+\.)?(\w+)")

# Match the regex against the text.
match = pattern.match(text)

# If there is a match, print the table name.
if match:
    table_name = match.group(1)
    print(table_name)
    ====
    # Example dictionary with 'ABC' and None values
sample_dict = {'key1': 'ABC', 'key2': 'value2', 'key3': None, 'key4': 'ABC', 'key5': None}

# Print the original dictionary
print("Original Dictionary:")
print(sample_dict)

# Replace 'ABC' with 'XXX' and None with 'YYY' in the dictionary
for key, value in sample_dict.items():
    if value == 'ABC':
        sample_dict[key] = 'XXX'
    elif value is None:
        sample_dict[key] = 'YYY'

# Print the modified dictionary
print("\nModified Dictionary:")
print(sample_dict)
