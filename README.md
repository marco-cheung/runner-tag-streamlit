# Welcome to Runner Tag App👋

**A open, freely accessible runner image search platform using racing bib number.**

Webapp link: [Runner Tag Platform](https://runner-tag.streamlit.app/)

<img src="https://github.com/marco-cheung/runner-tag-streamlit/blob/main/.streamlit/index_page.png" alt="Streamlit app" style="margin-top:40px"></img>

## Intro
This [Streamlit app](https://runner-tag.streamlit.app/) is designed to be a user-friendly and accessible platform for runners. Its primary function is to enable users to search for and view their race photos using bib number search.

In a running race, photographers may capture hundreds of thousands of images. These photos are a valuable memento for the participants, capturing their reviving moments and achievement. However, finding one's own photos amidst such a vast collection can be like looking for a needle in a haystack.

As a marathon runner myself, I understand this challenge firsthand. The desire to easily locate and view my own race photos led me to dream of creating a solution - a web application specifically designed to simplify this process for runners. This service uses advanced AI technology to tag photos with the bib numbers of the runners featured in them.

Earlier before, I joined a half-marathon race in Hong Kong and soon realized that it was painful to search and find my photos one-by-one in official photo website (with 21229 photos in total). Therefore, I decided to build on this platform for tagging these race photos. I hope this service not only enhance race experience of runners, but also enable event event organizer to provide a value-added service for runners after the race.

## Getting Started

To get started with our platform, simply enter the bib number you're interested in into the search bar, and the application will retrieve all photos where that bib number (partially) appears.

## Demo Video

https://github.com/marco-cheung/runner-tag-streamlit/assets/29329279/a63b5465-1eb1-456d-a056-b129473bdaa7

## How It Works

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
    <img src="https://github.com/marco-cheung/runner-tag-streamlit/blob/main/.streamlit/running-bib-detection.png" alt="Running bib detection" style="margin-top:20px"></img>
    Feel free to check out [here](https://universe.roboflow.com/marco-cheung/bib-number-labeling/model/14) if you also want to get a try on using the custom-trained model API!

2. **Optical Character Recognition (OCR)**: Once bib number area is isolated from each image using YOLOv8, OCR was used to detect and interpret the characters in the cropped bib number image. After comparing results from different open-source OCR models (e.g. [EasyOCR](https://github.com/JaidedAI/EasyOCR), [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR), [Tesseract OCR](https://github.com/tesseract-ocr/tesseract), etc), PaddleOCR turned out to be the best "out-of-the-box" tool with the highest accuracy for bib number recognition in our use case. This allows us to tag hundreds of thousands of images in reliable and efficient way.

The main combo of this platform were Streamlit and Google Sheets (for easy collaboration and updates by non-technical users):

**● Step 1: Set up a Google Sheet with your data**

**● Step 2: Use Streamlit to read the data from the Google Sheet**

**● Step 3: Build the user interface and search functionality (e.g. textbox, pagination using buttons) using Streamlit**

p.s. [This post](https://blog.streamlit.io/create-a-search-engine-with-streamlit-and-google-sheets/) motivated me to get my hands dirty to build my app by myself!


To summarize, here’s how to build this platform to tag bib numbers in a few steps:

**1. Annotate custom data and create datasets for training (using Roboflow)**

**2. Train a custom object detection model (YOLOv8) to detect bib number**

**3. Crop the bib number object(s) from original image**

**4. Use OCR toolkits (PaddleOCR) to recognize the number in each cropped image**

**5. Wrap the above steps into a python function and run model inference on cloud (In my case, I'm using GCP Vertex AI instance)**

**6. Export and save results in a Google Spreadsheet**

**7. Build a web service on Streamlit Community Cloud ((the free hosting and deployment service) for end-users to respond with the result**

## Moving forward

There is a lot of work remaining to build an accurate and responsive end-to-end web application in real-time. For example:

● OCR Accuracy: Fine-tune pre-trained OCR model (e.g. PaddleOCR). One way is to train a custom OCR tool using more labeled bib number data to make it more robust to different conditions.  


● Frontend: Create a web interface for users to upload their running race photos.


● Backend: Use a backend framework (e.g. Node.js) to handle file uploads. Store the uploaded images in a cloud storage service like AWS S3 or GCP Storage.


● Real-time Updates: Use WebSockets to push updates to the frontend in real-time whenever the model makes a new prediction.


● Deployment: Containerize application using Docker for easy deployment and scalability. Use an advanced app hosting service like Streamlit in Snowflake or Google App Engine with zero server management and zero configuration deployments.

## License

This project is open source and freely accessible under MIT license.

## Contribution

If you have suggestions for improvements or want to report a bug, please open an issue. Thank you for your contribution.
