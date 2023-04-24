pip install torch pillow pytesseract
import re
import torch
from PIL import Image
import pytesseract
img_regex = r"!\[(.*?)\]\((.*?)\)"
def extract_alt_text(image_path):
    with Image.open(image_path) as img:
        img_tensor = torch.as_tensor(np.array(img.convert("RGB")).transpose(2, 0, 1)).unsqueeze(0)
        text = pytesseract.image_to_string(img_tensor, lang='eng')
        return text.strip() if text else ""
def suggest_alt_text(md_path):
    with open(md_path, "r") as f:
        md_content = f.read()
    for match in re.findall(img_regex, md_content):
        alt_text = match[0]
        img_path = match[1]
        if not alt_text:
            alt_text = extract_alt_text(img_path)
        if not alt_text:
            alt_text = "A picture of some kind"
        md_content = md_content.replace(f"![{alt_text}]({img_path})", f"![{alt_text}]({img_path} '{alt_text}')")
    with open(md_path, "w") as f:
        f.write(md_content)
