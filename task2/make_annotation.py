
import xml.etree.ElementTree as ET
root = ET.parse('dataset/annotations.xml').getroot()
# print("root", root)
'''
class_index
0: mask no 
1: mask yes 
2: helmet no 
3: helmet yes
'''


for each_image in root.iter("image"):
    txt_filename = "dataset/labels/" +each_image.attrib["id"] + ".txt"
    # if each_image.attrib["id"]=="0":
    width = int(each_image.attrib["width"])
    height = int(each_image.attrib["height"])  
    lines = []
    for bbox_tag in each_image.iter("box"):
        if bbox_tag.attrib["label"] == "head":
            # class_index =
            xtl = float(bbox_tag.get("xtl"))
            ytl = float(bbox_tag.get("ytl"))
            xbr = float(bbox_tag.get("xbr"))
            ybr = float(bbox_tag.get("ybr"))                
            bbx_x = xtl/width
            bbx_y = ytl/height
            bbx_width = (xbr-xtl)/width
            bbx_height = (ybr-ytl)/width       
            # attribute_list = bbox_tag.findall("attribute")
            for attribute_tag in bbox_tag.iter("attribute"):
                if attribute_tag.attrib["name"]=="mask":                        
                    if attribute_tag.text == "yes":
                        class_index = 1                             
                    else:
                        class_index = 0
                if attribute_tag.attrib["name"] == "has_safety_helmet":
                    if attribute_tag.text == "yes":
                        class_index = 3
                    else:
                        class_index = 2
                line_string = str(class_index) + " " + \
                    str(bbx_x) + " " + str(bbx_y) + " " + \
                    str(bbx_width) + " " + str(bbx_height) 
                lines.append(line_string)
                
    if lines==[]:
        pass
    else:
        with open(txt_filename, 'w') as f:
            for line in lines:
                f.write(line)
                f.write('\n')

