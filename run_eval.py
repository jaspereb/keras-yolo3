import sys
import argparse
from yolo import YOLO, detect_video
from PIL import Image
import time
import os
import numpy as np

def detect_img(yolo):
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)
            r_image.show()
    yolo.close_session()

FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model_path', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--dataset_path', type=str,
        help='path to the VOC dataset top dir  '
    )

    parser.add_argument(
        '--anchors_path', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes_path', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    yolo = YOLO(**vars(FLAGS))



    """ 
    Evaluate against the test set and create a .txt file that the matlab VOC scripts can use 
    """
    print("Running tests")
    dataset_path = FLAGS.dataset_path

    testPath = dataset_path + 'ImageSets/Main/test.txt'
    imgsPath = dataset_path + 'JPEGImages/'

    visualise = False

    testFile = open(testPath, 'r')

    resultPath = os.path.split(FLAGS.model_path)[0]
    resultPath = os.path.join(resultPath, 'detections.txt')
    resultFile = open(resultPath, 'w')

    firstStart = time.time()
    cont = testFile.readlines()
    for i in range(0, len(cont)):
        print("detecting image: {}".format(cont[i].rstrip()))

        imgPath = imgsPath + cont[i].rstrip() + '.jpg'
        try:
            image = Image.open(imgPath)
        except:
            print('Image Open Error')

        out_boxes, out_scores, out_classes = yolo.get_boxes(image)

        if visualise:
            r_image = yolo.detect_image(image)
            r_image.show()

        for idx, c in reversed(list(enumerate(out_classes))):
            predicted_class = 'plum'
            box = out_boxes[idx]
            score = out_scores[idx]


            top, left, bottom, right = box #left,top,right,bottom = x0,y0,x1,y1
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))

            dataline = cont[i].rstrip() + ' ' + str(score) + ' ' + str(left) + ' ' + str(top) + ' ' + str(right) + ' ' + str(bottom) + '\n'
            resultFile.write(dataline)
            print(dataline)



    print("DONE~!! Don't forget to move the timing.txt file into the right folder")
    print("Detected on {} images in {} sec".format(len(cont), time.time() - firstStart))

    yolo.close_session()
