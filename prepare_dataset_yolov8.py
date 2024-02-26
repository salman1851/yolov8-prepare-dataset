import os
import glob
import cv2
import shutil

labels_folder = 'dataset\\labels'	# replace with the path of your dataset
images_folder = 'dataset\\images'	# replace with the path of your dataset

image_files = glob.glob(images_folder+'\\*')

labels = ['Design_Code', 'Mouse_Trap', 'QRCODE_ROI']	# replace with your class list

########## RESIZE IMAGES ##########

resized_images_folder = 'dataset\\images_resized'
if not os.path.exists(resized_images_folder):
	os.mkdir(resized_images_folder)

NEW_SIZE = 640

for i in image_files:
	print(i)
	img = cv2.imread(i)
	img_resize = cv2.resize(img, (NEW_SIZE,NEW_SIZE), interpolation = cv2.INTER_LINEAR)
	file_name = i.split('\\')[-1]
	# print(resized_images_folder+'\\'+file_name)
	cv2.imwrite(resized_images_folder+'\\'+file_name, img_resize)

print('Images resized.')

########## TRAIN VALID TEST SPLIT ########## 

yolo_dataset_folder = 'yolo_dataset_folder'
if not os.path.exists(yolo_dataset_folder):
	os.mkdir(yolo_dataset_folder)
	os.mkdir(yolo_dataset_folder + '\\train')
	os.mkdir(yolo_dataset_folder + '\\train\\images')
	os.mkdir(yolo_dataset_folder + '\\train\\labels')
	os.mkdir(yolo_dataset_folder + '\\valid')
	os.mkdir(yolo_dataset_folder + '\\valid\\images')
	os.mkdir(yolo_dataset_folder + '\\valid\\labels')
	os.mkdir(yolo_dataset_folder + '\\test')
	os.mkdir(yolo_dataset_folder + '\\test\\images')
	os.mkdir(yolo_dataset_folder + '\\test\\labels')

total_files = len(image_files)

train = int(0.7 * total_files)
valid = int(0.2 * total_files)
test = total_files - train - valid

shuffled_positions = range(total_files)

ttv_folders = [yolo_dataset_folder+'\\train', yolo_dataset_folder+'\\test', yolo_dataset_folder+'\\valid']

ttv_position = 0

for i, p in enumerate(shuffled_positions):
	if i >= train:
		ttv_position = 1
	elif i >= (train + valid):
		ttv_position = 2
	shutil.copy(image_files[i], ttv_folders[ttv_position] + '\\images\\' + image_files[i].split('\\')[-1])
	shutil.copy(labels_folder + '\\' + image_files[i].split('\\')[-1][:-4] + '.txt', ttv_folders[ttv_position] + '\\labels\\' + image_files[i].split('\\')[-1][:-4] + '.txt')

print('Dataset split into training and testing.')

########## YAML FILE ########## 

file = open(yolo_dataset_folder + '\\data.yaml', 'w')
L = ["train: ../train/images \n", "val: ../valid/images \n", "test: ../test/images \n", "\n", "nc: " + str(len(labels)) + " \n", "names: " + "['" + " ".join(labels).replace(' ',"', '") + "']" + "\n"]
file.writelines(L)
file.close()

print('YAML file created.')