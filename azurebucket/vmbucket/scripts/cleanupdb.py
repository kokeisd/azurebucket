import sqlite3

def deleteRecord():
    try:
        sqliteConnection = sqlite3.connect('../db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_query = "DELETE from vmbucket_vmbucket"
        #sql_delete_query = 'SELECT name from sqlite_master where type= "table"'
        cursor.execute(sql_delete_query)
        
        #print(cursor.fetchall())
        sqliteConnection.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")

deleteRecord()
