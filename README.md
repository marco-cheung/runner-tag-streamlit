# Welcome to Runner Tag App👋

**A open, freely accessible runner image search platform using racing bib number (RBN).**

Webapp link: [Runner Tag Platform](https://runner-tag.streamlit.app/)

<img src="https://github.com/marco-cheung/runner-tag-streamlit/blob/main/.streamlit/index_page.png" alt="Streamlit app" style="margin-top:40px"></img>

# Intro
This [Streamlit app](https://runner-tag.streamlit.app/) serves as an open and accessible platform for runners to find and view their images using RBN search.

Enjoy the convenience and simplicity of this app built with Streamlit, an open-source Python framework for creating web applications. Start exploring and reliving your running memories today!

# Getting Started

To get started with our platform, simply enter the bib number you're interested in into the search bar. Our system will then locate and display all images tagged with that bib number.

# How It Works

This platform utilizes two main computer vision techniques:

1. **Object Detection**: This technique is used to locate the bounding box of the bib number in the image. It helps to identify and isolate the area of interest in the image.

    A custom YOLOv8 model ([YOLOv8l](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt)) is built for object detection. YOLOv8 is a new state-of-the-art computer vision model built by [Ultralytics](https://github.com/ultralytics/ultralytics), it is known for its ability to detect objects in images with high speed and accuracy.

    The model was trained on a combination of self-annotated images and multiple public datasets related to bib-number class available on [Roboflow Universe](https://universe.roboflow.com/). These public datasets include:

    - [Thomas Lamalle's Bib Detection](https://universe.roboflow.com/thomas-lamalle/bib-detection)
    - [RBNR's Bib Detector](https://universe.roboflow.com/rbnr/bib-detector)
    - [Sputtipa's BIP](https://universe.roboflow.com/sputtipa/bip)
    - [Bibnumber's Bibnumber](https://universe.roboflow.com/bibnumber/bibnumber)
    - [Python Vertiefung's Python Vertiefung](https://universe.roboflow.com/python-vertiefung/python-vertiefung)
    - [HCMUS's Bib Detection Big Data](https://universe.roboflow.com/hcmus-3p8wh/bib-detection-big-data)
    - [H1 QTGU0's Bib Number](https://universe.roboflow.com/h1-qtgu0/bib-number)

    To help improve the ability of our model to generalize and thus perform more effectively on unseen images, image augmentation techniques were applied to expand data size for training. As a result, a total of 8703 images were used to train the model.

    Here is an example of our custom-trained model running on a image using [Roboflow Inference](https://universe.roboflow.com/marco-cheung/bib-number-labeling/model/14): 

    Feel free to check out [here](https://universe.roboflow.com/marco-cheung/bib-number-labeling/model/14) if you also want to get a try on using this pre-trained bib number labeling computer vision model on-cloud :)

2. **Optical Character Recognition (OCR)**: Once bib number area is isolated from each image using YOLOv8, OCR was used to detect and interpret the characters in the cropped bib number image. After comparing results from different open-source OCR models (e.g. [EasyOCR](https://github.com/JaidedAI/EasyOCR), [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR), [Tesseract OCR](https://github.com/tesseract-ocr/tesseract), etc), PaddleOCR turned out to be the best "out-of-the-box" tool with the highest accuracy for RBN recognition in our use case. This allows us to tag hundreds of thousands of images in reliable and efficient way.

# License

This project is open source and freely accessible under MIT license. I personally strongly believe in the power of open source and welcome everyone to use, modify, and distribute the code.

# Contact
[Github](https://github.com/marco-cheung)

[Linkedin](https://www.linkedin.com/in/marco-cheung-0b69b7137/)