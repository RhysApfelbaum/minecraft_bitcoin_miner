from struct import iter_unpack

OUTPUT_PATH = r'minecraft_bitcoin_miner\data_in\page_sequence.txt'
chunk = b'\x00\xff\x00\xff'

message_words = (i[0] for i in iter_unpack('>I', chunk))

with open(OUTPUT_PATH, 'w') as f:
    f.write(
        ','.join(
            ('{:08x}'.format(word) for word in message_words)
        )
    )
    for word in message_words:
        f.write()