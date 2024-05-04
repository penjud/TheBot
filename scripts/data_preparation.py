import glob
import bz2
import shutil
import os

def decompress_data(input_folder, output_folder):
    files = glob.iglob(f'{input_folder}/**/*.bz2', recursive=True)
    for path in files:
        market_id = os.path.basename(path).split('.')[0]
        with bz2.BZ2File(path) as fr, open(f'{output_folder}/{market_id}.csv', "wb") as fw:
            shutil.copyfileobj(fr, fw)
        print(f"Decompressed {market_id}")

if __name__ == "__main__":
    input_folder = 'path_to_compressed_data'
    output_folder = 'path_to_simulation_data'
    decompress_data(input_folder, output_folder)
