# pip install mtcnn
# pip install keras_vggface keras_applications

from mtcnn.mtcnn import MTCNN
import cv2
import numpy as np
from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
from scipy.spatial.distance import cosine

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# use this for the new model after training
# from keras.models import load_model

# use MTCNN as detector
detector = MTCNN()
model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')


# Create a rectangle on the face using detector
def create_bbox(image):
    faces = detector.detect_faces(image)
    bounding_box = faces[0]['box']

    cv2.rectangle(image,
                  (bounding_box[0], bounding_box[1]),
                  (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                  (0, 255, 255),
                  2)
    return image


# use the model to predict face
def get_embeddings(faces):
    face = np.asarray(faces, 'float32')
    face = preprocess_input(face, version=2)

    # modeli egitim yaptiktan sonra model= my_model kullan
    # model = my_model


    return model.predict(face)


# get similarity between faces with cosine function
def get_similarity(faces):
    embeddings = get_embeddings(faces)
    # use cosine function to calculate score
    score = cosine(embeddings[0], embeddings[1])

    if score <= 0.5:
        return True
    return False


# use to show boxes on faces
def show_faces(img_list):
    for image in img_list:
        face_image = create_bbox(cv2.imread(image))
        # cv2_imshow() yerine uygun fonksiyonu kullan; {from google.colab.patches import cv2_imshow }
        # cv2_imshow(face_image)


# extract face from the image
def extract_face(image, resize=(224, 224)):
    # resizing to 224,224 is because VGG is developed on images that are 224,224

    image = cv2.imread(image)
    faces = detector.detect_faces(image)
    x1, y1, width, height = faces[0]['box']  # taking the box location
    x2, y2 = x1 + width, y1 + height

    face_boundary = image[y1:y2, x1:x2]
    face_image = cv2.resize(face_boundary, resize)

    return face_image


def face_verification(img_list):
    # get faces from images
    try:
        img1 = extract_face(img_list[0])
        img2 = extract_face(img_list[1])
        return get_similarity([img1, img2])
    except:
        return False

def verify(foto_path, kimlik_path):

    # true-false doner
    result = face_verification([foto_path, kimlik_path])

    if result:
        return True
    else:
        return False