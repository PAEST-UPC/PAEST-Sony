#!/bin/python

import mysql.connector as connector
import numpy as np
from mysql.connector import Error


def insert_TS(xml_name, recording_time, country_code, tipe, comment, frequency, operator, orbital_position, path, cursor):
    insertStatement = "INSERT INTO TS (identifierTS, Recording_Date, Country_Code, Tipo, Comment, Frequency, Operator, Orbital_Position, Path) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(xml_name, recording_time, country_code, tipe, comment, frequency, operator, orbital_position, path)
    cursor.execute(insertStatement)

def insert_PMT(idPMT, pid, xml_name, cursor):
    insertStatement = "INSERT INTO PMT (idPMT, PIDNumber, identifierTS) VALUES ({0}, {1}, '{2}')".format(idPMT, pid, xml_name)
    cursor.execute(insertStatement)

def insert_Stream_Video(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idVideo, cursor):
    insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', {6}, NULL, NULL, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idVideo)
    cursor.execute(insertStatement)

def insert_Stream_Audio(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idAudio, cursor):
    insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, {6}, NULL, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idAudio)
    cursor.execute(insertStatement)

def insert_Stream_Subtitles(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idSubtitle, cursor):
    insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, NULL, {6}, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idSubtitle)
    cursor.execute(insertStatement)

def insert_Stream_Teletext(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idTeletext, cursor):
    insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, NULL, NULL, {6})".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idTeletext)
    cursor.execute(insertStatement)

def insert_Video(idVideo, W, H, I, name, cursor):
    insertStatement = "INSERT INTO Video (idVideo, Width, Height, Interlaced, TypeName) VALUES ({0}, {1}, {2}, {3}, '{4}')".format(idVideo, W, H, I, name)
    cursor.execute(insertStatement)

def insert_Audio(idAudio, audio_type, audio_language, cursor):
    insertStatement = "INSERT INTO Audio (idAudio, Audio_Type, Audio_Language) VALUES ({0}, {1}, '{2}')".format(idAudio, audio_type, audio_language)
    cursor.execute(insertStatement)

def insert_Subtitles(idSubtitle, subtitle_language, cursor):
    insertStatement = "INSERT INTO Subtitles (idSubtitles, Subtitles_Language) VALUES ({0}, '{1}')".format(idSubtitle, subtitle_language)
    cursor.execute(insertStatement)

def insert_Teletext(idTeletext, teletext_language, cursor):
    insertStatement = "INSERT INTO Teletext (idTeletext, Teletext_Language) VALUES ({0}, '{1}')".format(idTeletext, teletext_language)
    cursor.execute(insertStatement)

def obtain_TS(cursor):
    insertStatement = "SELECT identifierTS from TS"
    cursor.execute(insertStatement)
    TSlist = cursor.fetchall()
    return TSlist

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

def db_is_empty (cursor):
    insertStatement = "SELECT * from TS"
    cursor.execute(insertStatement)
    cursor.fetchall()
    rows = cursor.rowcount
    return rows
