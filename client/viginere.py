def vig_encrypt(text, key):
    encrypted_text = ""
    key_length = len(key)
    key_positions = [ord(char) for char in key]

    for i in range(len(text)):
        shift = key_positions[i % key_length]
        new_char = chr((ord(text[i]) + shift) % 1114112)
        encrypted_text += new_char
        
    return encrypted_text

def vig_decrypt(encrypted_text, key):
    decrypted_text = ""
    key_length = len(key)
    key_positions = [ord(char) for char in key]

    for i in range(len(encrypted_text)):
        shift = key_positions[i % key_length]
        new_char = chr((ord(encrypted_text[i]) - shift) % 1114112)
        decrypted_text += new_char
        
    return decrypted_text