# import os,sys
# import numpy as np
# import time
# import random
# from tkinter import *
# import time
# from tkinter import ttk
# import tkinter.ttk as ttk
# from pandas import DataFrame
# import pygetwindow as gw
# import webbrowser
# import csv
# import webbrowser
# from PIL import ImageGrab
# from PIL import Image

import os
import sys
import numpy as np
import time
import random
import csv
import webbrowser
from tkinter import *
from tkinter import ttk
from pandas import DataFrame
from PIL import ImageGrab, Image
# import pygetwindow as gw  # Removed because it is not used and causes import error

######### system appearance and general Function ###########
def Save_Table_image():
    num_of_rows = int(Row_num_entry.get())
    Main_window.state('zoomed')
    time.sleep(0.5)
    global Canvas_X, Canvas_Y,win_width,win_height
    Canvas_X, Canvas_Y = Frame_Canvas.winfo_width(), Frame_Canvas.winfo_height()

    win_width, win_height = Main_window.winfo_screenwidth(), Main_window.winfo_screenheight()

    x = win_width-Canvas_X
    y = win_height-Canvas_Y

    x1 = Canvas_X
    y1 = 1000


    path = os.getcwd()+r"\Table Image.JPG"
    image_exsist = os.path.isfile("Table Image.JPG")
    if(image_exsist is True):
        os.remove(path)
    #print(x,y,x1,y1)
    ImageGrab.grab().crop((x,y,x1,y1)).save(path)
    #im2 = ImageGrab.grab(bbox=(x,y,x1,y1))
    #im2.show()

def error_messege(msg):
    Table_View.delete("all")
    popup = Tk()
    popup.wm_title("ERROR!!")
    label = ttk.Label(popup, text=msg,font='Helvetica 15 bold')
    label.pack(side="top", fill="x", pady=10,padx=15)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def Open_Link(url):
    webbrowser.open_new(url)

def Re_Create_Window():
    global Frame_treats, Frame_Canvas, Frame_Apply,Table_View  ### global for frames
    Frame_treats.destroy()
    Frame_Canvas.destroy()
    Frame_Apply.destroy()
    Frame_treats = Frame(Main_window)  ### the filling cells frame
    Frame_Canvas = Frame(Main_window)  ### the treats frame
    Frame_Apply = Frame(Main_window)  #### the activation button frame
    Frame_treats.pack()
    Frame_Canvas.pack(expand=True, fill=BOTH)
    Frame_Apply.pack()

    Table_View = Canvas(Frame_Canvas, width=300, height=300, scrollregion=(0, 0, 500000, 500000))
    hbar = Scrollbar(Frame_Canvas, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=Table_View.xview)
    vbar = Scrollbar(Frame_Canvas, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=Table_View.yview)
    Table_View.config(width=300, height=300)
    Table_View.config(xscrollcommand=hbar.set)
    Table_View.pack(expand=True, fill=BOTH)


    ## button creating
    #Calc = Button(Frame_calc_example, bd=1, bg="white", fg="black",
     #             text="Calculate", padx=10, pady=1, command=Calc_Plants,height=1,width=5)
    #Calc.grid(row=4, column=10, sticky=W,padx=50,pady=2)
    Apply_Button_Block = Button(Frame_Apply, bd=1, bg="white", fg="black", text="Block design / Re-Shuffle",
                                padx=10, pady=5, command=Collect_Names_For_Blocks,height=2,width=18)
    Apply_Button_Block.grid(row=0, column=0, padx=0, pady=0)

    Apply_Button_Full_random = Button(Frame_Apply, bd=1, bg="white", fg="black", text="Full Random / Re-Shuffle",
                                      padx=10, pady=5, command=Collect_Names_For_Full_Random,height=2,width=18)
    Apply_Button_Full_random.grid(row=0, column=1)

    Clear_Board = Button(Frame_Apply, bd=1, bg="white", fg="black", text="Clear Board",
                         padx=10, pady=5, command=lambda: Table_View.delete("all"))
    Clear_Board.grid(row=0, column=2)
    ######## botton from file
    File_Apply_Button_Block = Button(Frame_Apply, bd=1, bg="lawn green", fg="black", text="File\n Block design / Re-Shuffle",
                                     padx=10, pady=5,
                                     command=Collect_Names_For_Blocks_file,height=2,width=18)  ### change to collect from file
    File_Apply_Button_Block.grid(row=2, column=0,pady=10,padx=7.5)

    File_Apply_Button_Full_random = Button(Frame_Apply, bd=1, bg="lawn green", fg="black",
                                           text="File\n Full Random / Re-Shuffle",
                                           padx=10, pady=5,
                                           command=Collect_Names_For_Full_Random_file,height=2,width=18)  ### change to collect from file
    File_Apply_Button_Full_random.grid(row=2, column=1,pady=10,padx=7.5)

    Info_file_Button = Button(Frame_Apply, bd=1, bg="white", fg="black", text="Take me\nto my files",
                              padx=10, pady=5, command=Open_File_Directory)  ### change to collect from file
    Info_file_Button.grid(row=3, column=2)

    if(num_of_cell>20):
        Table_View.create_text(Text_X, 50, text="\tThere are to many lines please press \n "
                                                "'Take me to my files' in order to open the 'Info' file",
                               font=("Times bold", 18), fill='red')


    Info_file_Button.grid(row=2, column=2)

def Calc_Plants():
    global num_of_cell,Summary_entry,Row_num_entry
    ####
    Summary_entry = Entry(Frame_calc_example, width=Box_width)
    Summary_entry.grid(row=4, column=3, sticky=W, padx=Top_Cell_distance)
    #######
    try:
        val_1 = int(factor1_entry.get())
        val_2 = int(Factor2_entry.get())
        if(Rep_entry.get()!=""):
            val_3 = int(Rep_entry.get())
            Final_Val = (val_1*val_2*val_3)
            Summary_entry.delete(0,'end')
            Summary_entry.insert(0,Final_Val)
            Summary_entry.config(state='disable')
        num_of_cell = val_1*val_2

        element = bool(Frame_treats.winfo_exists())
        if (element is True):
            Re_Create_Window()


        cell_by_treat(num_of_cell)
    except ValueError:
        Table_View.delete("all")  ### clears the board
        Summary_entry = Entry(Frame_calc_example, width=Box_width,state='disable')
        Summary_entry.grid(row=4, column=3, sticky=W, padx=Top_Cell_distance)
        #Table_View.delete("all")  ### clears the board

        val_1,val_2,val_3  = (factor1_entry.get()),(Factor2_entry.get()),Rep_entry.get() ## get's the numeric string of
        #Line,Treat,Return
        numeric_val_1 = val_1.isnumeric() ## check if numeric
        numeric_val_2 = val_2.isnumeric()## check if numeric
        numeric_val_3 = val_3.isnumeric()## check if numeric


        if(val_1=="" or val_2==""):
            Text_2 = "The 'Line' and 'Treat' boxes' must be filled"
            Table_View.create_text(Text_X, 100, text=Text_2, font=("Times bold", 20), fill='red')
        else:
            if((numeric_val_1 is False) or (numeric_val_2 is False)):
                Table_View.delete("all")  ### clears the board
                Text_1 = "Please enter numeric values in the top cells"
                Table_View.create_text(Text_X, 100, text=Text_1, font=("Times bold", 20), fill='red')
            if((val_3!="") and (numeric_val_3 is False)):
                Table_View.delete("all")  ### clears the board
                Text_1 = "Please enter numeric values in the top cells"
                Table_View.create_text(Text_X, 100, text=Text_1, font=("Times bold", 20), fill='red')

    #print(Final_Val)

def Chart_maker(num_of_plants,Treat_names,factor_1_array,factor_2_array):
   i = 1 ### number the letter
   j = 0 ### just for the symbol
   i_1 = 1 ## number of the letter
   j_1 = 0 ## number of the symbol

   k =temp = 97; ## ascii symbol for letter (97-a, 98-b, 99-c, 100 -d)
   Names = []
   end_count = []

   if (Row_letter_entry.get() == ""):  ### check's if row num was input, deafult is 4
       # Letter is the ascii value of the letter A
       Letter = "A"
    #    Letter = 65
       Row_letter_entry.insert(0, Letter)

   Table = Row_letter_entry.get().upper()
   ##
   ##
   for num in range(num_of_plants):
       if int(i)<10:
           Names.append(str(Table)+str(j)+str(i)+chr(k)) ###name of file at output "X01a-X09d"
           k+=1
           end_count.append(i)
           #i=1 if (end_count.count(9)==4) else none
       elif (10<=int(i)<19):
           Names.append(str(Table)+str(i)+chr(k))  ## new name of file at output "X10a-X18d
           k+=1
           end_count.append(i)
           if(end_count.count(18)==4):
               i=0
               Table = chr(ord(Table) + 1)
               if(Table==90): Table=74
               end_count=[]

       value = int(Row_num_entry.get())
       if (k==(temp+value)):
           k = k-(k-temp)
           i +=1
           #i_1 +=1
           j=0
   ## 2020.07.04 - adding Combined name the final columns
   Combined_name_zip = list(zip(Names,Treat_names))
   Combined_name = [f"{val[0]} ({val[1]})" for val in Combined_name_zip]

   Merged_Array = list(zip(Names,Treat_names,factor_1_array,factor_2_array,Combined_name))
   path = os.getcwd()+r"\Treat_file.csv"
   df = DataFrame(Merged_Array,columns=['Plant Position','Treat Name','Line','Treat',"Combined"]) ### inserting the arrays to csv
   try:
       export_csv = df.to_csv(path, index=None, header=True)
   except IOError:
       error_messege("close the 'Treat file'\nand run again")

   ### creating map in CSV
   #print(len(Treat_names)," len of treat names")
   #print(num_of_plants)
   if(len(Treat_names)>num_of_plants):
       Treat_names = Treat_names[:num_of_plants] ##
   letters = ["MAP","A","B","C","D","E","F","G","H","I","j"] ##
   Row_num = int(Row_num_entry.get())
   Map = []
   Map.append(letters[0:Row_num+1])
   counter= 1
   for i in range(0,len(Treat_names),Row_num):
       temp_list = (Treat_names[i:i+Row_num])
       temp_list.insert(0,counter)
       #temp_list.reverse()
       Map.append(temp_list)
       counter+=1
       if counter==19:
           counter=1
   #print(Map)

   path_2 = os.getcwd()+r"\Map.csv"
   df_2= DataFrame(Map)
   df_2.shift()[1:]
   try:
    export_csv = df_2.to_csv(path_2,index=None,header=None)
   except IOError:
       error_messege("close the 'Map' file\nand run again")

def Table_creation(Treat_Amount,Color_index,Treat_names):
    global Table_View
    ###


    ##
    #colors =["blue","green","yellow","red","black","white","orange","purple","pink","brown","DarkOrange4","salmon","mint cream","snow"]
    colors = ['blue', 'green', 'yellow', 'red', 'black', 'white', 'purple', 'pink', 'brown', 'salmon',
            'peach puff', 'gray', 'midnight blue', 'cornflower blue',
            'light slate blue', 'pale green', 'dark green','indian red',
            'saddle brown', 'orange', 'hot pink', 'deep pink', 'seashell2', 'seashell3', 'seashell4', 'medium blue'
            ,'SlateBlue4', 'cyan3', 'yellow4', 'tan4', 'maroon4', 'gray1', 'medium slate blue', 'gray25','lawn green', 'gray63'
            ,'mint cream', 'snow', 'gainsboro', 'dark slate gray', 'DarkOrange4','MediumPurple4', 'slate gray']
    if(max(Color_index)>=len(colors)):
        colors = ['sandy brown', 'RoyalBlue4', 'gold2', 'plum1', 'cornsilk4', 'gray10', 'gray78', 'aquamarine',
                  'blanched almond', 'dark slate blue', 'blue4', 'orchid1', 'gold', 'light goldenrod',
                  'LightSteelBlue3', 'chartreuse3',
                  'sienna3', 'gray47', 'DarkOrchid3', 'sky blue', 'gray58', 'dark khaki', 'medium sea green', 'gray50',
                  'PaleGreen2', 'PaleTurquoise4',
                  'chartreuse4', 'salmon1', 'blue violet', 'bisque2', 'purple2', 'navajo white', 'light salmon',
                  'wheat2', 'SeaGreen1', 'indian red', 'linen',
                  'gray71', 'MistyRose4', 'cornsilk2', 'honeydew3', 'light blue', 'MediumPurple1', 'hot pink',
                  'RoyalBlue3', 'SeaGreen3', 'PaleVioletRed2', 'tomato',
                  'gray43', 'gray72', 'gray89', 'salmon3', 'LemonChiffon2', 'khaki', 'gray15', 'khaki1',
                  'LightGoldenrod2', 'light pink', 'sienna1', 'gray75', 'gray30',
                  'coral3', 'gray54', 'blue', 'CadetBlue2', 'pink1', 'gray59', 'gray35', 'gray49', 'LavenderBlush3',
                  'gray65', 'DarkOrchid1', 'red4', 'LightGoldenrod4',
                  'yellow green', 'yellow4', 'IndianRed4', 'RosyBrown1', 'PeachPuff3', 'yellow3', 'thistle4', 'gray90',
                  'gray97', 'green yellow', 'DarkOliveGreen3', 'SteelBlue4',
                  'snow3', 'honeydew2', 'maroon3', 'DarkSeaGreen3', 'gray12', 'navy', 'gray6', 'gray29', 'sienna2',
                  'steel blue', 'gray45', 'OliveDrab2', 'DarkSlateGray4', 'DarkOrchid2',
                  'DarkOrange1', 'LightSkyBlue3', 'antique white', 'LavenderBlush2', 'lavender', 'gray99', 'sea green',
                  'gray39', 'goldenrod1', 'AntiqueWhite1', 'DarkGoldenrod3', 'light sea green',
                  'tomato4', 'tan2', 'light slate gray', 'lawn green', 'gray26', 'LightCyan3', 'SkyBlue1', 'cyan',
                  'gray25', 'brown3', 'light coral', 'gray55', 'maroon', 'dark goldenrod', 'gray79',
                  'LightCyan4', 'light sky blue', 'gray86', 'gray53', 'HotPink1', 'medium aquamarine', 'honeydew4',
                  'DeepPink3', 'gray11', 'SteelBlue2', 'dark olive green', 'pale turquoise', 'purple',
                  'green2', 'HotPink2', 'red3', 'saddle brown', 'medium turquoise', 'PaleTurquoise3', 'goldenrod3',
                  'slate gray', 'SlateBlue1', 'SeaGreen2', 'gray5', 'gray14', 'DarkSlateGray3', 'khaki4',
                  'midnight blue', 'gray44', 'coral', 'green4', 'goldenrod4', 'gray20', 'gray9', 'pale green',
                  'SlateBlue3', 'seashell2', 'lavender blush', 'LightSteelBlue4', 'gray69', 'thistle1', 'gray68',
                  'aquamarine2', 'LightYellow3', 'light goldenrod yellow', 'snow4', 'LightSteelBlue2', 'coral1',
                  'orchid4', 'plum4', 'gray61', 'LightBlue1', 'SpringGreen4', 'gray8', 'seashell4', 'DarkOrange4',
                  'gray7', 'violet red', 'medium spring green', 'CadetBlue3', 'PaleTurquoise1', 'MistyRose3', 'gray82',
                  'light grey', 'turquoise1', 'salmon2', 'SteelBlue3', 'powder blue', 'azure3', 'SlateBlue2', 'gray85',
                  'LightBlue2', 'green3', 'chartreuse2', 'brown2', 'ghost white', 'medium blue', 'lime green', 'gray36',
                  'ivory3', 'DarkSeaGreen2', 'dark green', 'burlywood4', 'magenta4', 'purple4', 'SkyBlue3', 'gray18',
                  'papaya whip',
                  'firebrick1', 'chocolate3', 'gray3', 'DodgerBlue3', 'gray74', 'HotPink4', 'DarkGoldenrod1', 'gray16',
                  'dark slate gray', 'gray19', 'white smoke', 'maroon1', 'PaleVioletRed3', 'gray33', 'maroon4',
                  'LightPink3', 'MediumPurple2',
                  'medium orchid', 'RosyBrown3', 'snow', 'DarkOrchid4', 'pink', 'PeachPuff4', 'seashell3',
                  'spring green', 'old lace', 'ivory2', 'LightSkyBlue4', 'LightSalmon2', 'dim gray', 'goldenrod2',
                  'rosy brown', 'medium slate blue', 'PeachPuff2',
                  'LemonChiffon3', 'gray48', 'thistle', 'VioletRed3', 'yellow2', 'LightBlue3', 'MediumPurple3',
                  'dark violet', 'DodgerBlue4', 'deep pink', 'bisque3', 'MediumOrchid4', 'LightSalmon4', 'orange red',
                  'gray', 'dark salmon', 'gold4', 'tan1',
                  'gray92', 'LightPink2', 'medium violet red', 'LightSkyBlue1', 'gray63', 'gray24', 'gray95', 'snow2',
                  'DarkOrange2', 'maroon2', 'gray67', 'gray27', 'gray23', 'pink3', 'salmon', 'SlateGray3', 'orange',
                  'VioletRed2', 'turquoise4', 'bisque',
                  'orchid2', 'slate blue', 'yellow', 'purple3', 'DarkGoldenrod4', 'burlywood1', 'gray83', 'gray38',
                  'gray37', 'gray34', 'magenta3', 'RosyBrown4', 'plum3', 'orchid3', 'LightPink1', 'gray94',
                  'aquamarine4', 'SkyBlue4', 'gray46', 'cornflower blue',
                  'LightYellow4', 'cyan2', 'gray52', 'LightGoldenrod3', 'DeepPink4', 'coral4', 'gray87',
                  'LightSteelBlue1', 'light steel blue', 'dark orange', 'purple1', 'PaleGreen3', 'turquoise3',
                  'MediumOrchid1', 'DarkOrange3', 'OrangeRed2', 'wheat4', 'gray88',
                  'CadetBlue4', 'IndianRed2', 'goldenrod', 'OliveDrab4', 'SteelBlue1', 'burlywood2', 'khaki3',
                  'DarkOliveGreen4', 'SlateGray2', 'LightGoldenrod1', 'DarkOliveGreen1', 'DarkSeaGreen1', 'gray73',
                  'salmon4', 'sienna4', 'alice blue', 'cadet blue',
                  'SpringGreen2', 'LemonChiffon4', 'gray64', 'VioletRed1', 'AntiqueWhite2', 'gold3', 'DodgerBlue2',
                  'forest green', 'MediumOrchid3', 'DeepSkyBlue4', 'MediumOrchid2', 'khaki2', 'blue2', 'gray57',
                  'deep sky blue', 'ivory4', 'OrangeRed4',
                  'CadetBlue1', 'gray40', 'azure2', 'PaleVioletRed1', 'red', 'IndianRed3', 'SlateGray1', 'brown4',
                  'pink4', 'azure4', 'peach puff', 'wheat3', 'DarkOliveGreen2', 'thistle2', 'PaleVioletRed4',
                  'pale violet red', 'orange2', 'firebrick4',
                  'azure', 'gray32', 'DarkGoldenrod2', 'MediumPurple4', 'VioletRed4', 'thistle3', 'orange3', 'tomato2',
                  'tomato3', 'gray84', 'chocolate2', 'mint cream', 'SlateGray4', 'gray76', 'coral2', 'turquoise',
                  'gray93', 'gray98', 'gray1',
                  'cornsilk3', 'HotPink3', 'gray77', 'DarkSeaGreen4', 'floral white', 'burlywood3', 'cyan3', 'gray13',
                  'NavajoWhite4', 'gray60', 'gray42', 'RosyBrown2', 'gray17', 'gray66', 'gray70', 'RoyalBlue1',
                  'LightSkyBlue2', 'PaleTurquoise2',
                  'SpringGreen3', 'royal blue', 'light slate blue', 'cyan4', 'LightPink4', 'LightCyan2',
                  'LavenderBlush4', 'gray56', 'chocolate1', 'lemon chiffon', 'MistyRose2', 'bisque4', 'wheat1',
                  'gainsboro', 'light cyan', 'orange4', 'PaleGreen1',
                  'magenta2', 'IndianRed1', 'gray22', 'NavajoWhite2', 'SkyBlue2', 'gray4', 'turquoise2', 'RoyalBlue2',
                  'DarkSlateGray2', 'firebrick2', 'brown1', 'DeepPink2', 'misty rose', 'AntiqueWhite3', 'red2',
                  'PaleGreen4', 'DeepSkyBlue2',
                  'DarkSlateGray1', 'gray62', 'dark turquoise', 'gray51', 'LightYellow2', 'NavajoWhite3', 'gray2',
                  'gray21', 'OrangeRed3', 'AntiqueWhite4', 'dark orchid', 'pink2', 'gray81', 'light yellow', 'gray80',
                  'medium purple', 'LightSalmon3',
                  'gray91', 'OliveDrab1', 'gray28', 'DeepSkyBlue3', 'tan4', 'dodger blue', 'LightBlue4', 'gray31',
                  'firebrick3', 'pale goldenrod', 'dark sea green', 'olive drab', 'SlateBlue4', 'plum2']




    #letters = ["A", "B", "C", "D","E","F","G","H","i","J","K","L","M","N"]
    counter_num = 0
    Token = 0
    Token_Color = 0
    Token_letter = 0


    if(Row_num_entry.get()==""): ### check's if row num was input, deafult is 4
        row_num = 4
        Row_num_entry.insert(0,4)

    else:
        row_num = int(Row_num_entry.get())

    Stopper = (Treat_Amount // row_num) * 20 + 40

    Y_Row_Number_Jumper=0
    Blocker = (220-row_num*20)
    table_count = 1 ### for index to table number
    ###
    Num_Of_Row = int(Row_num_entry.get())
    if(int(Row_num_entry.get())>4):
        Y_Row_Number_Jumper = (int(Row_num_entry.get())-4)*20


    ##


    text_jump,jumper = 70,350
    for i in range(20, Stopper, 20):
        counter_num += 1
        #print(Treat_Amount,Token)
        #if(Token>0):
            #print(" divide ",Treat_Amount/Token)
        for j in range(220, Blocker ,-20):
            if (Token<Treat_Amount):
                #Color_Index = random.randint(0, len(colors) - 1)
                temp = int(Color_index[Token_Color])
                #Table_View.create_text(text_jump,Blocker-10,text="Table",font=("Times",18 )) ## Table 1 - tittle
                Table_View.create_oval(i, j+Y_Row_Number_Jumper, i + 15, j + 15+Y_Row_Number_Jumper, fill=str(colors[temp])) ## create the circle by the index
                if(counter_num<19):
                    Table_View.create_text(i+8,Blocker+10+Y_Row_Number_Jumper,text=str(counter_num))
                elif(19<=counter_num<37):
                    text_jump+=jumper
                    #Table_View.create_text(text_jump+jumper, Blocker-10, text="Table", font=("Times", 18))  ## Table 2 - tittle
                    Table_View.create_line(i-2.5,238+Y_Row_Number_Jumper,i-2.5,(Blocker+Y_Row_Number_Jumper),dash=(10,10),fill="red") ## seperating line
                    counter_num=1
                    Table_View.create_text(i +8, Blocker+10+Y_Row_Number_Jumper, text=str(counter_num))
                #### temp
                #elif(counter_num>=37):
                    #text_jump+=jumper
                    #Table_View.create_text(text_jump,Blocker-10,text="Table",font=("Times",18))
                  #####
                Token_Color += 1
            Token+=1
        text_jump+jumper
    ## Add's the letters
    Token_letter,letter_num_holder=65,0
    for j in range(230,Blocker+20,-20):
        if(letter_num_holder==0):
            Table_View.create_text(10,j+Y_Row_Number_Jumper,text=chr(Token_letter))
        else:
            Table_View.create_text(10, j + Y_Row_Number_Jumper, text=chr(Token_letter)+str(letter_num_holder))
        Token_letter+=1
        if(Token_letter>90):
            Token_letter=65
            letter_num_holder+=1

    length_of_line = Treat_Amount/Num_Of_Row
    Table_View.create_line(20,238+Y_Row_Number_Jumper,25*length_of_line,238+Y_Row_Number_Jumper,dash=(4,2)) ### create dahsed line under before lenends

    ### modify legends
    X_axix_oval  = 20
    X_axix_oval_1 = 35
    X_axix_text = 140
    Y_axix_legend_1 = 245+Y_Row_Number_Jumper
    modify_1 = 15
    Token_legend = 0
    indicator_treat = 0
    #print(Treat_names)
    for legend in range(len(Treat_names)):
        if(Color_index.count(indicator_treat)>0):
            if (Token_legend<=5):
                Table_View.create_oval(X_axix_oval,Y_axix_legend_1,X_axix_oval_1,Y_axix_legend_1+modify_1,fill=(str(colors[indicator_treat])))
                Table_View.create_text(X_axix_text,Y_axix_legend_1+4,text=("-"+str(Treat_names[indicator_treat])+"("+str(Color_index.count(indicator_treat))+")"),font=("Times",15))
                Token_legend+=1
                indicator_treat+=1
                Y_axix_legend_1+=20
                if(Token_legend==5):
                    Y_axix_legend_1-=20*6
                    Token_legend=0
                    Y_axix_legend_1+=20
                    X_axix_oval+=220
                    X_axix_oval_1+=220
                    X_axix_text+=220
                    #indicator_treat+=1
        else:
            indicator_treat+=1



def Create_info_file():
    path =os.getcwd()+r"\Info.csv"
    df = DataFrame(columns=['Line', 'Treat', 'Repetition'])
    file_exists = os.path.isfile("Info.csv")
    export_csv = df.to_csv(path, index=None, header=True) if (file_exists is False) else None

def Open_File_Directory():

    path = os.getcwd()
    path_2 = path+r"\Info.csv"
    os.startfile(path)
    if(os.path.isfile(path_2) is False):
        Table_View.delete("all")  ### clears the board
        Title = Table_View.create_text(Text_X, 150, text="The directory that has just been opened, is the directory which"
                                                         "\n\tall of the files will be located including the:"
                                                         "\n\t1.Treat file\n\t2.Map\n\t3.Info\n\n"
                                                         "The files will alway be saved In the same driectory as rthe Program is saved\n", font=("Times bold", 15),fill='green')
        Title_2 = Table_View.create_text(Text_X, 235, text="All files but info must be closed during each run cycle", font=("Times bold", 15),
                                       fill='red')
        Title_3 = Table_View.create_text(Text_X, 260, text="fill the 'Info' file with the statistics principles suitable to 'Full Random' or 'Block design ", font=("Times bold", 15),
                                       fill='green')
    Create_info_file()
    os.startfile(path_2)

####################################
def Block_Desine(array,indicator):

    Color_Index_Block = []
    stopper = 0
    # print(len(array))
    counter_treat = indicator
    if(counter_treat==0):
        counter_treat = int(Factor2_entry.get()) * int(factor1_entry.get())
        #print(counter_treat, "the range of the sample", len(np.unique(array)))

    # print(counter_treat)
    while (stopper == 0):
        temp = []
        temp = random.sample(range(0, counter_treat), counter_treat)
        for i in range(len(temp)):
            Color_Index_Block.append(temp[i])
        if (len(Color_Index_Block) > len(array) - 2):
            stopper += 1
    # print (Color_Index_Block)
    return (Color_Index_Block)

def Collect_Names_For_Blocks():
    #Frame_treats.destroy()
    Table_View.delete("all")  ### clears the board
    Token = num_of_cell
    Treat_names = []
    Treat_names_modified = []
    Color_Index = []
    factor_1_array = []
    factor_2_array = []
    Repetition = int(Rep_entry.get())
    if(Token>0):
        if (Name_1.get()!=""):
            Treat_names.append(str(Name_1.get())+"_"+str(Name_1_T.get()))
            factor_1_array.append(str(Name_1.get()))
            factor_2_array.append(str(Name_1_T.get()))
            Tr_1.delete(0,'end')
            Tr_1.insert(0,str(Repetition))
            for i in range((int(Tr_1.get()))):
                temp = str(Treat_names[0])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_2.get()!=""):
            Treat_names.append(str(Name_2.get())+"_"+str(Name_2_T.get()))
            factor_1_array.append(str(Name_2.get()))
            factor_2_array.append(str(Name_2_T.get()))
            Tr_2.delete(0,'end')
            Tr_2.insert(0,str(Repetition))
            for i in range((int(Tr_2.get()))):
                temp = str(Treat_names[1])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if(Name_3.get()!=""):
            Treat_names.append(str(Name_3.get())+"_"+Name_3_T.get())
            factor_1_array.append(str(Name_3.get()))
            factor_2_array.append(str(Name_3_T.get()))
            Tr_3.delete(0,'end')
            Tr_3.insert(0,str(Repetition))

            for i in range((int(Tr_3.get()))):
                temp = str(Treat_names[2])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_4.get()!=""):
            Treat_names.append(str(Name_4.get())+"_"+str(Name_4_T.get()))
            factor_1_array.append(str(Name_4.get()))
            factor_2_array.append(str(Name_4_T.get()))
            Tr_4.delete(0,'end')
            Tr_4.insert(0,str(Repetition))
            for i in range((int(Tr_4.get()))):
                temp = str(Treat_names[3])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_5.get()!=""):
            Treat_names.append(str(Name_5.get())+"_"+str(Name_5_T.get()))
            factor_1_array.append(str(Name_5.get()))
            factor_2_array.append(str(Name_5_T.get()))
            Tr_5.delete(0,'end')
            Tr_5.insert(0,str(Repetition))
            for i in range((int(Tr_5.get()))):
                temp = str(Treat_names[4])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_6.get()!=""):
            Treat_names.append(str(Name_6.get())+"_"+str(Name_6_T.get()))
            factor_1_array.append(str(Name_6.get()))
            factor_2_array.append(str(Name_6_T.get()))
            Tr_6.delete(0, 'end')
            Tr_6.insert(0, str(Repetition))

            for i in range((int(Tr_6.get()))):
                temp = str(Treat_names[5])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_7.get()!=""):
            Treat_names.append(str(Name_7.get())+"_"+str(Name_7_T.get()))
            factor_1_array.append(str(Name_7.get()))
            factor_2_array.append(str(Name_7_T.get()))
            Tr_7.delete(0, 'end')
            Tr_7.insert(0, str(Repetition))
            for i in range((int(Tr_7.get()))):
                temp = str(Treat_names[6])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_8.get()!=""):
            Treat_names.append(str(Name_8.get())+"_"+str(Name_8_T.get()))
            factor_1_array.append(str(Name_8.get()))
            factor_2_array.append(str(Name_8_T.get()))
            Tr_8.delete(0, 'end')
            Tr_8.insert(0, str(Repetition))

            for i in range((int(Tr_8.get()))):
                temp = str(Treat_names[7])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_9.get()!=""):
            Treat_names.append(str(Name_9.get())+"_"+str(Name_9_T.get()))
            factor_1_array.append(str(Name_9.get()))
            factor_2_array.append(str(Name_9_T.get()))
            Tr_9.delete(0, 'end')
            Tr_9.insert(0, str(Repetition))

            for i in range((int(Tr_9.get()))):
                temp = str(Treat_names[8])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_10.get()!=""):
            Treat_names.append(str(Name_10.get())+"_"+str(Name_10_T.get()))
            factor_1_array.append(str(Name_10.get()))
            factor_2_array.append(str(Name_10_T.get()))
            Tr_10.delete(0, 'end')
            Tr_10.insert(0, str(Repetition))

            for i in range((int(Tr_10.get()))):
                temp = str(Treat_names[9])+"-"+str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        ######
        if (Name_11.get() != ""):
            Treat_names.append(str(Name_11.get()) + "_" + str(Name_11_T.get()))
            factor_1_array.append(str(Name_11.get()))
            factor_2_array.append(str(Name_11_T.get()))

            Tr_11.delete(0, 'end')
            Tr_11.insert(0, str(Repetition))

            for i in range((int(Tr_11.get()))):
                temp = str(Treat_names[10]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_12.get() != ""):
            Treat_names.append(str(Name_12.get()) + "_" + str(Name_12_T.get()))
            factor_1_array.append(str(Name_12.get()))
            factor_2_array.append(str(Name_12_T.get()))

            Tr_12.delete(0, 'end')
            Tr_12.insert(0, str(Repetition))

            for i in range((int(Tr_12.get()))):
                temp = str(Treat_names[11]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_13.get() != ""):
            Treat_names.append(str(Name_13.get()) + "_" + str(Name_13_T.get()))
            factor_1_array.append(str(Name_13.get()))
            factor_2_array.append(str(Name_13_T.get()))
            Tr_13.delete(0, 'end')
            Tr_13.insert(0, str(Repetition))

            for i in range((int(Tr_13.get()))):
                temp = str(Treat_names[12]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_14.get() != ""):
            Treat_names.append(str(Name_14.get()) + "_" + str(Name_14_T.get()))
            factor_1_array.append(str(Name_14.get()))
            factor_2_array.append(str(Name_14_T.get()))
            Tr_14.delete(0, 'end')
            Tr_14.insert(0, str(Repetition))

            for i in range((int(Tr_14.get()))):
                temp = str(Treat_names[13]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_15.get() != ""):
            Treat_names.append(str(Name_15.get()) + "_" + str(Name_15_T.get()))
            factor_1_array.append(str(Name_15.get()))
            factor_2_array.append(str(Name_15_T.get()))

            Tr_15.delete(0, 'end')
            Tr_15.insert(0, str(Repetition))

            for i in range((int(Tr_15.get()))):
                temp = str(Treat_names[14]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1

    if(Token>0):
        if (Name_16.get() != ""):
            Treat_names.append(str(Name_16.get()) + "_" + str(Name_16_T.get()))
            factor_1_array.append(str(Name_16.get()))
            factor_2_array.append(str(Name_16_T.get()))
            Tr_16.delete(0, 'end')
            Tr_16.insert(0, str(Repetition))

            for i in range((int(Tr_16.get()))):
                temp = str(Treat_names[15]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_17.get() != ""):
            Treat_names.append(str(Name_17.get()) + "_" + str(Name_17_T.get()))
            factor_1_array.append(str(Name_17.get()))
            factor_2_array.append(str(Name_17_T.get()))
            Tr_17.delete(0, 'end')
            Tr_17.insert(0, str(Repetition))
            for i in range((int(Tr_17.get()))):
                temp = str(Treat_names[16]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_18.get() != ""):
            Treat_names.append(str(Name_18.get()) + "_" + str(Name_18_T.get()))
            factor_1_array.append(str(Name_18.get()))
            factor_2_array.append(str(Name_18_T.get()))
            Tr_18.delete(0, 'end')
            Tr_18.insert(0, str(Repetition))

            for i in range((int(Tr_18.get()))):
                temp = str(Treat_names[17]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_19.get() != ""):
            Treat_names.append(str(Name_19.get()) + "_" + str(Name_19_T.get()))
            factor_1_array.append(str(Name_19.get()))
            factor_2_array.append(str(Name_19_T.get()))
            Tr_19.delete(0, 'end')
            Tr_19.insert(0, str(Repetition))

            for i in range((int(Tr_19.get()))):
                temp = str(Treat_names[18]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_20.get() != ""):
            Treat_names.append(str(Name_20.get()) + "_" + str(Name_20_T.get()))
            factor_1_array.append(str(Name_20.get()))
            factor_2_array.append(str(Name_20_T.get()))
            Tr_20.delete(0, 'end')
            Tr_20.insert(0, str(Repetition))

            for i in range((int(Tr_20.get()))):
                temp = str(Treat_names[19]) + "-" + str(i)
                Treat_names_modified.append(temp)
            Token-=1

    Treat_Amount = (len(Treat_names_modified))
    for i in range(len(Treat_names_modified)):
        for j in range(len(Treat_names)):
            if((Treat_names[j]) in (Treat_names_modified[i])):
                Color_Index.append(j)

    Color_Index_Block = Block_Desine(Color_Index,0) ## after sort in blocks

    Treat_names_modified_shuffle = []
    Line_Final_array =[]
    Treat_Final_array = []
    counter_array =[]

    ###short test of values
    User_Change = 0
    num1,num2,num3 = int(factor1_entry.get()),int(Factor2_entry.get()),int(Rep_entry.get())

    Color_Index_Test = (int(Summary_entry.get())==num1*num2*num3) ### keep just in case
    Color_Index_Test = (len(Treat_names_modified)==num1*num2*num3)

    Sum_Test = num1*num2*num3


    #print(Color_Index_Test,type(Color_Index_Test)," check the test", Color_Index_Test==True)
    #print(len(np.unique(factor_1_array)),(num1),bool(len(np.unique(factor_1_array))==num1), "checking extra safty")

    if(Color_Index_Test == True):
        for i in Color_Index_Block:
            counter_array.append(i)
            Treat_names_modified_shuffle.append(Treat_names[i]+"-"+str(counter_array.count(i)))
            Line_Final_array.append(factor_1_array[i])
            Treat_Final_array.append(factor_2_array[i])
    else:
        #Table_View.create_text(Text_X,100,text="Wrong Input For Block-Design",font=("Times bold",18 ),fill='red')
        User_Change+=1

    ########
    # print("idiot pruff")
    factor_1_minimize = list(np.unique(factor_1_array)) ### array of unique values of LIne
    Counter_List = [Line_Final_array.count(treat) for treat in factor_1_minimize] ##  in block the Line is equle
    factor_2_minimize = list(np.unique(factor_2_array))
    # print(factor_2_minimize,len(factor_2_minimize),int(Factor2_entry.get()),len(factor_2_minimize)==int(Factor2_entry.get()),"check the user treat")
    #print(factor_1_minimize,len(Counter_List),Counter_List)
    #print(len(np.unique(Counter_List)), "length of counter array")
    Num_Of_Line = (int(factor1_entry.get()))
    ################



    if((num1*num2*num3!=len(Treat_names_modified)) or (len(np.unique(Counter_List))!=1) or (User_Change==1) or (len(factor_2_minimize)!=int(Factor2_entry.get()))): ### change the color to red if not fit
        temp = Summary_entry.get()
        Summary_entry.delete(0, 'end')
        Summary_entry.config(fg="black",bg="red")
        Summary_entry.insert(0, temp)
        Table_View.create_text(Text_X,100,text="Wrong Input for Block-Design",font=("Times bold",18 ),fill='red')
        Table_View.create_text(Text_X, 100, text="______________________________", font=("Times bold", 18), fill='red')
        #if((int(Summary_entry.get())!=len(Treat_names_modified))):
        if(Sum_Test!=len(Treat_names_modified)):
            Table_View.create_text(Text_X,200,text="You may have gotten this message for one of the following reasons:\n1. "
                                                   "The Numberof repetitions is not equal to the number you declared in the settings\n"
                                                   "2.There is a mismatch between 'Line*Treat' \n\tand the number of cells to be filled\n"
                                                   "" ,font=("Times bold",18 ),fill='red')
        elif(len(np.unique(Counter_List))!=1):
            Table_View.create_text(Text_X, 150, text="In 'Block design' The numberof 'Lines' and to be equal",
                                   font=("Times bold", 18), fill='red')
        elif(len(factor_2_minimize)!=int(Factor2_entry.get())):
            Table_View.create_text(Text_X, 150, text="There is a mismatch between the number of 'Treats' you declared\n\t"
                                                     "and the number of 'Treats' entered",font=("Times bold", 18), fill='red')



    else:
        Title = Table_View.create_text(Title_Design, 100, text="Block Design", font=("Times bold", 15),
                                       fill='green')
        Summary_entry.delete(0,'end')
        Summary_entry.config(fg="black",bg="green")
        Summary_entry.insert(0, str(len(Treat_names_modified)))
        Table_creation(Treat_Amount, Color_Index_Block, Treat_names)
        Chart_maker(Treat_Amount, Treat_names_modified_shuffle, Line_Final_array, Treat_Final_array)

def Collect_Names_For_Full_Random():
    Table_View.delete("all")  ### clears the board
    Token = num_of_cell
    factor_1_array = []
    factor_2_array = []
    Treat_names = []
    Treat_names_modified = []
    Color_Index = []
    if(Token>0):
        if (Name_1.get()!=""):
            Treat_names.append(str(Name_1.get())+"_"+str(Name_1_T.get()))
            for i in range((int(Tr_1.get()))):
                temp = str(Treat_names[0])+"-"+str(i)
                factor_1_array.append(str(Name_1.get()))
                factor_2_array.append(str(Name_1_T.get()))
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_2.get()!=""):
            Treat_names.append(str(Name_2.get())+"_"+str(Name_2_T.get()))
            for i in range((int(Tr_2.get()))):
                temp = str(Treat_names[1])+"-"+str(i)
                factor_1_array.append(str(Name_2.get()))
                factor_2_array.append(str(Name_2_T.get()))
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_3.get()!=""):
            Treat_names.append(str(Name_3.get())+"_"+Name_3_T.get())
            for i in range((int(Tr_3.get()))):
                temp = str(Treat_names[2])+"-"+str(i)
                factor_1_array.append(str(Name_3.get()))
                factor_2_array.append(str(Name_3_T.get()))
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_4.get()!=""):
            Treat_names.append(str(Name_4.get())+"_"+str(Name_4_T.get()))
            for i in range((int(Tr_4.get()))):
                temp = str(Treat_names[3])+"-"+str(i)
                factor_1_array.append(str(Name_4.get()))
                factor_2_array.append(str(Name_4_T.get()))
                Treat_names_modified.append(temp)
            Token -= 1
    if(Token>0):
        if (Name_5.get()!=""):
            Treat_names.append(str(Name_5.get())+"_"+str(Name_5_T.get()))
            for i in range((int(Tr_5.get()))):
                temp = str(Treat_names[4])+"-"+str(i)
                factor_1_array.append(str(Name_5.get()))
                factor_2_array.append(str(Name_5_T.get()))
                Treat_names_modified.append(temp)
            Token -= 1
    if(Token>0):
        if (Name_6.get()!=""):
            Treat_names.append(str(Name_6.get())+"_"+str(Name_6_T.get()))
            for i in range((int(Tr_6.get()))):
                temp = str(Treat_names[5])+"-"+str(i)
                factor_1_array.append(str(Name_6.get()))
                factor_2_array.append(str(Name_6_T.get()))
                Treat_names_modified.append(temp)
            Token -= 1
    if(Token>0):
        if (Name_7.get()!=""):
            Treat_names.append(str(Name_7.get())+"_"+str(Name_7_T.get()))
            for i in range((int(Tr_7.get()))):
                temp = str(Treat_names[6])+"-"+str(i)
                factor_1_array.append(str(Name_7.get()))
                factor_2_array.append(str(Name_7_T.get()))
                Treat_names_modified.append(temp)
            Token -= 1
    if(Token>0):
        if (Name_8.get()!=""):
            Treat_names.append(str(Name_8.get())+"_"+str(Name_8_T.get()))
            for i in range((int(Tr_8.get()))):
                temp = str(Treat_names[7])+"-"+str(i)
                factor_1_array.append(str(Name_8.get()))
                factor_2_array.append(str(Name_8_T.get()))
                Treat_names_modified.append(temp)
            Token -= 1
    if(Token>0):
        if (Name_9.get()!=""):
            Treat_names.append(str(Name_9.get())+"_"+str(Name_9_T.get()))
            for i in range((int(Tr_9.get()))):
                temp = str(Treat_names[8])+"-"+str(i)
                factor_1_array.append(str(Name_9.get()))
                factor_2_array.append(str(Name_9_T.get()))
                Treat_names_modified.append(temp)
            Token -= 1
    if(Token>0):
        if (Name_10.get()!=""):
            Treat_names.append(str(Name_10.get())+"_"+str(Name_10_T.get()))
            for i in range((int(Tr_10.get()))):
                temp = str(Treat_names[9])+"-"+str(i)
                factor_1_array.append(str(Name_10.get()))
                factor_2_array.append(str(Name_10_T.get()))
                Treat_names_modified.append(temp)
            Token -= 1
    if(Token>0):
        if(Name_11.get()!=""):
            Treat_names.append(str(Name_11.get())+"_"+str(Name_11_T.get()))
            for i in range((int(Tr_11.get()))):
                temp = str(Treat_names[10])+"-"+str(i)
                factor_1_array.append(str(Name_11.get()))
                factor_2_array.append(str(Name_11_T.get()))
                Treat_names_modified.append(temp)
            Token -= 1
    if(Token>0):
        if(Name_12.get()!=""):
            Treat_names.append(str(Name_12.get())+"_"+str(Name_12_T.get()))
            for i in range((int(Tr_12.get()))):
                temp = str(Treat_names[11])+"-"+str(i)
                factor_1_array.append(str(Name_12.get()))
                factor_2_array.append(str(Name_12_T.get()))
                Treat_names_modified.append(temp)
            Token -= 1
        ###
    if(Token>0):
        if (Name_13.get() != ""):
            Treat_names.append(str(Name_13.get()) + "_" + str(Name_13_T.get()))
            for i in range((int(Tr_13.get()))):
                temp = str(Treat_names[12]) + "-" + str(i)
                factor_1_array.append(str(Name_13.get()))
                factor_2_array.append(str(Name_13_T.get()))
                Treat_names_modified.append(temp)
        Token-=1
        ###
    if(Token>0):
        if (Name_14.get() != ""):
            Treat_names.append(str(Name_14.get()) + "_" + str(Name_14_T.get()))
            for i in range((int(Tr_14.get()))):
                temp = str(Treat_names[13]) + "-" + str(i)
                factor_1_array.append(str(Name_14.get()))
                factor_2_array.append(str(Name_14_T.get()))
                Treat_names_modified.append(temp)
            Token-=1
        ####
    if(Token>0):
        if (Name_15.get() != ""):
            Treat_names.append(str(Name_15.get()) + "_" + str(Name_15_T.get()))
            for i in range((int(Tr_15.get()))):
                temp = str(Treat_names[14]) + "-" + str(i)
                factor_1_array.append(str(Name_15.get()))
                factor_2_array.append(str(Name_15_T.get()))
                Treat_names_modified.append(temp)
            Token-=1
            ####
    if(Token>0):
        if (Name_16.get() != ""):
            Treat_names.append(str(Name_16.get()) + "_" + str(Name_16_T.get()))
            for i in range((int(Tr_16.get()))):
                temp = str(Treat_names[15]) + "-" + str(i)
                factor_1_array.append(str(Name_16.get()))
                factor_2_array.append(str(Name_16_T.get()))
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_17.get() != ""):
            Treat_names.append(str(Name_17.get()) + "_" + str(Name_17_T.get()))
            for i in range((int(Tr_17.get()))):
                temp = str(Treat_names[16]) + "-" + str(i)
                factor_1_array.append(str(Name_17.get()))
                factor_2_array.append(str(Name_17_T.get()))
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_18.get() != ""):
            Treat_names.append(str(Name_18.get()) + "_" + str(Name_18_T.get()))
            for i in range((int(Tr_18.get()))):
                temp = str(Treat_names[17]) + "-" + str(i)
                factor_1_array.append(str(Name_18.get()))
                factor_2_array.append(str(Name_18_T.get()))
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_19.get() != ""):
            Treat_names.append(str(Name_19.get()) + "_" + str(Name_19_T.get()))
            for i in range((int(Tr_19.get()))):
                temp = str(Treat_names[18]) + "-" + str(i)
                factor_1_array.append(str(Name_19.get()))
                factor_2_array.append(str(Name_19_T.get()))
                Treat_names_modified.append(temp)
            Token-=1
    if(Token>0):
        if (Name_20.get() != ""):
            Treat_names.append(str(Name_20.get()) + "_" + str(Name_20_T.get()))
            for i in range((int(Tr_20.get()))):
                temp = str(Treat_names[19]) + "-" + str(i)
                factor_1_array.append(str(Name_20.get()))
                factor_2_array.append(str(Name_20_T.get()))
                Treat_names_modified.append(temp)
            Token-=1


    Treat_Amount = (len(Treat_names_modified))
    for i in range(len(Treat_names_modified)):
        for j in range(len(Treat_names)):
            if((Treat_names[j]) in (Treat_names_modified[i])):
                Color_Index.append(j)

    Treat_names_modified_shuffle = Treat_names_modified
    Treat_Amount = (len(Treat_names_modified_shuffle))

    for i in range(len(Treat_names_modified_shuffle)):
        for j in range(len(Treat_names)):
            if((Treat_names[j]) in (Treat_names_modified_shuffle[i])):
                Color_Index.append(j)

    Line_Final_array =[]
    Treat_Final_array = []
    counter_array = []
    for i in Color_Index:
        # print(Treat_names[i])
        counter_array.append(i)
        Line_Final_array.append(factor_1_array[i])
        Treat_Final_array.append(factor_2_array[i])
    ########################################
    merged = list(zip(Treat_names_modified_shuffle, factor_1_array, factor_2_array, Color_Index))
    random.shuffle(merged)
    Treat_names_modified_shuffle, Line_Final_array, Treat_Final_array, Color_Index = (zip(*merged))
    Table_creation(Treat_Amount,Color_Index,Treat_names)
    Chart_maker(Treat_Amount,list(Treat_names_modified_shuffle),list(Line_Final_array),list(Treat_Final_array))

    if(int(Summary_entry.get())!=len(Treat_names_modified)): ### change the color to red if not fit
        Summary_entry.delete(0, 'end')
        Summary_entry.config(fg="black",bg="red")
        Summary_entry.insert(0, str(len(Treat_names_modified)))
    else:
        Title = Table_View.create_text(Title_Design, 100, text="Full Random Design", font=("Times bold", 15),
                                       fill='green')

        Summary_entry.delete(0,'end')
        Summary_entry.config(fg="black",bg="green")
        Summary_entry.insert(0, str(len(Treat_names_modified)))

def Collect_Names_For_Blocks_file():
    ###
    global Summary_entry
    Frame_treats.pack_forget() ### make treat's disappear
    Summary_entry = Entry(Frame_calc_example, width=Box_width)
    Summary_entry.grid(row=4, column=3, sticky=W, padx=Top_Cell_distance)
    Table_View.delete("all") ### clears the board

    Treat_names = []
    Treat_names_modified = []
    Color_Index = []
    factor_1_array = []
    factor_2_array = []
    factor_3_array = []
    with open('Info.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            Factor = row['Line']
            Treat = row['Treat']
            Repetition = row['Repetition']
            factor_3_array.append(Repetition)
            Treat_names.append(Factor + "_" + Treat)
            for num in range(int(Repetition)):
                factor_1_array.append(Factor)
                factor_2_array.append(Treat)
                Treat_names_modified.append(Factor + "_" + Treat + "-" + str(num))

            

        val_1 = len(np.unique(factor_1_array)) ### the line unique value
        val_2 = len(np.unique(factor_2_array)) ### the treat unique value
        val_3 = len(np.unique(factor_3_array)) ### value of rep of each treat
        Rep_Value = str(''.join(np.unique(factor_3_array))) ### the value of each Rep
        final_val =val_1*val_2


        #Treat_names_modified_shuffled = Treat_names_modified
        Treat_Amount = len(Treat_names_modified)
        for i in range(len(Treat_names_modified)):
            for j in range(len(Treat_names)):
                if ((Treat_names[j]) in (Treat_names_modified[i])):
                    Color_Index.append(j)
        Color_Index_Block = Block_Desine(Color_Index,final_val)  ## after sort in blocks
        factor_1_array_modify = []
        factor_2_array_modify = []

        ### checking if values are good
        factor_1_array_short = (list(np.unique(factor_1_array)))
        val_4_array = [factor_1_array.count(value) for value in factor_1_array_short]
        val_4 =(len(np.unique(val_4_array)))


        for tr in range(len(factor_1_array)):
            factor_2_array_modify.append(factor_2_array[tr])  if factor_2_array[tr] not in factor_2_array_modify else None


        ###checking treat in block -
        val_5_array = [factor_2_array.count(treat) for treat in factor_2_array_modify]
        val_5 = len(np.unique(val_5_array))
        #print(val_5,val_3,val_4, "values for Treat")
        val_6 = val_3+val_4+val_5
        # print(val_5==1)
        Treat_names_modified_shuffle = []
        Line_Final_array = []
        Treat_Final_array = []
        counter_array = []
        if( val_3!=1 or val_4!=1 or val_5!=1):
            Table_View.delete("all")  ### clears the board
            Table_View.create_text(Text_X, 100, text="Wrong Input For Block-Design", font=("Times bold", 18),
                                   fill='red')
            if(val_3!=1):
                Table_View.create_text(Text_X, 150, text="Make Sure that all of the repetition are equal"
                                       ,font=("Times bold", 18), fill='red')

            elif(val_4!=1):

                Table_View.create_text(Text_X, 150, text="In 'Block design', the numbers of limes jas to be equal\n\t"
                                                         "within  each block",
                font = ("Times bold", 18), fill = 'red')

            elif(val_5!=1):
                Table_View.create_text(Text_X, 150, text="A 'Block design', requires an equal number of 'Treats'\n\t"
                                                         "in each block",
                                       font=("Times bold", 18), fill='red')

        else:
            for i in Color_Index_Block:
                counter_array.append(i)
                Treat_names_modified_shuffle.append(Treat_names[i] + "-" + str(counter_array.count(i)))
                Line_Final_array.append(Treat_names[i][:(Treat_names[i].index("_"))])
                Treat_Final_array.append(Treat_names[i][(Treat_names[i].index("_")) + 1:])






        if (val_3 != 1):  ### change the color to red if not fit
            temp = Summary_entry.get()
            Summary_entry.delete(0, 'end')
            Summary_entry.config(fg="black", bg="red")
            Summary_entry.insert(0, temp)

        elif((val_3==1) and (val_4==1) and (val_5==1)):
            Summary_entry.delete(0, 'end')
            factor1_entry.delete(0,'end')
            Factor2_entry.delete(0,'end')
            Rep_entry.delete(0,'end')

            Title = Table_View.create_text(Title_Design, 100, text="Block Design", font=("Times bold", 15),
                                           fill='green')

            p = (np.unique(factor_3_array[0]))
            Summary_entry.config(fg="black", bg="green")
            Summary_entry.insert(0, str(len(Treat_names_modified)))
            factor1_entry.insert(0,str(val_1))
            Factor2_entry.insert(0,str(val_2))
            Rep_entry.insert(0,Rep_Value)
            Summary_entry.config(state='disable')



            Table_creation(Treat_Amount, Color_Index_Block, Treat_names)
            Chart_maker(Treat_Amount, Treat_names_modified_shuffle, Line_Final_array, Treat_Final_array)

def Collect_Names_For_Full_Random_file():
    ###
    Frame_treats.pack_forget() ### make treat's disappear
    ###
    global Summary_entry
    Summary_entry = Entry(Frame_calc_example, width=Box_width)
    Summary_entry.grid(row=4, column=3, sticky=W, padx=Top_Cell_distance)
    Table_View.delete("all")  ### clears the board
    Treat_names = []
    factor_1_array = []
    factor_2_array = []
    factor_3_array = []
    Treat_names_modify = []
    Color_Index = []
    with open('Info.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            Factor = row['Line']
            Treat = row['Treat']
            Repetition = row['Repetition']
            factor_3_array.append(Repetition)
            Treat_names.append(Factor + "_" + Treat)
            for num in range(int(Repetition)):
                factor_1_array.append(Factor)
                factor_2_array.append(Treat)

                Treat_names_modify.append(Factor + "_" + Treat + "-" + str(num))
        Treat_names_modified_shuffled = Treat_names_modify
        Treat_Amount = len(Treat_names_modified_shuffled)

        factor_3_array = list(map(int,factor_3_array))


        val_1 = len(np.unique(factor_1_array)) ### the line unique value
        val_2 = len(np.unique(factor_2_array)) ### the treat unique value
        val_3 = len(np.unique(factor_3_array)) ### value of rep of each treat



        for i in range(len(Treat_names_modified_shuffled)):
            for j in range(len(Treat_names)):
                if ((Treat_names[j]) in (Treat_names_modified_shuffled[i])):
                    Color_Index.append(j)

    Title = Table_View.create_text(Title_Design, 100, text="Full Random Design", font=("Times bold", 15),
                                   fill='green')
    ##
    Summary_entry.delete(0, 'end')
    factor1_entry.delete(0)
    Factor2_entry.delete(0)
    Rep_entry.delete(0)

    factor1_entry.insert(0,str(val_1))
    Factor2_entry.insert(0,str(val_2))
    Summary_entry.insert(0,str(sum(factor_3_array)))
    Summary_entry.config(state='disable')
    ###
    merged = list(zip(Treat_names_modified_shuffled, factor_1_array, factor_2_array, Color_Index))
    random.shuffle(merged)
    Treat_names_modified_shuffle, Line_Final_array, Treat_Final_array, Color_Index = ((zip(*merged)))

    Table_creation(Treat_Amount, list(Color_Index), Treat_names)
    Chart_maker(Treat_Amount, list(Treat_names_modified_shuffle), list(Line_Final_array), list(Treat_Final_array))


def cell_by_treat(num_of_cell):
    if(num_of_cell>0):
        ## working on User entry Frame
        #print(num_of_cell)
        DBC_X,DBC_Y = 5,1 ## distance betweeen cells
        Trow, Trow_2, Brow, Drow =  8,9, 10, 11  ## for the first 10 treat's
        Trow_3, Trow_4, Brow_2, Drow_2 = 12,13, 14, 15  ## 10 - 20 treat
        #### title for the first 10 treats
        Name_of_Treat = Label(Frame_treats, text="Line Names")
        Name_of_Treat.grid(row=Trow, column=0, sticky=N)
        Name_of_Treat_2 = Label(Frame_treats, text="Treatments Names")
        Name_of_Treat_2.grid(row=Trow_2, column=0, sticky=N)
        Entry_Rep = Label(Frame_treats, text="Number of Repetitions")
        Entry_Rep.grid(row=Brow, column=0, sticky=N)
        ### 1 - A
        global Name_1,Name_1_T,Tr_1
        Name_1 = Entry(Frame_treats,width=Box_width)
        Name_1_T = Entry(Frame_treats,width=Box_width)
        Tr_1 = Entry(Frame_treats,width=Box_width)
        num_write_1 = Label(Frame_treats,text="1")
        Name_1.grid(row=Trow,column=1,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_1_T.grid(row=Trow_2,column=1,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_1.grid(row=Brow,column=1,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_1.grid(row=Drow,column=1,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ###2 - A
    if(num_of_cell>0):
        global Name_2, Name_2_T, Tr_2
        Name_2 = Entry(Frame_treats,width=Box_width)
        Name_2_T = Entry(Frame_treats,width=Box_width)
        Tr_2 = Entry(Frame_treats,width=Box_width)
        num_write_2 = Label(Frame_treats,text="2")
        ##grid
        Name_2.grid(row=Trow,column=2,stick=W,padx=DBC_X,pady=DBC_Y)
        Name_2_T.grid(row =Trow_2,column=2,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_2.grid(row=Brow,column=2,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_2.grid(row=Drow,column=2,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 3 - A
    if(num_of_cell>0):
        global Name_3, Name_3_T, Tr_3
        Name_3 = Entry(Frame_treats,width=Box_width)
        Name_3_T = Entry(Frame_treats,width=Box_width)
        Tr_3 = Entry(Frame_treats,width=Box_width)
        num_write_3 = Label(Frame_treats,text="3")
        ##grid
        Name_3.grid(row=Trow,column=3,stick=W,padx=DBC_X,pady=DBC_Y)
        Name_3_T.grid(row=Trow_2,column=3,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_3.grid(row=Brow,column=3,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_3.grid(row=Drow,column=3,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 4 -A
    if(num_of_cell>0):
        global Name_4, Name_4_T, Tr_4
        Name_4 = Entry(Frame_treats,width=Box_width)
        Name_4_T = Entry(Frame_treats,width=Box_width)
        Tr_4 = Entry(Frame_treats,width=Box_width)
        num_write_4 = Label(Frame_treats,text="4")
        ##grid
        Name_4.grid(row=Trow,column=4,stick=W,padx=DBC_X,pady=DBC_Y)
        Name_4_T.grid(row=Trow_2,column=4,stick=W,padx=DBC_X,pady=DBC_Y)
        Tr_4.grid(row=Brow,column=4,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_4.grid(row=Drow,column=4,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 5 - A
    if(num_of_cell>0):
        global Name_5, Name_5_T, Tr_5
        Name_5 = Entry(Frame_treats,width=Box_width)
        Name_5_T = Entry(Frame_treats,width=Box_width)
        Tr_5 = Entry(Frame_treats,width=Box_width)
        num_write_5 = Label(Frame_treats,text="5")
        ## grid
        Name_5.grid(row=Trow,column=5,stick=W,padx=DBC_X,pady=DBC_Y)
        Name_5_T.grid(row=Trow_2,column=5,stick=W,padx=DBC_X,pady=DBC_Y)
        Tr_5.grid(row=Brow,column=5,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_5.grid(row=Drow,column=5,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 6 - A
    if(num_of_cell>0):
        global Name_6, Name_6_T, Tr_6
        Name_6 = Entry(Frame_treats,width=Box_width)
        Name_6_T = Entry(Frame_treats,width=Box_width)
        Tr_6 = Entry(Frame_treats,width=Box_width)
        num_write_6 = Label(Frame_treats,text="6")
        #grid
        Name_6.grid(row=Trow,column=6,stick=W,padx=DBC_X,pady=DBC_Y)
        Name_6_T.grid(row=Trow_2,column=6,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_6.grid(row=Trow,column=6,stick=W,padx=DBC_X,pady=DBC_Y)
        Tr_6.grid(row=Brow,column=6,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_6.grid(row=Drow,column=6,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 7 - A
    if(num_of_cell>0):
        global Name_7, Name_7_T, Tr_7
        Name_7 = Entry(Frame_treats,width=Box_width)
        Name_7_T = Entry(Frame_treats,width=Box_width)
        Tr_7 = Entry(Frame_treats,width=Box_width)
        num_write_7 = Label(Frame_treats,text="7")
        ##grid
        Name_7.grid(row=Trow,column=7,stick=W,padx=DBC_X,pady=DBC_Y)
        Name_7_T.grid(row=Trow_2,column=7,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_7.grid(row=Brow,column=7,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_7.grid(row=Drow,column=7,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 8 - A
    if(num_of_cell>0):
        global Name_8, Name_8_T, Tr_8
        Name_8 = Entry(Frame_treats,width=Box_width)
        Name_8_T = Entry(Frame_treats,width=Box_width)
        Tr_8 = Entry(Frame_treats,width=Box_width)
        num_write_8 = Label(Frame_treats,text="8")
        #grid
        Name_8.grid(row=Trow,column=8,stick=W,padx=DBC_X,pady=DBC_Y)
        Name_8_T.grid(row=Trow_2,column=8,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_8.grid(row=Brow,column=8,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_8.grid(row=Drow,column=8,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 9 - A
    if(num_of_cell>0):
        global Name_9, Name_9_T, Tr_9
        Name_9 = Entry(Frame_treats,width=Box_width)
        Name_9_T = Entry(Frame_treats,width=Box_width)
        Tr_9 = Entry(Frame_treats,width=Box_width)
        num_write_9 = Label(Frame_treats,text="9")
        ## grid
        Name_9.grid(row=Trow,column=9,stick=W,padx=DBC_X,pady=DBC_Y)
        Name_9_T.grid(row=Trow_2,column=9,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_9.grid(row=Brow,column=9,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_9.grid(row=Drow,column=9,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 9 - A
    if(num_of_cell>0):
        global Name_10,Name_10_T,Tr_10
        Name_10 = Entry(Frame_treats,width=Box_width)
        Name_10_T = Entry(Frame_treats,width=Box_width)
        Tr_10 = Entry(Frame_treats,width=Box_width)
        num_write_10 = Label(Frame_treats,text="10")
        ##grid
        Name_10.grid(row=Trow,column=10,stick=W,padx=DBC_X,pady=DBC_Y)
        Name_10_T.grid(row=Trow_2,column=10,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_10.grid(row=Brow,column=10,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_10.grid(row=Drow,column=10,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        #########################################################
    if(num_of_cell>0):
        #### title for the
        # 10-20 treats
        Name_of_Treat = Label(Frame_treats,text="Line Names")
        Name_of_Treat.grid(row=Trow_3,column=0,sticky=N)
        Name_of_Treat_2 = Label(Frame_treats,text="Treatments  Names")
        Name_of_Treat_2.grid(row=Trow_4,column=0,sticky=N)
        Entry_Rep = Label(Frame_treats,text="Number of Repetitions")
        Entry_Rep.grid(row=Brow_2,column=0,sticky=N)
        ###  1 - B
        global Name_11,Name_11_T,Tr_11
        Name_11 = Entry(Frame_treats,width=Box_width)
        Name_11_T = Entry(Frame_treats,width=Box_width)
        Tr_11 = Entry(Frame_treats,width=Box_width)
        num_write_11 = Label(Frame_treats,text="11")
        #grid
        Name_11.grid(row=Trow_3,column=1,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_11_T.grid(row=Trow_4,column=1,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_11.grid(row=Brow_2,column=1,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_11.grid(row=Drow_2,column=1,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ###  2 - B
    if(num_of_cell>0):
        global Name_12, Name_12_T, Tr_12
        Name_12 = Entry(Frame_treats,width=Box_width)
        Name_12_T = Entry(Frame_treats,width=Box_width)
        Tr_12 = Entry(Frame_treats,width=Box_width)
        num_write_12 = Label(Frame_treats,text="12")

        Name_12.grid(row=Trow_3,column=2,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_12_T.grid(row=Trow_4,column=2,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_12.grid(row=Brow_2,column=2,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_12.grid(row=Drow_2,column=2,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 3- b
    if(num_of_cell>0):
        global Name_13, Name_13_T, Tr_13
        Name_13 = Entry(Frame_treats,width=Box_width)
        Name_13_T = Entry(Frame_treats,width=Box_width)
        Tr_13 = Entry(Frame_treats,width=Box_width)
        num_write_13 = Label(Frame_treats,text="13")
        ####
        Name_13.grid(row=Trow_3,column=3,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_13_T.grid(row=Trow_4,column=3,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_13.grid(row=Brow_2,column=3,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_13.grid(row=Drow_2,column=3,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        #### 4 - b
    if(num_of_cell>0):
        global Name_14, Name_14_T, Tr_14
        Name_14 = Entry(Frame_treats,width=Box_width)
        Name_14_T = Entry(Frame_treats,width=Box_width)
        Tr_14 = Entry(Frame_treats,width=Box_width)
        num_write_14 = Label(Frame_treats,text="14")
        ##grid
        Name_14.grid(row=Trow_3,column=4,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_14_T.grid(row=Trow_4,column=4,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_14.grid(row=Brow_2,column=4,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_14.grid(row=Drow_2,column=4,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ## 5 -b
    if(num_of_cell>0):
        global Name_15, Name_15_T, Tr_15
        Name_15 = Entry(Frame_treats,width=Box_width)
        Name_15_T = Entry(Frame_treats,width=Box_width)
        Tr_15 = Entry(Frame_treats,width=Box_width)
        num_write_15 = Label(Frame_treats,text="15")
        ##grid
        Name_15.grid(row=Trow_3,column=5,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_15_T.grid(row=Trow_4,column=5,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_15.grid(row=Brow_2,column=5,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_15.grid(row=Drow_2,column=5,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ### 6 - b
    if(num_of_cell>0):
        global Name_16, Name_16_T, Tr_16
        Name_16 = Entry(Frame_treats,width=Box_width)
        Name_16_T = Entry(Frame_treats,width=Box_width)
        Tr_16 = Entry(Frame_treats,width=Box_width)
        num_write_16 = Label(Frame_treats,text="16")
        ##grid
        Name_16.grid(row=Trow_3,column=6,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_16_T.grid(row=Trow_4,column=6,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_16.grid(row=Brow_2,column=6,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_16.grid(row=Drow_2,column=6,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ## 7 - b
    if(num_of_cell>0):
        global Name_17, Name_17_T, Tr_17
        Name_17 = Entry(Frame_treats,width=Box_width)
        Name_17_T = Entry(Frame_treats,width=Box_width)
        Tr_17 = Entry(Frame_treats,width=Box_width)
        num_write_17 = Label(Frame_treats,text="17")
        ##grid
        Name_17.grid(row=Trow_3,column=7,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_17_T.grid(row=Trow_4,column=7,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_17.grid(row=Brow_2,column=7,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_17.grid(row=Drow_2,column=7,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ## 8 -b
    if(num_of_cell>0):
        global Name_18, Name_18_T, Tr_18
        Name_18 = Entry(Frame_treats,width=Box_width)
        Name_18_T = Entry(Frame_treats,width=Box_width)
        Tr_18 = Entry(Frame_treats,width=Box_width)
        num_write_18 = Label(Frame_treats,text="18")
        ##grid
        Name_18.grid(row=Trow_3,column=8,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_18_T.grid(row=Trow_4,column=8,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_18.grid(row=Brow_2,column=8,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_18.grid(row=Drow_2,column=8,sticky=N,padx=DBC_X,pady=DBC_Y)
        ## 9 -b
    if(num_of_cell>0):
        global Name_19, Name_19_T, Tr_19
        Name_19 = Entry(Frame_treats,width=Box_width)
        Name_19_T = Entry(Frame_treats,width=Box_width)
        Tr_19 = Entry(Frame_treats,width=Box_width)
        num_write_19 = Label(Frame_treats,text="19")
        ###
        Name_19.grid(row=Trow_3,column=9,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_19_T.grid(row=Trow_4,column=9,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_19.grid(row=Brow_2,column=9,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_19.grid(row=Drow_2,column=9,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1
        ## 10 - b
    if(num_of_cell>0):
        global Name_20, Name_20_T, Tr_20
        Name_20 = Entry(Frame_treats,width=Box_width)
        Name_20_T = Entry(Frame_treats,width=Box_width)
        Tr_20 = Entry(Frame_treats,width=Box_width)
        num_write_20 = Label(Frame_treats,text="20")

        Name_20.grid(row=Trow_3,column=10,sticky=W,padx=DBC_X,pady=DBC_Y)
        Name_20_T.grid(row=Trow_4,column=10,sticky=W,padx=DBC_X,pady=DBC_Y)
        Tr_20.grid(row=Brow_2,column=10,sticky=W,padx=DBC_X,pady=DBC_Y)
        num_write_20.grid(row=Drow_2,column=10,sticky=N,padx=DBC_X,pady=DBC_Y)
        num_of_cell-=1





#### GUI Create #####
Main_window = Tk() #The app will be divided inside this window
Main_window.title("Array Randomizer")
Frame_calc_example = Frame(Main_window) ### the calc function frame
Frame_treats = Frame(Main_window) ### the filling cells frame
Frame_Canvas = Frame(Main_window) ### the treats frame
Frame_Apply = Frame(Main_window) #### the activation button frame

###
Frame_calc_example.pack() ### delete
Frame_treats.pack()
Frame_Canvas.pack(expand=True, fill=BOTH)
Frame_Apply.pack()
#######
######
Table_View = Canvas(Frame_Canvas,width=300,height=300,scrollregion=(0,0,500000,500000))
hbar = Scrollbar(Frame_Canvas,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=Table_View.xview)
vbar = Scrollbar(Frame_Canvas,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=Table_View.yview)
Table_View.config(width=300,height=300)
Table_View.config(xscrollcommand=hbar.set)
Table_View.pack(expand=True,fill=BOTH)

## button creating
Calc = Button(Frame_calc_example,bd=1,bg="light gray",fg="black",
              text="Calculate",padx=10,pady=2,command=Calc_Plants)
Calc.grid(row=4,column=6,sticky=N,pady=5,padx=0.5)
Apply_Button_Block = Button(Frame_Apply,bd=1,bg="white",fg="black",text="Block design / Re-Shuffle",
             padx=10,pady=5,command=Collect_Names_For_Blocks,height=2,width=18)
Apply_Button_Block.grid(row=0,column=0,padx=0,pady=0)

Apply_Button_Full_random = Button(Frame_Apply,bd=1,bg="white",fg="black",text="Full Random / Re-Shuffle",
                     padx=10,pady=5,command=Collect_Names_For_Full_Random,height=2,width=18)
Apply_Button_Full_random.grid(row=0,column=1)

Clear_Board = Button(Frame_Apply,bd=1,bg="white",fg="black",text="Clear Board",
             padx=10,pady=5,command=lambda :Table_View.delete("all"))
Clear_Board.grid(row=0,column=2)
######## botton from file
File_Apply_Button_Block = Button(Frame_Apply,bd=1,bg="lawn green",fg="black",text="File\n Block design / Re-Shuffle",
             padx=10,pady=5,command=Collect_Names_For_Blocks_file,height=2,width=18)  ### change to collect from file
File_Apply_Button_Block.grid(row=3,column=0,pady=10,padx=7.5)

File_Apply_Button_Full_random = Button(Frame_Apply,bd=1,bg="lawn green",fg="black",text="File\n Full Random / Re-Shuffle",
                     padx=10,pady=5,command=Collect_Names_For_Full_Random_file,height=2,width=18) ### change to collect from file
File_Apply_Button_Full_random.grid(row=3,column=1,padx=7.5)

Info_file_Button =Button(Frame_Apply,bd=1,bg="white",fg="black",text="Take me\nto my files",
                     padx=10,pady=5,command=Open_File_Directory) ### change to collect from file
Info_file_Button.grid(row=3, column=2)
####################################################################################
### cell creating #####
Box_width = 8
Factor1 = Label(Frame_calc_example,text="#Line")
Factor2 = Label(Frame_calc_example,text="#Treat")
Rep = Label(Frame_calc_example,text="#Repetition")
Summary = Label(Frame_calc_example,text="Sum of Sample")
Row_num = Label(Frame_calc_example,text="Number of rows")
Row_Letter = Label(Frame_calc_example,text="Table")

factor1_entry = Entry(Frame_calc_example,width=Box_width)
Factor2_entry = Entry(Frame_calc_example,width=Box_width)
Rep_entry = Entry(Frame_calc_example,width=Box_width)
Summary_entry = Entry(Frame_calc_example,width=Box_width,state='disabled')
Row_num_entry = Entry(Frame_calc_example,width=Box_width)
Row_letter_entry = Entry(Frame_calc_example,width=Box_width)

Top_Cell_distance = 10
Factor1.grid(row=3,column=0,sticky=N,padx=Top_Cell_distance)
Factor2.grid(row=3,column=1,sticky=N,padx=Top_Cell_distance)
Rep.grid(row=3,column=2,sticky=N)
Summary.grid(row=3,column=3,sticky=N)
Row_num.grid(row=3,column=4,sticky=N,padx=Top_Cell_distance)
Row_Letter.grid(row=3,column=5,sticky=N,padx=Top_Cell_distance)


factor1_entry.grid(row=4,column=0,sticky=W,padx=Top_Cell_distance)
Factor2_entry.grid(row=4,column=1,sticky=W,padx=Top_Cell_distance)
Rep_entry.grid(row=4,column=2,sticky=W,padx=Top_Cell_distance)
Summary_entry.grid(row=4,column=3,sticky=W,padx=Top_Cell_distance)
Row_num_entry.grid(row=4,column=4,sticky=W,padx=Top_Cell_distance)
Row_letter_entry.grid(row=4,column=5,sticky=W,padx=Top_Cell_distance)

#### first open explanation ######

#######Links ########

#link1 = Label(Table_View, text="Manual Download", fg="blue", cursor="hand2",anchor=CENTER)
#link1.pack()
#link1.bind("<Button-1>", lambda e: Open_Link("https://drive.google.com/open?id=1rvqGeSa9-de5NJs0ICY1tDuTNI__e5P2"))
link2 = Label(Table_View, text="YouTube Guide", fg="blue", cursor="hand2",anchor=CENTER)
link2.pack()
link2.bind("<Button-1>", lambda e: Open_Link("https://youtu.be/B_aKeMaB5yU"))

################################
global Text_X,Text_Y,win_width,Title_Design
win_width, win_height = Main_window.winfo_screenwidth(), Main_window.winfo_screenheight()
Text_X,Text_Y = win_width/2,win_height
Title_Design = win_width/10

Title = Table_View.create_text(Text_X, 100, text="A short explanation before you start", font=("Times bold", 15), fill='green',anchor=CENTER)
Title_under = Table_View.create_text(Text_X, 100, text="_______________________________", font=("Times bold", 15), fill='green',anchor=CENTER)
Text_1 = """1.Line - e.g.: Plants species, Soil type Genotype name\n2.Treat/Treatment - e.g, Irrigattion, Medium type, Droguht level, Control\n3.Repetition - the number of repetition you will have in each block(Relevant only for 'Block Design)"""
Table_View.create_text(Text_X, 150, text=Text_1, font=("Times bold", 15), fill='green')
#Table_View.create_text(177, 80, text="2. Treat - Irrigation, Drought, Control etc", font=("Times bold", 15), fill='green')
#Table_View.create_text(316, 105, text="3.Repetition - number of Repetition you will have (only for Block method)", font=("Times bold", 15), fill='green')

Table_View.create_text(Text_X, 200, text="Important Info", font=("Times bold", 15), fill='green')
Table_View.create_text(Text_X, 200, text="__________", font=("Times bold", 15), fill='green')
Table_View.create_text(Text_X, 235, text="1.Please read the manual and watch the video guide before using the program \n\t(Links to both are located at Top of the Screen)", font=("Times bold", 15), fill='green')
Table_View.create_text(Text_X-80, 280, text="2.The following sybols can not be used in the program\n\t"""
                                         " comma ',' underscore  '_'  dash '-' " ,font=("Times bold", 15), fill='red')

Table_View.create_text(Text_X-110, 330, text="""3.Please press the 'clear board' button in order to clear the cell""" ,font=("Times bold", 15), fill='green')

#print(win_width)
Main_window.state('zoomed')
Main_window.mainloop()

