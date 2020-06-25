import xml.etree.ElementTree as ET
from os import getcwd

sets=['train', 'val']
classes = ["plum"]

# dataPath = '/home/jasper/Datasets/Day'
# dataName = 'Day'
dataPath = '/home/jasper/Datasets/Night'
dataName = 'Night'

def convert_annotation(dataPath, image_id, list_file):
    in_file = open(dataPath + '/Annotations/%s.xml'%(image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

for image_set in sets:
    image_ids = open(dataPath + '/ImageSets/Main/%s.txt'%(image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(dataName, image_set), 'w')
    for image_id in image_ids:
        list_file.write(dataPath + '/JPEGImages/%s.jpg'%(image_id))
        convert_annotation(dataPath, image_id, list_file)
        list_file.write('\n')
    list_file.close()

