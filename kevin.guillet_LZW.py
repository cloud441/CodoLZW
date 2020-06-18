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



#---------   Utilitaries function Section    ----------#



##
#   error_format(): Thrower of file format error:
##

def error_format():
    print("\nerror: File format must be '.txt' for compression and '.lzw' for decompression.\n")




##
#   write_zip_file(): Write the compressed version of the file in another file:
##

def write_zip_file(path, data, old_size):

    output_name = path.split(".")[0]
    output_name = output_name.split("/")[-1]
    new_size = sum([len(i) for i in data])
    with open(output_name + ".lzw", "w") as file_out:

        for bitwise in data:
            file_out.write(bitwise)
#            file_out.write("\n")

        file_out.write("\nSize before LZW compression: " + str(old_size) + " bits")
        file_out.write("\nSize after LZW compression: " + str(new_size) + " bits")
        file_out.write("\nCompression ratio: " + str(round(new_size / old_size, 3)) + "\n")



##
#   write_dico_file(): Write the dictionnary of character in a csv file:
##

def write_dico_file(path, dico):

    output_name = path.split(".")[0]
    output_name = output_name.split("/")[-1]

    with open(output_name + "_dico" + ".csv", "w") as file_out:

        for i in range(len(dico) - 1):
            file_out.write(dico[i] + ",")
        file_out.write(dico[-1] + "\r\n")




##
#   write_table_file(): Write the LZW compression table in a csv file:
##

def write_table_file(path, table):

    dataframe = pd.DataFrame(table, columns=['Buffer','Input','New sequence','Address','Output'])
    output_name = path.split(".")[0]
    output_name = output_name.split("/")[-1]

    dataframe.to_csv(output_name + "_LZWtable" + ".csv", index=False, line_terminator='\r\n')




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




#---------    LZW Data Compression Algorithm Section   ----------#




##
#   lzw_zip(): Lossless LZW Compression algorithm:
##

def lzw_zip(path):

    if (len(path) < 4 or path[-4:] != ".txt"):
        error_format();
        return None

    with open(path, "r") as file_in:


        data = file_in.read()
        table = []
        table_line = []
        dico_size, dico = dico_constructor(data)
        write_dico_file(path, dico)
        buf = ""
        output = []
        nb_bit = ceil(log2(dico_size))
        nb_original_bit = nb_bit


        for char in data:

            table_line = [buf, char]

            if char == '\n':
                continue

            if (buf + char) in dico:
                buf += char
                table_line += [""]
                table_line += [""]

                if dico.index(buf) >= pow(2, nb_bit):
                    output += [to_bitwise(dico.index('%'), nb_bit)]
                    nb_bit += 1
                    table_line += ["@[" + '%' + "]=" + str(dico.index('%'))]


            elif (buf != ""):
                output += [to_bitwise(dico.index(buf), nb_bit)]

                dico += [buf + char]
                dico_size += 1
                table_line += [buf + char]
                table_line += [str(dico_size - 1)]
                table_line += ["@[" + buf + "]=" + str(dico.index(buf))]

                buf = char

            table += [table_line]


        table += [[buf, "", "", "", "@[" + buf + "]=" + str(dico.index(buf))]]
        if buf in dico:
            output += [to_bitwise(dico.index(buf), nb_bit)]



    write_zip_file(path, output, nb_original_bit * (len(data) - 1))
    write_table_file(path, table)





##
#   lzw_unzip(): Lossless LZW Decompression algorithm:
##

def lzw_unzip(path):

    if (len(path) < 4 or path[-4:] != ".lzw"):
        error_format();
        return None
    else:
        print("Not implemented yet")




#---------    Main entry Section    ----------#




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




##
#   main(): Encapsulate main function of the file:
##

def main():

    args = parse_argument()

    if (args):

        if (args.compress):
            lzw_zip(args.path)

        else:
            lzw_unzip(args.path)





if __name__ == "__main__":
    main()
