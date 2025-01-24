import os
import cv2 as cv

# Dictionaries
input_folder = "Dataset/Dataset_removed_blurry_images"
output_folder = "Dataset/Dataset_resized_4_240p"

# Sizes
desired_width = 426
desired_height = 240

# Create output folder
os.makedirs(output_folder, exist_ok=True)

def resize_and_rotate(image, desired_width, desired_height):
    """
    Resize and if needed rotate.
    """
    height, width = image.shape[:2]
    
    # Rotator
    if height > width:
        image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
        height, width = width, height

    # Find new size
    scale = min(desired_width / width, desired_height / height)
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Resizer
    resized_image = cv.resize(image, (new_width, new_height), interpolation=cv.INTER_AREA)

    # if smaller than desired size add black border.
    final_image = cv.copyMakeBorder(
        resized_image,
        top=(desired_height - new_height) // 2,
        bottom=(desired_height - new_height + 1) // 2,
        left=(desired_width - new_width) // 2,
        right=(desired_width - new_width + 1) // 2,
        borderType=cv.BORDER_CONSTANT,
        value=[0, 0, 0]  # Black
    )
    return final_image

# process files
for image_file in os.listdir(input_folder):
    input_path = os.path.join(input_folder, image_file)
    output_path = os.path.join(output_folder, image_file)

    # pass if file is invalid
    if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"Invalid file: {image_file}")
        continue

    # Load photo
    image = cv.imread(input_path)
    if image is None:
        print(f"Couldn't load photo: {image_file}")
        continue

    # Resize and Rotate
    resized_image = resize_and_rotate(image, desired_width, desired_height)

    # Save file
    cv.imwrite(output_path, resized_image)
    print(f"Processed: {image_file} -> {output_path}")

print("All photos are resized!")
