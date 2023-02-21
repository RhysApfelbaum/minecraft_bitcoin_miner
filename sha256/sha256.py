import struct
import hashlib

# Unsigned integer with 32-bit overflow
class Word(int):
    MASK = 0xffffffff

    def __add__(self, other):
        return Word(int.__add__(self, other) & Word.MASK)

    def __lshift__(self, other):
        return Word(int.__lshift__(self, other) & Word.MASK)
    
    def __rshift__(self, other):
        return Word(int.__rshift__(self, other))
    
    def __or__(self, other):
        return Word(int.__or__(self, other))

    def __and__(self, other):
        return Word(int.__and__(self, other))

    def __not__(self, other):
        return Word(int.__not__(self, other))

    def __xor__(self, other):
        return Word(int.__xor__(self, other))
    
    def __repr__(self):
        return hex(self)


# Define NSA Constants

INIT_STATE = [
    Word(0x6a09e667),
    Word(0xbb67ae85),
    Word(0x3c6ef372),
    Word(0xa54ff53a),
    Word(0x510e527f),
    Word(0x9b05688c),
    Word(0x1f83d9ab),
    Word(0x5be0cd19)
]

K = [
    Word(0x428a2f98), Word(0x71374491), Word(0xb5c0fbcf), Word(0xe9b5dba5), Word(0x3956c25b), Word(0x59f111f1), Word(0x923f82a4), Word(0xab1c5ed5),
    Word(0xd807aa98), Word(0x12835b01), Word(0x243185be), Word(0x550c7dc3), Word(0x72be5d74), Word(0x80deb1fe), Word(0x9bdc06a7), Word(0xc19bf174),
    Word(0xe49b69c1), Word(0xefbe4786), Word(0x0fc19dc6), Word(0x240ca1cc), Word(0x2de92c6f), Word(0x4a7484aa), Word(0x5cb0a9dc), Word(0x76f988da),
    Word(0x983e5152), Word(0xa831c66d), Word(0xb00327c8), Word(0xbf597fc7), Word(0xc6e00bf3), Word(0xd5a79147), Word(0x06ca6351), Word(0x14292967),
    Word(0x27b70a85), Word(0x2e1b2138), Word(0x4d2c6dfc), Word(0x53380d13), Word(0x650a7354), Word(0x766a0abb), Word(0x81c2c92e), Word(0x92722c85),
    Word(0xa2bfe8a1), Word(0xa81a664b), Word(0xc24b8b70), Word(0xc76c51a3), Word(0xd192e819), Word(0xd6990624), Word(0xf40e3585), Word(0x106aa070),
    Word(0x19a4c116), Word(0x1e376c08), Word(0x2748774c), Word(0x34b0bcb5), Word(0x391c0cb3), Word(0x4ed8aa4a), Word(0x5b9cca4f), Word(0x682e6ff3),
    Word(0x748f82ee), Word(0x78a5636f), Word(0x84c87814), Word(0x8cc70208), Word(0x90befffa), Word(0xa4506ceb), Word(0xbef9a3f7), Word(0xc67178f2)
]

# SHA256 main functions
def majority(x: Word, y: Word, z: Word) -> Word:
    return (x & y) ^ (x & z) ^ (y & z)

def choice(x: Word, y: Word, z: Word) -> Word:
    return (x & y) ^ (~x & z)

# 32-bit right rotate
def rotate(x: Word, bits: Word) -> Word:
    return (x >> bits) | (x << (32 - bits)) 

def sigma0(x: Word) -> Word:
    return rotate(x, 7) ^ rotate(x, 18) ^ (x >> 3)

def sigma1(x: Word) -> Word:
    return rotate(x, 17) ^ rotate(x, 19) ^ (x >> 10)

def cap_sigma0(x: Word) -> Word:
    return rotate(x, 2) ^ rotate(x, 13) ^ rotate(x, 22)

def cap_sigma1(x: Word) -> Word:
    return rotate(x, 6) ^ rotate(x, 11) ^ rotate(x, 25)

def bytes_to_words(buffer: bytes) -> list[Word]:
    return [Word(i[0]) for i in struct.iter_unpack('>I', buffer)]

# Organise the message into chunks containing 16 Words 
def prepare_chunks(raw_message: bytes) -> list[list[Word]]:

    # Append a 1 to the end of the message
    message = raw_message + b'\x80'

    # Split the message into 64-byte chunks
    result = []
    start = 0
    message_length = len(message)
    while message_length - start > 64:
        result.append(bytes_to_words(message[start : start + 64]))
        start += 64

    # Pad the last chunk with zeros and the length of the message as a unsigned 64-bit integer
    last_chunk = message[start:]
    last_chunk += b'\0' * (56 - len(last_chunk)) + struct.pack('>Q', len(raw_message) * 8)
    result.append(bytes_to_words(last_chunk))
    return result

def expand(w: list[Word]) -> Word:
    w.append(w[0] + sigma0(w[1]) + w[9] + sigma1(w[14]))
    return w.pop(0)

def compress(state: list[Word], chunk: list[Word], k: list[Word]) -> list[Word]:
    for i in range(64):
        t1 = state[7] + cap_sigma1(state[4]) + choice(state[4], state[5], state[6]) + k[i] + expand(chunk)
        t2 = cap_sigma0(state[0]) + majority(state[0], state[1], state[2])

        state[7] = state[6]
        state[6] = state[5]
        state[5] = state[4]
        state[4] = state[3] + t1
        state[3] = state[2]
        state[2] = state[1]
        state[1] = state[0]
        state[0] = t1 + t2
    return state

def sha256(message: bytes) -> bytes:
    state = INIT_STATE
    for chunk in prepare_chunks(message):
        working_state = [i for i in state]
        working_state = compress(working_state, chunk, K)
        state = [i[0] + i[1] for i in zip(working_state, state)]
    return struct.pack('>8I', *state)

digest = sha256(b'')
print(digest.hex())