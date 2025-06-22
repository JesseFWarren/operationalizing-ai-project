from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load model + processor once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def describe_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption or "[Image could not be interpreted]"
    except Exception as e:
        return "[Image processing failed]"
