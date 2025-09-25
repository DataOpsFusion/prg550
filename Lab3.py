#!/usr/bin/env python3

# Program: PRG550 Lab 03
# Student: Tan Dat, Ta
# Command: NLTK_DATA=./nltk_data/ python3 Lab3.py 2701.txt.utf-8 ignore_list.txt

import re
import sys
from nltk.tokenize import sent_tokenize
import string
from collections import Counter
import itertools
from typing import Optional

ABBREV_PLACEHOLDER = "|_"


def main():
    display()


def get_filename():
    if len(sys.argv) < 2:
        print("Usage: Lab3.py <filename> [ignore_word]")
        sys.exit(1)
    filename = sys.argv[1]
    ignore_word = sys.argv[2] if len(sys.argv) > 2 else None
    return filename, ignore_word


def read_file_chunk(filename, chunk_size=4096):
    with open(filename, 'r', encoding='utf-8') as file:
        buffer = ""
        while chunk := file.read(chunk_size):
            buffer += chunk
            if buffer.count('"') % 2 == 1:
                continue

            yield buffer
            buffer = ""


def read_sentence(filename):
    sanitize.whitespace = re.compile(r'\s+')
    sanitize.space = r' '
    sanitize.ellipsis_match = re.compile(r'\.{3,} ([A-Z])')
    sanitize.ellipsis_replacement = r'. \1'
    sanitize.abbrev_match = re.compile(r'(\.)( +)([a-z0-9])')
    sanitize.abbrev_replacement = fr'{ABBREV_PLACEHOLDER} \3'

    buffer = ""
    for chunk in read_file_chunk(filename):
        buffer += chunk
        buffer = sanitize(buffer)
        sentences = sent_tokenize(buffer)

        yield from pop_sentence(sentences)

        last_sentence = buffer.rfind(sentences[-1])
        buffer = buffer[last_sentence:] if sentences else ""

    yield from pop_sentence(sent_tokenize(buffer), finalize=True)


def sanitize(text):
    text = re.sub(sanitize.whitespace, sanitize.space, text)
    text = re.sub(sanitize.ellipsis_match, sanitize.ellipsis_replacement, text)
    text = re.sub(sanitize.abbrev_match, sanitize.abbrev_replacement, text)

    return text


def count_word(sentence: str) -> int:
    return len(sentence.split())


def most_common_words(text: str, n=10,
                      ignore_list: Optional[list[str]] = None):
    words = re.findall(r'\b\w+\b', text.lower())
    counter = Counter(words)
    if ignore_list:
        for word in ignore_list:
            del counter[word.lower()]
    return sorted(counter.most_common(n))


def pop_sentence(sentences, finalize=False):
    while len(sentences) > 1:
        if sentences[1][0].islower():
            sentences[0] += " " + sentences.pop(1)
            continue

        yield sentences.pop(0).replace(ABBREV_PLACEHOLDER, ".")

    if finalize and sentences:
        yield sentences.pop(0).replace(ABBREV_PLACEHOLDER, ".")


def display():
    filename, ignore_word = get_filename()
    words = 0
    sentences = 0
    ignore_list_content = open(ignore_word).read().split(
        ',') if ignore_word else []
    for sentence in read_sentence(filename):
        print(f"{count_word(sentence):3} word: {sentence}")
        words += count_word(sentence)
        sentences += 1
    print("----------")
    print(f"{sentences} sentences")
    print(f"{words} words: TOTAL")
    print(
        f"Top 10 most common words: {
            most_common_words(
                open(filename).read(),
                ignore_list=ignore_list_content)}")


if __name__ == "__main__":
    main()
