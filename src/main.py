from copystatic import copy_files
from generatepage import generate_page_recursive


def main():
    try:
        copy_files()
        generate_page_recursive("./content/", "./template.html", "./public/")
    except Exception as e:
        print(f"Error in Loading Page : {e}")


main()
