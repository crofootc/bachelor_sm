import mysql.connector
import config

def create_social_media():
  curs.execute(
     f'''CREATE TABLE `bachelor`.`social_media` (
      `username` VARCHAR(30) NOT NULL,
      `name` VARCHAR(45) NULL,
      `follower_count` INT NULL,
      `following_count` INT NULL,
      `posts` INT NULL,
      `date` DATETIME NULL);

    '''
    )

def set_up():

    create_social_media()


if __name__ == "__main__":
    conn = mysql.connector.connect(host=config.host, user=config.user, database=config.db, password=config.pw)
    curs = conn.cursor()
    print(curs)

    set_up()
