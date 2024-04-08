import os

ROOT_DIR = "./datafiles/graphics/"
OUTPUT_DIR = "./tiles"


PNG_HEADER = "8950 4e47 0d0a 1a0a"
JPEG_HEADER = "ffd8ffe1"
JFIF_HEADER = "ffd8ffe000104a464946"
IHDR_LENGTH = "0000 000d"
CHUNK_TYPE = "49484452" #(IHDR)


def decode_df_image(df_file):
  binary_df = open(df_file, "rb").read()
  hexa_df = binary_df.hex()
  position_chunk_type = hexa_df.find(CHUNK_TYPE)
  if position_chunk_type != -1:
    return (bytes.fromhex(PNG_HEADER + IHDR_LENGTH + hexa_df[position_chunk_type:]), 'png')
  
  for header, extension in [(JPEG_HEADER,'jpg'), (JFIF_HEADER, 'jpg')]:
    position_signature = hexa_df.find(header)
    if position_signature != -1:
      return (bytes.fromhex(hexa_df[position_signature:]), extension)
  return (None, None)

def main():
  for root, _, files in os.walk(ROOT_DIR):
    for file in files:
      if file.endswith(".df"):
        binary_png, extension = decode_df_image(os.path.join(root, file))
        if binary_png:
          output_dir = os.path.join(OUTPUT_DIR, root)
          if not os.path.exists(output_dir): os.mkdir(output_dir)
          with open(os.path.join(output_dir, file.replace(".df","."+extension)), "wb") as f:
            f.write(binary_png)
        else:
          print("error with", file)

if __name__ == "__main__":
    main()