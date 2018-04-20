#!/usr/bin/python
# encoding: utf-8

import psycopg2
import os

def connect_db(dbname, user, password):
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='localhost' password='%s'" % (dbname, user, password))
        return conn
    except:
        print "I am unable to connect to the database"


def get_matching_records(conn):
    print 'Getting Exactly Matching Records'
    try:
        cur = conn.cursor()
        cur.execute(
                    'SELECT \
                            fe.id, \
                            fe.slug, \
                            fe.is_active, \
                            fe.type, \
                            fe.created_at, \
                            be.id, \
                            be.slug, \
                            be.is_active, \
                            be.type, \
                            be.created_at \
                    FROM \
                            consultants_frontend fe, \
                            consultants_backend be \
                    WHERE \
                            fe.id=be.id and \
                            fe.slug=be.slug and \
                            fe.is_active=be.is_active and \
                            fe.type=be.type and \
                            fe.created_at=be.created_at; \
                    ')
        all_records = cur.fetchall()
        report_results(all_records, "get_matching_records")
    except:
        print "something went wrong"


def get_mismatching_records(conn):
    print 'Getting Common Mismatching Records'
    try:
        cur = conn.cursor()
        cur.execute(
                    'SELECT \
                            fe.id, \
                            fe.slug, \
                            fe.is_active, \
                            fe.type, \
                            fe.created_at, \
                            be.id, \
                            be.slug, \
                            be.is_active, \
                            be.type, \
                            be.created_at \
                    FROM \
                            consultants_frontend fe, \
                            consultants_backend be \
                    WHERE \
                            (fe.id=be.id) and \
                            (fe.slug!=be.slug or \
                            fe.is_active!=be.is_active or \
                            fe.type!=be.type or \
                            fe.created_at!=be.created_at); \
                    ')
        all_records = cur.fetchall()
        report_results(all_records, "get_mismatching_records")
    except:
        print "something went wrong"


def get_unique_records_consultants_backend(conn):
    print 'Getting Unique Records consultants_backend'
    try:
        cur = conn.cursor()
        cur.execute(
                    'SELECT \
                            be.id, \
                            be.slug, \
                            be.is_active, \
                            be.type, \
                            be.created_at \
                    FROM \
                            consultants_backend be \
                    LEFT JOIN \
                            consultants_frontend fe \
                    ON \
                            be.id=fe.id \
                    WHERE \
                            fe.id is Null; \
                    ')
        all_records = cur.fetchall()
        report_results(all_records, "get_unique_records_consultants_backend")
    except:
        print "something went wrong"


def get_unique_records_consultants_frontend(conn):
    print 'Getting Unique Records consultants_frontend'
    try:
        cur = conn.cursor()
        cur.execute(
                    'SELECT \
                            fe.id, \
                            fe.slug, \
                            fe.is_active, \
                            fe.type, \
                            fe.created_at \
                    FROM \
                            consultants_frontend fe \
                    LEFT JOIN \
                            consultants_backend be \
                    ON \
                            fe.id=be.id \
                    WHERE be.id is Null \
                    ')
        all_records = cur.fetchall()
        report_results(all_records, "get_unique_records_consultants_frontend")
    except:
        print "something went wrong"


def report_results(all_records, file_name):
    print "Recording results %s\n" % file_name
    try:
        if not os.path.exists("reports"):
            os.makedirs("reports")
        report = open("reports/%s.txt" % file_name, "w")
        for record in all_records:
            report.write(str(record))
        report.close()
    except:
        print "something went wrong"


def run_me():
    print "Starting Test!\n"
    conn = connect_db("postgres", "postgres", "postgres")
    get_matching_records(conn)
    get_mismatching_records(conn)
    get_unique_records_consultants_backend(conn)
    get_unique_records_consultants_frontend(conn)
    print "We're Done!"


run_me()
