from struct import iter_unpack

OUTPUT_PATH = r'minecraft_bitcoin_miner\data_in\page_sequence.txt'
chunk = b'\x12\x34\xab\xcd'

message_words = (i[0] for i in iter_unpack('>I', chunk))

with open(OUTPUT_PATH, 'w') as f:
    f.write(
        ','.join(
            ('{:x}'.format(word) for word in message_words)
        )
    )
    for word in message_words:
        f.write()

    