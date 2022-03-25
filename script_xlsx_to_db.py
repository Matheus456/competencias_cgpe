import sqlite3
import pandas as pd

def insert_data(cur, df, table, model_fields, excel_header):
    for index, row in df.iterrows():
        rows = ()
        number_of_columns = len(model_fields.split(',')) - 1
        for value in excel_header:
            rows += (row[value], )
        cur.execute("INSERT OR IGNORE INTO " + table + " (" + model_fields + ") values(" + "?,"*number_of_columns + "?" + ")", 
                    (rows))    


xls = pd.ExcelFile('./arquivo_excel/competencias.xlsx')

df_areas = pd.read_excel(xls, 'areas')
df_colaboradores = pd.read_excel(xls, 'colaboradores')
df_soft_skills = pd.read_excel(xls, 'soft_skills')
df_hard_skills = pd.read_excel(xls, 'hard_skills')
df_colaborador_soft = pd.read_excel(xls, 'colaboradores_soft_skills')
df_colaborador_hard  = pd.read_excel(xls, 'colaboradores_hard_skills')
df_startup  = pd.read_excel(xls, 'startups')
df_sub_area  = pd.read_excel(xls, 'hierarquia_skills')

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

insert_data(cur, df_areas, "gestao_competencia_area", "id,nome", ["id_area", "nome_area"])
insert_data(cur, df_startup, "gestao_competencia_startup", "id,nome", ["id_startup", "nome_startup"])
insert_data(cur, df_sub_area, "gestao_competencia_subarea", "id,nome,area_id", ["id_hierarquia", "nome_hierarquia", "id_area"])
insert_data(cur, df_colaboradores, "gestao_competencia_colaborador", "id,nome, area_id, email, startup_id", ["id_colab", "nome_colab", "id_area", "email", "startup"])
insert_data(cur, df_soft_skills, "gestao_competencia_softskill", "id,nome,area_id", ["id_soft_skill", "nome_soft_skill", "id_area"])
insert_data(cur, df_hard_skills, "gestao_competencia_hardskill", "id,nome,area_id,subarea_id", ["id_hard_skill", "nome_hard_skill", "id_area", "id_hierarquia"])
insert_data(cur, df_colaborador_soft, "gestao_competencia_colaboradorsoftskill", "colaborador_id,soft_skill_id", ["id_colab", "id_soft_skill"])
insert_data(cur, df_colaborador_hard, "gestao_competencia_colaboradorhardskill", "colaborador_id,hard_skill_id", ["id_colab", "id_hard_skill"])

con.commit()
con.close()