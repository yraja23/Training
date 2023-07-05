# import re

# # Extract the location from user input
# user_input = "loc: location 607"
# location_match = re.search(r"\bloc(?:ation)?\s+(\d+)\b", user_input)
# if location_match:
#     location = location_match.group(1)
#     print("Location:", location)
# else:
#     print("Location not found in user input")

# import re

# User input examples
# user_inputs = [
#     "loc: location 607",
#     "Location 123 is available",
#     "The desired location is 999",
#     "Location: 456"
# ]

# for user_input in user_inputs:
#     location_match = re.search(r"\b\d+\b", user_input)
#     if location_match:
#         location = location_match.group()
#         print("Location:", location)
#     else:
#         print("Location not found in user input")
import re

# User input examples
user_inputs = [
    "loc: location 607",
    "Location 123 is available",
    "The desired location is 999",
    "Location: 456",
    "ABC123XYZ",
    "123ABC456",
    "Location7",
    "9Location"
]

for user_input in user_inputs:
    location_match = re.search(r"\d+", user_input)
    if location_match:
        location = location_match.group()
        print("Location:", location)
    else:
        print("Location not found in user input")
