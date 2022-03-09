from os.path import join

file_path: str = ''
json_path: str = ''

DATA_FOLDER: str = 'data'
ANALYSIS_FOLDER: str = join(DATA_FOLDER, 'analysis_results')
SHOT_IMAGES_FOLDER: str = 'static/images'
UPLOAD_FOLDER: str = 'static/uploads'
STATIC_VIDEOS: str = 'static/media/videos'
STATIC_IMAGES: str = 'static/media/images'

ALLOWED_EXTENSIONS: set = {'mp4'}