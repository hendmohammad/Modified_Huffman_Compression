from compression import compress
from decompression import decompress

import json
import os
import struct


def bits_to_bytes(bits):
       if not bits:
        return b""
    pad = (-len(bits)) % 8
    bits += "0" * pad
    return int(bits, 2).to_bytes(len(bits) // 8, "big")


def bytes_to_bits(data, bit_length):
      if not data:
        return ""
    bits = bin(int.from_bytes(data, "big"))[2:].zfill(len(data) * 8)
    return bits[:bit_length]


def compress_file(in_path, out_path, limit):
    with open(in_path, "rb") as f:
        raw = f.read()

    ext = os.path.splitext(in_path)[1]

    if len(raw) == 0:  
        header = {"empty": True, "ext": ext}
        payload = b""
    else:
        text = raw.decode("latin-1")
        bits, sym_dec, org_dec, org_bits = compress(text, limit)
        header = {
            "empty": False,
            "ext": ext,
            "sym": sym_dec,          
            "org": org_dec,          
            "org_bits": org_bits,
            "bit_length": len(bits),
        }
        payload = bits_to_bytes(bits)

    header_bytes = json.dumps(header).encode("utf-8")
    with open(out_path, "wb") as f:
        f.write(struct.pack(">I", len(header_bytes)))
        f.write(header_bytes)
        f.write(payload)

    return len(raw), os.path.getsize(out_path)


def decompress_file(in_path, out_path):
    with open(in_path, "rb") as f:
        header_len = struct.unpack(">I", f.read(4))[0]
        header = json.loads(f.read(header_len).decode("utf-8"))
        payload = f.read()

    if header["empty"]:
        raw = b""
    else:
        bits = bytes_to_bits(payload, header["bit_length"])
        text = decompress(bits, header["sym"], header["org"], header["org_bits"])
        raw = text.encode("latin-1")

    with open(out_path, "wb") as f:
        f.write(raw)

    return header["ext"], len(raw)


def pick_file(title, filetypes=(("All files", "*.*"),)):
    """File-chooser window (Tkinter). Falls back to typing the path."""
    path = ""
    try:
        from tkinter import Tk, filedialog
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        root.destroy()
    except Exception:
        pass  
    if not path:
        path = input(f"{title} - type the file path: ").strip().strip('"')
    return path


def read_limit():
    while True:
        try:
            value = float(input("Minimum symbol probability (0 to 1, e.g. 0.01): "))
            if 0 <= value <= 1:
                return value
        except ValueError:
            pass
        print("Invalid value, enter a number between 0 and 1.")

def file_menu():

    while True:
        print("\n1) Compress a file\n2) Decompress a file\n3) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            in_path = pick_file("Select the file to compress")
            if not os.path.isfile(in_path):
                print("File not found.")
                continue
            limit = read_limit()
            out_path = os.path.splitext(in_path)[0] + ".bin"
            if os.path.abspath(out_path) == os.path.abspath(in_path):
                out_path = in_path + ".bin"
            before, after = compress_file(in_path, out_path, limit)
            print(f"Saved: {out_path}")
            print(f"Size: {before} -> {after} bytes (including overhead)")
            if before:
                print(f"Ratio: {after / before:.2%} of the original")

        elif choice == "2":
            in_path = pick_file("Select the compressed (.bin) file",
                                (("Compressed", "*.bin"), ("All files", "*.*")))
            if not os.path.isfile(in_path):
                print("File not found.")
                continue
            tmp_out = os.path.splitext(in_path)[0] + "_restored"
            ext, size = decompress_file(in_path, tmp_out)
            final = tmp_out + ext
            os.replace(tmp_out, final)
            print(f"Saved: {final} ({size} bytes)")

        elif choice == "3":
            break


if __name__ == "__main__":
    file_menu()
