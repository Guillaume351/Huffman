# coding: utf8
# vim: set noexpandtab:

'''
Some functions to manipulate binary files...

Author : Xavier Crégut <prenom.nom@enseeiht.fr>
'''

def one_byte(binary_file):
    '''
    Returns the next byte from a binary file.

    :param binary_file: a binary file (opened with option 'b')
    :returns: the next byte or None if end of file is reached
    '''
    bytes = binary_file.read(1)
    if len(bytes) == 0:
        return None
    else:
        return bytes[0]

def write_byte(binary_file, byte):
    '''
    Write a byte in a binary file.

    :param binary_file: the byte is written in this file
    :param byte: the byte to write
    '''
    assert 0 <= byte <= 255
    binary_file.write(byte.to_bytes(1, 'little'))


def bytes(binary_file):
    for line in binary_file:
        for byte in line:
            yield byte

def bits(binary_file):
    '''
    Returns one bit at a time from the remaning bytes of a binary file.
    '''

    for byte in bytes(binary_file):
        for i in range(8):
            yield (byte >> 7)
            byte = (byte << 1) & 255
    '''
    byte = one_byte(binary_file)
    while byte != None:
        for i in range(8):
            yield (byte >> 7)
            byte = (byte << 1) & 255
        byte = one_byte(binary_file)
    '''


def string_from_byte(byte):
    '''
    A string representation of that byte.

    :param byte: a byte (-1 <= byte <= 255)
    :returns: the string representation of that byte
    '''
    assert -1 <= byte <= 255
    if byte == -1:
        return "'\\$'"
    elif byte == ord("'"):
        return "'\\''"
    else:
        return repr(chr(byte))


