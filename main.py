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

for i in range (1, nombre_de_lignes) :
    line = fichier_log.readline()
    split = line.split(" ")
    ip.append(split[0])
    user.append(split[2])
    date.append(split[3])
    Type.append(split[5])
    site.append(split[10])
    print(split[10])
print(ip)

