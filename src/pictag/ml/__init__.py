import torch
from torchvision import models, transforms
from PIL import Image
import importlib.resources

def load_model():
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    model.eval()
    return model

# アプリ起動時に一度だけモデルをロード
model = load_model()

# 前処理パイプラインの定義
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ラベルリストを準備
labels = []
with open("imagenet_classes.txt", "r", encoding="utf-8") as f:
    labels = [line.strip() for line in f.readlines()]

def get_image_tags(image_path, model, preprocess, top_k=3):
    image = Image.open(image_path).convert("RGB")
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    output = None
    with torch.no_grad():
        output = model(input_batch)

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top_prob, top_indices = torch.topk(probabilities, top_k)

    tags = []
    for i, index in enumerate(top_indices):
        tags.append({
            "label": labels[index.item()],
            "probability": round(top_prob[i].item() * 100, 2)
        })

    return tags
