def decompress(compressed_data , huffman_table , original_code_table , original_bits):
    decompressed_data = ''
    #It is not efficient to loop on the compressed_data bit by bit ,so all we need is
    # to find the minimum length in codes (keys) of huffman_table
    min_length_huffman = 1e9
    for  key in huffman_table:
        min_length_huffman = min(min_length_huffman , len(key))

    #if we find the code represents "others" then we need to know the length of bits in the original_code_table
    length_of_bits = original_bits

    i = 0
    while i < len(compressed_data):
        val = huffman_table.get(compressed_data[i:i+min_length_huffman])

        if val is not None: # If the code have a corresponding value in huffman_table
           i+=min_length_huffman
           if val != 'others' :
               decompressed_data += val
           elif val == 'others' :
               val = original_code_table.get(compressed_data[i:i+length_of_bits])
               decompressed_data += val
               i+=length_of_bits


        else:
            j = 1
            while val is None:
               val = huffman_table.get(compressed_data[i:i+min_length_huffman+j])
               j+=1

            i+=min_length_huffman+j-1
            if val != 'others' :
                decompressed_data += val
            elif val == 'others' :
                val = original_code_table.get(compressed_data[i:i+length_of_bits])
                decompressed_data += val
                i+=length_of_bits

    return decompressed_data