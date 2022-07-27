import numpy as np
import tensorflow_hub as hub
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import sys
sys.path.append("..")

LABEL_FILENAME = 'labels/label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(
    LABEL_FILENAME, use_display_name=True)

print('''
 _                    _ _               __  __           _      _             
| |    ___   __ _  __| (_)_ __   __ _  |  \/  | ___   __| | ___| |            
| |   / _ \ / _` |/ _` | | '_ \ / _` | | |\/| |/ _ \ / _` |/ _ \ |            
| |__| (_) | (_| | (_| | | | | | (_| | | |  | | (_) | (_| |  __/ |  _   _   _ 
|_____\___/ \__,_|\__,_|_|_| |_|\__, | |_|  |_|\___/ \__,_|\___|_| (_) (_) (_)
                                |___/                                         
''')
model = 'models/landmark-detection/'
hub_model = hub.load(model)
print('''
 __  __           _      _   _                    _          _   _ 
|  \/  | ___   __| | ___| | | |    ___   __ _  __| | ___  __| | | |
| |\/| |/ _ \ / _` |/ _ \ | | |   / _ \ / _` |/ _` |/ _ \/ _` | | |
| |  | | (_) | (_| |  __/ | | |__| (_) | (_| | (_| |  __/ (_| | |_|
|_|  |_|\___/ \__,_|\___|_| |_____\___/ \__,_|\__,_|\___|\__,_| (_)
''')

def load_image_into_numpy_array(image):
    (image_width, image_height) = image.size
    return np.array(image.getdata()).reshape((1, image_height, image_width, 3)).astype(np.uint8)


def detect_landmark(image, filename):
    image_path = Image.open(image)
    image_path = image_path.convert('RGB')
    image_np = load_image_into_numpy_array(image_path)
    flip_image_horizontally = False
    convert_image_to_grayscale = False
    if(flip_image_horizontally):
        image_np[0] = np.fliplr(image_np[0]).copy()
    if(convert_image_to_grayscale):
        image_np[0] = np.tile(
                np.mean(image_np[0], 2, keepdims=True), (1, 1, 3)).astype(np.uint8)
    results = hub_model(image_np)
    result = {key: value.numpy() for key, value in results.items()}
    label_id_offset = 0
    image_np_with_detections = load_image_into_numpy_array(image_path)
    viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections[0],
            result['detection_boxes'][0],
            (result['detection_classes'][0] + label_id_offset).astype(int),
            result['detection_scores'][0],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            line_thickness=5,
            min_score_thresh=.3,
            agnostic_mode=False)
    detect_landmark.label = viz_utils.visualize_boxes_and_labels_on_image_array.class_name
    print(detect_landmark.label)
    predicted_image = Image.fromarray(
            image_np_with_detections.squeeze())
    predicted_image.save('static/output/landmark_detection/downloads/' + filename)
    predicted_image_path = 'static/output/landmark_detection/downloads/' + filename
    return predicted_image_path