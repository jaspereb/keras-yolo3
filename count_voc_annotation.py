import xml.etree.ElementTree as ET
from os import getcwd

sets=['allData']
classes = ["plum"]

dataPath = '/home/jasper/Datasets/Day'
dataName = 'Day'
# dataPath = '/home/jasper/Datasets/Night'
# dataName = 'Night'

def count_annotation(dataPath, image_id):
    in_file = open(dataPath + '/Annotations/%s.xml'%(image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    boxes = 0

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        boxes = boxes + 1

    return boxes

for image_set in sets:
    count = 0
    image_ids = open(dataPath + '/ImageSets/Main/%s.txt'%(image_set)).read().strip().split()
    for image_id in image_ids:
        count = count + count_annotation(dataPath, image_id)

    print("For image set {} a total of {} bounding boxes were found from {} files".format(image_set, count, len(image_ids)))
