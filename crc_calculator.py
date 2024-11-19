# https://www.lammertbies.nl/comm/info/crc-calculation
from binascii import unhexlify
import codecs
from ctypes import c_ushort
import crcmod 

# Calculate CRC for hex input

def calculate_crc(input_data):       
        """
        Calculate the CRC value for the given hex input data.

        Parameters:
        input_data (str): A hex string representing the input data.

        Returns:
            int: The calculated CRC value.
        """     
        crcValue = 0x0000  # Initialize CRC value
        try:
            input_data = unhexlify(input_data)  # Convert hex string to bytes
            crc_ccitt_tab = init_crc_ccitt()  # Initialize CRC table
            is_string = isinstance(input_data, str)  # Check if input is a string
            is_bytes = isinstance(input_data, bytes)  # Check if input is bytes

            for c in input_data:
                d = ord(c) if is_string else c  # Get the byte value
                tmp = (c_ushort(crcValue >> 8).value) ^ d  # Update CRC value
                crcValue = (c_ushort(crcValue << 8).value) ^ int(crc_ccitt_tab[tmp], 0)  # Calculate new CRC value
                
        except Exception as e:
            print("EXCEPTION(calculate): {}".format(e))  # Handle exceptions
        return crcValue  # Return the calculated CRC value


def init_crc_ccitt():
    """
    Initialize the CRC-CCITT table used for CRC calculations.

    Returns:
    list: A list containing the pre-calculated CRC values for each byte.
    """
    crc_ccitt_tab = []  # Initialize CRC table
    try:
        '''The algorithm uses tables with precalculated values'''
        crc_ccitt_constant = 0x1021  # CRC-CCITT polynomial constant

        for i in range(256):
            crc = 0  # Initialize CRC for this byte
            c = i << 8  # Shift byte to the left

            for j in range(8):
                if ((crc ^ c) & 0x8000):  # Check if the MSB is set
                    crc = c_ushort(crc << 1).value ^ crc_ccitt_constant  # Update CRC with polynomial
                else:
                    crc = c_ushort(crc << 1).value  # Just shift left
                c = c_ushort(c << 1).value  # Shift byte left
            crc_ccitt_tab.append(hex(crc))  # Append CRC value to table
            
    except Exception as err:
        print("crc init error: " + str(err))  # Handle initialization errors
    return crc_ccitt_tab  # Return the CRC table


if __name__ == "__main__":
    """
    Main function to execute CRC calculations for given input values.
    """
    val = '530008000460'  # Input value for CRC calculation
    # 0x11021 - Polynomial
    # 0x1D0F - Initial value
    # 0 - XOR value
    # False - Reverse input and output bytes    
    # Create CRC function with polynomial
    # codecs.decode(val,'hex') - Convert hex string to bytes
    # str(hex(crc16(codecs.decode(val,'hex')))) - Calculate CRC for hex input
    # hex_crc.replace('0x', '') - Remove '0x' prefix
    # print() - Print hex CRC value
    crc16=crcmod.mkCrcFun(0x11021, initCrc=0x1D0F, xorOut=0, rev=False) # Create CRC function with polynomial
    hex_crc = str(hex(crc16(codecs.decode(val,'hex'))))  # Calculate CRC for hex input
    hex_crc = hex_crc.replace('0x', '') # Remove '0x' prefix 0xAAEB
    print(hex_crc)  # Print hex CRC value

    # Calculate CRC for ASCII input 
    # val.encode() - Convert string to bytes
    # hex() - Convert bytes to hex string
    # replace('0x', '') - Remove '0x' prefix
    # print() - Print ASCII CRC value
    ascii_crc = hex(crc16(val.encode()))  # Calculate CRC for ASCII input
    ascii_crc = ascii_crc.replace('0x', '')  # Remove '0x' prefix 0x236D
    print(ascii_crc)  # Print ASCII CRC value