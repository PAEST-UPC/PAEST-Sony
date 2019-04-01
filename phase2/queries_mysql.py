#!/bin/python

import mysql.connector as connector
import numpy as np
from mysql.connector import Error


def insert_TS(xml_name, recording_time, country_code, tipe, comment, frequency, operator, orbital_position, path, cursor):
    insertStatement = "INSERT INTO TS (identifierTS, Recording_Date, Country_Code, Tipo, Comment, Frequency, Operator, Orbital_Position, Path) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(xml_name, recording_time, country_code, tipe, comment, frequency, operator, orbital_position, path)
    cursor.execute(insertStatement)

def insert_PMT(idPMT, pid, xml_name, num_onid, name_onid, network_onid, country_onid, cursor):
    insertStatement = "INSERT INTO PMT (idPMT, PIDNumber, identifierTS, Number_ONID, Name_Operator_ONID, Network_Operator_ONID, Country_Code_ONID) VALUES ({0}, {1}, '{2}', {3}, '{4}', '{5}', '{6}')".format(idPMT, pid, xml_name, num_onid, name_onid, network_onid, country_onid)
    cursor.execute(insertStatement)

def insert_Stream_Video(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idVideo, cursor):
    insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext, idPrivate) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', {6}, NULL, NULL, NULL, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idVideo)
    cursor.execute(insertStatement)

def insert_Stream_Audio(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idAudio, cursor):
    insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext, idPrivate) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, {6}, NULL, NULL, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idAudio)
    cursor.execute(insertStatement)

def insert_Stream_Subtitles(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idSubtitle, cursor):
    insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext, idPrivate) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, NULL, {6}, NULL, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idSubtitle)
    cursor.execute(insertStatement)

def insert_Stream_Teletext(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idTeletext, cursor):
    insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext, idPrivate) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, NULL, NULL, {6}, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idTeletext)
    cursor.execute(insertStatement)

def insert_Stream_Private(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idPrivate, cursor):
    insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext, idPrivate) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, NULL, NULL, NULL, {6})".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idPrivate)
    cursor.execute(insertStatement)

def insert_Video(idVideo, W, H, I, name, bit_rate, pixel_aspect, display_aspect, frame_rate, cursor):
    insertStatement = "INSERT INTO Video (idVideo, Width, Height, Interlaced, TypeName, Bit_Rate_Mode, Pixel_Aspect_Ratio, Display_Aspect_Ratio, Frame_Rate) VALUES ({0}, {1}, {2}, {3}, '{4}', '{5}', {6}, {7}, {8})".format(idVideo, W, H, I, name, bit_rate, pixel_aspect, display_aspect, frame_rate)
    cursor.execute(insertStatement)

def insert_Audio(idAudio, audio_type, audio_language, bit_rate_mode, bit_rate, channels, frame_rate, cursor):
    insertStatement = "INSERT INTO Audio (idAudio, Audio_Type, Audio_Language, BitRate_Mode, BitRate, Channels, FrameRate) VALUES ({0}, {1}, '{2}', '{3}', {4}, '{5}', {6})".format(idAudio, audio_type, audio_language, bit_rate_mode, bit_rate, channels, frame_rate)
    cursor.execute(insertStatement)

def insert_Subtitles(idSubtitle, subtitle_language, cursor):
    insertStatement = "INSERT INTO Subtitles (idSubtitles, Subtitles_Language) VALUES ({0}, '{1}')".format(idSubtitle, subtitle_language)
    cursor.execute(insertStatement)

def insert_Teletext(idTeletext, teletext_language, cursor):
    insertStatement = "INSERT INTO Teletext (idTeletext, Teletext_Language) VALUES ({0}, '{1}')".format(idTeletext, teletext_language)
    cursor.execute(insertStatement)

def insert_Private(idPrivate, standard, cursor):
    insertStatement = "INSERT INTO Private (idPrivate, HBBT) VALUES ({0}, {1})".format(idPrivate, standard)
    cursor.execute(insertStatement)

def insert_URL(idURL, url, idPrivate, cursor):
    insertStatement = "INSERT INTO URL (idURL, URL, idPrivate) VALUES ({0}, '{1}', {2})".format(idURL, url, idPrivate)
    cursor.execute(insertStatement)

def obtain_TS(cursor):
    insertStatement = "SELECT identifierTS from TS"
    cursor.execute(insertStatement)
    TS_mysql_list = cursor.fetchall()
    TS_list = []
    for name in TS_mysql_list:
        name = str(name)
        x = name.split("'")
        TS_list.append(x[1])
    return TS_list

def obtain_PMT(cursor):
    insertStatement = "SELECT * from PMT"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    if rows > 0:
        insertStatement = "SELECT idPMT from PMT ORDER BY idPMT DESC LIMIT 1"
        cursor.execute(insertStatement)
        l = cursor.fetchall()
        rows = str(l[0])
        rows = rows.split("(")[1]
        rows = rows.split(",")[0]
        rows = int(rows)
    return rows

def obtain_Stream(cursor):
    insertStatement = "SELECT * from Stream"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    if rows > 0:
        insertStatement = "SELECT idStream from Stream ORDER BY idStream DESC LIMIT 1"
        cursor.execute(insertStatement)
        l = cursor.fetchall()
        rows = str(l[0])
        rows = rows.split("(")[1]
        rows = rows.split(",")[0]
        rows = int(rows)
    return rows

def obtain_Video(cursor):
    insertStatement = "SELECT * from Video"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    if rows > 0:
        insertStatement = "SELECT idVideo from Video ORDER BY idVideo DESC LIMIT 1"
        cursor.execute(insertStatement)
        l = cursor.fetchall()
        rows = str(l[0])
        rows = rows.split("(")[1]
        rows = rows.split(",")[0]
        rows = int(rows)
    return rows

def obtain_Audio(cursor):
    insertStatement = "SELECT * from Audio"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    if rows > 0:
        insertStatement = "SELECT idAudio from Audio ORDER BY idAudio DESC LIMIT 1"
        cursor.execute(insertStatement)
        l = cursor.fetchall()
        rows = str(l[0])
        rows = rows.split("(")[1]
        rows = rows.split(",")[0]
        rows = int(rows)
    return rows

def obtain_Subtitles(cursor):
    insertStatement = "SELECT * from Subtitles"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    if rows > 0:
        insertStatement = "SELECT idSubtitles from Subtitles ORDER BY idSubtitles DESC LIMIT 1"
        cursor.execute(insertStatement)
        l = cursor.fetchall()
        rows = str(l[0])
        rows = rows.split("(")[1]
        rows = rows.split(",")[0]
        rows = int(rows)
    return rows

def obtain_Teletext(cursor):
    insertStatement = "SELECT * from Teletext"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    if rows > 0:
        insertStatement = "SELECT idTeletext from Teletext ORDER BY idTeletext DESC LIMIT 1"
        cursor.execute(insertStatement)
        l = cursor.fetchall()
        rows = str(l[0])
        rows = rows.split("(")[1]
        rows = rows.split(",")[0]
        rows = int(rows)
    return rows

def obtain_Private(cursor):
    insertStatement = "SELECT * from Private"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    if rows > 0:
        insertStatement = "SELECT idPrivate from Private ORDER BY idPrivate DESC LIMIT 1"
        cursor.execute(insertStatement)
        l = cursor.fetchall()
        rows = str(l[0])
        rows = rows.split("(")[1]
        rows = rows.split(",")[0]
        rows = int(rows)
    return rows

def obtain_URL(cursor):
    insertStatement = "SELECT * from URL"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    if rows > 0:
        insertStatement = "SELECT idURL from URL ORDER BY idURL DESC LIMIT 1"
        cursor.execute(insertStatement)
        l = cursor.fetchall()
        rows = str(l[0])
        rows = rows.split("(")[1]
        rows = rows.split(",")[0]
        rows = int(rows)
    return rows

def db_is_empty (cursor):
    insertStatement = "SELECT * from TS"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    return rows


def obtain_PMTs_fromTS (TS, cursor):
    insertStatement = ("SELECT idPMT from PMT where identifierTS='" + TS + "'")
    cursor.execute(insertStatement)
    l = cursor.fetchall()
    PMT_list = []
    if len(l) > 0:
        for name in l:
            name = str(name)
            x = name.split("(")
            x = x[1].split(",")
            PMT_list.append(int(x[0]))
    return PMT_list

def obtain_Streams_fromTS (TS, cursor):
    insertStatement = ("SELECT idStream from Stream where identifierTS='" + TS + "'")
    cursor.execute(insertStatement)
    l = cursor.fetchall()
    Stream_list = []
    if len(l) > 0:
        for name in l:
            name = str(name)
            x = name.split("(")
            x = x[1].split(",")
            Stream_list.append(int(x[0]))
    return Stream_list

def obtain_Videos_fromTS (TS, cursor):
    insertStatement = ("SELECT idVideo from Stream where identifierTS='" + TS + "'")
    cursor.execute(insertStatement)
    l = cursor.fetchall()
    Video_list = []
    if len(l) > 0:
        for name in l:
            name = str(name)
            x = name.split("(")
            x = x[1].split(",")
            if x[0]!='None':
                Video_list.append(int(x[0]))
    return Video_list

def obtain_Audios_fromTS (TS, cursor):
    insertStatement = ("SELECT idAudio from Stream where identifierTS='" + TS + "'")
    cursor.execute(insertStatement)
    l = cursor.fetchall()
    Audio_list = []
    if len(l) > 0:
        for name in l:
            name = str(name)
            x = name.split("(")
            x = x[1].split(",")
            if x[0]!='None':
                Audio_list.append(int(x[0]))
    return Audio_list

def obtain_Subtitles_fromTS (TS, cursor):
    insertStatement = ("SELECT idSubtitles from Stream where identifierTS='" + TS + "'")
    cursor.execute(insertStatement)
    l = cursor.fetchall()
    Subtitles_list = []
    if len(l) > 0:
        for name in l:
            name = str(name)
            x = name.split("(")
            x = x[1].split(",")
            if x[0]!='None':
                Subtitles_list.append(int(x[0]))
    return Subtitles_list

def obtain_Teletext_fromTS (TS, cursor):
    insertStatement = ("SELECT idTeletext from Stream where identifierTS='" + TS + "'")
    cursor.execute(insertStatement)
    l = cursor.fetchall()
    Teletext_list = []
    if len(l) > 0:
        for name in l:
            name = str(name)
            x = name.split("(")
            x = x[1].split(",")
            if x[0]!='None':
                Teletext_list.append(int(x[0]))
    return Teletext_list

def obtain_Private_fromTS (TS, cursor):
    insertStatement = ("SELECT idPrivate from Stream where identifierTS='" + TS + "'")
    cursor.execute(insertStatement)
    l = cursor.fetchall()
    Private_list = []
    if len(l) > 0:
        for name in l:
            name = str(name)
            x = name.split("(")
            x = x[1].split(",")
            if x[0]!='None':
                Private_list.append(int(x[0]))
    return Private_list

def obtain_URL_fromTS (private, cursor):
    insertStatement = ("SELECT idURL from URL where idPrivate=" + str(private))
    cursor.execute(insertStatement)
    l = cursor.fetchall()
    URL_list = []
    if len(l) > 0:
        for name in l:
            name = str(name)
            x = name.split("(")
            x = x[1].split(",")
            if x[0]!='None':
                URL_list.append(int(x[0]))
    return URL_list

def delete_TS (TS, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    insertStatement = ("DELETE from TS where identifierTS='" + TS + "'")
    cursor.execute(insertStatement)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def delete_PMT (idNum, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    insertStatement = ("DELETE from PMT where idPMT=" + str(idNum))
    cursor.execute(insertStatement)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def delete_Stream (idNum, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    insertStatement = ("DELETE from Stream where idStream=" + str(idNum))
    cursor.execute(insertStatement)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def delete_Video (idNum, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    insertStatement = ("DELETE from Video where idVideo=" + str(idNum))
    cursor.execute(insertStatement)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def delete_Audio (idNum, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    insertStatement = ("DELETE from Audio where idAudio=" + str(idNum))
    cursor.execute(insertStatement)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def delete_Subtitle (idNum, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    insertStatement = ("DELETE from Subtitles where idSubtitles=" + str(idNum))
    cursor.execute(insertStatement)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def delete_Teletext (idNum, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    insertStatement = ("DELETE from Teletext where idTeletext=" + str(idNum))
    cursor.execute(insertStatement)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def delete_Private (idNum, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    insertStatement = ("DELETE from Private where idPrivate=" + str(idNum))
    cursor.execute(insertStatement)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def delete_URL (idNum, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    insertStatement = ("DELETE from URL where idURL=" + str(idNum))
    cursor.execute(insertStatement)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

