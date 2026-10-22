from file_handling import compress_file_menu, decompress_file_menu

while True:
    print("\n\nModified Huffman Compressor: \n ")
    print("1. Compress ")
    print("2. Decompress ")
    print("3. Exit")

    choice = input("Choose: ").strip()

    if choice == "1":
        compress_file_menu()

    elif choice == "2":
        decompress_file_menu()

    elif choice == "3":
        break

    else:
        print("Invalid choice.")
