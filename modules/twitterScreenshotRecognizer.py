import torch
from torchvision import transforms
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


from PIL import Image, ImageFile
import torch.nn.functional as F

model = torch.load("./neuro/mymodel-25-epochs")
def inspect(image):
        
    labels = ['trash','tweets']

    img = image

    img_transforms = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    img = img_transforms(img).to(device)
    img = torch.unsqueeze(img, 0)

    model.eval()
    prediction = F.softmax(model(img), dim=1)
    prediction = prediction.argmax()
    return labels[prediction]