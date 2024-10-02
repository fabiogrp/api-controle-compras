from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date
import datetime
import calendar
from fastapi.responses import JSONResponse
import sqlite3
import peewee
import json
#import Compra

class Compra (BaseModel):
    data_compra: Optional[date]
    valor_compra: float
    qtd_parcelas: Optional[int]
    descricao: str
    id_usuario: int
#--------------------------------------------------------------

conn = sqlite3.connect('comprasCartao.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
dia_fechamento_fatura = 4


def get_proximo_mes(data):
    #converter string em data
    partes_data =  str(data).split('-')
    ano = int(partes_data[0])
    mes = int(partes_data[1])
    dia = int(partes_data[2])
    data = datetime.date(ano, mes, dia)
    
    #Obtendo a quantidade de dias para o final do mês
    ultimo_dia_mes = calendar.monthrange(data.year, data.month)[1]
    dias_final_mes = datetime.timedelta(ultimo_dia_mes - data.day + 1)
    #Somando a quantidade de dias restantes com a data atual
    proximo_mes = data + dias_final_mes
    return proximo_mes


app = FastAPI()


@app.get("/")
async def root():
    #return JSONResponse(content = {"message": "Hello World!!!"})
    return {"message": "Hello World!!!"}

@app.get("/users/{id}")
async def get_users(id):

    cursor.execute("SELECT * FROM usuario WHERE id = ?", id)
    usuario = cursor.fetchone()
    print(usuario)
    #return JSONResponse(content = usuario)
    return usuario

@app.get("/users")
async def get_users():
    cursor.execute("SELECT id,nome FROM usuario")
    lista_usuarios = cursor.fetchall()
    return lista_usuarios

@app.get("/compra/{id}/{mes}")
async def get_compra_usuario(id, mes):
    cursor.execute("SELECT data_compra, valor_parcela, parcela, qtd_parcelas, descricao FROM compras JOIN parcela ON parcela.id_compra = compras.id WHERE id_usuario = ? AND mes_fatura = ? ORDER BY data_compra DESC", (id, mes))
    compras = cursor.fetchall()
    #return JSONResponse(content = {"compras":compras})
    #return {"compras":compras}
    return compras

@app.get("/compra")
async def get_all_compras():
    return "Caiu na get_all_compras"


@app.post("/compra", status_code = 201)
async def save_compra(compra: Compra):
    if not compra.data_compra:
        compra.data_compra = str(datetime.date.today())
        
    if not compra.qtd_parcelas:
        compra.qtd_parcelas = 1
    
    cursor.execute("INSERT INTO compras (data_compra, valor_compra, descricao, id_usuario, qtd_parcelas) VALUES(?, ?, ?, ?,?)", (compra.data_compra, compra.valor_compra, compra.descricao, compra.id_usuario, compra.qtd_parcelas))
    conn.commit()

    cursor.execute("SELECT last_insert_rowid()")
    ultimo_id = cursor.fetchone()
    id_compra = ultimo_id[0]
    data_compra = str(compra.data_compra)
    mes_fatura = data_compra
       
    for i in range(1, int(compra.qtd_parcelas) + 1):
        valor_parcela = float(compra.valor_compra) / int(compra.qtd_parcelas)   
        if i > 1:
            mes_fatura = get_proximo_mes(mes_fatura)
        else:
            if int(data_compra[8:]) >= dia_fechamento_fatura:
                mes_fatura = get_proximo_mes(mes_fatura)
            
        cursor.execute("INSERT INTO parcela (id_compra, parcela, valor_parcela, mes_fatura) VALUES(?, ?, ?, ?)",(id_compra, i, valor_parcela, str(mes_fatura)[:7]))
        
    conn.commit()
    
    return compra
    #return JSONResponse(content = {"compras": "compras"})

    @app.post("/compra_teste", status_code = 201)
    async def compra_teste(compra: Compra):

        
        if not compra.data_compra:
            compra.data_compra = str(datetime.date.today())
        
        if not compra.qtd_parcelas:
            compra.qtd_parcelas = 1

        return "compra"
    



