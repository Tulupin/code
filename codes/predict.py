from diffusers import StableDiffusionPipeline
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

model_id = "./sd-model-finetuned"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda:0")

prompt = "A blue manicure on one hand"
image = pipe(prompt).images[0]

image.save("./result.png")
