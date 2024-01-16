import cv2 as cv
import os

folder = 'data'
pos = 'pos'
neg = 'neg'
anno = 'annotations'
fdr = pos

if not os.path.exists(f'{folder}/{pos}/{anno}'):
    os.makedirs(f'{folder}/{pos}/{anno}')
if not os.path.exists(f'{folder}/{neg}/{anno}'):
    os.makedirs(f'{folder}/{neg}/{anno}')


def shot():
    global fdr
    cam = cv.VideoCapture(0)
    t = len(os.listdir(f'{folder}/{fdr}'))
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
            cv.imwrite(f'{folder}/{fdr}/{t:04d}.jpg', frame)
            print(f'{folder}/{fdr}/{t:04d}.jpg')
            t += 1
        if k == ord('n'):
            if fdr == pos:
                fdr = neg
            else:
                fdr = pos
            t = len(os.listdir(f'{folder}/{fdr}'))
            print(f'Folder: {fdr}')


def label():
    # run system labelImg.exe
    os.system('labelImg.exe')


def txt2dat(files):
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

        with open(f'{file}.dat', "w") as f:
            for file_name, data_list in data.items():
                f.write("%s %d %s\n" % (file_name, len(data_list) //
                        4, " ".join(map(str, data_list))))


def dat2vec():
    pass


if __name__ == "__main__":
    # shot()
    txt2dat([f'{folder}/{pos}/{anno}/pos.txt'])
    pass
