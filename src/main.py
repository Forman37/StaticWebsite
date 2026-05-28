from copystatic import copy_files


def main():
    try:
        copy_files()
    except Exception as e:
        print(f"Error in Loading Page : {e}")


main()
