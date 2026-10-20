from compression import compress
from decompression import decompress
from file_handling import file_menu


def text_mode():
    text = input("Enter the text: ")
    limit = float(input("Enter the minimum limit of probabilities (e.g. 0.05): "))

    # compression
    compressed, symDecode_table, originalDecode_table, original_bits = compress(text, limit)
    print("\nCompressed bits      :", compressed)

    # decompression
    decompressed = decompress(compressed, symDecode_table, originalDecode_table, original_bits)
    print("\nDecompressed text    :", decompressed)


def main():
    while True:
        print("\n=== Modified Huffman Compression ===")
        print("1) Text mode (type a text)")
        print("2) File mode (compress / decompress files)")
        print("3) Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            text_mode()
        elif choice == "2":
            file_menu()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
