

import discord
import random 
import os
from keep_me import keep_alive
from replit import db



sad_words_response = ["ولش بابا خودتو اذیت نکن ", "این نیز بگذرد بمولا", "اصن ارزششو نداره", "بیخیال ولش باو ",
                          "چیشده؟ برام بگو"]

sad_words=["هعی","تف","ناراحتم","شت","شتت","هعی داق","ریدم","فاک","فاااک","اه"]

learned_input = []

learned_output = []

keys = db.keys()

for i in keys:
  if db[i] == "o1":
    learned_output.append(i)
  elif db[i] == "i1":
    learned_input.append(i)

def db_reset() :
  for x in keys:
    del db[x]


#db_reset()


flag = False
_input = None
_output = None


cl = discord.Client()

      
@cl.event
async def on_ready():
    print("we're logged in as {0.user} :)) ".format(cl))


def main():

  @cl.event
  async def on_message(ms):

    msg = ms.content

    if ms.author == cl.user:
        return

    elif msg.startswith("سلام"):
        await ms.channel.send("بححح سلاممم")

    elif msg == "$delete":
      await ms.channel.send("چه کلمه ای رو میخوای حذف کنی؟")
      @cl.event
      async def on_message(ms4):
        for x in learned_output:
          if x == ms4.content:
            ind=learned_output.index(ms4)
            del db [ms4]
            del db [learned_input[ind]]
            del learned_input[ind]
            learned_output.remove(ms4)
            await ms.channel.send("حذف شد")
          else:
            await ms.channel.send("اصلا من همچین کلمه ای رو بلد نیستم")



    
    elif msg.startswith("راهنما") or msg.startswith("help"):
        await ms.channel.send("$teach برای یاد دادن کلمه ها کافیه بنویسی")

    elif msg.startswith("چطوری") or msg.startswith("خوبی"):
        await ms.channel.send(random.choice(["خوبم مرسی","خوبم ممنون","هعی میگذرونیم",
                                             "اصن مهمه؟","بد نیستم تنکس"]))

    elif msg.startswith("اها"):
        await ms.channel.send("هممم")

    elif any(word in msg for word in sad_words):
        sad_words_response_random = random.choice(sad_words_response)
        await ms.channel.send(sad_words_response_random)

    elif msg.startswith("$teach"):
        global flag
        flag = True
        await ms.channel.send("چه کلمه ای میخوای بهم یاد بدی؟ ")

        @cl.event
        async def on_message(ms2):
            global flag
            if flag:
                msg = ms2.content
                if not msg == "$teach" and not ms2.author == cl.user and ms2.author == ms.author:
                    global _output
                    _output = msg
                    await ms.channel.send("وقتی چی میگن اینو بگم؟")

                    @cl.event
                    async def on_message(ms3):
                        global flag
                        if flag:
                            msg = ms3.content
                            if not cl.user == ms.author and not msg == _output and ms3.author == ms.author:
                                
                                global learned_input, learned_output
                                _input = msg 
                                learned_input.append(_input)
                                learned_output.append(_output)
                                await ms.channel.send("حله")
                                main()
                                db[_output] = "o1"
                                db[_input] = "i1"


    global learned_input, learned_output
    for i in learned_input:
      if i == msg :
        input_index = learned_input.index(i)
        proper_output = learned_output[input_index]
        await ms.channel.send(proper_output)

main()
token = os.environ['token']
keep_alive()
cl.run(token)
