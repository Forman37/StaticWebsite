import sys
import traceback
from copystatic import copy_files
from generatepage import generate_page_recursive


def main():
    try:
        if len(sys.argv) > 1:
            basepath = sys.argv[1]
            if basepath == " ":
                basepath = "/"
        else:
            basepath = "/"

        print(basepath)
        copy_files()
        generate_page_recursive("./content/", "./template.html", "./docs/", basepath)
    except Exception as e:
        print(f"Error in Loading Page : {e}")
        traceback.print_exc()


main()
