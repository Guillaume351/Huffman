# coding: utf8
# vim: set noexpandtab:

'''
Print the content of a file in a tabular way, each byte on a line.
First column is the number of the byte.
Second colum is the byte (0 <= byte <= 255).
Third colum is the binary representation of the byte.
Last colum is the string representation of the byte (using string_from_byte).
'''

from es import *

def print_byte_bin_ascii(file_name):
	with open(file_name, 'rb') as f_in:
		print('{:>4} {:>4} {:>8} {}'.format('#', 'byte', 'binary', 'ASCII'))
		number = None
		for number, byte in enumerate(bytes(f_in)):
			print('{:4} {:4} {:08b} {}'.format(number, byte, byte, string_from_byte(byte)))
		if number is None:
			print('empty file')


if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		print_byte_bin_ascii(sys.argv[1])
