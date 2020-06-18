    #############################################
    #                                           #
    #  LZW Compression/Decompression Algorithm  #
    #                                           #
    #############################################


import numpy as np
import pandas as pd
import argparse as ap
import sys
from math import ceil, log2





##
#   error_format(): Thrower of file format error:
##

def error_format():
    print("\nerror: File format must be '.txt' for compression and '.lzw' for decompression.\n")




##
#   Write_zip_file(): Write the compressed version of the file in another file:
##

def write_zip_file(path, data):

    output_name = path.split(".")[0]
    output_name = output_name.split("/")[-1]
    with open(output_name + ".lzw", "w") as file_out:

        for bitwise in data:
            file_out.write(bitwise)
#            file_out.write("\n")





##
#   dico_constructor(): Create the initial dictionnary from the file and return
#       the size and itself:
##

def dico_constructor(data):
    size = 0
    dico = []
    index = 0

    for char in data:

        # Insert into dictionnary according to lexical order:
        if (char not in dico) and char != '\n':

            for i in range(size):
                if ord(dico[i]) > ord(char):
                    index = i
                    break
                else:
                    index = size

            dico = dico[:index] + [char] + dico[index:]
            size += 1


    #append the special LZW character '%':
    index = 0
    for i in range(size):
        if ord(dico[i]) > ord('%'):
            index = i
            break

    dico = dico[:index] + ['%'] + dico[index:]
    size += 1

    return size, dico




##
#   to_bitwise(): Translate a integer to bitwise value in 'nb_bit' bits:
##

def to_bitwise(nb, nb_bits):
    bitwise = ""

    while (nb_bits > 0):
        if nb >= pow(2, nb_bits - 1):
            bitwise += "1"
            nb -= pow(2, nb_bits - 1)
        else:
            bitwise += "0"
        nb_bits -= 1

    return bitwise





##
#   lzw_zip(): Lossless LZW Compression algorithm:
##

def lzw_zip(path):

    if (len(path) < 4 or path[-4:] != ".txt"):
        error_format();
        return None

    with open(path, "r") as file_in:

        data = file_in.read()
        dico_size, dico = dico_constructor(data)
        buf = ""
        output = []
        nb_bit = ceil(log2(dico_size))

        for char in data:

            if char == '\n':
                continue

            if (buf + char) in dico:
                buf += char

                if dico.index(buf) >= pow(2, nb_bit):
                    output += [to_bitwise(dico.index('%'), nb_bit)]
                    nb_bit += 1


            elif (buf != ""):
                output += [to_bitwise(dico.index(buf), nb_bit)]

                if dico_size <= pow(2, nb_bit):
                    dico += [buf]
                    dico_size += 1

                buf = char

        if buf in dico:
            output += [to_bitwise(dico.index(buf), nb_bit)]



    write_zip_file(path, output)






##
#   lzw_unzip(): Lossless LZW Decompression algorithm:
##

def lzw_unzip(path):

    if (len(path) < 4 or path[-4:] != ".lzw"):
        error_format();
        return None
    else:
        print("Not implemented yet")







##
#   parse_argument(): Parse the command line and check the use of arguments:
##

def parse_argument():

    parser = ap.ArgumentParser()

    #Add all of the possible arguments:
    parser.add_argument("-c", "--compress", help="Compress the file given after the '-p' option using the lossless LZW compression algorithm.",
                        action="store_true")
    parser.add_argument("-u", "--unzip", help="Decompress the file given after the '-p' option using the lossless LZW decompression algorithm.",
                        action="store_true")
    parser.add_argument("-p", "--path", help="Specify the file to Compress/Decompress.")

    #parse the argument:
    args = parser.parse_args()

    #Check if bad use of arguments:
    if (args.path == None or (args.compress == args.unzip)):
        print("\nerror: You must use these commands to proceed:\n",
                "\tpython3 kevin.guillet_LZW.py -c -p path/to/the/file.txt",
                "\tor",
                "\tpython3 kevin.guillet_LZW.py -u -p path/to/the/file.lzw\n",
                sep="\n")
        return None

    return args






def main():

    args = parse_argument()

    if (args):

        if (args.compress):
            lzw_zip(args.path)

        else:
            lzw_unzip(args.path)




if __name__ == "__main__":
    main()
