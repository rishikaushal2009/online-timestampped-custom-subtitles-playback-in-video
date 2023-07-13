from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        return 'Video uploaded successfully', 200


@app.route('/api/subtitles', methods=['POST'])
def create_subtitles():
    subtitle_data = request.get_json()
    if not subtitle_data:
        return 'No subtitle data provided', 400

    video_id = subtitle_data.get('video_id')
    if not video_id:
        return 'Video ID not specified', 400

    subtitle_text = subtitle_data.get('subtitle_text')
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


if __name__ == '__main__':
    app.run(debug=True)
