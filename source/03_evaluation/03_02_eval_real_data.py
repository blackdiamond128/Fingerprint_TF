# %%
import numpy as np
import matplotlib.pyplot as plt
import cv2

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Model

import os

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("GPU: ", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")



# %%
# load data
img_real = np.load('../../dataset/np_data/img_real.npy')
label_real = np.load('../../dataset/np_data/label_real.npy')

print(img_real.shape, label_real.shape)



# %%
# load model
model_path = '../../model/result/fp160.h5'
model_dir = os.path.dirname(model_path)
model = tf.keras.models.load_model(model_path)
model.summary()



# %%
# match real image
total_count = 0
error_count = 0
error_rage = 0.9
for input_idx in range(label_real.shape[0]):
    print('Processing #', input_idx, '')
    for db_idx in range(label_real.shape[0]):
        input_img = img_real[input_idx].reshape((1, 160, 160, 1)).astype(np.float32) / 255.
        db_img = img_real[db_idx].reshape((1, 160, 160, 1)).astype(np.float32) / 255.
        pred_right = model.predict([input_img, db_img])
        if (input_idx == db_idx):
            if (pred_right < error_rage):
                print('False Reject = ', pred_right)
                error_count += 1
        if (input_idx != db_idx):
            if (pred_right > error_rage):
                print('False Accept = ', pred_right, ', ID = ', db_idx)
                error_count += 1
        total_count += 1

# show result
print('Evaluation Finished')
print('Total Count = ', total_count)
print('Error Count = ', error_count)
print('Error Rate = ', (error_count / total_count) * 100)



# %%
