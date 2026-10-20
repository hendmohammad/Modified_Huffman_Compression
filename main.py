from compression import compress
from decompression import decompress

text = input("Enter the text: ")
limit = float(input("Enter the minimum limit of probabilities (e.g. 0.05): "))


# compression
compressed, symDecode_table, originalDecode_table, original_bits = compress(text, limit)
print("\nCompressed bits      :", compressed)

# decompression
decompressed = decompress(compressed, symDecode_table, originalDecode_table, original_bits)
print("\nDecompressed text    :", decompressed)