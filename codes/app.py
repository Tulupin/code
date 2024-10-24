from flask import Flask, request, jsonify
from flask_cors import cross_origin
import io
from PIL import Image
import base64
import torch
from diffusers import StableDiffusionPipeline

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32
model_id = "./sd-model-finetuned"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch_dtype)
pipe = pipe.to(device)

@app.route('/generate', methods=['POST'])
@cross_origin()
def generate_similar_image():
    # 获取文本输入
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # 生成图像
    buffer = io.BytesIO()
    output = generate(text)
    output.save(buffer, format='PNG')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode('utf-8')

    return jsonify({'image': f'data:image/jpeg;base64,{image_data}'}), 200


def generate(prompt):
    """
    输入文本，返回生成后的图像。
    """
    image = pipe(prompt).images[0]
    return image


if __name__ == '__main__':
    app.run(port=5000, debug=False)