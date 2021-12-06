import sqlite3
import pandas as pd

# Acessando xlsx
xls = pd.ExcelFile('competencias.xlsx')

# Separando em dataframes
df_areas = pd.read_excel(xls, 'areas')
df_colaboradores = pd.read_excel(xls, 'colaboradores')
df_soft_skills = pd.read_excel(xls, 'soft_skills')
df_hard_skills = pd.read_excel(xls, 'hard_skills')
df_colaborador_soft = pd.read_excel(xls, 'colaboradores_soft_skills')
df_colaborador_hard  = pd.read_excel(xls, 'colaboradores_hard_skills')

# Conectando com o banco
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

for index, row in df_areas.iterrows():
    cur.execute("INSERT OR IGNORE INTO gestao_competencia_area (id,nome) values(?,?)", 
                (row['id_area'], row['nome_area']))

for index, row in df_colaboradores.iterrows():
    cur.execute("INSERT OR IGNORE INTO gestao_competencia_colaborador (id,nome, area_id, email) values(?,?,?,?)", 
                (row['id_colab'], row['nome_colab'], row['id_area'], row['email']))    

for index, row in df_soft_skills.iterrows():
    cur.execute("INSERT OR IGNORE INTO gestao_competencia_softskill (id,nome, area_id) values(?,?,?)", 
                (row['id_soft_skill'], row['nome_soft_skill'], row['id_area']))    

for index, row in df_hard_skills.iterrows():
    cur.execute("INSERT OR IGNORE INTO gestao_competencia_hardskill (id,nome, area_id) values(?,?,?)", 
                (row['id_hard_skill'], row['nome_hard_skill'], row['id_area']))    

for index, row in df_colaborador_soft.iterrows():
    cur.execute("INSERT OR IGNORE INTO gestao_competencia_colaboradorsoftskill (colaborador_id,soft_skill_id) values(?,?)", 
                (row['id_colab'], row['id_soft_skill']))    

for index, row in df_colaborador_hard.iterrows():
    cur.execute("INSERT OR IGNORE INTO gestao_competencia_colaboradorhardskill (colaborador_id,hard_skill_id) values(?,?)", 
                (row['id_colab'], row['id_hard_skill']))    


con.commit()
con.close()