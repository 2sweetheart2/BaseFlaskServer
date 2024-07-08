import os
from pathlib import Path

"""
here you can specify constants for paths or something else.
I wrote the paths here so as not to write them every time everywhere and not to create confusion.
"""

APP_NAME = 'flask-server-base'

USERCONTENT_PATH = Path(os.getcwd() + '/api/images')
URL = "https://your_url"
PFP_URL = "https://your_url/resuorces"
FM_UPDATE_PATH = Path(os.getcwd() + '/api/templates/fm')
SERVER = Path(os.getcwd() + '/api/logs')
PFP_URL_USERS = PFP_URL + '/users'
PFP_URL_OTHER = PFP_URL + '/others'
CHAT_IMAGE_URL = PFP_URL + '/chat_image'
MP4_URL = PFP_URL + '/videos'

FBS_PATH = Path(os.getcwd() + '/api/templates/fbs')
WAV_PATH = Path(USERCONTENT_PATH / 'audio')
DOCX_PATH = Path(USERCONTENT_PATH / 'docx')
MP4_PATH = Path(USERCONTENT_PATH / 'videos')
