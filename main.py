import discord
import os
from keep_me import keep_alive
import json
import randfacts
from deep_translator import GoogleTranslator
from datetime import datetime
import pytz


token = os.environ['token']


#we use a text file as db because we have some issues with replit database
# If there is not a txt file we'll add one and write {} in it 
try:
  open("learned_words" , "x")
  learned_words_txt = open("learned_words" , "w")
  
  learned_words_txt.write("{}")
  learned_words_txt.close()
  learned_words_txt = open("learned_words" , "r")


#if we already have a file we should just open it
except:
  learned_words_txt = open("learned_words" , "r")


#dictionary which contain added outputs and inputs
learned_words = json.load(learned_words_txt)



# we'll need this several times in code to make everything easier
def update_txt():
  global learned_words
  j = json.dumps(learned_words)
  with open('learned_words','w') as f:
    f.write(j)
    f.close()

def update_history(input,output,user):
  try:
    open("history" , "x")
    history = open("history" , "w")
    tehran_tz = pytz.timezone('Asia/Tehran')
    tehran_dt = datetime.now(tehran_tz)
    tehran_time = tehran_dt.strftime("%H:%M:%S")
    history.write(input + ' -> ' + output + ' by ' + user + ' at ' + tehran_time + '\n')
  except:
    history = open("history" , "a")
    tehran_tz = pytz.timezone('Asia/Tehran')
    tehran_dt = datetime.now(tehran_tz)
    tehran_time = tehran_dt.strftime("%H:%M:%S")
    history.write(input + ' -> ' + output + ' by ' + user + ' at ' + tehran_time + '\n' )
    
    
  
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
      
    elif msg.startswith("$history"):
      if ms.author.id == 740139892419461131:
        history = open('history','r')
        await ms.channel.send(history.read())
      else:
        await ms.channel.send('this command is dad-only :P')
        

      
    elif msg.startswith("$reset_database"):
      
      if not len(learned_words) == 0:
        learned_words.clear()
        update_txt()
        await ms.channel.send("دیتا بیس ریست شد")
      else:
        await ms.channel.send("دیتا بیس خالیه")


    elif msg.startswith("راهنما") or msg.startswith("help"):
        await ms.channel.send("$delete برای پاک کردنشون بنویس  $teach برای یاد دادن کلمه ها کافیه بنویسی")


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
    
    elif msg.startswith("$teach"):
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
            if ms2.content == "$teach" or ms2.content == "$delete" or ms2.content == "$reset_database" or ms2.content == "help" or ms2.content == "راهنما" or ms2.content == "$fact" or ms2.content == "$weirdfact" :
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
                      if ms3.content == "$teach" or ms3.content == "$delete" or ms3.content == "$reset_database" or ms3.content == "help" or ms3.content == "راهنما" or ms3.content == "$fact" or ms3.content == "$weirdfact" :
                        await ms2.channel.send("you were not supposed to do that")
                        flag = False
                        main()
                      
                      if flag:
                          msg = ms3.content
                          if not cl.user == ms.author and not msg == _output and ms3.author == ms.author:

                              #we add the word to both database and dictionary and also save t to history
                              _input = ms3.content
                              learned_words[_input] = _output
                              user = str(ms3.author)
                              update_txt()
                              update_history(_input,_output,user)
                            
                              await ms.channel.send("حله")
                              main()


    elif msg == "$fact" :
      fact = randfacts.get_fact(filter_enabled=True)
      await ms.channel.send(fact)
      translated = GoogleTranslator(source='en', target='fa').translate(text=fact)
      await ms.channel.send(translated)


    elif msg == "$weirdfact" :
      fact = randfacts.get_fact(only_unsafe=True)
      await ms.channel.send(fact)
      translated = GoogleTranslator(source='en', target='fa').translate(text=fact)
      await ms.channel.send(translated)

    
    

                            
    #here we check if Kanna have learned the messages if yes we send the proper answer
    
    for i in keys:
      if i == msg:
        await ms.channel.send(learned_words[i])
        main()
                  

main()
keep_alive()
cl.run(token)



      




