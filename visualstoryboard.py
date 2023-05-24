# -*- coding: utf-8 -*-
"""VisualStoryboard.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16AY5OCdFpHYTHviuvTggt8Fard-ILycW
"""

!pip install transformers
!pip install accelerate
!pip install torch torchvision transformers ftfy einops Pillow
!pip install git+https://github.com/huggingface/transformers.git
!pip install diffusers
!pip install clip

from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import matplotlib.pyplot as plt
from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')

user_input = input("write your prompt:")

story = generator(user_input, max_length=105, num_return_sequences=1)[0]['generated_text']

print(story)

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

sentences = story.split('.')
sentences = [s.strip() for s in sentences if len(s.strip()) > 0]

from transformers import CLIPProcessor, CLIPModel

import numpy as np

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

for i in range (0,len(sentences)):
  prompt = sentences[i]
  print(prompt)
  num_images = 3
  images=[]
  images.append(0)
  scores=[]
  scores.append(0)

  images1=pipe(prompt).images
  image1=images1[0]
  images.append(image1)
  inputs = processor(text=[prompt], images=image1, return_tensors="pt", padding=True)
  outputs = model(**inputs)
  logits_per_image = outputs.logits_per_image.detach().numpy() # this is the image-text similarity score
  scores.append(logits_per_image)

  images2=pipe(prompt).images
  image2=images2[0]
  images.append(image2)
  inputs = processor(text=[prompt], images=image2, return_tensors="pt", padding=True)
  outputs = model(**inputs)
  logits_per_image = outputs.logits_per_image.detach().numpy() # this is the image-text similarity score
  scores.append(logits_per_image)

  images3=pipe(prompt).images
  image3=images3[0]
  images.append(image3)
  inputs = processor(text=[prompt], images=image3, return_tensors="pt", padding=True)
  outputs = model(**inputs)
  logits_per_image = outputs.logits_per_image.detach().numpy() # this is the image-text similarity score
  scores.append(logits_per_image)

  index = np.argmax(scores)
  image = images[index]
  plt.imshow(image)
  plt.show()

# for i in range (0,len(sentences)):
#   prompt = sentences[i]
#   print(prompt)
#   num_images = 3
#   images=[]
#   scores=[]
#   for j in range (0,num_images):
#     images=pipe(prompt).images
#     image=images[j]
#     inputs = processor(text=[prompt], images=image, return_tensors="pt", padding=True)
#     outputs = model(**inputs)
#     logits_per_image = outputs.logits_per_image # this is the image-text similarity score
#     scores[j]=logits_per_image
  
#   score=0
#   for j in range(0,len(scores)):
#     if (scores[j]>score):
#       score=scores[j]
  
#   index=scores.index(score)

#   image=images[index]

#   plt.imshow(image)
#   plt.show()