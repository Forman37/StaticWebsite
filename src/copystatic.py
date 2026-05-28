import os
import shutil


def copy_files():
    try:
        current_file = os.path.dirname(os.path.abspath(__file__))
        current_folder = os.path.dirname(current_file)

        public_dir = os.path.join(current_folder, "public")

        static_dir = os.path.join(current_folder, "static")

        delete_public_folder_contents(public_dir)
        transfer_static_files(static_dir, public_dir)
    except Exception as e:
        return f"Error : {e}"


def delete_public_folder_contents(dir):
    if os.path.isdir(dir):
        shutil.rmtree(dir)


def transfer_static_files(static_dir, public_dir):
    traverse_directory(static_dir, public_dir)


def traverse_directory(cur_dir, public_dir):
    if not os.path.isdir(public_dir):
        os.mkdir(public_dir)

    dir_contents = os.listdir(cur_dir)

    for item in dir_contents:
        new_path = os.path.join(cur_dir, item)
        if os.path.isdir(new_path):
            new_dir_path = os.path.join(public_dir, item)
            os.mkdir(new_dir_path)
            traverse_directory(new_path, new_dir_path)
        elif os.path.isfile(new_path):
            shutil.copy2(new_path, public_dir)
        else:
            print(f"Not a file or dir : {item}")
