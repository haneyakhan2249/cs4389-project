import sys
from blowfish import Blowfish

KEY_SIZE = 128
HALF_SIZE = 64
CHARACTER_SIZE = 8
NUMBER_OF_ROUNDS = 8
NUMBER_OF_CHARACTERS = 16


# Converts plaintext to ciphertext
# also has input for key
def encrypt(key, plaintext):
    # stores the cipher text
    ciphertext = ""
    # get the number of full blocks within the inputted plaintext
    number_of_blocks = len(plaintext) / NUMBER_OF_CHARACTERS
    # characters to pad is the number of characters in each block in every block minus the left over characters
    remaining_characters = (len(plaintext) % NUMBER_OF_CHARACTERS)
    # padded plaintext is initialized to plaintext
    padded_plaintext = plaintext
    # pads the last block if there are remaining characters
    if (remaining_characters != 0):
        characters_to_pad = NUMBER_OF_CHARACTERS - remaining_characters
        for i in range(0, characters_to_pad):
            padded_plaintext += "."
        number_of_blocks += 1
    # creates an empty array of all the blocks from the text
    blocks = []
    # stores each block into an array
    for i in range(0, int(number_of_blocks)):
        # stores the substrings in blocks
        blocks.append(padded_plaintext[(i * NUMBER_OF_CHARACTERS): ((i + 1) * NUMBER_OF_CHARACTERS)])
    # applies encryption function on every block
    subkeys = create_subkeys(key)
    for i in blocks:
        ciphertext += str(feistel_cipher(i, subkeys, 'ENCRYPT'))
    return morsecodify(ciphertext)


# Convert ciphertext to plaintext
# another input is the key
def decrypt(key, ciphertext):
    ciphertext = demorsecodify(ciphertext)
    # stores the cipher text
    plaintext = ""
    # get the number of full blocks within the inputted plaintext
    number_of_blocks = len(ciphertext) / NUMBER_OF_CHARACTERS
    # characters to pad is the number of characters in each block in every block minus the left over characters
    remaining_characters = (len(ciphertext) % NUMBER_OF_CHARACTERS)
    # padded plaintext is initialized to plaintext
    padded_ciphertext = ciphertext
    # pads the last block if there are remaining characters
    if (remaining_characters != 0):
        characters_to_pad = NUMBER_OF_CHARACTERS - remaining_characters
        for i in range(0, characters_to_pad):
            padded_ciphertext += "."
        number_of_blocks += 1
    # creates an empty array of all the blocks from the text
    blocks = []
    # stores each block into an array
    for i in range(0, int(number_of_blocks)):
        # stores the substrings in blocks
        blocks.append(padded_ciphertext[(i * NUMBER_OF_CHARACTERS): ((i + 1) * NUMBER_OF_CHARACTERS)])
    # applies encryption function on every block
    subkeys = create_subkeys(key)
    for i in blocks:
        plaintext += str(feistel_cipher(i, subkeys, 'DECRYPT'))  
    return plaintext


# Feistel cipher implementation
# innput is a 128 byte block, subkey array, and 'encrypt' or 'decrypt'
def feistel_cipher(block, subkeys, func):
    # gets the left half and right half of block
    left_half = block[0: int(len(block) / 2)]
    right_half = block[int(len(block) / 2): len(block)]
    for i in range(0, NUMBER_OF_ROUNDS):
        # perform f function using right half and subkey for the round: f function is blowfish
        # perform XOR
        # reverse key order if decrypting
        if(func == 'ENCRYPT'):
            hash_value = f_function(right_half, subkeys[i].encode())
            xor_result = xor(hash_value, left_half, int(NUMBER_OF_CHARACTERS/2))
        else:
            hash_value = f_function(right_half, subkeys[NUMBER_OF_ROUNDS - 1 - i].encode())
            xor_result = xor(hash_value, left_half, int(NUMBER_OF_CHARACTERS/2))
        # Permutation achieved through swapping
        # The new left half is the old right half
        left_half = right_half
        # the new right half is the result
        right_half = xor_result
    return str(right_half) + str(left_half)


# XOR function between 2 strings
def xor(operand_one, operand_two, length):
    # result = operand_one ^ operand_two
    result = ""
    # goes through every character
    for i in range(0, length):
        # uses Python bitwise XOR fuction and ord() to convert char to int
        result +=  chr(ord(operand_one[i]) ^ ord(operand_two[i]))
    return result


# F function for Feistel cipher - Blowfish cipher
def f_function(half_block, subkey):
    bf = Blowfish(subkey)
    result = bf.encrypt(half_block)
    return result


# Creates the subkeys for each round
# input is key
def create_subkeys(key):
    subkeys = []
    # 1st round - shift by 8 bytes 0-31, 96-127
    # 2nd round - shift by 8 bytes 8-39, 88-119
    # 3rd round - shift by 8 bytes 16-47, 80-111
    # 4th round - shift by 8 bytes 24-55, 72-103
    # 5th round - shift by 8 bytes 32-63, 64-95
    # 6th round - shift by 8 bytes 40-71, 56-87
    # 7th round - shift by 8 bytes 48-79, 48-79
    # 8th round - shift by 8 bytes 56-87, 40-71

    # 1st round - shift by 1 char 0-3, 12-15
    # 2nd round - shift by 1 char 1-4, 11-14
    # 3rd round - shift by 1 char 2-5, 10-13
    # 4th round - shift by 1 char 3-6, 9-12
    # 5th round - shift by 1 char 4-7, 8-11
    # 6th round - shift by 1 char 5-8, 7-10
    # 7th round - shift by 1 char 6-9, 6-9
    # 8th round - shift by 1 char 7-10, 5-8

    for i in range(0, NUMBER_OF_ROUNDS):
        start_index_one = i  # 0,1,2,3 ...
        end_index_one = int( i + ( NUMBER_OF_ROUNDS / 2 ) )  # 4,5,6,7 .....
        start_index_two = int( ( NUMBER_OF_CHARACTERS - ( NUMBER_OF_ROUNDS / 2) ) - i )  # 12,11,10,9 ....
        end_index_two = int( NUMBER_OF_CHARACTERS  - i )  # 16,15,14,13 ....
        subkeys.append( str(key[start_index_one:end_index_one] + key[start_index_two:end_index_two] ) )
    return subkeys


# Converts encrypted string into encrypted  psuedomorecode string
def morsecodify(string):
    byte_array= ''.join(format(ord(i),'b').zfill(8) for i in string)
    pseudo_morse_code = ""
    for i in byte_array:
        if int(i) == 0:
            pseudo_morse_code += str('(')
        if int(i) == 1:
            pseudo_morse_code += str(')')
    return pseudo_morse_code


# Converts psuedomorecode string into encrypted unicode string
def demorsecodify(pseudo_morse_code):
    byte_array = ''
    for i in pseudo_morse_code:
        if i == '(':
            byte_array += '0'
        if i == ')':
            byte_array += '1'

    crypted_unicode = "".join([chr(int(x,2)) for x in [byte_array[i:i+8] 
                           for i in range(0,len(byte_array), 8)
                           ]
            ])
    return crypted_unicode





################# RUN CODE #######################


if __name__ == '__main__':

    if(len(sys.argv) != 4):
        print("\nPlease provide three arguments!")
        print(" - to encrypt: python nested.py encrypt [16-bit key] [plaintext]")
        print(" - to decrypt: python nested.py decrypt [16-bit key] [ciphertext]\n")
    else:
        func = sys.argv[1]
        key = sys.argv[2]
        text = sys.argv[3]

        if(len(key) != 16):
            print("\nKey size should be 16 bits\n")
            exit()

        if(func == 'encrypt'):
            print("\n" + encrypt(key, text) + "\n")
        elif(func == 'decrypt'):
            print("\n" + decrypt(key, text) + "\n")  



################# TESTING #####################

# test = 'DUBDUBDUBDUBDUBDUBTESTTESTTESTTEST'
# print(test)
# crypted = encrypt("testtesttesttest", test)
# print("cyrypted: " + crypted)
# decrypted = decrypt("testtesttesttest", crypted)
# print(decrypted)

# test2 = 'DUBDUBDUBDUBDUBD'
# print(test2)
# crypted2 = encrypt("testtesttesttest", test2)
# print("cyrypted: " + crypted)
# decrypted2 = decrypt("testtesttesttest", crypted2)
# print(decrypted2)

# test3 = 'DUBDUB12djadnj76'
# print(test3)
# crypted3 = encrypt("testtesttesttest", test3)
# print("cyrypted: " + crypted3)
# decrypted3 = decrypt("testtesttesttest", crypted3)
# print(decrypted3)


# TESTING XOR
# test_xor1 = xor('asim', '5239', 4)
# test_xor2 = xor('asim', test_xor1, 4)
# test_xor3 = xor('5239', test_xor1, 4)
# test_xor4 = xor('asim', 'asin', 4)
# test_xor5 = xor('asim', test_xor4, 4)
# print test_xor2
# print test_xor3
# print test_xor5
# print xor('asim', 'asin', 4)
# print xor('1','3', 1)