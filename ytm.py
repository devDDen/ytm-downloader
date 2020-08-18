#!/usr/bin/env python
import os
import requests
import time
import sys

def download_youtubedl():
    if os.name == "nt":
        if not(os.path.exists("ytd.exe")):
            durl = "https://youtube-dl.org/downloads/latest/youtube-dl.exe"
            r = requests.get(durl, allow_redirects=True)
            open('ytd.exe', 'wb').write(r.content)
    else:
        if not(os.path.exists("ytd")):
            durl = "https://youtube-dl.org/downloads/latest/youtube-dl"
            r = requests.get(durl, allow_redirects=True)
            open('ytd', 'wb').write(r.content)
        
def use_ytdl_p(url):
    if os.name == "nt":
        os.system("ytd.exe -f bestaudio -i -o %(playlist_title)s/%(title)s.%(ext)s " + url)
    else:
        os.system("python ytd -f bestaudio -i -o '%(playlist_title)s/%(title)s.%(ext)s' " + url)
    
def use_ytdl(url):
    if os.name == "nt":
        os.system("ytd.exe -f bestaudio -i -o %(title)s.%(ext)s " + url)
    else:
        os.system("python ytd -f bestaudio -i -o '%(title)s.%(ext)s' " + url)
        
def editpath(defpath):
    global path
    if defpath == "":
        path = os.getcwd() + "/"
    else:
        if defpath[len(path)-1]!="/":
            path += "/"

def dirlist(path):
    pathlist=[]
    for fileName in os.listdir(path):
        if os.path.isdir(path+fileName):
            pathlist.extend(dirlist(path+fileName+"/"))
        else:
            pathlist.append(path+fileName)
    return pathlist
            
def convertToMp3(fileName):  
    if os.name == "nt":
        os.system("ffmpeg.exe -i " + '"' + fileName +  '" ' + '"' + fileName[:str.rfind(fileName,".")] + '.mp3"')
    else:
        os.system("ffmpeg -i " + '"' + fileName +  '" ' + '"' + fileName[:str.rfind(fileName,".")] + '.mp3"')

def lconvertToMp3(fileName):  
    if os.name == "nt":
        os.system("ffmpeg.exe -i " + '"' + fileName +  '" ' + '"' + fileName[:str.rfind(fileName,"/")] + str.lower(fileName[str.rfind(fileName,"/"):str.rfind(fileName,".")]) + '.mp3"') 
    else:
        os.system("ffmpeg -i " + '"' + fileName +  '" ' + '"' + fileName[:str.rfind(fileName,"/")] + str.lower(fileName[str.rfind(fileName,"/"):str.rfind(fileName,".")]) + '.mp3"')

    
def checkffmpeg(path):
    if os.name == "nt":
        if not(os.path.exists(path + "ffmpeg.exe")):
                print("Download and put ffmpeg.exe into this folder. You can download ffmpeg.exe here: https://cloud.mail.ru/public/4swb/3T3VJ4srN")
        
def args(args, urls):
    global convert
    global delorig
    global lowreg
    for x in args:
        if "http" in x:
            if "&" in x:
                urls.append(x[:str.find(x, "&")])
            else:
                urls.append(x)
        if "-path=" in x:
            os.chdir(x[str.find(x, "=")+1:])
        if "-convert=" in x:
            print(x[str.find(x, "=")+1:])
            convert = x[str.find(x, "=")+1:]
        if "-delorig=" in x:
            delorig = x[str.find(x, "=")+1:]
        if "-lowreg=" in x:
            lowreg = x[str.find(x, "=")+1:]

convert="T"
delorig="T"
lowreg="F"
path=""
pathlist=[]
pathlist1=[]
pathlist2=[]
urls=[]

args(sys.argv, urls)
editpath(path)

download_youtubedl()

pathlist1 = dirlist(path)

for x in urls:
    if "playlist" in x or "channel" in x:
        use_ytdl_p(x)
    else:
        use_ytdl(x)
        
pathlist2 = dirlist(path)

for y in pathlist2:
    if not(y in pathlist1):
        pathlist.append(y)
        
for z in pathlist:
    z.replace(" ", "$20")
        
if convert=="T":
    checkffmpeg(path)
    for x in pathlist:
        print(x)
        if lowreg=="T":
            lconvertToMp3(x)
        else:
            convertToMp3(x)
        
for z in pathlist:
    z.replace("$20", " ")
        
if delorig=="T":
    for x in pathlist:
        os.remove(x)