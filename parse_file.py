from tkinter import filedialog
from scrape_logs import get_wlogs
from database_gestion import update_documents_in_db


def create_dict_list(dict_arr, lua_content):
    brace_count = 0
    for line in lua_content:
        #get values
        if brace_count == 1:
            Server_name = (line.replace('"', '').replace('=', '').replace('[', '').replace(']', '').replace('{', '').strip()).split('_')[1]
        if brace_count == 2:
            Faction_name = line.replace('"', '').replace('=', '').replace('[', '').replace(']', '').replace('{', '').strip()
        if brace_count == 3:
            Race_name = line.replace('"', '').replace('=', '').replace('[', '').replace(']', '').replace('{', '').strip()
        if brace_count == 4:
            Class_name = line.replace('"', '').replace('=', '').replace('[', '').replace(']', '').replace('{', '').strip()
        if brace_count == 5:
            Player_name = line.replace('"', '').replace('=', '').replace('[', '').replace(']', '').replace('{', '').strip()
        if brace_count == 6 and "[1]" in line:
            Player_level = int(line.split(',')[0].strip())
        if brace_count == 6 and "[2]" in line:
            Guild_name = line.split(',')[0].replace('"', '').strip()

        #brace_count effects
        if brace_count > 0 and "{" in line:
            brace_count += 1
        if brace_count > 0 and "}" in line:
            if brace_count == 2:
                brace_count -= 2
            else:
                brace_count -= 1
        if "Servers" in line:
            brace_count += 1
        if brace_count < 1:
            continue

        #skipping useless informations
        if "[3]" in line or "[4]" in line or "[5]" in line:
            continue

        #push dict in data
        if brace_count == 6 and "[2]" in line:
            player_dict = {
                'Nom du joueur': Player_name,
                'Serveur': Server_name,#.split('_')[1],
                'Faction': Faction_name,
                'Race': Race_name,
                'Level': Player_level,
                'Guilde': Guild_name,
                'Classe': Class_name,
               'Main_spe': '',
               'lvl_spe': 0
            }
            dict_arr.append(player_dict)

# Fonction pour uploader le fichier .lua et insérer son contenu dans la base de données
def upload_lua_file():
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers Lua", "*.lua")])
    if file_path:
        with open(file_path, 'r', encoding='utf8') as lua_file:
            lua_content = lua_file.readlines()
            dict_arr = []
            create_dict_list(dict_arr, lua_content)
            get_wlogs(dict_arr)
            print(dict_arr)
            update_documents_in_db(dict_arr)