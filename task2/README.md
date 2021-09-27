# PPE Task
In this task, I am going to create a model to identify if a person is wearing a ​face mask​​
and a ​safety helmet​​​.
## Task description

You will be using the dataset provided by us. The dataset folder consists of an image folder
and a xml annotation file. The annotations have human heads and several other objects. You
only need human head objects for this task. Please refer to the meta element of the xml file
for more details.
The ‘id’ attribute of the image element refers to the name of the image file. xtl, ytl, xbr, ybr
represents the location of the bounding box of the object. x, y refers to the coordinates and tl,
br are abbreviations of top left and bottom right respectively.

## Steps
1. Choose right model for this project. 
- From annotation file, I used "head" objects. It has information for  bounding box of Head. But it doesn't involve the bounding box of mask and helmet. So, I used the bounding box information of head for mask and helmet validation.
- I used YOLOR which is the lastet object detection model and supports high-accuracy and faster speed than Yolov1-Yolv5.

2. Preparing Annotation
- From the xml offered, I have extracted proper information and made annotation files per each image.
- Those annotation files invole mask and helmet information including bounding box.
- And then I made train, valid, test images: 70%, 20%, 10%

3. Train, valid, test images
- I have done all of them on Google Colab.
- Source code can be found [here](https://colab.research.google.com/drive/1OGzv1AVq4jpXCbqJr52xahSMrhdXE0yg)
or use this code: "TrainingYOLOR_mask_helmet_detection.ipynb"
