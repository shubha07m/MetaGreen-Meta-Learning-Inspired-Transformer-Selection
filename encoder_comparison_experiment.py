# Run this command in the same folder as this file in terminal beofre starting this: sudo powermetrics -i 1000
# --samplers cpu_power,gpu_power -a --hide-cpu-duty-cycle --show-usage-summary --show-extra-power-info >>
# powersample_encoder.txt

import os
import time
import csv
import torch
from PIL import Image
import numpy as np
from transformers import AutoProcessor, AutoTokenizer, AutoImageProcessor, AutoModelForCausalLM, \
    BlipForConditionalGeneration, VisionEncoderDecoderModel, set_seed

device = "cuda" if torch.cuda.is_available() else "cpu"

# Folder containing the images
image_folder = "diverse_100"

# Get a list of all image files in the folder

image_files = sorted([os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(('.jpg', '.jpeg', '.png'))], key=lambda x: int(''.join(filter(str.isdigit, x))))

# Define the number of images to process
num_images_to_process = 100  # Change this value to the desired number of images

# Define models with their corresponding checkpoints
models = [
    ("nlpconnect/vit-gpt2-image-captioning", "VisionEncoderDecoderModel", "AutoImageProcessor"),
    ("microsoft/git-large-coco", "AutoModelForCausalLM", "AutoProcessor"),
    ("microsoft/git-base-coco", "AutoModelForCausalLM", "AutoProcessor"),
    ("Salesforce/blip-image-captioning-base", "BlipForConditionalGeneration", "AutoProcessor"),
    ("Salesforce/blip-image-captioning-large", "BlipForConditionalGeneration", "AutoProcessor")
]


def generate_caption(image, model_checkpoint, model_type, processor_type, start_time):
    # Extract model name from model_checkpoint
    model_name = model_checkpoint.split('/')[1]

    # Load the processor, model, and tokenizer based on the model type
    processor = eval(f"{processor_type}.from_pretrained")(model_checkpoint)
    model = eval(f"{model_type}.from_pretrained")(model_checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

    inputs = processor(images=image, return_tensors="pt").to(device)

    generated_ids = model.generate(pixel_values=inputs.pixel_values, max_length=50, do_sample=True, num_beams=1)

    generated_caption = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Write timestamp to CSV file
    with open('timestamps_encoder.csv', 'a', newline='') as csvfile:
        fieldnames = ['Image', 'ModelName', 'StartTime', 'EndTime', 'ElapsedTime', 'GeneratedCaption']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({'Image': image.filename, 'ModelName': model_name, 'StartTime': start_time, 'EndTime': end_time,
                         'ElapsedTime': elapsed_time, 'GeneratedCaption': generated_caption})


if __name__ == "__main__":
    with open('timestamps_encoder.csv', 'w', newline='') as csvfile:
        fieldnames = ['Image', 'ModelName', 'StartTime', 'EndTime', 'ElapsedTime', 'GeneratedCaption']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for image_file in image_files[:num_images_to_process]:
        print(f"Processing image: {image_file}")
        img = Image.open(image_file)
        print('image and library loaded!')

        for model_checkpoint, model_type, processor_type in models:
            print(f'Starting execution of {model_checkpoint} model')
            start_time = time.time()
            generate_caption(img, model_checkpoint, model_type, processor_type, start_time)
            # time.sleep(5)

    print('end of program execution')
