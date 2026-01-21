import sys
import os


def ouverture() :
    emplacement_fichier = input("veuillez saisir l'emplacement du fichier de logs a ouvrir ex:(/emplacement/fichier/log): ")
    if emplacement_fichier == "" :
        ouverture()
    else :
        print(f"ouverture de {emplacement_fichier}")
        return(emplacement_fichier)

emplacement_fichier = ouverture()
fichier_log = open(emplacement_fichier)

line = fichier_log.readline()
nombre_de_lignes = len(line)

ip = []
user = []
date = []
Type = []
site = []
useragent = []

for line in fichier_log :
    split = line.split(" ")
    ip.append(split[0])
    user.append(split[2])
    date.append(split[3])
    Type.append(split[5])
    if len(split[10]) < 4 :
        print(f"erreur de lecture ligne du site visiter dans une ligne, ceci peux etre du a une requete sans url et etre ignorer")
    else :
        site.append(split[10])
    useragent.append(f"{split[11]}{split[12]}")

fichier_log.close

def filtre_site(site_input):
    temp = []
    filt = []
    for i in range(len(site_input)) :
        domain = site_input[i].split("/")
        temp.append(domain[2])
    
    for i in range(len(temp)):
        dom = temp[i].split(".")
        if dom[0] == "www" :
            filt.append(f"{dom[1]}.{dom[2]}")
        else :
            filt.append(temp[i])
    return(filt)

def site_visiter(site_filtré):
    sitevisiter = list(set(site_filtré))
    return(sitevisiter)

def comptage_sitevisité(site_visiter_input, sitefiltré_input):
    compte = []
    for l in range(len(site_visiter_input)):
        compte.append(0)

    for i in range(len(sitefiltré_input)):
        for y in range(len(site_visiter_input)):
            if sitefiltré_input[i] == sitefiltré_input[y]:
                compte[y] = compte[y] + 1
    return(compte)

sitefiltré = filtre_site(site)

liste_site_visiter = site_visiter(sitefiltré)



def comptage_user_agent(useragent_input):
    result = []
    opera_win = 0
    opera_lin = 0
    firefox_win = 0
    firefox_lin = 0
    firefox_android = 0
    firefox_apple = 0
    other = 0
    for i in range(len(useragent_input)):
        if useragent_input[i] == '"Mozilla/5.0(X11;' :
            firefox_lin = firefox_lin + 1
        elif useragent_input[i] == '"Mozilla/5.0(Android' :
            firefox_android = firefox_android + 1
        elif useragent_input[i] == '"Mozilla/5.0(compatible;' or useragent_input[i] == '"Mozilla/5.0(Windows;' :
            firefox_win = firefox_win + 1
        elif useragent_input[i] == '"Mozilla/5.0(Macintosh;' :
            firefox_apple = firefox_apple + 1
        elif useragent_input[i] == '"Opera/8.28.(X11;Linux' :
            opera_lin = opera_lin + 1
        elif useragent_input[i] == '"Opera/9.37.(WindowsNT' :
            opera_win = opera_win + 1
        else :
            other = other + 1
    result.append(opera_win)
    result.append(opera_lin)
    result.append(firefox_win)
    result.append(firefox_lin)
    result.append(firefox_android)
    result.append(firefox_apple)
    result.append(other)
    return(result)
    



def filtre_user(user) :
    user = list(set(user))
    return user


def nombre_de_requete_user(testuser) :
    temp = 0
    for i in range(len(user)) :
        if user[i] == testuser :
            temp = temp + 1
    return temp

def liste_requete_user(user_filtré) :
    tab = []
    for i in range(len(user_filtré)) :
        tab.append(nombre_de_requete_user(user_filtré[i]))
    return tab


fichier_log.close

html_contenu = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Résumer logs Proxy web</title>
    <link rel="stylesheet" href="main.css">
</head>
<body>
    <div class="dashboard-container">
    <div style="width: 600px;">
        <canvas id="Graphique_requetes_user"></canvas>
    </div>
    <div style="width: 600px;">
        <p>navigateurs les plus utilisés</p>
        <canvas id="Graphique_navigateur"></canvas>
    </div>
    <div style="width: 600px;">
        <p>sites les plus visités</p>
        <canvas id="Graphique_site"></canvas>
    </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            new Chart(document.getElementById("Graphique_requetes_user"), {{
                type: "line",
                data: {{
                    labels: {filtre_user(user)},
                    datasets: [{{
                        label: "nombre de requetes par cette utilisateur",
                        data: {liste_requete_user(filtre_user(user))},
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    position: 'top',
                    title: {{
                        display: true,
                        text: "Graphique du nombre de requetes par cette utilisateur",
                        color: 'white'
                    }}
                }}
            }});
        </script>
        <script>
            new Chart(document.getElementById("Graphique_navigateur"), {{
                type: 'doughnut',
                data: {{
                    labels: {["opera_windows", "opera_linux", "firefox_windows", "firefox_linux", "firefox_android", "firefox_apple", "other"]},
                    datasets: [{{
                        label: "navigateur les plus utilisée par requetes",
                        data: {comptage_user_agent(useragent)},
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    position: 'top',
                    title: {{
                        display: true,
                        text: "Nombre de requetes :"
                    }}
                }}
            }});
        </script>
        <script>
            new Chart(document.getElementById("Graphique_site"), {{
                type: 'doughnut',
                data: {{
                    labels: {liste_site_visiter},
                    datasets: [{{
                        label: "site les plus visiter",
                        data: {comptage_sitevisité(liste_site_visiter, sitefiltré)},
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    position: 'top',
                    title: {{
                        display: true,
                        text: "nombre de visite"
                    }}
                }}
            }});
        </script>

</body>
</html>"""

html = open("main.html", "w")
print("ecriture du fichier html ...")
html.writelines(html_contenu)
html.close()
print("Analyse terminer !")

#tentative d'ouverture avec navigateur par defaut :
def q_ouvrire_fichier() :
    ouverture = input("Ouvrir le htlm (y/n): ")
    if ouverture == "y" :
        if os.name == 'nt' :
            print("win detecter tentative d'ouverture")
            os.system(f'start {fichier_html}')
        elif os.name == 'posix' and os.uname().sysname == 'Darwin':
            print("MacOS detecter tentative d'ouverture")
            os.system(f'open {fichier_html}')
        else:
            print("Linux/BSD detecter, tentative d'ouverture avec xdg")
            os.system(f'xdg-open {fichier_html}')
    elif ouverture == "n" :
        print("vous devrez ouvrir main.html par vous meme")
    else:
        q_ouvrire_fichier()


fichier_html = "main.html"
q_ouvrire_fichier()

