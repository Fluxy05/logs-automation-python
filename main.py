import sys
import os



fichier_log = open("logA10.log")

line = fichier_log.readline()
nombre_de_lignes = len(line)

ip = []
user = []
date = []
Type = []
site = []

for line in fichier_log :
    split = line.split(" ")
    ip.append(split[0])
    user.append(split[2])
    date.append(split[3])
    Type.append(split[5])
    site.append(split[10])
    print(split[10])
print(ip)
fichier_log.close


if sys.platform == "linux" :
    os.system("cp header.txt main.html")
elif sys.platform == "win" :
    os.system("copy header.txt main.html")

html = open("main.html", "a")
html.write(" ")
html.write("<p>Hello</p>")
html.close