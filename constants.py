# Constants file. All constant used in the main program should have this notation. We highly recommend avoiding the use of numbers instead of these constants#

########################

# Numerical Constants codec Audio/Video#

VIDEO_MPEG = 2
VIDEO_AVC = 27
VIDEO_HEVC = 36
AUDIO_MPEG_1 = 3
AUDIO_MPEG_2 = 4
AUDIO_MPEG_4 = 11
AUDIO_MPEG_AAC = 15
AUDIO_AC3 = 129
AUDIO_DTS = 134
AUDIO_MPEG4_AAC = 17

# Numerical Constants private sections

PRIVATE = 5

# Numerical Constants Teletext/Subtitles

TEXT = 6

# Error constant

MISSING = -1

# Paths

PARSER_PATH = "/home/ubuntu/pae/scripts/ParserTeam/"
MERGER_PATH = "/home/ubuntu/pae/scripts/MergerTeam/"
DATABASE_PATH = "/home/ubuntu/pae/scripts/DBTeam/PAEST-Sony/phase2/"
INPUT_PATH = "/home/ubuntu/pae/Input/"
TS_PATH = "/home/ubuntu/pae/TS/"
MERGED_XMLS_PATH = "/home/ubuntu/pae/xml/MergerTeam/"
FLUSH_PATH = "/home/ubuntu/pae/TMP/"
NEWPARSER_PATH = '/home/ubuntu/pae/xml/NewParser'

# Scripts

MEDIAINFO = 'run_mediainfo.sh'
MERGER = 'merger_main.py'
DATAMINER = 'main_DataMiner.py'

# Commands
RUN_PARSER = './run_mediainfo.sh'
RUN_MERGER = 'python3 merger_main.py'
RUN_DATAMINER = 'python3 main_DataMiner.py dbPhase2'


#
YES = ["yes", "Yes", "YES", "Y", "y"]
NO = ["no", "No", "NO", "N", "n"]

# Searcher Constants

dbServerName = "127.0.0.1"
dbUser = "ubuntu"
dbPassword = "paesa19"
dbName = "test48000"
dictdbName = "dictionary"
charSet = "utf8mb4"

NOT_DEFINED = 'not defined'

# Merger Constants

NAMESPACE_URL_SA = "http://www.streamanalyser.com/schema"
INPUT_PATH_SA = "/home/ubuntu/pae/xml/StreamAnalyzer/"

SA_EXTENTION_LEN = 7

T_T2 = "Terrestial"
C_C2 = "Cable"
S_S2 = "Satellite"

TYPE_POS = 0
T_COUNTRY_POS = 1
T_FREQUENCY_POS = 4
T_COMMENT_POS = 5
C_COUNTRY_POS = 2
C_FREQUENCY_POS = 5
C_COMMENT_POS = 8
C_OPERATOR_POS = 1
S_FREQUENCY_POS = 2
S_COMMENT_POS = 7
S_ORBITPOS_POS = 1

NAMESPACE_URL_NP = "https://mediaarea.net/mediainfo"

VIDEO_LABELS = ["ID", "MenuID", "Width", "Height", "BitRate_Mode", "PixelAspectRatio", "DisplayAspectRatio", "FrameRate"]
AUDIO_LABELS = ["ID", "MenuID", "BitRate_Mode", "BitRate", "Channels", "FrameRate"]
NAME_LABELS = ["ID", "ServiceName"]
NP_EXTENTION = ".xml"
NP_EXTENTION_LEN = 4

DEFAULT_EXTENTION = ".xml"
ONID_EXCEL_PATH = "/home/ubuntu/pae/scripts/MergerTeam/Original_network_id_TranslationTable.xlsx"

SA_EXTENSION = "-sa.xml"