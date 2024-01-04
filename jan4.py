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
