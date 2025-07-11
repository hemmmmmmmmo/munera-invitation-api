import cloudinary
import cloudinary.uploader

class CloudinaryClient:
    def __init__(self):
        cloudinary.config(
            cloud_name="dhbwze6c5",
            api_key="793217434692262",
            api_secret="yo9mEOHQoyfNjQkJEhDFegi5e6A",
            secure=True  # Ensure HTTPS URLs
        )

    def upload_image(self, file_path, public_id=None):
        try:
            response = cloudinary.uploader.upload(
                file_path,
                public_id=public_id,
                overwrite=True,
                resource_type="image"
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Cloudinary upload failed: {str(e)}")
