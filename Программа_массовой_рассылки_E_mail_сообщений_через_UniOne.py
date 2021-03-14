#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, json, base64
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class FrOpenFile(LabelFrame):
    lLabel : Label
    lNameFile : Entry
    lFileSelect : Button

    def __init__(self, parent):
        LabelFrame.__init__(self, parent)
        self.parent = parent
        self.init_set()

    def init_set(self):
        self["height"] = 47
        self.lLabel = Label(self, text=" Имя файла . . ")
        self.lNameFile = Entry(self)
        self.lFileSelect = Button(self, text="...")

    def update_set(self):
        self.update()
        ms_width = self.winfo_width()
        self.lLabel.place(x=1,y=1)
        self.lFileSelect.place(x=ms_width-35,y=1,width=20,height=20)
        self.update()
        self.lNameFile.place(x=self.lLabel.winfo_width()+20,y=1,width=ms_width-self.lLabel.winfo_width()-57)

class FrMain(Frame):
    StrOpenFileHTML = " "           # Х/З
    LabelUserId: Label              # значение "api_key" клиента отправителя на портале UneOne
    StrUserId: Entry                # значение "api_key" клиента отправителя на портале UneOne
    LabelFromEmailName : Label      # 
    EntryFromEmailName : Entry      # E-mail отправителя (от имени какого ящика отправляется письмо)
    LabelFromEmailText : Label      #
    EntryFromEmailText : Entry      # Имя (насменование) от чьего имени отправляется письмо
    LabellSubject : Label           #
    StrlSubject : Entry             # Темя собщения
    FrOpenFileHTML : FrOpenFile     # Имя файла HTML в котором хранится текст сообщения
    FrOpenFileEmail : FrOpenFile    # Текстовый файл (.txt) котором хранится список E-mail на которые будет отправлено сообщение
    LabelTitle : Label              #
    ButtonTitle : Button            # 
    StrTitle : Text                 # Список Файлов вложений
    ButtonOk : Button               # Кнопка ОК (отправить)
    ButtonESC : Button              # Кнопка Отменить

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_set()

    def init_set(self):
        self.parent.title("Программа массовой рассылки E-mail уведомлений через UniOne.io ")
        self.pack(fill=BOTH, expand=1)
        self.update()
        self.LabelUserId = Label(self, text='Код "api_key" . . ')
        self.LabelUserId.place(x=5, y=10)
        self.StrUserId = Entry(self)
        self.StrUserId.insert(0, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.StrUserId.place(x=200, y=10, width=730)
        self.LabelFromEmailName = Label(self, text="E-mail отправителя . . ")
        self.LabelFromEmailName.place(x=5,y=35)
        self.EntryFromEmailName = Entry(self)
        self.EntryFromEmailName.place(x=200,y=35,width=730)
        self.EntryFromEmailName.insert(0,"E-mail@Email.ru")
        self.LabelFromEmailText = Label(self, text="Наименование отправителя . . ")
        self.LabelFromEmailText.place(x=5,y=60)
        self.EntryFromEmailText = Entry(self)
        self.EntryFromEmailText.place(x=200,y=60,width=730)
        self.EntryFromEmailText.insert(0,"От чьего имени отправить сообщение ")
        self.LabellSubject = Label(self, text="Тема сообщения . . ")
        self.LabellSubject.place(x=5,y=85)
        self.StrlSubject = Entry(self)
        self.StrlSubject.insert(0,"Тема E-mail сообщения")
        self.StrlSubject.place(x=200,y=85,width=730)
        self.FrOpenFileHTML = FrOpenFile(self)
        self.FrOpenFileHTML["text"] = "Текст сообщения HTML файл (*.html) . . "
        self.FrOpenFileHTML.lNameFile.insert(0, "C:/*.html")
        self.FrOpenFileHTML.place(x=5,y=110,width=self.winfo_width()-10)
        self.FrOpenFileHTML.lFileSelect.configure(command=self.selectnamefilehtml)
        self.FrOpenFileHTML.update_set()
        self.FrOpenFileHTML.update()
        self.FrOpenFileEmail = FrOpenFile(self)
        self.FrOpenFileEmail["text"] = "Текстовый файл со списком E-mail (*.txt) . . "
        self.FrOpenFileEmail.lNameFile.insert(0, "C:/*.txt")
        self.FrOpenFileEmail.place(x=5, y=160, width=self.winfo_width() - 10)
        self.FrOpenFileEmail.lFileSelect.configure(command=self.selectnamefileemail)
        self.LabelTitle = Label(self, text='Список вложений . . ')
        self.LabelTitle.place(x=5,y=215)
        self.ButtonTitle = Button(self, text = "Добавить Вложение",command=self.selectnamefileall)
        self.ButtonTitle.place(x=800,y=210,width=140)
        self.StrTitle = Text(self)
        self.StrTitle.place(x=5, y=240, width=940, height = 320)
        self.ButtonESC = Button(self, text="Отменить", command=self.quit)
        self.ButtonESC.place(x=855,y=620,width=90)
        self.ButtonOK = Button(self, text="OK", command=self.sendmessage)
        self.ButtonOK.place(x=765, y=620, width=90)
        self.FrOpenFileEmail.update_set()
        self.FrOpenFileEmail.update()

    def selectnamefileall(self):
        StrOpenFile = filedialog.askopenfile(filetypes=(("All files", "*.*"), ("All files", "*.*")))
        if StrOpenFile is None:
            StrName = ""
        else:
            StrName = StrOpenFile.name+"\n"
            self.StrTitle.insert("1.0",StrName)
        StrOpenFile.close()


    def selectnamefilehtml(self):
        self.StrOpenFileHTML = filedialog.askopenfile(filetypes=(("HTML files", "*.html"), ("HTML files", "*.htm")))
        if self.StrOpenFileHTML is None:
            self.FrOpenFileHTML.lNameFile.delete(0, END)
            self.FrOpenFileHTML.lNameFile.insert(0,"C:/*.html" )
        else:
            StrName = self.StrOpenFileHTML.name
            self.FrOpenFileHTML.lNameFile.delete(0,END)
            self.FrOpenFileHTML.lNameFile.insert(0,StrName)
        self.StrOpenFileHTML.close()

    def selectnamefileemail(self):
        self.StrOpenFileEmail = filedialog.askopenfile(filetypes=(("TXT files", "*.txt"), ("TXT files", "*.txt")))
        if self.StrOpenFileEmail is None:
            self.FrOpenFileEmail.lNameFile.delete(0, END)
            self.FrOpenFileEmail.lNameFile.insert(0, "C:/*.txt")
        else:
            StrName = self.StrOpenFileEmail.name
            self.FrOpenFileEmail.lNameFile.delete(0, END)
            self.FrOpenFileEmail.lNameFile.insert(0, StrName)
        self.StrOpenFileEmail.close()

    def sendmessage(self):
        lSpFileName = []  #Список файлов которые необходимо вставить во вложения
        lSpFileName1 = []  #Список файлов которые необходимо вставить во вложения
        lApiKey = self.StrUserId.get()
        lSubject = self.StrlSubject.get() # Тема E-mail письма
        lFileHTMLName = self.FrOpenFileHTML.lNameFile.get() # Имя файла текста письма в HTML
        lFileEmailName = self.FrOpenFileEmail.lNameFile.get() # Имя текстового файла с E-mail адресами
        lFromEmailName = self.EntryFromEmailName.get() #E-mail адрес ящика отправки
        lFromEmailNameReply = self.EntryFromEmailName.get()  # E-mail адрес ящика отправки
        lFromEmailNameТехт = self.EntryFromEmailText.get()  # Отображаемое имя E-mail адрес ящика отправки
        lFragErorr = 1
        lStrError = ''
        lSpFlagError = [lApiKey == '' or lApiKey == 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', lFileHTMLName == 'C:/*.html' or lFileHTMLName == '', lFileEmailName == 'C:/*.txt' or lFileEmailName == '', lFromEmailName =='E-mail@Email.ru' or lFromEmailName =='']
        lSpTeteError = ['Не корректный <lApiKey>',  'Не корректно указано имя файла HTML', 'Не корректно указано имя файла E-mail', 'Не корректно указано E-mail отправителя']
        for i in [0,1,2,3]:
            if lSpFlagError[i]: lStrError = lStrError+str(lSpTeteError[i])+'\n'
        if lStrError == '': lFragErorr = 0
        else: messagebox.showinfo('Внимание ОШИБКА !', lStrError)
        if lFragErorr == 0:
            lNameSends = self.StrTitle.get("1.0",END)[0:-2] # Преобразуем данные из Text в Список
            lSpFile = lNameSends.split('\n')
            lSpFileLen = len(lSpFile)
            li = 0
            while li < lSpFileLen:
                lSpFileName1 = []
                lStr = lSpFile[li]
                lSpFileName1.append(lStr[0:lStr.rfind('/')+1:])
                lSpFileName1.append(lStr[lStr.rfind('/')+1::])
                lSpFileName1.append(lStr[lStr.rfind('.')+1::][0:3:])
                lSpFileName.append(lSpFileName1)
                li = li+1
            lcUrl = "https://eu1.unione.io/ru/transactional/api/v1/email/send.json"  # Url-адрес сервера для отправки POST-запроса
            lFileLogName = lFileEmailName[0:-4:] + ".log"  # Имя Log-файла
            lFileDoc = open(lFileHTMLName, "r")  # Открываем файл в котором лежит HTML-страница письма
            lcPostHtmlText = lFileDoc.read()  # Сохраняем содержимое письма в переменную
            lFileDoc.close()  # Закрываем файл
            lSpInd = len(lSpFileName)  # Определяем длинну списка описывеющего вложения
            i = 0  # Обнуляем номер индекса вложения
            ljAttachments = []  # Создаем пустой список вложений
            while i < lSpInd:  # Запускаем цикл перебора списка описывающего вложения и формируем список вложений
                lfType = "text/" + lSpFileName[i][2]
                lfName = lSpFileName[i][1]
                lFileDoc = open(lSpFileName[i][0]+lSpFileName[i][1], 'rb')
                lBase64Str = str(base64.b64encode(lFileDoc.read()))
                lFileDoc.close()
                lfContent = lBase64Str[2:-1:]
                lfAll = {
                    "type": lfType,
                    "name": lfName,
                    "content": lfContent
                    }
                ljAttachments.append(lfAll)
                i = i + 1
            lcLogFile = open(lFileLogName, "w")
            for lcEmail in open(lFileEmailName, "r"):
                lcEmailStr = lcEmail.rstrip()
                lcPostStr = {
                    "api_key": lApiKey,
                    "message":
                        {
                            "template_engine": "simple",
                            "global_substitutions":
                                {
                                    "someVar": "some val"
                                },
                            "global_metadata":
                                {
                                    "key1": "val1"
                                },
                            "body":
                                {
                                    "html": lcPostHtmlText,
                                    "plaintext": "",
                                    "amp": "<!doctype html><html amp4email><head> <meta charset=\"utf-8\"><script async src=\"https://cdn.ampproject.org/v0.js\"></script> <style amp4email-boilerplate>body{visibility:hidden}</style></head><body> Hello, AMP4EMAIL world.</body></html>"
                                },  
                            "subject": lSubject,
                            "from_email": lFromEmailName,
                            "from_name": lFromEmailNameТехт,
                            "reply_to": lFromEmailNameReply,
                            "track_links": 1,
                            "track_read": 1,
                            "recipients": [
                                {
                                    "email": lcEmailStr,
                                    "substitutions":
                                        {
                                            "substitutionName": "substitutionVal",
                                            "UNSUB_hash": "Qwcd1789"
                                        }
                                }
                            ],
                            "headers":
                                {
                                    "X-MyHeader": "some_useful_data"
                                },
                            "attachments": ljAttachments,
                            "options":
                                {
                                    "unsubscribe_url": "someurl"
                                }
                        }
                }
                lcUrlPost = requests.post(lcUrl, data=json.dumps(lcPostStr))
                lcLogText = str(lcUrlPost.status_code) + "=>" + lcEmailStr + "  \n"
                print(lcLogText[0:-2:])
                lcLogFile.write(lcLogText)
            lcLogFile.close()
            sys.exit()

def СheckingError():
    
    return lFragErorr

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))



def main():
    root = Tk()
    root.geometry("950x650+300+300")
    app = FrMain(root)
    center(root)
    root.mainloop()

if __name__ == '__main__':
    main()

