import pandas as pd
import joblib
import os
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import LabelBinarizer
# get all the image folder paths
all_paths = os.listdir('../input/data')
folder_paths = [x for x in all_paths if os.path.isdir('C:/Users/Lohith/Desktop/Project/Classification/input/data/' + x)]
print(f"Folder paths: {folder_paths}")
print(f"Number of folders: {len(folder_paths)}")

create_labels = ['cover','cut','pull','leg','non_pitch_view','straight']
# create a DataFrame
data = pd.DataFrame()

image_formats = ['jpg', 'JPG', 'PNG', 'png'] # we only want images that are in this format
labels = []
counter = 0

for i, folder_path in tqdm(enumerate(folder_paths), total=len(folder_paths)):
    if folder_path not in create_labels:
        continue
    image_paths = os.listdir('C:/Users/Lohith/Desktop/Project/Classification/input/data/'+folder_path)
    label = folder_path
    # save image paths in the DataFrame
    for image_path in image_paths:
        if image_path.split('.')[-1] in image_formats:
            data.loc[counter, 'image_path'] = f"C:/Users/Lohith/Desktop/Project/Classification/input/data/{folder_path}/{image_path}"
            labels.append(label)
            counter += 1
labels = np.array(labels)
# one-hot encode the labels
lb = LabelBinarizer()
labels = lb.fit_transform(labels)

if len(labels[0]) == 1:
    for i in range(len(labels)):
        index = labels[i]
        data.loc[i, 'target'] = int(index)
elif len(labels[0]) > 1:
    for i in range(len(labels)):
        index = np.argmax(labels[i])
        data.loc[i, 'target'] = int(index)# shuffle the dataset

data = data.sample(frac=1).reset_index(drop=True)

print(f"Number of labels or classes: {len(lb.classes_)}")
print(f"The first one hot encoded labels: {labels[0]}")
print(f"Mapping the first one hot encoded label to its category: {lb.classes_[0]}")
print(f"Total instances: {len(data)}")
 
# save as CSV file
data.to_csv('C:/Users/Lohith/Desktop/Project/Classification/input/data.csv', index=False)
 
# pickle the binarized labels
print('Saving the binarized labels as pickled file')
joblib.dump(lb, 'C:/Users/Lohith/Desktop/Project/Classification/outputs/lb.pkl')
 
print(data.head(5))