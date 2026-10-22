import streamlit as st
import os
import tempfile

from file_handling import compress_file, decompress_file

Output_Dir = "Output"

st.set_page_config(
    page_title="Modified Huffman",
    page_icon="📄",
    layout="wide",
)

# storing results in Streamlit session state
if "compressed_data" not in st.session_state:
    st.session_state.compressed_data = None

if "decompressed_data" not in st.session_state:
    st.session_state.decompressed_data = None

if "compressed_bits" not in st.session_state:
    st.session_state.compressed_bits = None

st.title("Modified Huffman File Compressor")
st.write("Compress a text file or decompress a compressed .bin file.")


with st.container(border=True):

    f = st.file_uploader(
        "Choose a file",
        type=["txt", "bin"]
    )
 
    option = st.radio(
        "Choose an option",
        ["Compression", "Decompression"],
        index=None
    )

    # entering minimum probability limit after choosing compression option
    limit = None

    if option == "Compression":
        limit = st.number_input(
            "Minimum Probability Limit",
            min_value=0.0,
            max_value=1.0,
            value=None,
            step=0.01,
            format="%.2f",
            placeholder="e.g. 0.05"
        )

    submit = st.button("Submit")


    if submit:
        if f is None:
            st.warning("Please select a file.")

        elif option is None:
            st.warning("Please choose an option.")

        elif option == "Compression" and limit is None:
            st.warning("Please enter the minimum probability limit.")

        else:
            # reset previous results before a new operation
            st.session_state.compressed_data = None
            st.session_state.decompressed_data = None
            st.session_state.compressed_bits = None

            temp_input = None
            temp_output = None

            try:
                # save the uploaded file temporarily bec. existing file_handling functions expect file paths, not uploads.
                original_name = os.path.basename(f.name)
                original_ext = os.path.splitext(original_name)[1]

                with tempfile.NamedTemporaryFile(
                    mode="wb",
                    suffix=original_ext,
                    prefix="upload_",
                    dir=Output_Dir,
                    delete=False
                ) as temp_file:
                    temp_file.write(f.getvalue())
                    temp_input = temp_file.name


                if option == "Compression":

                    out_path = os.path.join(Output_Dir, "compressed.bin")

                    before, after, bits = compress_file(
                        temp_input,
                        out_path,
                        limit,
                        return_bits=True
                    )
                    st.session_state.compressed_bits = bits

                    # read the actual binary file for the download button
                    with open(out_path, "rb") as file:
                        st.session_state.compressed_data = file.read()

                    st.success("File successfully compressed!")


                elif option == "Decompression":

                    temp_output = os.path.join(Output_Dir, "decompressed_temp")

                    ext, size = decompress_file(
                        temp_input,
                        temp_output
                    )

                    final_path = os.path.join(Output_Dir, "decompressed.txt")

                    os.replace(temp_output, final_path)
                    temp_output = None

                    # read the restored original bytes for downloading
                    with open(final_path, "rb") as file:
                        st.session_state.decompressed_data = file.read()

                    st.success("File successfully decompressed!")


            except Exception as e:
                st.error(f"Operation failed: {e}")

            finally:
                if temp_input and os.path.exists(temp_input):
                    os.remove(temp_input)

                if temp_output and os.path.exists(temp_output):
                    os.remove(temp_output)


# displaying compressed bits
if (option == "Compression" and st.session_state.compressed_bits is not None):
    st.subheader("Compressed Bitstream")
    st.code(st.session_state.compressed_bits)

# showing the download button for the latest successful operation
if st.session_state.compressed_data is not None:

    st.download_button(
        "Download",
        data=st.session_state.compressed_data,
        file_name="compressed.bin",
        mime="application/octet-stream"
    )

elif st.session_state.decompressed_data is not None:

    st.download_button(
        "Download",
        data=st.session_state.decompressed_data,
        file_name="decompressed.txt",
        mime="application/octet-stream"
    )
