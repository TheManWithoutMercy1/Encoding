import reedsolo as rs

def data_words(binarystream):
    data_words_list = []
    # Split the bitstream into chunks of 8 bits
    for i in range(0, len(binarystream), 8):
        # Take each 8-bit chunk and convert to integer
        word = binarystream[i:i+8]
        data_words_list.append(word)  # Store binary strings    
    print("Data words:", data_words_list)
    return data_words_list

def integrate_reed_solo(data_words_list, version):
    # Convert binary strings to integers (bytes)
    data_bytes = [int(byte, 2) for byte in data_words_list]

    # Error correction codeword length for each version
    if version == 1:
        ec_codewords = 7  # Version 1 uses 7 EC codewords
    elif version == 2:
        ec_codewords = 10  # Version 2 uses 10 EC codewords
    else:
        raise ValueError("Currently, only Version 1 and Version 2 are supported")

    # Initialize Reed-Solomon codec for the appropriate EC codeword size
    rs_codec = rs.RSCodec(ec_codewords)

    # Encode the full message to get the error correction (EC) bytes
    full_encoded = rs_codec.encode(data_bytes)

    # The last `ec_codewords` bytes are the parity (Reed-Solomon always appends)
    ec_bytes = full_encoded[-ec_codewords:]

    # Final codeword sequence = original data + parity bytes
    final_bytes = data_bytes + list(ec_bytes)

    # Convert the final codewords (bytes) back to 8-bit binary strings
    encoded_binary = [format(byte, '08b') for byte in final_bytes]

    print(f"Final encoded (data + EC): {encoded_binary}")
    return encoded_binary
