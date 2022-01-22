import os
import sys
import time
import traceback
import ctypes

version = '0.2.1'

import argparse
parser = argparse.ArgumentParser(description = 'Encodes or decodes Game Genie codes on all platforms it has been released in (NES/SNES/GB, etc.)', epilog = 'See README.md for more information.\n\nGGWorkshop {0}\n(c) 2022 GamingWithEvets Inc. All rights reserved.'.format(version), formatter_class=argparse.RawTextHelpFormatter, allow_abbrev = False)
parser.add_argument('option', choices = ['encode', 'decode'], metavar = '<option>', default = 'decode', help = 'program mode - encode/decode')
parser.add_argument('platform', choices = ['nes', 'snes', 'gb', 'gear', 'mega'], metavar = '<platform>', default = 'nes', help = 'game genie platform - nes/gb/gear/snes/mega')
parser.add_argument('address', metavar = '<address/code>', help = 'if "encode" option is used, this is the hex address used for encryption. if not, this is the code used for decryption.')
parser.add_argument('value', metavar = '<value>', nargs = '?', help = 'hex value used for encryption (MUST BE USED with "encode" option)')
parser.add_argument('condition', metavar = '<condition>', nargs = '?', help = 'conditional hex value used for encryption (optional; MUST BE USED with "encode" option)')
parser.add_argument('-n', '--nologo', action = 'store_true', help = 'skips the logo animation on startup')
parser.add_argument('-a', '--autoexit', action = 'store_true', help = 'skips the Enter presses when exiting')
args = parser.parse_args()
if args.option == 'encode':
	if not args.value:
		parser.error('the following arguments are required when using "encode" option: <value>')

if args.option == 'encode':
	try: testval_a = int(args.address, 16)
	except ValueError: parser.error('invalid hex address: $' + args.address)
	try: testval_v = int(args.value, 16)
	except ValueError: parser.error('invalid hex value: #$' + args.value)
	try:
		if args.condition: testval_c = int(args.condition, 16)
	except ValueError: parser.error('invalid conditional hex value: #$' + args.condition)

	if len(args.address) != 4:
		parser.error('hex address must be 4 digits')
	if len(args.value) != 2:
		parser.error('hex value must be 2 digits')
	if args.condition and len(args.condition) != 2:
		parser.error('conditional hex value must be 2 digits')

	if testval_a < 32768 or testval_a > 65535:
		parser.error('hex address must be between $8000 and $FFFF')
	if testval_v < 0 or testval_v > 255:
		parser.error('hex value must be between #$00 and #$FF')
	if args.condition and testval_c < 0 or testval_v > 255:
		parser.error('conditional hex value must be between #$00 and #$FF')

option = args.option
platform = args.platform
if option == 'encode':
	address = args.address
	value = args.value
	if args.condition: condition = args.condition
	else: condition = ''
elif option == 'decode':
	code = args.address

ctypes.windll.kernel32.SetConsoleTitleW('GGWorkshop by GamingWithEvets v.' + version)

def codetolist(code):
	return [char for char in code]

def join(l):
	converted = ''
	for bit in l:
		converted += bit

	return converted


class NES():
	def __init__(self):
		self.letters = {
			'A': '0000',
			'P': '0001',
			'Z': '0010',
			'L': '0011',
			'G': '0100',
			'I': '0101',
			'T': '0110',
			'Y': '0111',
			'E': '1000',
			'O': '1001',
			'X': '1010',
			'U': '1011',
			'K': '1100',
			'S': '1101',
			'V': '1110',
			'N': '1111'
		}

	def invalid_code(self):
		print('This NES Game Genie code is INVALID!\nCheck if there are any spaces in your code and try again.')
		quitter()

	def decoder(self, code):
		self.code_str = code.upper()

		self.code = codetolist(self.code_str)

		if len(self.code) != 6:
			if len(self.code) != 8:
				self.invalid_code()

		self.code_true = []
		self.invalid = False
		for letter in self.code:
			if letter in list(self.letters.keys()):
				self.code_true.append(letter)
			else:
				self.invalid = True
				self.code_true.append('A')

		self.code_true_str = join(self.code_true)

		self.code_bin = []
		for char in self.code:
			if char.isspace() or char.isnumeric():
				self.invalid_code()

			self.i = 1
			while self.i != 16:
				if char.upper() == list(self.letters.keys())[self.i]:
					self.code_bin.append(list(self.letters.values())[self.i])
					break

				self.i += 1
				if self.i == 16:
					self.code_bin.append(list(self.letters.values())[0])

		self.bits_bin = []
		for bits in self.code_bin:
			self.bits_bin.append(codetolist(bits))

		self.code_reformat = []
		self.code_reformat.append(['1', self.bits_bin[3][1], self.bits_bin[3][2], self.bits_bin[3][3]])
		self.code_reformat.append([self.bits_bin[4][0], self.bits_bin[5][1], self.bits_bin[5][2], self.bits_bin[5][3]])
		self.code_reformat.append([self.bits_bin[1][0], self.bits_bin[2][1], self.bits_bin[2][2], self.bits_bin[2][3]])
		self.code_reformat.append([self.bits_bin[3][0], self.bits_bin[4][1], self.bits_bin[4][2], self.bits_bin[4][3]])
		if len(self.code) == 6:
			self.code_reformat.append([self.bits_bin[0][0], self.bits_bin[1][1], self.bits_bin[1][2], self.bits_bin[1][3]])
			self.code_reformat.append([self.bits_bin[5][0], self.bits_bin[0][1], self.bits_bin[0][2], self.bits_bin[0][3]])
		elif len(self.code) == 8:
			self.code_reformat.append([self.bits_bin[6][0], self.bits_bin[7][1], self.bits_bin[7][2], self.bits_bin[7][3]])
			self.code_reformat.append([self.bits_bin[5][0], self.bits_bin[6][1], self.bits_bin[6][2], self.bits_bin[6][3]])
			self.code_reformat.append([self.bits_bin[0][0], self.bits_bin[1][1], self.bits_bin[1][2], self.bits_bin[1][3]])
			self.code_reformat.append([self.bits_bin[7][0], self.bits_bin[0][1], self.bits_bin[0][2], self.bits_bin[0][3]])

		self.code_reformat_joined = []
		for item in self.code_reformat:
			self.code_reformat_joined.append(join(item))

		self.address = ''
		self.value = ''
		self.condition = ''
		for i in range(4):
			self.address += str(hex(int(self.code_reformat_joined[i], 2))).upper()[2:]
		if len(self.code) == 8:
			for i in range(4, 6):
				self.condition += str(hex(int(self.code_reformat_joined[i], 2))).upper()[2:]
			for i in range(6, 8):
				self.value += str(hex(int(self.code_reformat_joined[i], 2))).upper()[2:]
		elif len(self.code) == 6:
			for i in range(4, 6):
				self.value += str(hex(int(self.code_reformat_joined[i], 2))).upper()[2:]

		print('NES Game Genie code decoded successfully.\n\nCode: {0}'.format(self.code_str))

		if self.invalid:
			print('\nThis code contains INVALID letters and will NOT work on a real NES Game Genie.\nTo use this code on real hardware, use this replacement code: ' + self.code_true_str)

		if len(self.code) == 8:
			print('\nAddress: {0}\nCondition: {1}\nValue: {2}\n\nIf the value at ${0} is equal to #${1},\nthis code will substitute it with #${2}.'.format(self.address, self.condition, self.value))
		elif len(self.code) == 6:
			print('\nAddress: {0}\nValue: {1}\n\nThis code will substitute the value at ${0} with #${1}.'.format(self.address, self.value))

	def encoder(self, address, value, condition):
		self.address = address.upper()
		self.condition = condition.upper()
		self.value = value.upper()

		self.code_bin = []
		for i in self.address:
			self.code_bin.append(str(bin(int(i, 16)))[2:].zfill(4))
		if self.condition:
			for i in self.condition:
				self.code_bin.append(str(bin(int(i, 16)))[2:].zfill(4))
		for i in self.value:
			self.code_bin.append(str(bin(int(i, 16)))[2:].zfill(4))

		self.bits_bin = []
		for bits in self.code_bin:
			self.bits_bin.append(codetolist(bits))

		self.code_reformat = []
		if not self.condition:
			self.code_reformat.append([self.bits_bin[4][0], self.bits_bin[5][1], self.bits_bin[5][2], self.bits_bin[5][3]])
			self.code_reformat.append([self.bits_bin[2][0], self.bits_bin[4][1], self.bits_bin[4][2], self.bits_bin[4][3]])
		else:
			self.code_reformat.append([self.bits_bin[6][0], self.bits_bin[7][1], self.bits_bin[7][2], self.bits_bin[7][3]])
			self.code_reformat.append([self.bits_bin[2][0], self.bits_bin[6][1], self.bits_bin[6][2], self.bits_bin[6][3]])
		self.code_reformat.append(['0', self.bits_bin[2][1], self.bits_bin[2][2], self.bits_bin[2][3]])
		self.third_letter_too = ['1', self.bits_bin[2][1], self.bits_bin[2][2], self.bits_bin[2][3]]
		self.code_reformat.append([self.bits_bin[3][0], self.bits_bin[0][1], self.bits_bin[0][2], self.bits_bin[0][3]])
		self.code_reformat.append([self.bits_bin[1][0], self.bits_bin[3][1], self.bits_bin[3][2], self.bits_bin[3][3]])
		self.code_reformat.append([self.bits_bin[5][0], self.bits_bin[1][1], self.bits_bin[1][2], self.bits_bin[1][3]])
		if self.condition:
			self.code_reformat.append([self.bits_bin[4][0], self.bits_bin[5][1], self.bits_bin[5][2], self.bits_bin[5][3]])
			self.code_reformat.append([self.bits_bin[7][0], self.bits_bin[4][1], self.bits_bin[4][2], self.bits_bin[4][3]])

		self.code_reformat_joined = []
		for item in self.code_reformat:
			self.code_reformat_joined.append(join(item))

		self.third_letter_too_joined = join(self.third_letter_too)
		self.third_letter_too_str = list(self.letters.keys())[list(self.letters.values()).index(self.third_letter_too_joined)]

		self.code = []
		for bits in self.code_reformat_joined:
			self.code.append(list(self.letters.keys())[list(self.letters.values()).index(bits)])
		self.code_str = join(self.code)
		self.code_str_too = self.code_str[:2] + self.third_letter_too_str + self.code_str[3:]

		print('NES Game Genie code generated successfully.')
		

		if len(self.code) == 8:
			print('\nAddress: {0}\nCondition: {1}\nValue: {2}\n'.format(self.address, self.condition, self.value))
			print('Codes: {0}, {1}\n'.format(self.code_str, self.code_str_too))
			print('If the value at ${0} is equal to #${1},\nthis code will substitute it with #${2}.'.format(self.address, self.condition, self.value))
		elif len(self.code) == 6:
			print('\nAddress: {0}\nValue: {1}\n'.format(self.address, self.value))
			print('Codes: {0}, {1}\n'.format(self.code_str, self.code_str_too))
			print('This code will substitute the value at ${0} with #${1}.'.format(self.address, self.value))

# you don't mind this clear function in almost every console python script by me, eh?
def clear():
	if os.name == 'nt':
		_ = os.system('cls')
	else:
		_ = os.system('clear')

def quitter():
	if not args.autoexit:
		print('\nPress Enter 10 times to exit! Sorry if that\'s too much Enter presses for you.', end = '')
		input()
		i = 9
		while i != 0:
			print(str(i) + ' left!', end = '')
			input()
			i -= 1
		clear()
	exit()

def logo():
	if not args.nologo:
		print('  _____  _______          __        _        _\n\
 / ____|/ ____\\ \\        / /       | |      | |\n\
| |  __| |  __ \\ \\  /\\  / /__  _ __| | _____| |__   ___  _ __\n\
| | |_ | | |_ | \\ \\/  \\/ / _ \\| \'__| |/ / __| \'_ \\ / _ \\| \'_ \\\n\
| |__| | |__| |  \\  /\\  / (_) | |  |   <\\__ \\ | | | (_) | |_) |\n\
 \\_____|\\_____|   \\/  \\/ \\___/|_|  |_|\\_\\___/_| |_|\\___/| .__/\n\
   The Game Genie Encoder/Decoder by GWE - For Python   | |\n\
   Logo Designed with Text to ASCII Art Generator       |_|\n\
   patorjk.com/software/taag\n\nIf the program doesn\'t respond for a long time, please press\nCTRL+C or CTRL+BREAK and report any errors in the traceback.\n\nv.' + version)
		time.sleep(3)

try:
	clear()
	logo()
	clear()
	
	if platform == 'nes':
		ggnes = NES()
		if option == 'decode':
			ggnes.decoder(code)
		elif option == 'encode':
			ggnes.encoder(address, value, condition)
	else:
		print('GGWorkshop {0} supports NES Game Genie decoding and encoding only.\nPlease go to https://github.com/gamingwithevets/<repo name here>/releases\nto check for updates!'.format(version))

	quitter()

except KeyboardInterrupt:
	print('\nCTRL+C/CTRL+BREAK hotkey detected! Breaking program.')
	print(traceback.format_exc())
	print('If the traceback shows an error, please report it to https://github.com/gamingwithevets/<repo name here>/issues\nif possible.')
	quitter()
except Exception:
	print('\nAn error has occurred!')
	print(traceback.format_exc())
	print('If possible, please report it to https://github.com/gamingwithevets/<repo name here>/issues')
	quitter()
