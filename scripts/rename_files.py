import os


list_of_files = os.listdir("./data")
list_of_files = [os.path.join(os.getcwd(), "data", file)
                 for file in list_of_files]

for i, file_path in enumerate(list_of_files):
    os.rename(src=file_path,
              dst=os.path.join(os.getcwd(), "data", f"file{i}.jpg"))
