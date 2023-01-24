from matplotlib import pyplot as plt
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import requests
import os
import openai
import streamlit as st
import streamlit_helper as sh
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

sh.introduction()

image = sh.input_image()
if image:
    st.image(image, caption="Selected Image", use_column_width=True)

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-101")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-101")

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(
    outputs, target_sizes=target_sizes, threshold=0.6
)[0]

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(
        f"Detected {model.config.id2label[label.item()]} with confidence "
        f"{round(score.item(), 3)} at location {box}"
    )

ingredients = list(
    set(
        [
            model.config.id2label[label.item()].capitalize()
            for label in results["labels"]
        ]
    )
)


st.write("Detected items:")
for ingredient in ingredients:
    st.write(f"- {ingredient}")


my_prompt = (
    "The following is a list of items in my fridge. What could I cook for dinner?:"
)
for ingredient in ingredients:
    my_prompt += f"\n- {ingredient}"

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=my_prompt,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)
recipe = response["choices"][0]["text"]

st.header(f"Here is something you can try:")
st.write(recipe)

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"I want to cook {recipe}. Give me a list of steps",
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)
instructions = response["choices"][0]["text"]

st.header(f"Here are the instructions for this recipe:")
st.write(instructions)
