import cv2
import os
import shutil

# Folders
dataset_folder = "Dataset/Dataset_without_preprocessing"
blurred_folder = "Dataset/Dataset_discarded_images"
clear_folder = "Dataset/Dataset_removed_blurry_images"

# Create folders if doesn't exists
os.makedirs(blurred_folder, exist_ok=True)
os.makedirs(clear_folder, exist_ok=True)

# Blurrity Threshold
blur_threshold = 2.0

# Function controls blurrity
def is_blurry(image_path, threshold=blur_threshold):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return False  # invalid file
    variance = cv2.Laplacian(image, cv2.CV_64F).var()
    return variance < threshold

# Control and move images
for image_file in os.listdir(dataset_folder):
    image_path = os.path.join(dataset_folder, image_file)

    if is_blurry(image_path):
        # Move blurry
        shutil.copy(image_path, os.path.join(blurred_folder, image_file))
        print(f"Blurry: {image_file} -> {blurred_folder}")
    else:
        # Move non-blurry
        shutil.copy(image_path, os.path.join(clear_folder, image_file))
        print(f"Clean: {image_file} -> {clear_folder}")

print("All images have been moved to their folders!")
