from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from itertools import product

allowed_chars = [chr(i) for i in range(ord('A'), ord('Z')+1) + range(ord('a'), ord('z')+1)]

BLOCK_SIZE = 32
PADDING = ' '

# def pad(s):
# 	return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

def pad(s):
	return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

def encrypt(key, data):
	return AES.new(key).encrypt(pad(data))

def decrypt(key, data):
	return AES.new(key).decrypt(data)


key1 = b'abcdefghjklmabcdefghjklmijaq'
key2 = b'aaaa'
key = key1 + key2

data = '''123121241 1233
1231231231 1231
1231231234 4531
3242342342 1351
4353453134 5432'''

encrypted = encrypt(key, data)

# for pwd_list in product(allowed_chars, repeat=len(key2)):
# 	testing_key = ''.join(pwd_list)
# 	key = key1 + testing_key
# 	decrypted = decrypt(key, encrypted)

# 	if ord(decrypted[-1]) > 0 and ord(decrypted[-1]) < 32:
# 		decrypted = decrypted[:-ord(decrypted[-1])]

# 	is_decrypted = True
# 	for number in decrypted.split():
# 		if not number.isdigit():
# 			is_decrypted = False
# 			break
# 	if is_decrypted:
# 		print pwd_list
# 		print decrypted
# 		break


def bruteforce(encrypted, allowed_chars, key_prefix, suffix_length):
	for chars_combination in product(allowed_chars, repeat=suffix_length):
		key = key_prefix + ''.join(chars_combination)
		decrypted = decrypt(key, encrypted)

		# at least first char should be a digit
		# fast check
		if not decrypted[0].isdigit():
			continue
		if ord(decrypted[-1]) > 0 and ord(decrypted[-1]) < 32:
			pad_char = decrypted[-1]
			pad_size = ord(pad_char)
			if decrypted[-pad_size:] != pad_char * pad_size:
				continue
			decrypted = decrypted[:-ord(decrypted[-1])]

		is_decrypted = True
		for number in decrypted.split():
			if not number.isdigit():
				is_decrypted = False
				break

		if is_decrypted:
			return decrypted
	print "DIDNT FIND ANYTHING :("

#print bruteforce(encrypted, allowed_chars, key1, len(key2))