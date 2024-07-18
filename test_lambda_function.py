import json
from lambda_function import lambda_handler

# Load the event from a JSON file
with open('./event/sample.json') as f:
    event = json.load(f)

# Mock context (if necessary)
context = {}

# Invoke the lambda_handler function with the event and context
response = lambda_handler(event, context)

# Print the response
print(json.dumps(response, indent=2))
