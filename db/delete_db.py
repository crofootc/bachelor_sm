import mysql.connector
import config

def delete_tables():
    # Select Tables to Drop
    tables = ['social_media']

    sql = "DROP TABLE "
    for i in range(len(tables)-1):
        sql += f"`bachelor`.`{tables[i]}`, "
    sql += f"`bachelor`.`{tables[-1]}`;"

    curs.execute(sql)
    print(sql)

    print("DATABASE DROPPED")


if __name__ == "__main__":
    conn = mysql.connector.connect(host=config.host, user=config.user, database=config.db, password=config.pw)

    curs = conn.cursor()
    print(curs)

    delete_tables()
