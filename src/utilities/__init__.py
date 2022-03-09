from os.path import join

video_name: str = ''
json_path: str = ''

DATA_FOLDER: str = 'data'
VIDEO_FOLDER: str = join(DATA_FOLDER, 'videos')
ANALYSIS_FOLDER: str = join(DATA_FOLDER, 'analysis_results')
SHOT_IMAGES_FOLDER: str = 'static/images'

ALLOWED_EXTENSIONS: set = {'mp4'}
