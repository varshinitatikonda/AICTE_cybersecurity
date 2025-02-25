# Image Steganography Tool

This project provides a simple steganography tool to hide and retrieve encrypted messages within images using the Least Significant Bit (LSB) method.

## Features
- Hide a secret message inside an image.
- Encrypt the message using a password-based XOR encryption.
- Retrieve and decrypt the hidden message from an encoded image.
- Supports PNG images for encoding and decoding.

## Requirements
Ensure you have the following installed:
- Python 3.x
- Pillow (PIL fork) for image processing

You can install the required package using:
```bash
pip install pillow
```

## Usage
Run the script and follow the prompts.

### Encoding a Message
```bash
python test.py
```
Select `e` for encoding, then provide:
- The path to the input image.
- The message to hide.
- A password for encryption.
- The path to save the output image (use PNG format).

Example:
```
Input image path: input.png
Message to hide: Hello, World!
Encryption password: mysecurepassword
Output image path: output.png
```

### Decoding a Message
```bash
python test.py
```
Select `d` for decoding, then provide:
- The path to the encoded image.
- The password used for encryption.

Example:
```
Encoded image path: output.png
Decryption password: mysecurepassword
```
The hidden message will be displayed if the correct password is used.

## How It Works
1. **Encryption:** The message is encrypted using an XOR operation with a key derived from the SHA-256 hash of the password.
2. **Encoding:** The encrypted message is converted into binary and embedded into the Least Significant Bits (LSBs) of the image pixels.
3. **Decoding:** The LSBs are extracted, the encrypted message is reconstructed, and then decrypted using the password.
4. **Delimiter:** A predefined binary delimiter (`1111111111111110`) marks the end of the message.

## Limitations
- The message size must not exceed the image's capacity.
- The output image must be saved as PNG to avoid compression artifacts.
- Incorrect passwords result in unreadable decrypted messages.
