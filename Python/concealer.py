"""
This module includes encoding functionality to conceal credentials used throughout the funspace project
"""
import base64


def encode_string_with_key_vigenere(key: str, clear: str) -> str:
    """
    Using a Vigenere cypher, encode a string using another.

    :param key: a string to use as a key/cypher
    :param clear: the text to encode
    :return: the encryted/encoded string
    """
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]

        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)

        enc.append(enc_c)

    encoded = base64.urlsafe_b64encode(''.join(enc).encode()).decode()
    return encoded





