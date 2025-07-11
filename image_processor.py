from PIL import Image, ImageDraw, ImageFont
import os
from cloudinary_client import CloudinaryClient  # Make sure this is imported

class ImageProcessor:
    def __init__(self):
        self.template_path = "invitation_template.png"
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

        # Finalized font sizes
        self.font_header = ImageFont.truetype("arialbd.ttf", 124)
        self.font_emphasis = ImageFont.truetype("arialbd.ttf", 106)
        self.font_normal = ImageFont.truetype("arial.ttf", 96)

        # Initialize Cloudinary
        self.cloudinary = CloudinaryClient()

    def generate(self, name, email):
        image = Image.open(self.template_path).convert("RGBA")
        draw = ImageDraw.Draw(image)
        width, height = image.size

        # Text content
        lines = [
            "You're Invited!",
            f"Welcome, {name}!",
            "We can't wait to see you at",
            "MUNERA 2025"
        ]

        fonts = [
            self.font_header,
            self.font_emphasis,
            self.font_normal,
            self.font_header
        ]

        # Calculate total text block height
        total_height = 0
        line_heights = []
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=fonts[i])
            line_height = bbox[3] - bbox[1]
            line_heights.append(line_height)
            total_height += line_height + 12

        y = (height - total_height) // 2

        for i, line in enumerate(lines):
            font = fonts[i]
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y), line, font=font, fill="white")
            y += line_heights[i] + 12

        # Save locally
        safe_name = name.replace(" ", "_")
        output_path = os.path.join(self.output_dir, f"{safe_name}.png")
        image.save(output_path)

        # Upload to Cloudinary and get the URL
        cloud_result = self.cloudinary.upload_image(output_path, public_id=f"invites/{safe_name}")
        image_url = cloud_result["secure_url"]

        return image_url
