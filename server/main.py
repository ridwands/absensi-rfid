import pymysql #MYSQL CLIENT
from app import app #Flask RUN
from db_config import mysql #Config DB
from flask import request, jsonify
import json
from time import strftime #Time Now

import requests


#Route 
@app.route('/mahasiswa', methods=['GET'])
def mahasiswa():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("Select * from mahasiswa")
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.status_code = 200
        if len(rows)==0:
            return jsonify(
                {
                    "Message":"Data Not Found"
                }
            ), 200
        else:
            return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/mahasiswa/<int:id>', methods=['GET'])
def mahasiswa_one(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from mahasiswa where id=%s", id)
        row = cursor.fetchone()
        res = jsonify(row)
        res.status_code = 200

        if row is None:
            return jsonify(
                {
                    "Message " : " Data Not Found"
                }
            )
        else:
            return res
    except Exception as e:
         print(e)
    finally:
        cursor.close()
        conn.close()
    
@app.route('/mahasiswa', methods=['POST'])
def mahasiswa_add():
    try:
        _json = request.json
        _rfid_id = _json['rfid_id']

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        #time now
        now=strftime("%Y-%m-%d")

        #take data from mahasiswa
        mahasiswa = cursor
        mahasiswa.execute("select * from mahasiswa where rfid_id=%s", _rfid_id)
        mahasiswa = mahasiswa.fetchone() 


        if mahasiswa is None:
            sql = "Insert into mahasiswa (rfid_id) values (%s)"
            data = (_rfid_id)
            cursor.execute(sql,data)
            conn.commit()
            res = jsonify({
                "Message" : "ID Successfully Added"
            })
            return res
         #cek table absensi
        cursor.execute("select * from absensi where nim=%s", mahasiswa['nim'])
        absensi = cursor.fetchone()
        cursor.execute("select * from absensi where nim=%s and waktu_keluar is NULL", mahasiswa['nim'])
        cekabsen = cursor.fetchone()

        #Send To FCM 
        if absensi is None:
        #     url = "https://fcm.googleapis.com/fcm/send"
        #     payload = "{\n  \"notification\": \n  {\n    \"title\": \"Your Student Have Present\"\n  },\n \n  \"priority\" : \"high\",\n  \"to\" : \"/topics/news\"\n}"
        #     headers = {
        #         'authorization': "key=API-KEY",
        #         'content-type': "application/json",
        #         'cache-control': "no-cache",
        #         'postman-token': "3b77109a-d8d0-70c4-c8bb-9f5625355a06"
        #         }
        #     response = requests.request("POST", url, data=payload, headers=headers)

            nim = mahasiswa['nim']
            sql = "Insert into absensi (nim) values (%s)"
            data = (nim)
            cursor.execute(sql,data)
            conn.commit()
            res = jsonify({
                "Message" : "Student Sucessfully Present"
            })
            return res
        elif cekabsen > 0:
            # #Send To FCM
            # url = "https://fcm.googleapis.com/fcm/send"
            # payload = "{\n  \"notification\": \n  {\n    \"title\": \"Your Student Go Home\"\n  },\n \n  \"priority\" : \"high\",\n  \"to\" : \"/topics/news\"\n}"
            # headers = {
            #     'authorization': "API-KEY",
            #     'content-type': "application/json",
            #     'cache-control': "no-cache",
            #     'postman-token': "3b77109a-d8d0-70c4-c8bb-9f5625355a06"
            #     }
            # response = requests.request("POST", url, data=payload, headers=headers)

            now = strftime("%Y-%m-%d %H:%M:%S")
            nim = mahasiswa['nim']
            sql = "update absensi set waktu_keluar=%s where nim=%s"
            data = (now, nim)
            cursor.execute(sql,data)
            conn.commit()
            res = jsonify({
                "Message" : "Student Sucessfully Go Home"
            })
            return res
        else:
            res = jsonify({
                "Message" : "You Have Present"
            })
            return res
       
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        conn.close()
   

@app.route('/mahasiswa/<id>', methods=['PUT'])
def mahasiswa_update(id):
    try:
        _json = request.json
        _nim = _json['nim']
        _rfid_id = _json['rfid_id']
        _nama = _json['nama']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        check_nim = cursor.execute("select * from mahasiswa where nim=%s", _nim)
        check_rfid = cursor.execute("select * from mahasiswa where nim=%s", _rfid_id)

        if request.method=='PUT':
            if check_nim > 0:
                return jsonify(
                    {
                        "Message" : "Data Nim was available"
                    }
                ), 200
            elif check_rfid > 0:
                return jsonify(
                    {
                        "Message" : "Data RFID ID was available"
                    }
                ), 200
            else:
                sql = "update mahasiswa set nim=%s, rfid_id=%s, nama=%s where id=%s"
                data = (_nim, _rfid_id, _nama, id)
                cursor.execute(sql, data)
                conn.commit()
                res = jsonify("Mahasiswa Has Been Updated")
                res.status_code = 200
                res.headers.add('Access-Control-Allow-Origin', '*') 
                return res
            
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        conn.close()

@app.route('/mahasiswa/<id>', methods=['DELETE'])
def mahasiswa_delete(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("delete from mahasiswa where id=%s", id)
        conn.commit()
        res = jsonify('Mahasiswa Has Been Deleted')
        res.status_code=200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message' : 'Not Found: ' + request.url,
    }
    res = jsonify(message)
    res.status_code= 404
    return res
