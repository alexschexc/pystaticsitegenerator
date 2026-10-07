import os
import shutil

def copy_static(source, destination):
    if not os.path.isdir(source):
        raise ValueError(f"Source directory does not exist: {source}")

    if os.path.exists(destination):
        shutil.rmtree(destination)

    copy_directory(source, destination)

def copy_directory(source, destination):
    os.mkdir(destination)

    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        destination_path = os.path.join(destination, name)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            copy_directory(source_path, destination_path)
