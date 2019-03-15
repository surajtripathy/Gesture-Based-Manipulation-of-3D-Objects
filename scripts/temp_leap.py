import cv2, Leap, math, ctypes, sys , time
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator
new_model = keras.models.load_model('Leap_motion_model.h5')
#new_model._make_predict_function()
graph = tf.get_default_graph()
#new_model.summary()

def convert_distortion_maps(image):

    distortion_length = image.distortion_width * image.distortion_height
    xmap = np.zeros(distortion_length/2, dtype=np.float32)
    ymap = np.zeros(distortion_length/2, dtype=np.float32)

    for i in range(0, distortion_length, 2):
        xmap[distortion_length/2 - i/2 - 1] = image.distortion[i] * image.width
        ymap[distortion_length/2 - i/2 - 1] = image.distortion[i + 1] * image.height

    xmap = np.reshape(xmap, (image.distortion_height, image.distortion_width/2))
    ymap = np.reshape(ymap, (image.distortion_height, image.distortion_width/2))

    #resize the distortion map to equal desired destination image size
    resized_xmap = cv2.resize(xmap,
                              (image.width, image.height),
                              0, 0,
                              cv2.INTER_LINEAR)
    resized_ymap = cv2.resize(ymap,
                              (image.width, image.height),
                              0, 0,
                              cv2.INTER_LINEAR)

    #Use faster fixed point maps
    coordinate_map, interpolation_coefficients = cv2.convertMaps(resized_xmap,
                                                                 resized_ymap,
                                                                 cv2.CV_32FC1,
                                                                 nninterpolation = False)

    return coordinate_map, interpolation_coefficients

def undistort(image, coordinate_map, coefficient_map, width, height):
    destination = np.empty((width, height), dtype = np.ubyte)

    #wrap image data in numpy array
    i_address = int(image.data_pointer)
    ctype_array_def = ctypes.c_ubyte * image.height * image.width
    # as ctypes array
    as_ctype_array = ctype_array_def.from_address(i_address)
    # as numpy array
    as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
    img = np.reshape(as_numpy_array, (image.height, image.width))

    #remap image to destination
    destination = cv2.remap(img,
                            coordinate_map,
                            coefficient_map,
                            interpolation = cv2.INTER_LINEAR)

    #resize output to desired destination size
    destination = cv2.resize(destination,
                             (width, height),
                             0, 0,
                             cv2.INTER_LINEAR)
    return destination

def run(controller):
    maps_initialized = False
    #count = 0
    while(True):
        frame = controller.frame()
        image = frame.images[0]
        if image.is_valid:
            if not maps_initialized:
                left_coordinates, left_coefficients = convert_distortion_maps(frame.images[0])
                right_coordinates, right_coefficients = convert_distortion_maps(frame.images[1])
                maps_initialized = True

            undistorted_left = undistort(image, left_coordinates, left_coefficients, 640, 240)
            #undistorted_right = undistort(image, right_coordinates, right_coefficients, 640, 240)
            cv2.imwrite('temp.jpg',undistorted_left)
            img_height = 120
            img_width = 320
            imgs = load_img('temp.jpg', color_mode = "grayscale" ,target_size=(img_height, img_width, 1))
            #imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2GRAY)
            img_array = np.array(imgs)
            img_array = img_array.astype(np.float32)
            img_array = np.multiply(img_array, 1.0 / 255.0)
            img_array = img_array.reshape(1,img_height,img_width,1)
            with graph.as_default():
                [preds] = new_model.predict(img_array)
            preds = list(preds)
            handType = ''
            f = open('temp_data','a')
            for hand in frame.hands:
                handType = "Left Hand" if hand.is_left else "Right Hand"
                #print(handType + "Hand ID:" + str(hand.id) + "    " + str(hand.palm_position))

            #print(max(preds))
            pred_str = (chr(ord('A')+preds.index(max(preds))))
            #print(pred_str)
            f.write(handType+' '+ pred_str + '\n')
            f.flush()
            time.sleep(0.1)
            #display images
            #cv2.imshow('Left Camera', undistorted_left)
            #cv2.imshow('Right Camera', undistorted_right)
            '''if count> 200 and count<= 700:
                cv2.imwrite('./img_data/fist/'+str(count)+'.jpg', undistorted_left)
            count+=1
            print(count)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.1)'''
def main():
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)
    try:
        run(controller)
    except KeyboardInterrupt:
        sys.exit(0)

'''if __name__ == '__main__':
    main()'''
