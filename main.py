#imports 


from tkinter import *
import math
from tkinter.scrolledtext import ScrolledText



# --------------------------------- Constants ---------------------------------------------# 

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


session_timer=None
chance_timer = None
user_text=""


# # ---------------------------- TIMER & COUNTDOWN MECHANISM ------------------------------- # 

# ---------------------------- SESSION TIMER countdown ------------------------------- # 


def session_count_down(session_count):


    count_min = math.floor(session_count/60)
    count_sec = session_count%60

    #when the reamining is less then 10 seconds 
    if count_sec<10:
      count_sec=f"0{count_sec}"


    #when the timer is at the begining 
    if count_sec ==0 :
       count_sec="00"
  
    
    canvas.itemconfig(timer_text,text=f"{count_min}:{count_sec}")

    #here we are calling the function we maked above , where every 1 second , the count is decremented by 1 ,
    #  and according to what the count is , we will display it on the canvas ,
    #  or every one second , we are providing a new status for the count and how the time will be displayed (the new time will be the timer variable).
    #  # .after() is a method that executes a certain function after a given amount of time, .after_cancel() cancels that task. 
    if session_count > 0 :

      global session_timer
      session_timer=window.after(1000,session_count_down,session_count-1)

   


# ---------------------------- session end Checking mechanism  ------------------------------- #  


    # when the time is 0 change the welcome label and try to save the text that the user entered! 
     
    if session_count==0:    
            canvas.itemconfig(welcome_text,text="Now your ideas are born!")
            

            global user_text
            if user_text == "":
                return
            try:
                f = open('writeups.txt', 'r')
            except FileNotFoundError:
                f = open('writeups.txt', 'w')
                f.write(user_text)
                user_text = ""
                return
            else:
                cont = f.read()
                if cont == "":
                    text_to_write = user_text
                else:
                    text_to_write = f'\n{user_text}'
        
                with open('writeups.txt', 'a') as f:
                    f.write(text_to_write)
                    user_text = ""
            finally:
                return
         






# ---------------------------- TIMER Start ------------------------------- #  



def start_timer():

      
  session_time = 300

  session_count_down(session_time)




# # --------------------------------------- Listening To The Keyboard and checking the status of writing !  ------------------------------- # 



#what we are doing here is when the user starts typing , if he stops for 5 seconds and there is no event , then 
#we will delete every thing he write, but if he writed and there is an event , we will restart the timer and waits till he h
#stops again , so he have a chance of 5 or 10 seconds to write again !

                  
def clear_text(event=None):
        global chance_timer
        if not event:
            statement_label.delete('1.0', END)

        else:
            if chance_timer:
                window.after_cancel(chance_timer)
                chance_timer = None

            chance_timer = window.after(10000, clear_text)



 #test
# def writing_count_starts(event):
    
#     if event.char:
#         print("not pressed")
#         count.count_down()
#     if not event.char :
#         print(" pressed")
#         return is_pressed==False

# def writing_count_stops(event):
#      if event.char:
#         print("pressed")
#         count.stop_count_down()
#         count.n=5           

     


# ---------------------------- UI SETUP ------------------------------- #

window=Tk()
window.title("Disappearing Text App")
window.config(bg=YELLOW)
window.minsize(width=1000, height=700)





canvas=Canvas( width=900 , height=100 , bg=YELLOW , highlightthickness=0 )

timer_label=canvas.create_text(100,90,text="Time Left:",fill="red",font=(FONT_NAME,12,"bold"))

timer_text=canvas.create_text(190 ,90,text="00:00",fill="black",font=(FONT_NAME,12,"bold"))

welcome_text=canvas.create_text(700 ,30,text="Disappearing Text App!",fill="black",font=(FONT_NAME,15,"bold"))

canvas.place(x=0,y=5)





statement_label = ScrolledText(height=5, width=57,font=("Courier",18,"bold"),fg="Black",bg=YELLOW )
statement_label.place(x=250,y=200)
statement_label.configure(wrap='word')




button_start=Button(width=90,border=3,text="Start",command=start_timer)
button_start.place(x=350,y=430)   




window.bind('<Key>', clear_text)
window.mainloop()