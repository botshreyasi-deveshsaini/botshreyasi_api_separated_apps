# import pickle
# import json

# # Specify the path to your pkl file
# pkl_file_path = '/home/manoj/vikas-projects/grpc/bot_files/conversations/call/1846963.pkl'

# # Specify the path to save the JSON file
# json_file_path = '/home/manoj/vikas-projects/grpc/bot_files/conversations/call/1846963.json'

# # Open the pkl file in binary mode for reading
# with open(pkl_file_path, 'rb') as pkl_file:
#     # Load the object from the pkl file
#     obj = pickle.load(pkl_file)
#     # print(obj)
# # Open the JSON file in write mode
# # print(f"Full obj>>>>>>>>>>>{obj}")
# with open(json_file_path, 'w') as json_file:
#     # Convert the object to JSON and write it to the file
#     json.dump(obj, json_file)

# # Optionally, print the JSON object
# print(json.dumps(obj, indent=4))

import pickle

# # Specify the path to your pickle file
# file_path = '/home/manoj/vikas-projects/grpc/bot_files/conversations/call/1846963.pkl'

# # Open the file in binary mode for reading
# with open(file_path, 'rb') as file:
#     # Load the object from the pickle file
#     obj = pickle.load(file)

# # Now you can use the loaded object
# # For example, print the contents of the object
# print(obj)

import pickle


with open('/home/manoj/vikas-projects/grpc/bot_files/conversations/call/1851610.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)