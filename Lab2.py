#!/usr/bin/env python3

# Program: PRG550 Lab 02
# Student: Tan Dat, Ta
from itertools import cycle
from base64 import b64encode, b64decode
import string


def main():
    print(caesar_cipher("Have a nice day!", 5))
    print(caesar_cipher("V engr guvf rkrepvfr ng 5 fgnef...", 39))

    phrase = "Never trust an atom, they make up everything - even the stories your coffee tells you when it's too early."
    key = "atom"

    cipher = encrypt_xor(phrase, key)
    print("Encrypted:", cipher)

    decrypted = decrypt_xor(cipher, key)
    print("Decrypted:", decrypted)

    print("Round-trip success?", decrypted == phrase)


def caesar_cipher(prompt: str, key: int) -> str:
    cipher: str = ""
    shift_key: int = key % 26

    for char in prompt:
        if "a" <= char <= "z":
            cipher += chr(((ord(char) - ord("a")) + shift_key) % 26 + ord("a"))

        elif "A" <= char <= "Z":
            cipher += chr(((ord(char) - ord("A")) + shift_key) % 26 + ord("A"))

        else:
            cipher += char
    return cipher


def encrypt_xor(plain_text: str, key: str) -> str:
    plain_bytes = plain_text.encode()
    key_bytes = key.encode()
    xored_bytes = bytes(
        plain_byte ^ key_byte
        for plain_byte, key_byte in zip(plain_bytes, cycle(key_bytes))
    )
    return b64encode(xored_bytes)


def decrypt_xor(cipher_b64: str, key: str) -> str:
    cipher_bytes = b64decode(cipher_b64)
    key_bytes = key.encode()
    xored_bytes = bytes(
        cipher_byte ^ key_byte
        for cipher_byte, key_byte in zip(cipher_bytes, cycle(key_bytes))
    )
    return xored_bytes.decode()


def score_english(text):
    common_characters = " etaoinshrdlu"
    matches = sum(text.lower().count(character)
                  for character in common_characters)

    return matches / len(text) if len(text) else 0


if __name__ == "__main__":
    main()
