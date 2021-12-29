import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pytesseract
import re

def read_image(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def scale_image(image, width):
    height = int(image.shape[0] * (width / image.shape[1]))
    dsize = (width, height)
    output = cv2.resize(image, dsize)
    return output, (width / image.shape[1])

def rgb_to_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray

def blur_image(image):
    blur = cv2.GaussianBlur(image, (5,5), 0)
    return blur

def canny_image(image):
    edges = cv2.Canny(image,100,200)
    return edges

def imshow(image, cmap="viridis"):
    plt.axis("off")
    plt.imshow(image, cmap=cmap, vmin=0, vmax=255)

def find_contours(image):
    contours, im2 = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_rectangle(contours):
    return max(contours, key=cv2.contourArea)

def draw_contours(image, contours, color=(0,255,0)):
    im = cv2.drawContours(image.copy(), contours, -1, color, 3)
    return im

def extract(path):
    try:
        image = read_image(path)
        scaled_image, ratio = scale_image(image, 300)
        gray = rgb_to_gray(scaled_image)
        blur = blur_image(gray)
        edges = canny_image(gray)
        contours = find_contours(edges)
        rect = get_rectangle(contours)
        drawed = cv2.drawContours(scaled_image.copy(), [rect], 0, (255,0,0), 3)
        id_card_area = (rect/ratio).astype(int)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        x,y,w,h = cv2.boundingRect(id_card_area)
        ROI = gray[y:y+h, x:x+w]
        TC_image = image[0:int(ROI.shape[0]/2), 0:int(ROI.shape[1]/2)]
        tc_data = pytesseract.image_to_string(TC_image)
        tc_no = re.findall(r"[0-9]{11}",tc_data)[0]

        surname_regex = r"Soyad.*\n*(.*)\n*"
        name_regex = r"Name.*\n*(.*)\n*"
        date_regex = r"[0-9]{2}\.[0-9]{2}\.[0-9]{4}"
        document_no_regex = r"Document.*\n*([A-Z0-9]+)"

        NAME_image = ROI[int(ROI.shape[0]/4):ROI.shape[0], int(ROI.shape[1]/4):int((ROI.shape[1]/6)*4)]


        name_data = pytesseract.image_to_string(NAME_image, lang="tur")
        surname = re.findall(surname_regex, name_data)[0]
        firstname = re.findall(name_regex, name_data)[0]
        birth_date = re.findall(date_regex, name_data)[0]
        valid_until = re.findall(date_regex, name_data)[1]
        document_no = re.findall(document_no_regex, name_data)[0]

        return {
            "surname": surname,
            "name": firstname,
            "tc_no": tc_no,
            "birth_date": birth_date,
            "valid_until": valid_until,
            "document_no": document_no
        }
    except:
        return False