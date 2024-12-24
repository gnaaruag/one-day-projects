Ki = [
	0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
	0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
	0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
	0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
	0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
	0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
	0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
	0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def rotr(x, n):
	return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def Sigma0(x):
	return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)

def Sigma1(x):
	return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)

def sigma0(x):
	return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)

def sigma1(x):
	return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)

def Ch(x, y, z):
	return (x & y) ^ (~x & z)

def Maj(x, y, z):
	return (x & y) ^ (x & z) ^ (y & z)

'''
sha256 preprocessing
'''
def sha256_preprocess(message):
	message_bits = ''.join(format(ord(c), '08b') for c in message)
	curr_len = len(message_bits)
	message_bits += '1'
	# smallest non negative soln to l + 1 + k = 448 mod 512
	message_bits += '0' * ((448 - (curr_len + 1) % 512) % 512)
	message_bits += format(len(message) * 8, '064b')
	# M ||1 || 0....0 || L
	return message_bits

'''
sha256 compression
'''
def sha256_compression(block):
	hi = Hi.copy()

	words = [int(block[i:i+32], 2) for i in range(0, len(block), 32)]
	a, b, c, d, e, f, g, h = hi

	for i in range(16, 64):
		new_word = (sigma1(words[i - 2]) + words[i - 7] + sigma0(words[i - 15]) + words[i - 16]) & 0xFFFFFFFF
		words.append(new_word)

	for i in range(64):
		T1 = (h + Sigma1(e) + Ch(e, f, g) + Ki[i] + words[i]) & 0xFFFFFFFF
		T2 = (Sigma0(a) + Maj(a, b, c)) & 0xFFFFFFFF

		h = g
		g = f
		f = e
		e = (d + T1) & 0xFFFFFFFF
		d = c
		c = b
		b = a
		a = (T1 + T2) & 0xFFFFFFFF

	for i in range(8):
		hi[i] = (hi[i] + [a, b, c, d, e, f, g, h][i]) & 0xFFFFFFFF
 
	return hi

'''
sha256 computation
'''
def sha256_computation(block):
	# message preprocessing
	blocks = [block[i:i+512] for i in range(0, len(block), 512)]
	global Hi
	Hi = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
	for block in blocks:
		Hi = sha256_compression(block)
	return ''.join(f'{h:08x}' for h in Hi)
		
'''
sha256 aggregation
'''
def sha256(message):
	# preprocess
	padded_message = sha256_preprocess(message)
	# hash computation
	fin_hash = sha256_computation(padded_message)
	return fin_hash

'''
simple function to test the sha256 implementation
'''
def test():
	messages = ["hello", "wxwx"*10, "ayz"*100, "mel"*1000]

	expected_hashes = [
		"2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
		"ebded9ded85f4592f18437b98c31beb6dda930d7ea47937f5e86800309a015be",
		"4d814954b607b9549b8aec28c996d3ecc5996b0d86db988459af5ea6c8d489c3",
		"b0b8563ef1b40796f4a0e15eeabbd08e3a096157e057b7901a8dfa132097e75e"
	]

	for i, message in enumerate(messages):
		computed_hash = sha256(message)
		print(f"Expected: {expected_hashes[i]}")
		print(f"Computed: {computed_hash}")
		assert computed_hash == expected_hashes[i], f"Mismatch: '{message}'"
test()

