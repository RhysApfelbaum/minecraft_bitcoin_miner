PREFIX = '''
` up::
press_state := 0
return
`::
if (press_state)
    return
press_state := 1

'''

BLOCK_TEMPLATE = '''
Send %d
Send {LButton}
Send {RButton}
Sleep 200
'''

msg = [
    b'\x00',
    b'\x00',
    b'\x00',
    b'\xc0',
    b'\x00',
    b'\x00',
    b'\xc0',
    b'\x00',
    b'\x00',
    b'\x00',
    b'\xc0',
    b'\xc0',
    b'\x00',
    b'\xc0',
    b'\x00',
    b'\x00',
]

msg_keys = ''
high_mask = 0x80
low_mask = 0x40
print('Item slot sequence:', end=' ')
for word in msg:
    quartal_val = bool(high_mask & word[0]) * 2 + bool(low_mask & word[0]) * 1
    inv_slot_num = quartal_val + 1
    print(inv_slot_num, end=' ')
    msg_keys += BLOCK_TEMPLATE % (quartal_val + 1)
    


with open('data_in.ahk', 'w') as f:
    f.write(PREFIX + msg_keys + 'return\n')

