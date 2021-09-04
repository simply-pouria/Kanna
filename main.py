
import discord
import random 
import os
from keep_me import keep_alive
from replit import db

# some secret stuff :)
# F1,F2,S1,S2, and R1 are not secrets but a bit impolite to be in code :/
F1 = os.environ['F1']
 
F2 = os.environ['F2']

S1 = os.environ['S1']

S2 = os.environ['S2']

R1 = os.environ['R1']

token = os.environ['token']


# lists which contain default outputs and inputs
sad_words_response = ["ولش بابا خودتو اذیت نکن ", "این نیز بگذرد بمولا", "اصن ارزششو نداره" ,"بیخیال ولش باو",
                      "چیشده؟ برام بگو"]

sad_words = ["هعی" ,"تف" ,"ناراحتم", S1 , S2 ,"هعی داق", R1, F1, F2, ]


# using replit db to store words
def get_keys():
    keys = db.keys()
    return keys


# variables which I use later in code
flag = False
flag_2 = False
_input = None
_output = None


# creates a list of outputs
def get_outputs():
    outputs = []
    for x in get_keys():
        out = db[x]
        outputs.append(out)
        return outputs


# gets output returns input
def get_key(_k_):
    for x in get_keys():
        if db[x] == _k_:
            return x


# just in case I wanted to reset the database
def db_reset():
    for x in get_keys():
        del db[x]


# simple stuff!
cl = discord.Client()


@cl.event
async def on_ready():
    print("we're logged in as {0.user} :)) ".format(cl))


# when we use a conditional statement on_message won't update.
# so in order to have multipile if's and elif's we have to add a few more on_messages's
# the problem is whenever a new on_message apears the older ones stop working
# so we have to write the whole code in a function and then call it in the end.
def main():
    @cl.event
    async def on_message(ms):

        msg = ms.content

        if ms.author == cl.user:
            return

        # now we use  lists in line 26 and 29
        elif any(word in msg for word in sad_words):
            sad_words_response_random = random.choice(sad_words_response)
            await ms.channel.send(sad_words_response_random)

        elif msg.startswith("$reset_database"):
            db_reset()
            await ms.channel.send("دیتا بیس ریست شد")

        elif msg.startswith("راهنما") or msg.startswith("help"):
            await ms.channel.send("$delete برای پاک کردنشون بنویس  $teach برای یاد دادن کلمه ها کافیه بنویسی")

        elif msg.startswith("چطوری") or msg.startswith("خوبی"):
            await ms.channel.send(random.choice(["خوبم مرسی", "خوبم ممنون", "هعی میگذرونیم",
                                                 "اصن مهمه؟", "بد نیستم تنکس"]))

        # our words remain even after restart so we need to delete some of them
        elif msg == "$delete":
            global flag_2
            flag_2 = True
            await ms.channel.send("چه کلمه ای رو میخوای حذف کنی؟")

            @cl.event
            async def on_message(ms4):
                global flag_2
                if flag_2:

                    if not ms4.author == cl.user and ms4.author == ms.author and not ms4.content == "$delete":
                        # i is used to understand when the whole list is checked and there is no match for the word so
                        # anna doesn't even know what the word is,let alone deleting it
                        i = 0
                        for x in get_outputs():
                            i = i + 1
                            if x == ms4.content:
                                del db[get_key(x)]
                                await ms4.channel.send("حذف شد")
                                # we use flag to stop fetching message after the operation
                                flag_2 = False
                                main()
                            elif i == len(get_keys()):
                                await ms4.channel.send("من اصلا این کلمه رو بلد نیستم")
                                flag_2 = False
                                main()
                            else:
                                print("shit")
                                main()

        elif msg.startswith("$teach"):
            global flag
            flag = True
            await ms.channel.send("چه کلمه ای میخوای بهم یاد بدی؟ ")

            @cl.event
            async def on_message(ms2):

                if flag:
                    msg = ms2.content

                    if not msg == "$teach" and not ms2.author == cl.user and ms2.author == ms.author:
                        global _output
                        _output = msg
                        await ms.channel.send("وقتی چی میگن اینو بگم؟")

                        @cl.event
                        async def on_message(ms3):

                            for y in get_keys():
                                if y == ms3.content:
                                    await ms3.channel.send("برای این کلمه جواب بلدم")
                                    global flag
                                    flag = False
                                    main()

                            if flag:
                                msg = ms3.content
                                if not cl.user == ms.author and not msg == _output and ms3.author == ms.author:
                                    _input = msg
                                    db[_input] = _output
                                    await ms.channel.send("حله")
                                    main()

        # here we check if Kanna have learned the messages if yes we send the proper answer
        for g in get_keys():
            if g == msg:
                await ms.channel.send(db[msg])


main()
keep_alive()
cl.run(token)
