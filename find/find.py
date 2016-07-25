import os


def list_dir(path):
    file_list = os.listdir(path)
    for file in file_list:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_dir(file_path)
        print file_path

if __name__ == "__main__":
    list_dir('/Users/zhixichen/workspace/PycharmProjects/find/')