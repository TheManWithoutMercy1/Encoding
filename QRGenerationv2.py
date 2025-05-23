from reedsoloencoding import data_words
from reedsoloencoding import integrate_reed_solo
from matrix_placement import *
from masks import* 
from image import create_qr_image
import os
import copy 
class QR_Generation:
    def __init__(self, input_string):
        self.string = input_string
        self.bit_string = ''  
        self.required_bits = None  
        self.version = None

    def encoding_string(self):
        """
        Encode string into byte mode bits (Version 1 and 2).
        Character Capacity for Version 1, Level L is 17 for Byte Mode
        Character Capacity for Version 2, Level L is 32 for Byte Mode
        """
        string_length = len(self.string)

        if string_length <= 17:
           self.version = 1
           self.required_bits = 152
        elif string_length <= 32:
            self.version = 2
            self.required_bits = 272
        else:
          raise ValueError("Only supports up to version 2 (max 32 characters) for now.")

        byte_mode = '0100'  # Byte mode indicator
        print(f"Mode indicator: {byte_mode}")

        char_count = len(self.string)
        print(f"Character count: {char_count}")

        # Convert character count to 8-bit binary
        char_count_bin = format(char_count, '08b')
        print(f"Character count in binary (8-bit padded): {char_count_bin}")

        self.bit_string = byte_mode + char_count_bin  # Start bit string

    def byte_mode_encoding(self):
        """
        Convert each character to its 8-bit binary representation.
        """
        print(f"Original string: {self.string}")
        binary_data = ''.join(format(ord(i), '08b') for i in self.string)
        self.bit_string += binary_data

        print("Character to Binary Conversion:")
        for char in self.string:
            char_binary = format(ord(char), '08b')
            print(f"{char} → {char_binary}")

        print(f"Bit string after encoding data: {self.bit_string}")

    def determine_bits(self):
        """
        Calculate total bit length and check against required capacity.
        """
        num_total_bits = len(self.bit_string)
        print(f"Total bits so far: {num_total_bits}")
        if num_total_bits < self.required_bits:
            print(f"Bit string is {self.required_bits - num_total_bits} bits too short. Padding needed.")
        else:
            print("No padding needed. Bit string meets required length.")

    @staticmethod
    def add_terminators(bit_string, num_total_bits, required_bits):
        diff = required_bits - num_total_bits
        if diff <= 0:
            print("No terminator needed.")
            return bit_string
        elif diff >= 4:
            print("Adding 4-bit terminator.")
            return bit_string + '0000'
        else:
            print(f"Adding {diff}-bit terminator.")
            return bit_string + ('0' * diff)

    @staticmethod
    def add_zero_multiple_8(bit_string):
        remainder = len(bit_string) % 8
        if remainder == 0:
            print("Bit string already a multiple of 8.")
            return bit_string
        padding = 8 - remainder
        print(f"Adding {padding} zero(s) to align to byte boundary.")
        return bit_string + ('0' * padding)

    @staticmethod
    def pad_bytes(required_bits,bit_string):
        pad1 = '11101100'
        pad2 = '00010001'
        toggle = True

        while len(bit_string) + 8 <= required_bits: 
            bit_string += pad1 if toggle else pad2
            toggle = not toggle

        print(f"Padded to final bit length: {len(bit_string)}")
        return bit_string

    def generate_final_bit_stream(self):
        """
        Full end-to-end bit stream generation for the input string.
        """
        self.encoding_string()
        self.byte_mode_encoding()
        self.determine_bits()

        # Add terminators
        self.bit_string = self.add_terminators(self.bit_string, len(self.bit_string), self.required_bits)

        # Make bit string a multiple of 8
        self.bit_string = self.add_zero_multiple_8(self.bit_string)

        # Add pad bytes if necessary
        self.bit_string = self.pad_bytes(self.required_bits,self.bit_string)

        print("Final Bit String:")
        print(self.bit_string)
        print(f"Total length: {len(self.bit_string)} bits")
        
        data_words_list = data_words(self.bit_string)
        ir = integrate_reed_solo(data_words_list,self.version)
        matrix = create_matrix(self.version)
        if self.version == 1:
                matrix2, data_bit_positions = place_data_bits_v1(matrix, ir)
        elif self.version == 2:
                matrix2, data_bit_positions = place_data_bits_v2(matrix, ir)

        matrix_copy = copy.deepcopy(matrix2)
        matrix_0 = apply_mask_0(matrix_copy, data_bit_positions)
        penalty1 = evaluate_penalty(matrix_0)
        print(penalty1)

        matrix_1 = apply_mask_1(matrix_copy, data_bit_positions)
        penalty2 = evaluate_penalty(matrix_1)
        print(penalty2)
        

        matrix_2 = apply_mask_2(matrix_copy,data_bit_positions)
        penalty3 = evaluate_penalty(matrix_2)
        print(penalty3)

        matrix_3 = apply_mask_3(matrix_copy,data_bit_positions)
        penalty4 = evaluate_penalty(matrix_3)
        print(penalty4)

        matrix_4 = apply_mask_4(matrix_copy,data_bit_positions)
        penalty5 = evaluate_penalty(matrix_4)
        print(penalty5)

        matrix_5 = apply_mask_5(matrix_copy,data_bit_positions)
        penalty6 = evaluate_penalty(matrix_5)
        print(penalty6)

        matrix_6 = apply_mask_6(matrix_copy,data_bit_positions)
        penalty7 = evaluate_penalty(matrix_6)
        print(penalty7)

        matrix_7 = apply_mask_7(matrix_copy,data_bit_positions)
        penalty8 = evaluate_penalty(matrix_7)
        print(penalty8)

        penalties = [penalty1, penalty2, penalty3, penalty4, penalty5, penalty6, penalty7, penalty8]
        masked_matrices = [matrix_0, matrix_1, matrix_2, matrix_3, matrix_4, matrix_5, matrix_6, matrix_7]
        mask_functions = [apply_mask_0,apply_mask_1,apply_mask_2,apply_mask_3,apply_mask_4,apply_mask_5,apply_mask_6,apply_mask_7,]

        lowest_penalty = min(penalties)
        best_mask = penalties.index(lowest_penalty)
        print("the lowest penalty of all these is: ", lowest_penalty, "using mask:", best_mask)
        matrix3 = mask_functions[best_mask](matrix2, data_bit_positions)
        matrix4 = format_info(matrix3,self.version,best_mask)
        return matrix4
        #img = create_qr_image(matrix4)
        #downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        #img_path = (os.path.join(downloads_path, "qrv2test.png"))
        #img.save(img_path)
        #img.show()  # Show the image for verification
        #return img_path
    
#string = input("what string do you want to put?")
#qr_gen = QR_Generation(string)
#qr_gen.generate_final_bit_stream()
