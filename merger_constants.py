#! /usr/bin/python

NAMESPACE_URL_SA="http://www.streamanalyser.com/schema"
INPUT_PATH_SA="/home/carlos/pae/xml/StreamAnalyzer/"
OUTPUT_PATH="/home/carlos/pae/xml/MergerTeam/"
TS_PATH="/home/ubuntu/pae/TS/"

SA_EXTENTION_LEN=7

T_T2="Terrestial"
C_C2="Cable"
S_S2="Satellite"

TYPE_POS=0
T_COUNTRY_POS=1
T_FREQUENCY_POS=4
T_COMMENT_POS=5
C_COUNTRY_POS=2
C_FREQUENCY_POS=5
C_COMMENT_POS=8
C_OPERATOR_POS=1
S_FREQUENCY_POS=2
S_COMMENT_POS=7
S_ORBITPOS_POS=1

NAMESPACE_URL_NP="https://mediaarea.net/mediainfo"
INPUT_PATH_NP="/home/carlos/pae/xml/NewParser/"

VIDEO_LABELS=["ID", "MenuID", "Width", "Height", "BitRate_Mode", "PixelAspectRatio", "DisplayAspectRatio", "FrameRate"]
AUDIO_LABELS=["ID", "MenuID", "BitRate_Mode", "BitRate", "Channels", "FrameRate"]
NP_EXTENTION=".xml"
NP_EXTENTION_LEN=4

DEFAULT_EXTENTION=".xml"



