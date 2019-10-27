import os
import xml.dom.minidom
import argparse
import xml.etree.ElementTree as ET
from core.config import cfg

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-annotation_folder', help='Input Dataset folder', required=True)
parser.add_argument('-output_folder', help='Output annotation folder', required=True)
parser.add_argument('-data_type', help='Type of data test ot train', required=True)

def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    objs = []
    for obj in root.findall('object'):
        if obj.findall('name')[0].text in cfg.CLASS_LABELS:
            print( obj.findall('name')[0].text," is -> ", cfg.CLASS_LABELS[obj.findall('name')[0].text])
            bounding_box = obj.findall('bndbox')[0]
            row = ','.join([bounding_box.findall('xmin')[0].text, bounding_box.findall('ymin')[0].text, bounding_box.findall('ymax')[0].text, bounding_box.findall('ymax')[0].text, cfg.CLASS_LABELS[obj.findall('name')[0].text]])
            yield row


def main():
    args = parser.parse_args()
    total_rows = []
    print(args.annotation_folder)
    for file in os.listdir(os.path.join(args.annotation_folder, 'Annotations')):
        file_rows = list(parseXML(os.path.join(args.annotation_folder, 'Annotations', file)))
        if len(file_rows) == 0:
            continue
        final_row = os.path.join(args.annotation_folder, 'Annotations', file.split('.')[0] + '.jpg') + ' ' + ' '.join(file_rows)
        print(final_row)
        total_rows.append(final_row)
    
    final_file = os.path.join(args.output_folder, args.data_type + '.txt')
    w = open(final_file, 'w')
    for t in total_rows:
        w.write(t + '\n')
    w.close()
    

if __name__ == '__main__':
    main()