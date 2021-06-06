import os
from uuid import uuid4


DATASET_PATH = "dataset"


def main():
    for dir_path, dir_names, file_names in os.walk("repos"):
        for file_name in file_names:
            full_path = os.path.join(dir_path, file_name)
            if full_path.endswith(".py"):
                new_file_path = os.path.join(DATASET_PATH, f"{uuid4()}.py")
                os.rename(full_path, new_file_path)
    os.rmdir("repos")

if __name__ == '__main__':
    main()