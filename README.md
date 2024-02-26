This Python script prepares the dataset in a form in which it can be fed into the YOLOv8 training pipeline. 

Replace the path of the dataset with your own in lines 6 and 7. You also need to replace the elements of the 'labels' list object (line 11) with the names of the classes in your own dataset.

The program resizes all images into square images (NEW_SIZE parameter/variable) before randomly placing them into train, validation and test folders by 70:20:10 ratio and creating a YAML file. The resulting dataset is placed in the path of the 'yolo_dataset_folder' variable (line 33).
