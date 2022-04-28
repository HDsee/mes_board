from flask import *
from mysql.connector import pooling
import boto3
import re
import os

# 讀取.env的隱藏資料
from dotenv import load_dotenv

load_dotenv()
rdsHost = os.getenv("rdsHost")
rdsDatabease = os.getenv("rdsDatabase")
rdsUser = os.getenv("rdsUser")
rdsPassword = os.getenv("rdsPassword")
s3ID = os.getenv("s3ID")
s3Key = os.getenv("s3Key")


connection_pool = pooling.MySQLConnectionPool(pool_name="db",
                                            pool_size=10,
                                            pool_reset_session=True,
                                            host=rdsHost,
                                            database=rdsDatabease,
                                            user=rdsUser,
                                            password=rdsPassword,
                                            port=3306)


app=Flask(__name__)


app.secret_key="HD"

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/api/message', methods=['POST'])
def save_message():
    message = request.form['message']
    image = request.files['file'] 
    rdsUrl = "https://d2xfotk02kb3rl.cloudfront.net/"+image.filename
    print(message)
    print(image)
    print(image.filename)

    s3 = boto3.client('s3', 
        aws_access_key_id=s3ID,
        aws_secret_access_key=s3Key
    )
    try:
        s3.upload_fileobj(image, "hdts3", image.filename)
    except:
        return {"error": True, "message": "s3伺服器內部錯誤"}

    try:
        db = connection_pool.get_connection()
        cursor = db.cursor(buffered = True, dictionary = True)
        cursor.execute("INSERT INTO `mes-board` (message, image) VALUES (%s, %s)", (message, rdsUrl))
    except Exception as e:
        print(e)
        db.rollback()
        return {"error": True, "message": "rds伺服器內部錯誤"}
    finally:
        cursor.close()
        db.commit()
        db.close()

    return {'ok': True}, 200

@app.route('/api/message', methods=['GET'])
def get_message():
    try:
        db = connection_pool.get_connection()
        cursor = db.cursor(buffered = True, dictionary = True)
        cursor.execute("select message,image FROM `mes-board`")
        result = cursor.fetchall()
        print(result)
    except Exception as e:
        print(e)
        return {"error": True, "message": "伺服器內部錯誤"}
    finally:
        cursor.close()
        db.close()

    return {'data': result}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3010 , debug=True)