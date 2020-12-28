import os
from pathlib import Path
import random

def delete_images(path, number_of_images, extension='jpg'):
    images = Path(path).glob(f'*.{extension}')
    for image in random.sample(images, number_of_images):
        image.unlink()

def drop_frames(path):
    x = [x[0] for x in os.walk(path)]
    for dir in x[1:]:
        files = os.listdir(dir)
        num_files_to_remove = len(files) - 1 
        for file in files[:num_files_to_remove]:
            os.remove(dir + '\\' + file)
    print('Removed Frames')

if __name__ == '__main__':
    drop_frames('output2')