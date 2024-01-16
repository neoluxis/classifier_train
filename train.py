import cv2 as cv
import os

from config import *


def shot():
    if not os.path.exists(f'{dataset_path}/{posi_path}'):
        os.makedirs(f'{dataset_path}/{posi_path}')
    if not os.path.exists(f'{dataset_path}/{nega_path}'):
        os.makedirs(f'{dataset_path}/{nega_path}')
    cam = cv.VideoCapture(1)
    tpos = len(os.listdir(f'{dataset_path}/{posi_path}'))
    tneg = len(os.listdir(f'{dataset_path}/{nega_path}'))
    mode = True  # True: posi, False: nega
    while True:
        ret, frame = cam.read()
        if not ret:
            print('failed to grab frame')
            continue
        cv.imshow('Cam', frame)
        k = cv.waitKey(1)
        if k == ord('q'):
            break
        if k == ord('s'):
            if mode:
                cv.imwrite(f'{dataset_path}/{posi_path}/{tpos:04d}.jpg', frame)
                print(f'{dataset_path}/{posi_path}/{tpos:04d}.jpg')
                tpos += 1
            else:
                cv.imwrite(f'{dataset_path}/{nega_path}/{tneg:04d}.jpg', frame)
                print(f'{dataset_path}/{nega_path}/{tneg:04d}.jpg')
                tneg += 1
        if k == ord('n'):
            mode = not mode
            if mode:
                print(f'Folder: {posi_path}')
            else:
                print(f'Folder: {nega_path}')


def labeling():
    # run system labelImg.exe
    print(
        f"Please label the images in {dataset_path}/{posi_path} \nwith tools in {labelor}/{labelor_exe}.")
    print(f"When finish, press any key to continue.")
    os.system('pause')


def txt2dat(files):
    # positive samples
    data = {}
    for file in files:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                datum = line.split(",")
                file_name = datum[0]
                position = datum[1:]
                if file_name not in data:
                    data[file_name] = position
                else:
                    data[file_name].extend(position)

        with open(f'{posi_dat_fname}', "w") as f:
            for file_name, data_list in data.items():
                f.write("%s %d %s\n" % (file_name, len(data_list) //
                        4, " ".join(map(str, data_list))))
    # negative samples
    abs_path = os.path.abspath(f'{dataset_path}/{nega_path}')
    with open(f'{nega_dat_fname}', "w") as f:
        for file_name in os.listdir(f'{dataset_path}/{nega_path}'):
            f.write(f'{abs_path}/{file_name}\n')

if __name__ == '__main__':
    txt2dat([f'{dataset_path}/{posi_path}/{posi_anno_fname}'])
