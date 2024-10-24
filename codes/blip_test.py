import os

import torch
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration

processor = Blip2Processor.from_pretrained("./BLIP-2-opt/")
model = Blip2ForConditionalGeneration.from_pretrained("./BLIP-2-opt/")

folder_path = "./1/"
images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith('.jpg')]
for i in range(1, len(images) + 1):
    print(str(i) + '.jpg')
    image = Image.open(folder_path + str(i) + '.jpg')
# for img_path in images:
#     image = Image.open(img_path)
    # 所以相应地在生成inputs的时候，也不要放在GPU上或者使用16精度计算
    inputs = processor(images=image, return_tensors="pt")
    generated_ids = model.generate(**inputs)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

    print(generated_text)

    # prompt = "Question: Please focus on describing the characteristics of the nail art in the picture Answer:"
    # # 注意这个时候的inputs.keys()包括了'pixel_values', 'input_ids', 'attention_mask'
    # inputs = processor(images=image, text=prompt, return_tensors="pt") #.to(device, torch.float16)
    # generated_ids = model.generate(**inputs)
    # generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    # print(img_path.replace(folder_path, ''), ": " , generated_text)
