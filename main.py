import discord
import random 
import os
from keep_me import keep_alive
import json


#some secret stuff :)
#F1,F2,S1,S2, and R1 are not secrets but a bit impolite to be in code :/
F1 = os.environ['F1']

F1 = os.environ['F1']

F2 = os.environ['F2']

S1 = os.environ['S1']

S2 = os.environ['S2']

R1 = os.environ['R1']

token = os.environ['token']


#we use a text file as db because we have some issues with replit database
# If there is not a txt file we'll add one and write {} in it 
try:
  open("learned_words" , "x")
  learned_words_txt = open("learned_words" , "w")
  learned_words_txt.write("{}")
  learned_words_txt = open("learned_words" , "r")


#if we already have a file we should just open it
except:
  learned_words_txt = open("learned_words" , "r")

#lists which contain default outputs and inputs
sad_words_response = ["ولش بابا خودتو اذیت نکن ", "این نیز بگذرد بمولا", "اصن ارزششو نداره",
"بیخیال ولش باو ","چیشده؟ برام بگو"]

sad_words=["هعی","تف","ناراحتم","هعی داق",R1,F1,F2,S1,S2]


#dictionary which contain added outputs and inputs
learned_words = json.load(learned_words_txt)



# we'll need this several times in code to make everything easier
def update_txt():
  global learned_words
  j = json.dumps(learned_words)
  with open('learned_words','w') as f:
    f.write(j)
    f.close()


keys = learned_words.keys()


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

    elif msg.startswith("$reset_database"):
      if not len(learned_words) == 0:
        learned_words.clear()
        update_txt()
        await ms.channel.send("دیتا بیس ریست شد")
      else:
        await ms.channel.send("دیتا بیس خالیه")


    elif msg.startswith("راهنما") or msg.startswith("help"):
        await ms.channel.send("$delete برای پاک کردنشون بنویس  $teach برای یاد دادن کلمه ها کافیه بنویسی")

    elif msg.startswith("چطوری") or msg.startswith("خوبی"):
        await ms.channel.send(random.choice(["خوبم مرسی","خوبم ممنون","هعی میگذرونیم",
                                             "اصن مهمه؟","بد نیستم تنکس"]))

    #our words remain even after restart so we need to delete some of them
    elif msg == "$delete":
      if not len(learned_words) == 0:
        global flag_2
        flag_2 = True
        await ms.channel.send("چه کلمه ای رو میخوای حذف کنی؟")

        @cl.event
        async def on_message(ms4):
          global flag_2
          if flag_2:

            if not ms4.author == cl.user and ms4.author == ms.author and not ms4.content == "$delete" :
              # i is used to understand when the whole list is checked and there is no match for the word so kanna don't even know what the word is,let alone deleting it
              i=0
              for y in keys:
                i = i + 1
                m = learned_words[y]
                if m == ms4.content:
                  #we need to delete the words from dictionary
                  del learned_words[y]
                  update_txt()
                  await ms.channel.send("حذف شد")
                  flag_2 = False
                  #we use flag to stop fetching message after the operation 
                  main()
                elif i == len(learned_words):
                  await ms.channel.send("من اصلا این کلمه رو بلد نیستم")
                  flag_2 = False
                  main()
        

      else:
        await ms.channel.send("دیتا بیس خالیه")        
    
    elif msg.startswith("$teach") :
        global flag
        flag = True
        await ms.channel.send("چه کلمه ای میخوای بهم یاد بدی؟ ")

        @cl.event
        async def on_message(ms2):
            for y in learned_words.values():
              if y == ms2.content:
                await ms2.channel.send("این کلمه رو از قبل بلد بودم")
                global flag
                flag = False
                main()
            if ms2.content == "$teach" or ms2.content == "$delete" or ms2.content == "$reset_database" or ms2.content == "help" or ms2.content == "راهنما" :
              await ms2.channel.send("you were not supposed to do that")
              flag = False
              main()


            if flag:
                msg = ms2.content
                
                if not msg == "$teach" and not ms2.author == cl.user and ms2.author == ms.author:
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
                      if ms3.content == "$teach" or ms3.content == "$delete" or ms3.content == "$reset_database" or ms3.content == "help" or ms3.content == "راهنما" :
                        await ms2.channel.send("you were not supposed to do that")
                        flag = False
                        main()
                      
                      if flag:
                          msg = ms3.content
                          if not cl.user == ms.author and not msg == _output and ms3.author == ms.author:

                              #we add the word to both database and dictionary
                              _input = ms3.content
                              learned_words[_input] = _output
                              update_txt()
                              await ms.channel.send("حله")
                              main()
                            
    #here we check if Kanna have learned the messages if yes we send the proper answer
    
    for i in keys:
      if i == msg:
        await ms.channel.send(learned_words[i])
        main()


main()
keep_alive()
cl.run(token)