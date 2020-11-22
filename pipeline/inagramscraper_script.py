from instagramscraper import Instagram
from config import profile, insta_pw, profile_path
from random import randint
from time import sleep


insta = Instagram()

# insta.follower_count
insta.login(profile, insta_pw)


file = open(profile_path, "r")

contents = file.read()
# dictionary = ast.literal_eval(contents)

file.close()
candidates = eval(contents.replace("\n",""))

for person in candidates:
    user = candidates[person]

    insta.upload_record(user)

    sleep(randint(10,100))
