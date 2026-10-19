from Modified_Huffman_Decompression import decompress

#example from the lecture 3 slide 44
compressed_data = '00011010001010001100100100010100110110011010100111000110010010111'

huffman_table = {'00' : 'a' ,
                 '011' : 'b',
                  '010' : 'c',
                  '11' : 'd',
                 '10': 'others'}

original_code_table = {'0000':'a',
                       '0001' : 'b',
                       '0010' : 'c',
                       '0011' : 'd',
                       '0100' : 'f',
                       '0101' : 'p',
                       '0110' : 'q',
                       '0111' : 'u',
                       '1000' : 'z' }

decompressed_data = decompress(compressed_data , huffman_table , original_code_table)

true_result = 'abcazdafcqdadcuabapd'

if decompressed_data == true_result:
    print('function works correctly')
else:
    print('function does not work correctly')