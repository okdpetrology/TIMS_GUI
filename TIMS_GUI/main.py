import pandas as pd
from gooey import Gooey, GooeyParser
import os
import re
import copy
import TIMS_functions as tims

@Gooey(
    program_name="TIMS Auto-format",
    program_description="Automate TIMS data export",
    #image_dir='/Users/Khalil/Desktop/Fall2020/GUI_test/image'
     )

def main():

    parser = GooeyParser()
    main_page = parser.add_argument_group("User Interface")

    main_page.add_argument(
        "-i",
        "--Input",
        nargs='*',
        help= ".DAT files used for data formatting.",
        #required=True,
        widget="MultiFileChooser",
        gooey_options=dict(wildcard="TIMS data file (*.DAT)|*.DAT",)
    )
    main_page.add_argument(
        '-name',
        '--OutputFileName',
        help="Type in output file name. Automatically adds number to prevent file overwriting.",
        widget='Textarea',
        gooey_options={
        # height of the text area in pixels
        'height': 24,
        # prevents the user from editing when true
        #'readonly': False
    })


    # main_page.add_argument(
    #     "-i",
    #     "--Input2",
    #     required = False,
    #     help = ".DAT file used for data formatting.",
    #     widget = "FileChooser",
    #     gooey_options=dict(wildcard="TIMS data file (*.DAT)|*.DAT")
    # )
    main_page.add_argument(
        "-o",
        "--Output",
        help="Folder to place output .xlsx file",
        widget="DirChooser")

    args = parser.parse_args()

    # data_files = ['/Volumes/KSTICK/20210408/DY01-0F5.DAT', '/Volumes/KSTICK/20210408/DY01-0F4.DAT',
    #           '/Volumes/KSTICK/20210408/DY01-0F3.DAT', '/Volumes/KSTICK/20210408/DY13-0F2.DAT',
    #           '/Volumes/KSTICK/20210408/DY13-0F1.DAT']  # Mac-dependent...

    ### Actual data processing to EXCEL
    test_files = args.Input[1:]
    print("Files chosen for formatting: ")
    for file in test_files:
        print(file)
    print('***********************************************')
    mega = tims.mega_format(test_files)

    #output file
    path = args.Output
    n = 1
    name = args.OutputFileName
    if '.xlsx' in name:
        name = name.split('.')[0]
    else:
        pass
    while n < 20:
        if os.path.isfile(os.path.join(path, name + str('_') + str(n) + ".xlsx")):
            n += 1
        else:
            break

    name = name + str('_') + str(n) + '.xlsx'

    tims.files_process_toEXCEL(mega, path, name)
    print('Name of output file: ', name)


if __name__ == "__main__":
    main()