import mysql.connector
from mysql.connector import errorcode
from model.settings import USER_TEST, PASSWORD

class linebotDB():
    def __init__(self):
        try:
            cnx = mysql.connector.connect(user=USER_TEST,
                                          password=PASSWORD,
                                          database='linebot')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("database connect success")
            cnx.close()

    def set_userId_imageId(self, usr_id, img_id):
        cnx = mysql.connector.connect(user=USER_TEST,
                                          password=PASSWORD,
                                          database='linebot')
        cursor = cnx.cursor()
        add_img = ("INSERT INTO member "
                   "(user_id, image_id) " 
                   "VALUES (%s, %s)ON DUPLICATE KEY UPDATE image_id=%s")
        data_member = (usr_id, img_id, img_id)
        cursor.execute(add_img, data_member)
        cnx.commit()
        print("insert usr and img success!")
        cursor.close()
        cnx.close()

    def get_user(self, usr_id):
        cnx = mysql.connector.connect(user=USER_TEST,
                                          password=PASSWORD,
                                          database='linebot')
        cursor = cnx.cursor()
        query = ("SELECT image_id FROM member WHERE user_id = %s")
        data_member = (usr_id,)
        cursor.execute(query, data_member)
        img_name = cursor.fetchone()
        cursor.close()
        cnx.close()
        if img_name:
            return img_name[0]
        return "No User"
