

import discord
import random 
import os
from keep_me import keep_alive
from replit import db

#some secret stuff :)
#F1,F2,S1,S2, and R1 are not secrets but a bit impolite to be in code :/
F2 = os.environ['F2']

S1 = os.environ['S1']

S2 = os.environ['S2']

R1 = os.environ['R1'] 

token = os.environ['TK']



#lists which contain default outputs and inputs
sad_words_response = ["ولش بابا خودتو اذیت نکن ", "این نیز بگذرد بمولا", "اصن ارزششو نداره",
"بیخیال ولش باو ","چیشده؟ برام بگو"]

sad_words=["هعی","تف","ناراحتم",S1,S2,"هعی داق",R1,F1,F2,]

#dictionary which contain added outputs and inputs
learned_input_output = {}

#using replit db to store words
keys = db.keys()
keys2 = learned_input_output.keys()
for i in keys:
  learned_input_output[i] = db[i]

#variables which I use later in code
flag = False
flag_2 = False
_input = None
_output = None


#simple stuff!
cl = discord.Client()

@cl.event
async def on_ready():
    print("we're logged in as {0.user} :)) ".format(cl))


#when we use a conditional statement on_message won't update.
#so in order to have multipile if's and elif's we have to add a few more on_messages's 
#the problem is whenever a new on_message apears the older ones stop working
#so we have to write the whole code in a function and then call it in the end.
def main():

  @cl.event
  async def on_message(ms):

    msg = ms.content

    if ms.author == cl.user:
        return

    #now we use  lists in line 26 and 29
    elif any(word in msg for word in sad_words):
        sad_words_response_random = random.choice(sad_words_response)
        await ms.channel.send(sad_words_response_random)

    elif msg.startswith("!reset_database"):
      if not len(learned_input_output) == 0:
        learned_input_output.clear()
        for x in keys:
          del db[x]
          main()
        await ms.channel.send("دیتا بیس ریست شد")
      else:
        await ms.channel.send("دیتا بیس خالیه")
    elif msg.startswith("راهنما") or msg.startswith("help"):
        await ms.channel.send("$delete برای پاک کردنشون بنویس  $teach برای یاد دادن کلمه ها کافیه بنویسی")

    elif msg.startswith("چطوری") or msg.startswith("خوبی"):
        await ms.channel.send(random.choice(["خوبم مرسی","خوبم ممنون","هعی میگذرونیم",
                                             "اصن مهمه؟","بد نیستم تنکس"]))

    #our words remain even after restart so we need to delete some of them
    elif msg == "!delete":
      if not len(learned_input_output) == 0:
        global flag_2
        flag_2 = True
        await ms.channel.send("چه کلمه ای رو میخوای حذف کنی؟")

        @cl.event
        async def on_message(ms4):
          global flag_2
          if flag_2:

            if not ms4.author == cl.user and ms4.author == ms.author and not ms4.content == "!delete" :
              # i is used to understand when the whole list is checked and there is no match for the word so kanna don't even know what the word is,let alone deleting it
              i=0
              for y in keys2:
                i = i + 1
                m = learned_input_output[y]
                if m == ms4.content:
                  #we need to delete the words both from database and dictionary
                  del db [y]
                  del learned_input_output[y]
                  await ms.channel.send("حذف شد")
                  flag_2 = False
                  #we use flag to stop fetching message after the operation 
                  main()
                elif i == len(learned_input_output):
                  await ms.channel.send("من اصلا این کلمه رو بلد نیستم")
                  flag_2 = False
                  main()
                else:
                  print ('shit')
                  main()
      else:
        await ms.channel.send("دیتا بیس خالیه")        
    
    elif msg.startswith("!teach"):
        global flag
        flag = True
        await ms.channel.send("چه کلمه ای میخوای بهم یاد بدی؟ ")

        @cl.event
        async def on_message(ms2):
          if not ms2.author == cl.user:
              for y in learned_input_output.values():
                if y == ms2.content:
                  await ms2.channel.send("این کلمه رو از قبل بلد بودم")
                  global flag
                  flag = False
                  main()

              if flag:
                  msg = ms2.content
                  
                  if not msg == "!teach" and not ms2.author == cl.user and ms2.author == ms.author:
                      global _output
                      _output = msg
                      await ms.channel.send("وقتی چی میگن اینو بگم؟")

                      @cl.event
                      async def on_message(ms3):
                        for y in keys:
                          if y == ms3.content:
                            await ms3.channel.send("برای این کلمه جواب بلدم")
                            global flag
                            flag = False
                            main()
                        
                        if flag:
                            msg = ms3.content
                            if not cl.user == ms.author and not msg == _output and ms3.author == ms.author:
                                  
                                
                                #we add the word to both database and dictionary
                                _input = msg 
                                
                                learned_input_output[_input] = _output
                                db[_input] = _output
                                await ms.channel.send("حله")
                                main()
                                
    #here we check if Kanna have learned the messages if yes we send the proper answer
    
    for i in keys2:
      if i == msg :
        await ms.channel.send(db[i])
        main()


main()
keep_alive()
cl.run(token)