import torch
import numpy as np
from PIL import Image
from transformers import AutoImageProcessor, AutoModel

# Load DINOv2 model
model_name = "facebook/dinov2-base"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def extract_embedding(image_path):
    """Extract DINOv2 embedding from an image"""
    try:
        # Load and process image
        image = Image.open(image_path).convert('RGB')
        
        # Preprocess
        inputs = processor(images=image, return_tensors="pt")
        
        # Extract features
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get the CLS token embedding (first token)
        embedding = outputs.last_hidden_state[:, 0, :].squeeze()
        
        # Convert to numpy array
        embedding_np = embedding.cpu().numpy()
        
        # Ensure it's a 1D numpy array
        if len(embedding_np.shape) > 1:
            embedding_np = embedding_np.flatten()
        
        return embedding_np
        
    except Exception as e:
        print(f"Error extracting embedding: {str(e)}")
        raise