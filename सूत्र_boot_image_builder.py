# 🕉️ सूत्र Bootable Image Builder


import os
import struct


IMAGE_NAME = "सूत्र.img"


def header_लिखो(f):

    print("Boot header लिख रहा है...")

    f.write(b"SUTRAOS")     # signature
    f.write(struct.pack("I", 1))  # version


def kernel_जोड़ो(f):

    print("Kernel जोड़ रहा है...")

    if not os.path.exists("परीक्षण.सूत्रबिन"):
        print("त्रुटि: kernel binary नहीं मिला")
        return False

    with open("परीक्षण.सूत्रबिन", "rb") as k:

        data = k.read()

        f.write(struct.pack("I", len(data)))
        f.write(data)

    return True


def build():

    print("🕉️ सूत्र Bootable Image निर्माण प्रारम्भ")

    with open(IMAGE_NAME, "wb") as f:

        header_लिखो(f)

        if not kernel_जोड़ो(f):
            return

    print("Bootable image निर्मित:", IMAGE_NAME)


build()
