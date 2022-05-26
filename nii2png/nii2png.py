#########################################
#       nii2png for Python 3.7          #
#         NIfTI Image Converter         #
#                v0.2.91                #
#                                       #
#         Modified by Lujia Zhong       #
#       https://lujiazho.github.io/     #
#              26 May 2022              #
#              MIT License              #
#                                       #
#     Written by Alexander Laurence     #
# http://Celestial.Tokyo/~AlexLaurence/ #
#    alexander.adamlaurence@gmail.com   #
#              09 May 2019              #
#              MIT License              #
#########################################

import os, nibabel
import numpy as np
import sys, getopt
import imageio


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('nii2png.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('nii2png.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg

    print('Input file is ', inputfile)
    print('Output folder is ', outputfile)

    # set fn as your 4d nifti file
    image_array = nibabel.load(inputfile).get_data()
    print(image_array.shape)

    if len(image_array.shape) == 3:
        # set 4d array dimension values
        nx, ny, nz = image_array.shape

        # set destination folder
        if not os.path.exists(outputfile):
            os.makedirs(outputfile)
            print("Created ouput directory: " + outputfile)
        for dir_ in ["x_axis", "y_axis", "z_axis"]:
            if not os.path.exists(os.path.join(outputfile, dir_)):
                os.makedirs(os.path.join(outputfile, dir_))

        print('Reading NIfTI file...')

        names = {0:"_x", 1:"_y", 2:"_z"}

        for i, total_slices in enumerate(image_array.shape):
            # iterate through slices
            for current_slice in range(0, total_slices):
                # rotate
                if i == 0:
                    data = np.rot90(image_array[current_slice, :, :], k=1)
                elif i == 1:
                    data = np.rot90(image_array[:, current_slice, :], k=1)
                elif i == 2:
                    data = np.rot90(image_array[:, :, current_slice], k=1)

                #alternate slices and save as png
                if i == 0:
                    img_path = os.path.join(outputfile, "x_axis", inputfile[:-4] + names[i] + "{:0>3}".format(str(current_slice+1))+ ".png")
                elif i == 1:
                    img_path = os.path.join(outputfile, "y_axis", inputfile[:-4] + names[i] + "{:0>3}".format(str(current_slice+1))+ ".png")
                elif i == 2:
                    img_path = os.path.join(outputfile, "z_axis", inputfile[:-4] + names[i] + "{:0>3}".format(str(current_slice+1))+ ".png")
                
                imageio.imwrite(img_path, data)
                print('Saved.')

        print('Finished converting images')
    else:
        print('Not a 3D Image. Please try again.')

# call the function to start the program
if __name__ == "__main__":
   main(sys.argv[1:])