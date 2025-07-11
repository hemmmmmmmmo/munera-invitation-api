from flask import Flask, request, jsonify
from flask_cors import CORS
from image_processor import ImageProcessor
from cloudinary_client import CloudinaryClient
import os

app = Flask(__name__)
CORS(app)

# Initialize services
image_processor = ImageProcessor()
cloudinary_client = CloudinaryClient()

@app.route("/api/generate-invitation", methods=["GET"])
def generate_invitation():
    name = request.args.get("name")
    email = request.args.get("email")

    if not name or not email:
        return jsonify({"error": "Missing email or name in query parameters"}), 400

    try:
        image_path = image_processor.generate(name, email)
        upload_result = cloudinary_client.upload_image(image_path)
        image_url = upload_result.get("secure_url", "")

        return jsonify({
            "name": name,
            "email": email,
            "status": "Generated",
            "image_url": image_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate_batch", methods=["POST"])
def generate_batch():
    try:
        data = request.get_json()
        if not data or 'delegates' not in data:
            return jsonify({'error': 'Missing or invalid JSON: expected key "delegates"'}), 400

        invitations = []
        for delegate in data['delegates']:
            name = delegate.get('name')
            email = delegate.get('email')
            if name and email:
                image_path = image_processor.generate(name, email)
                upload_result = cloudinary_client.upload_image(image_path)
                image_url = upload_result.get("secure_url", "")

                invitations.append({
                    "name": name,
                    "email": email,
                    "status": "Generated",
                    "image_url": image_url
                })

        return jsonify({
            "generated_count": len(invitations),
            "invitations": invitations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
