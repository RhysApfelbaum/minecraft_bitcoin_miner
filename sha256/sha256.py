import struct

INIT_STATE = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19
]

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

test_message = b''

# Format 32 bit int as hex
def prettyhex32(x: int) -> str:
    raw = '{:08x}'.format(x)
    result = ''
    for i in range(0, 8, 2):
        result += raw[i] + raw[i + 1] + ' '
    return result

# SHA256 main functions
def majority(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)

def choice(x: int, y: int, z: int) -> int:
    return (x & y) ^ (~x & z)

def rotate(x: int, bits: int) -> int:
    return (x >> bits) | (x << (32 - bits)) 

def sigma0(x: int) -> int:
    return rotate(x, 7) ^ rotate(x, 18) ^ (x >> 3)

def sigma1(x: int) -> int:
    return rotate(x, 17) ^ rotate(x, 19) ^ (x >> 10)

def cap_sigma0(x: int) -> int:
    return rotate(x, 2) ^ rotate(x, 13) ^ rotate(x, 22)

def cap_sigma1(x: int) -> int:
    return rotate(x, 6) ^ rotate(x, 11) ^ rotate(x, 25)

def bytes_to_ints(b: bytes) -> list[int]:
    return [i[0] for i in struct.iter_unpack('>I', b)] 

# This is the tricky part
def prepare_chunks(raw_message: bytes) -> list[list[int]]:
    message = raw_message + b'\x80'
    result = []
    start = 0
    message_length = len(message)
    while message_length - start > 64:
        result.append(bytes_to_ints(message[start : start + 64]))
        start += 64
    last_chunk = message[start:]
    last_chunk += b'\0' * (56 - len(last_chunk)) + struct.pack('>Q', len(raw_message) * 8)
    result.append(bytes_to_ints(last_chunk))
    return result

def expand(w: list[int]) -> int:
    w.append(w[0] + sigma0(w[1]) + w[9] + sigma1(w[14]))
    return w.pop(0)

def compress(state: list[int], chunk: list[int], k: list[int]) -> list[int]:
    for i in range(64):
        letters = 'abcdefgh'
        for x in range(8): print('round', i, letters[x], ':' , prettyhex32(state[x])) 
        print()
        t1 = state[7] + cap_sigma1(state[4]) + choice(state[4], state[5], state[6]) + k[i] + expand(chunk)
        t2 = cap_sigma0(state[0]) + majority(state[0], state[1], state[2])

        state[7] = state[6]
        state[6] = state[5]
        state[5] = state[4]
        state[4] = (state[3] + t1) & 0xffffffff
        state[3] = state[2]
        state[2] = state[1]
        state[1] = state[0]
        state[0] = (t1 + t2) & 0xffffffff
        input()
    return state

def sha256(message: bytes) -> list[int]:
    state = INIT_STATE
    working_vars = state
    for chunk in prepare_chunks(message):
        working_vars = compress(working_vars, chunk, K)
        state = [0xffffffff & sum(i) for i in zip(state, working_vars)]
    return state

digest = sha256(test_message)
for i in digest:
    print(prettyhex32(i & 0xffffffff))