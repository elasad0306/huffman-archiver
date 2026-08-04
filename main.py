from collections import Counter
import heapq
import pickle
import os

class node_model:
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other: node_model):
        return self.freq < other.freq

def get_code(node: node_model, current_code: str, codes: dict):

    if node.char is not None:
        codes[node.char] = current_code
    else:
        get_code(node.left, current_code + "0", codes)
        get_code(node.right, current_code + "1", codes)

def compress_to_bytes(encoded_text):
   padding_value = (8 - len(encoded_text) % 8)% 8
   encoded_text += "0" * padding_value
   byte_array = bytearray()

   for i in range(0, len(encoded_text), 8):
       byte_chunk = encoded_text[i:i+8]
       byte_array.append(int(byte_chunk, 2))
   return padding_value, bytes(byte_array) 


def write_huffman_file(output_filename, padding_value, frequencies, compressed_bytes):
    with open(output_filename, "wb") as f:
        f.write(bytes([padding_value]))

        freq_bytes = pickle.dumps(frequencies)

        f.write(len(freq_bytes).to_bytes(4, byteorder='big'))
        f.write(freq_bytes)
        f.write(compressed_bytes)

if __name__ == "__main__":
    file_path = "./tests/picture.jpg"

    with open(file_path, 'rb') as f:
        text = f.read()

    frequencies = Counter(text)

    heap = [node_model(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = node_model(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    root = heap[0]

    huffman_codes = {}
    get_code(root, "", huffman_codes)

    encoded_text = "".join(huffman_codes[char] for char in text)

    padding, compressed_data = compress_to_bytes(encoded_text)

    file_name_only, extension = os.path.splitext(os.path.basename(file_path))

    output_filename = f"./tests/compressed_file/arch_{file_name_only}.huff"

    write_huffman_file(output_filename, padding, frequencies, compressed_data)

    print("Compression terminée avec succès")
    print(f"Nom du fichier:{os.path.basename(output_filename)}")