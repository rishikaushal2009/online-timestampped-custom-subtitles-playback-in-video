from flask import Flask, request, send_from_directory, jsonify
from flask import send_file
from flask_cors import CORS
import os
import uuid
import re
import urllib.parse
import logging

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)


def remove_special_characters(filename):
    # Define the pattern to match special characters
    pattern = r'[^\w\s.-]'
    
    # Remove special characters from the filename using regex substitution
    cleaned_filename = re.sub(pattern, '', filename)
    
    return cleaned_filename


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})




@app.route('/api/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return 'No video file provided', 400

    video_file = request.files['video']
    if video_file.filename == '':
        return 'No video file selected', 400

    if video_file:
        video_filename = video_file.filename
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))
        
        # Generate a unique videoId
        video_id = str(uuid.uuid4())
        
        # Return the videoId in the response
        return {'message': 'Video uploaded successfully', 'videoId': video_id}, 200



@app.route('/api/subtitles', methods=['POST'])
def create_subtitles():
    subtitle_data = request.get_json()
    if not subtitle_data:
        return 'No subtitle data provided', 400

    video_id = subtitle_data.get('videoId')
    if not video_id:
        return 'Video ID not specified', 400

    subtitle_text = subtitle_data.get('subtitles')
    if not subtitle_text:
        return 'Subtitle text not provided', 400

    subtitle_file_name = f'{video_id}_subtitles.txt'
    with open(os.path.join(app.config['UPLOAD_FOLDER'], subtitle_file_name), 'a') as subtitle_file:
        subtitle_file.write(f'{subtitle_text}\n')

    return 'Subtitles created successfully', 200


@app.route('/api/subtitles/<video_id>', methods=['GET'])
def get_subtitles(video_id):
    subtitle_file_name = f'{video_id}_subtitles.txt'
    subtitle_file_path = os.path.join(app.config['UPLOAD_FOLDER'], subtitle_file_name)

    if os.path.exists(subtitle_file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], subtitle_file_name, as_attachment=True)

    return 'Subtitles not found', 404





@app.route('/api/uploads/<path:filename>', methods=['GET'])
def serve_video(filename):
    print('Custom message')
    #video_filename = video_path.split('/')[-1]  # Extract the filename from the video path
    #logging.debug(filename)
    # Construct the full path to the video file based on the filename
    full_video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    #Check if the video file exists
    if not os.path.isfile(full_video_path):
        return 'Video not found', 404

    # Serve the video file using send_from_directory
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return send_file(full_video_path,mimetype='video/mp4')


                               


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404


if __name__ == '__main__':
    app.run(debug=True)
