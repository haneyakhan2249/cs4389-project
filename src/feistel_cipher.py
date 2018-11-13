from blowfish import Blowfish

KEY_SIZE = 128
HALF_SIZE = 64
CHARACTER_SIZE = 8
NUMBER_OF_ROUNDS = 8
NUMBER_OF_CHARACTERS = 16

# This function is complete
# XOR function between 2 strings
def xor(operand_one, operand_two, length):
    # result = operand_one ^ operand_two
    result = ""
    # Goes through every character
    for i in range(0, length):
        # Uses Python bitwise XOR fuction and ord() to convert char to int
        result +=  chr(ord(operand_one[i]) ^ ord(operand_two[i]))
        # print chr(ord(operand_one[i]) ^ ord(operand_two[i]))
        # ord(operand_one[i]) ^ ord(operand_two[i])
    return result


# This function is mostly complete (needs f function)
# takes a block of input of 128 bytes
# takes an array of subkeys
def feistel_cipher(block):
    # gets the left half and right half of block
    left_half = block[0: (len(block) / 2)]
    right_half = block[(len(block) / 2): len(block)]
    print('Original Left Half:' + left_half)
    print('Original Right Half:' + right_half)
    for i in range(0, NUMBER_OF_ROUNDS):
        print('Round: ' + str(i))
        ###############################TO DO #################################
    #     # Perform f function using right half and subkey for the round
    #     result = internal_function(right_half, subkeys[i])

        # Performing XOR
        xor_result = xor(right_half, left_half, NUMBER_OF_CHARACTERS/2)
        # Permutation achieved through swapping
        # The new left half is the old right half
        left_half = right_half
        # the new right half is the result
        right_half = xor_result
        # print 'XOR result: ' + xor_result
        # print 'New Left Half: ' + left_half
        # print 'New Right Half: ' + right_half
    return str(right_half) + str(left_half)

# This function is mostly complete (needs feistel cipher)
# Takes some plaintext where each character is an ASCII character (8 bytes)
# Returns the equivalent ciphertext
def encrypt(plaintext):
    # Stores the cipher text
    ciphertext = ""
    # Get the number of full blocks within the inputted plaintext
    number_of_blocks = len(plaintext) / NUMBER_OF_CHARACTERS
    # Characters to pad is the number of characters in each block in every block minus the left over characters
    remaining_characters = (len(plaintext) % NUMBER_OF_CHARACTERS)
    # Padded plaintext is initialized to plaintext
    padded_plaintext = plaintext
    # Pads the last block if there are remaining characters
    if (remaining_characters != 0):
        characters_to_pad = NUMBER_OF_CHARACTERS - remaining_characters
        for i in range(0, characters_to_pad):
            padded_plaintext += "."
        number_of_blocks += 1
    # Creates an empty array of all the blocks from the text
    blocks = []
    # Stores each block into an array
    for i in range(0, number_of_blocks):
        # Stores the substrings in blocks
        blocks.append(padded_plaintext[(i * NUMBER_OF_CHARACTERS): ((i + 1) * NUMBER_OF_CHARACTERS)])
    # Applies encryption function on every block
    ######################### TO DO #####################################
    # for i in blocks:
    #     ciphertext += str(feistel_cipher(i, subkeys))

    # print blocks
    return ciphertext

# This function needs to be written
# F function
def internal_function(half_block, subkey):
    # result = xor(half_block, )
    result = half_block
    return result


# This function needs to be written
# Creates the subkeys for each round
def create_subkeys(key):
    subkeys = []
    return subkeys

# This function needs to be written (should be easy as reverse of encrypt)
# Takes some plaintext where each character is an ASCII character (8 bytes)
# Returns the equivalent ciphertext
def decrypt(ciphertext, subkeys):
    plaintext = ""
    # Get the number of blocks within the inputted plaintext
    number_of_blocks = len(plaintext) / 128
    blocks = []
    # Pad the last block
    for i in range(0, number_of_blocks):
        # Stores the substrings in blocks
        blocks[i] = [(i * KEY_SIZE), ((i + 1) * KEY_SIZE)]
    # Applies encryption function
    for i in number_of_blocks:
        ciphertext += str(feistel_cipher(number_of_blocks[i]))
    return plaintext






# Random Testing Dara

# print test_encrypt('DUBDUBDUBDUBDUBDUBTESTTESTTESTTEST')
# print test_feistel_cipher('DUBDUBDUBDUBDUBD')
# print test_feistel_cipher('DUBDUB12djadnj76')


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