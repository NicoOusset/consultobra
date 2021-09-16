import os
from flask import Flask, request, jsonify
from datetime import datetime
import pymysql
import pandas as pd
import numpy as np
 
app = Flask(__name__)
db = pymysql.connect(host='localhost',
                    user='root',
                    password='',
                    db='consultobra')

@app.route('/guardarExcel', methods=['POST'])
def guardarExcel():

    try:
        files = request.files.getlist('file')
        filename = 'datosConsultobra.xlsx'
        
        for file in files:
                filename = 'datosConsultobra.xlsx'
                print(filename)
                file.save(os.path.join('', filename))
        
        leerExcel(filename)

    except Exception as e:        
        return jsonify({'result':'Error al guardar el Excel: '+str(e)})
   
    return jsonify({'result':'success'})


def leerExcel(nombreExcel):
    rubrosCargados = []
    df1 = pd.read_excel(nombreExcel, sheet_name="Hoja1")
    df = df1.replace(np.nan, '', regex=True)

    for index, row in df.iterrows():
        # print(row['RUBROS'], row['ÍTEMS'], row[0])
        # ---- Rubro ----
        idRubro = row[0]
        NombreRubro = row[1]

        # ---- Item ----
        IdItem = row[2]        
        NombreItem = row[3]
        Unidad = row[4]
        Materiales = row[5]
        Obreros = row[6]
        Herramental = row[7]
        Cargas_sociales = row[8]
        Comentario = row[9]
        Oficial_especializado = row[10]
        Oficial = row[11]
        Medio_oficial = row[12]
        Ayudante = row[13]
        ItemActivo = row[14]

        if Oficial_especializado == "":
            Oficial_especializado=0

        if Oficial == "":
            Oficial=0 

        if Medio_oficial == "":
            Medio_oficial=0

        if Ayudante == "":
            Ayudante=0 
       
        flag = True
        if not rubrosCargados:
            for r in rubrosCargados:
                if(idRubro == r[0]):
                    flag=False

        if(flag):
            rubrosCargados.append(idRubro)
            cargarRubroDesdeExcel(idRubro, NombreRubro, 'Si')

        cargarItemDesdeExcel(IdItem,NombreItem,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,Oficial_especializado,Oficial,Medio_oficial,Ayudante,idRubro, ItemActivo)
    
    print("Carga de datos finalizada")


def cargarRubroDesdeExcel(id, nombre, activo):

    try:
        cursor=db.cursor()
        sql = (" SELECT * FROM rubros " + 
               " WHERE Id = %s ")
        tupla=(id)
        cursor.execute(sql,tupla)
        rubro=cursor.fetchone()

        if not rubro:
            sql1 = (" INSERT INTO rubros " + 
                    " VALUES (%s,%s,%s) ")
            tupla1=(id, nombre, activo)
            cursor.execute(sql1,tupla1)
        else:
            sql1 = (" UPDATE rubros SET Nombre=%s, Activo=%s " + 
                    " WHERE Id = %s ")
            tupla1=( nombre, activo, id)
            cursor.execute(sql1,tupla1)

        db.commit()
        cursor.close()
        
    except Exception as e:        
        return str(e)

    return 'Rubro registrado correctamente'


def cargarItemDesdeExcel(IdItem,NombreItem,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,Oficial_especializado,Oficial,Medio_oficial,Ayudante,RubroId,ItemActivo):

    try:
        cursor=db.cursor()
        sql = (" SELECT * FROM items " + 
               " WHERE Id = %s ")
        tupla=(IdItem)
        cursor.execute(sql,tupla)
        item=cursor.fetchone()

        if not item:
            sql1 = (" INSERT INTO items (Id,Nombre,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,Oficial_especializado,Oficial,Medio_oficial,Ayudante,RubroId,Activo) " + 
                    " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s")
            tupla1=(IdItem, NombreItem,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,Oficial_especializado,Oficial,Medio_oficial,Ayudante,RubroId,ItemActivo)
            cursor.execute(sql1,tupla1)
        else:
            sql1 = (" UPDATE items SET Nombre=%s, Unidad=%s, Materiales=%s, Obreros=%s, Herramental=%s, Cargas_sociales=%s, Comentario=%s, Oficial_especializado=%s, Oficial=%s, Medio_oficial=%s, Ayudante=%s, RubroId=%s , Activo=%s " + 
                    " WHERE Id = %s ")
            tupla1=(NombreItem,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,Oficial_especializado,Oficial,Medio_oficial,Ayudante,RubroId,ItemActivo,  IdItem)
            cursor.execute(sql1,tupla1)

        db.commit()
        cursor.close()
        
    except Exception as e:   
        print(str(e))     
        return str(e)

    return 'Rubro registrado correctamente'


@app.route('/buscarRubros', methods=['POST'])
def buscarRubros():

    try:
        cursor=db.cursor()                
        sql = (" SELECT r.Id, r.Nombre FROM rubros r " + 
               " WHERE r.Activo = 'Si' ")       
        cursor.execute(sql)
        rubrosBusqueda = cursor.fetchall()
        cursor.close()

        cantidadRubros=0
        rubros=[]
        for i in rubrosBusqueda:
            elemento = {}            
            elemento['Id'] = i[0]
            elemento['Nombre'] = i[1]
            rubros.append(elemento)      
            cantidadRubros=cantidadRubros+1
        
    except Exception as e:        
        return jsonify({'result':'Error al buscar rubros: '+str(e)})
    
    return jsonify({'result':'success', 'rubros':rubros, 'cantidad de rubros': cantidadRubros})


@app.route('/buscarItems', methods=['POST'])
def buscarItems():
    
    try:
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM items FROM consultobra;"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)        
        columnasItem.append("Nombre_Rubro")
        
        sql = (" SELECT i.*, r.Nombre FROM items i INNER JOIN rubros r " + 
               " ON i.RubroId = r.Id")       
        cursor.execute(sql)
        itemsBusqueda = cursor.fetchall()
        cursor.close()

        cantidadItems=0
        items=[]
        for i in itemsBusqueda:
            elemento = {}
            for index in range(len(columnasItem)):
                elemento[columnasItem[index]] = i[index]
            items.append(elemento)      
            cantidadItems=cantidadItems+1
        
    except Exception as e:        
        return jsonify({'result':'Error al buscar items: '+str(e)})

    #return jsonify({'result':'success', 'items':itemsBusqueda, 'cantidad de items': cantidadItems})
    return jsonify({'result':'success', 'items':items, 'cantidad de items': cantidadItems})


@app.route('/buscarItemsPorRubro', methods=['POST'])
def buscarItemsPorRubro():
    idRubro=request.json['idRubro']

    try:
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM items FROM consultobra;"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)

        sql = (" SELECT * FROM items  " + 
               " WHERE RubroId=%s ")
        tupla=(idRubro)
        cursor.execute(sql,tupla)
        itemsBusqueda = cursor.fetchall()
        cursor.close()

        cantidadItems=0
        items=[]
        for i in itemsBusqueda:
            elemento = {}
            for index in range(len(columnasItem)):
                elemento[columnasItem[index]] = i[index]
            items.append(elemento)      
            cantidadItems=cantidadItems+1
        
    except Exception as e:        
        return jsonify({'result':'Error al buscar items: '+str(e)})

    #return jsonify({'result':'success', 'items':itemsBusqueda, 'cantidad de items': cantidadItems})
    return jsonify({'result':'success', 'items':items, 'cantidad de items': cantidadItems})



# ----------------------  CALCULOS DE PRECIOS -------------------------------

@app.route('/calcularPrecio', methods=['POST'])
def calcularPrecio():
    
    Tipo_de_Costo=request.json['tipo_de_costo']
    Cargas_Sociales=request.json['cargas_sociales']
    Iva21 = request.json['iva']
    Prorratear_Total_Obtenido =request.json['prorratear']
    Valores_Items = request.json['valores_items']
    Costo_Logistica_Materiales = request.json['costo_logistica_materiales'] 
    Gastos_Generales = request.json['gastos_generales']
    Margen_Contribucion = request.json['margen_contribucion']
    Superficie_a_Edificar = request.json['superficie_a_edificar']

    if Tipo_de_Costo == "Materiales y Mano de Obra":
        factorTipoCosto = 1
    else:
        factorTipoCosto = 0

    if Cargas_Sociales == "Si":
        factorCargaSocial = 1
    else:
        factorCargaSocial = 0

    if Iva21 == "Si":
        factorIva = 1
    else:
        factorIva = 1.21

    cursor=db.cursor()
    sql = (" SELECT Id, Materiales, Obreros, Herramental, Cargas_sociales FROM items  " + 
           " ORDER BY Id ")    
    cursor.execute(sql)
    itemsBusqueda = cursor.fetchall()
    cursor.close()

    costo_directo_total = 0
    datos_items=[] 

    for item in itemsBusqueda:
        itemId = item[0]        
        valor_materiales =  round(item[1], 2) 
        valor_obreros =  round(item[2], 2) 
        valor_herramental =  round(item[3], 2) 
        valor_cargas_sociales =  round(item[4], 2)        
        
        cantidad = 0
        for v in Valores_Items:
            Id = v['idItem']
            if itemId == Id:
                cantidad=v['cantidad']
                
        recursos_materiales = round(factorTipoCosto * factorIva * valor_materiales, 2) 
        mano_de_obra = round(valor_obreros + valor_herramental + valor_cargas_sociales * factorCargaSocial, 2) 
        costo_unitario = round(recursos_materiales + mano_de_obra , 2) 
        costo_directo = round(costo_unitario * cantidad , 2)         

        costo_directo_total = round(costo_directo_total + costo_directo , 2) 

        elemento = {}
        elemento['id'] = itemId
        elemento['cantidad'] = cantidad
        elemento['recursos_materiales'] = recursos_materiales
        elemento['mano_de_obra'] = mano_de_obra
        elemento['costo_unitario'] = costo_unitario
        elemento['costo_directo'] = costo_directo
        datos_items.append(elemento)

    print(costo_directo_total)

    costo_de_obra = round( costo_directo_total + Costo_Logistica_Materiales + Gastos_Generales + Margen_Contribucion, 2)
  
    if Iva21 == "Si":
        Iva =round( 0.21 * costo_de_obra, 2)
        porcentaje_iva = 21
    else:
        Iva = 0
        porcentaje_iva = 0
    
    costo_final = Iva + costo_de_obra

    if costo_directo_total > 0:        
        porcentaje_costo_logistica_materiales = round(Costo_Logistica_Materiales * 100 / costo_directo_total , 2) 
        porcentaje_Gastos_Generales = round(Gastos_Generales * 100 / (Costo_Logistica_Materiales + costo_directo_total) , 2) 
        porcentaje_Margen_Contribucion = round(Margen_Contribucion * 100 / (Costo_Logistica_Materiales + Gastos_Generales +costo_directo_total) , 2) 
        porcentaje_final = round(costo_final * 100 / costo_directo_total, 2) 
    else:
        porcentaje_costo_logistica_materiales = 0
        porcentaje_Gastos_Generales = 0
        porcentaje_Margen_Contribucion = 0
        porcentaje_final = 0
    
    porcentajes = {}
    porcentajes['porcentaje_costo_logistica_materiales'] = porcentaje_costo_logistica_materiales
    porcentajes['porcentaje_Gastos_Generales'] = porcentaje_Gastos_Generales
    porcentajes['porcentaje_Margen_Contribucion'] = porcentaje_Margen_Contribucion
    porcentajes['porcentaje_final'] = porcentaje_final
    porcentajes['porcentaje_iva'] = porcentaje_iva    
    
    if Superficie_a_Edificar > 0:
        precio_metro_cuadrado = round( costo_final / Superficie_a_Edificar , 2)
    else:
        precio_metro_cuadrado = 0
    

    for d in datos_items:
        if costo_directo_total == 0:
            incidencia = 0
        else:
            incidencia = round( 100 * d['costo_directo'] / costo_directo_total, 2)

        d['incidencia'] = incidencia

        if Prorratear_Total_Obtenido == "Si":
            costo_final_item = round(costo_final * incidencia / 100 , 2)          
        else:
            costo_final_item = round(costo_directo_total * incidencia  / 100  , 2)

        if d['cantidad'] > 0:
            costo_unitario_final = round( costo_final_item / d['cantidad'] , 2)   
        else:
            costo_unitario_final = 0

        d['precio_final_item'] = costo_final_item
        d['costo_unitario_final'] = costo_unitario_final
   
    return jsonify({'result':'success', "datos_item":datos_items, 'costo_directo_total':costo_directo_total, 'costo_de_obra':costo_de_obra, 'costo_final':costo_final, 'porcentajes':porcentajes, 'precio_metro_cuadrado':precio_metro_cuadrado})


# ----------------   CREAR RUBRO DESDE JSON - TEST -------------------
@app.route('/crearRubro', methods=['POST'])
def crearRubro():

    id=request.json['id']
    nombre=request.json['nombre']
    activo=request.json['activo']
   
    try:
        cursor=db.cursor()
        sql = (" INSERT INTO rubros " + 
               " VALUES (%s,%s,%s) ")
        tupla=(id, nombre, activo)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()
        
    except Exception as e:        
        return jsonify({'result':'Error al registrar el rubro: '+str(e)})

    return jsonify({'result':'Rubro registrado correctamente'})
       
    
if __name__ == "__main__":
    app.run(debug=True,
            port=4000)