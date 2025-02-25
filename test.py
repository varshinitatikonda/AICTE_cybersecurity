from PIL import Image
import hashlib
import os


def sanitize_path(path: str) -> str:
    """Remove surrounding quotes and whitespace from paths."""
    return path.strip(' "\'')


def encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    """XOR encrypt/decrypt data with a key."""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])


def encode_image(image_path, data, password, output_path):
    try:
        # Sanitize and validate paths
        image_path = sanitize_path(image_path)
        output_path = sanitize_path(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Open and convert image to RGB
        img = Image.open(image_path).convert("RGB")
        encoded = img.copy()
        width, height = img.size
        pixels = encoded.load()

        # Encrypt data
        key = hashlib.sha256(password.encode()).digest()
        encrypted_data = encrypt_decrypt(data.encode(), key)

        # Convert to binary with delimiter
        delimiter = b'1111111111111110'
        data_bin = ''.join(format(b, '08b') for b in encrypted_data) + delimiter.decode()
        data_len = len(data_bin)

        # Check message size
        max_capacity = width * height * 3
        if data_len > max_capacity:
            raise ValueError(f"Message too large! Max capacity: {max_capacity // 8} characters")

        # Embed data in LSBs
        data_index = 0
        for row in range(height):
            for col in range(width):
                if data_index >= data_len:
                    break
                r, g, b = pixels[col, row]

                # Modify channels
                r = (r & ~1) | int(data_bin[data_index])
                data_index += 1

                if data_index < data_len:
                    g = (g & ~1) | int(data_bin[data_index])
                    data_index += 1

                if data_index < data_len:
                    b = (b & ~1) | int(data_bin[data_index])
                    data_index += 1

                pixels[col, row] = (r, g, b)

        encoded.save(output_path)
        print(f"Success! Encrypted message saved to:\n{output_path}")
        return True

    except Exception as e:
        print(f"Encoding Error: {str(e)}")
        return False


def decode_image(image_path, password):
    try:
        image_path = sanitize_path(image_path)
        img = Image.open(image_path).convert("RGB")
        width, height = img.size
        pixels = img.load()

        # Extract LSBs
        data_bin = []
        for row in range(height):
            for col in range(width):
                r, g, b = pixels[col, row]
                data_bin.append(str(r & 1))
                data_bin.append(str(g & 1))
                data_bin.append(str(b & 1))

        data_bin = ''.join(data_bin)

        # Find delimiter
        delimiter = '1111111111111110'
        delimiter_index = data_bin.find(delimiter)
        if delimiter_index == -1:
            return "No hidden message found or incorrect password!"

        encrypted_bin = data_bin[:delimiter_index]

        # Convert to bytes
        try:
            encrypted_bytes = bytes([
                int(encrypted_bin[i:i + 8], 2)
                for i in range(0, len(encrypted_bin), 8)
            ])
        except ValueError:
            return "Invalid message encoding detected!"

        # Decrypt data
        key = hashlib.sha256(password.encode()).digest()
        decrypted_data = encrypt_decrypt(encrypted_bytes, key)

        return decrypted_data.decode(errors='ignore')

    except Exception as e:
        return f"Decoding Error: {str(e)}"


if __name__ == "__main__":
    action = input("Encode (e) or Decode (d)? ").lower()

    if action == 'e':
        img_path = input("Input image path: ")
        message = input("Message to hide: ")
        password = input("Encryption password: ")
        output_path = input("Output image path (use PNG): ")

        encode_image(img_path, message, password, output_path)

    elif action == 'd':
        img_path = input("Encoded image path: ")
        password = input("Decryption password: ")
        result = decode_image(img_path, password)
        print("\nDecrypted Message:", result)

    else:
        print("Invalid choice! Please enter 'e' or 'd'.")