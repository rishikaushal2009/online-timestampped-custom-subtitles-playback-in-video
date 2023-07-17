from flask import Flask, request, send_from_directory, jsonify
from flask import send_file, Response
from flask_cors import CORS
import os
import uuid
import re
import urllib.parse
import logging
import mimetypes
'''
@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

def send_file_partial(path):
    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(path)
    
    size = os.path.getsize(path)    
    byte1, byte2 = 0, None
    
    m = re.search('(\d+)-(\d*)', range_header)
    if m:
        g = m.groups()
        byte1 = int(g[0])
        if g[1]:
            byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1 + 1
    
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    mimetype = mimetypes.guess_type(path)[0]
    rv = Response(data, 206, mimetype=mimetype, direct_passthrough=True)
    rv.headers.add('Content-Range', f'bytes {byte1}-{byte1 + length - 1}/{size}')

    return rv

'''
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
#CORS(app)



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
        return send_file(subtitle_file_path, as_attachment=True)

    return 'Subtitles not found', 404








@app.route('/api/uploads/<path:filename>', methods=['GET'])
def serve_video(filename):
    '''
   # Construct the full path to the video file based on the filename
    full_video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Check if the video file exists
    if not os.path.isfile(full_video_path):
        return 'Video not found', 404

    # Set the appropriate Content-Type header
    video_mimetype = 'video/mp4'

    # Check if the Range header is present
    range_header = request.headers.get('Range')
    if range_header:
        # If Range header is present, send the whole video file
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype=video_mimetype)

    # If Range header is not present, send the video file with appropriate headers
    response = send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype=video_mimetype)
    response.headers['Accept-Ranges'] = 'bytes'

    return response
    '''
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename,
                               conditional=True)

 

                               


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404


if __name__ == '__main__':
    app.run(debug=True)
