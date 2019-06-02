# coding: utf8
# vim: set noexpandtab:

from PR01.es import *

def print_bits(file_name):
	'''
	Print the content of a file as bits.

	:param file_name: the name of the file
	'''
	with open(file_name, 'rb') as f_in:
		for count, bit in enumerate(bits(f_in)):
			if count > 0 and count % 8 == 0:
				print('.', end='')
			print(bit, end='')
		print()

if __name__ == '__main__':
	print_bits('exemple-sujet.txt')
