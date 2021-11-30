import os
from flask import Flask, request, jsonify
from datetime import datetime
import conexionBD
import pandas as pd
import numpy as np

 
app = Flask(__name__)

'''
global HOST
HOST = 'us-cdbr-east-04.cleardb.com'
global DB
DB = 'heroku_04e936a4aba4f0a'
global USER
USER = 'b78ad30286a20d'
global PASS
PASS = '2a85203a'

'''

global HOST
HOST = 'localhost'
global DB
DB = 'consultobra'
global USER
USER = 'root'
global PASS
PASS = ''





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
        ItemActivo = row[10]

        if Materiales == "":
            Materiales=0
        if Obreros == "":
            Obreros=0
        if Herramental == "":
            Herramental=0
        if Cargas_sociales == "":
            Cargas_sociales=0       
       
        flag = True
        if not rubrosCargados:
            for r in rubrosCargados:
                if(idRubro == r[0]):
                    flag=False

        if(flag):
            rubrosCargados.append(idRubro)
            cargarRubroDesdeExcel(idRubro, NombreRubro, 'SI')

        cargarItemDesdeExcel(IdItem,NombreItem,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,idRubro, ItemActivo)
    
    print("Carga de datos finalizada")


def cargarRubroDesdeExcel(id, nombre, activo):

    try:
        db = conexionBD.conectar(HOST, DB, USER, PASS)
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
        conexionBD.desconectar(db)
        
    except Exception as e:        
        return str(e)

    return 'Rubro registrado correctamente'


def cargarItemDesdeExcel(IdItem,NombreItem,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,RubroId,ItemActivo):

    try:
        print(IdItem)
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql = (" SELECT * FROM items " + 
               " WHERE Id = %s ")
        tupla=(IdItem)
        cursor.execute(sql,tupla)
        item=cursor.fetchone()

        if not item:            
            sql1 = ("INSERT INTO items (Id,Nombre,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,RubroId,Activo) " + 
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
            tupla1=(IdItem,NombreItem,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,RubroId,ItemActivo)
            cursor.execute(sql1,tupla1)
            
        else:
            sql1 = (" UPDATE items SET Nombre=%s, Unidad=%s, Materiales=%s, Obreros=%s, Herramental=%s, Cargas_sociales=%s, Comentario=%s, RubroId=%s, Activo=%s " + 
                    " WHERE Id = %s ")
            tupla1=(NombreItem,Unidad,Materiales,Obreros,Herramental,Cargas_sociales,Comentario,RubroId,ItemActivo,IdItem)
            cursor.execute(sql1,tupla1)
            print("aqui3")

        db.commit()
        cursor.close()
        conexionBD.desconectar(db)
        
    except Exception as e:   
        print(str(e))     
        return str(e)

    return 'Rubro registrado correctamente'


@app.route('/buscarRubros', methods=['GET'])
def buscarRubros():

    try:
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()                
        sql = (" SELECT r.Id, r.Nombre FROM rubros r " + 
               " WHERE r.Activo = 'SI' ORDER BY r.Id ")       
        cursor.execute(sql)
        rubrosBusqueda = cursor.fetchall()
        cursor.close()
        conexionBD.desconectar(db)

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


@app.route('/buscarItemsPorRubro', methods=['GET'])
def buscarItemsPorRubro():
    idRubro=request.json['idRubro']

    try:
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM items FROM "+ DB + ";"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)

        sql = (" SELECT * FROM items i " + 
               " WHERE RubroId=%s and (i.Activo='SI' or i.Activo='Si') ORDER BY i.Id ")
        tupla=(idRubro)
        cursor.execute(sql,tupla)
        itemsBusqueda = cursor.fetchall()
        cursor.close()
        conexionBD.desconectar(db)

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


@app.route('/buscarItemsPorRubroConInactivos', methods=['GET'])
def buscarItemsPorRubroConInactivos():
    idRubro=request.json['idRubro']

    try:
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM items FROM "+ DB + ";"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)

        sql = (" SELECT * FROM items i " + 
               " WHERE RubroId=%s ORDER BY i.Id ")
        tupla=(idRubro)
        cursor.execute(sql,tupla)
        itemsBusqueda = cursor.fetchall()
        cursor.close()
        conexionBD.desconectar(db)

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




@app.route('/buscarItems', methods=['GET'])
def buscarItems():
    
    try:
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM items FROM "+ DB + ";"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)        
        columnasItem.append("Nombre_Rubro")
        
        sql = (" SELECT i.*, r.Nombre FROM items i  " + 
               " INNER JOIN rubros r ON i.RubroId = r.Id "+
               " WHERE i.Activo='SI' or i.Activo='Si' ORDER BY i.Id ")       
        cursor.execute(sql)
        itemsBusqueda = cursor.fetchall()
        cursor.close()
        conexionBD.desconectar(db)

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


@app.route('/buscarItemsConInactivos', methods=['GET'])
def buscarItemsConInactivos():
    
    try:
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM items FROM "+ DB + ";"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)        
        columnasItem.append("Nombre_Rubro")
        
        sql = (" SELECT i.*, r.Nombre FROM items i  " + 
               " INNER JOIN rubros r ON i.RubroId = r.Id "+
               " ORDER BY i.Id ")       
        cursor.execute(sql)
        itemsBusqueda = cursor.fetchall()
        cursor.close()
        conexionBD.desconectar(db)

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

    db = conexionBD.conectar(HOST, DB, USER, PASS)
    cursor=db.cursor()
    sql = (" SELECT Id, Materiales, Obreros, Herramental, Cargas_sociales FROM items  " + 
           " ORDER BY Id ")    
    cursor.execute(sql)
    itemsBusqueda = cursor.fetchall()
    cursor.close()
    conexionBD.desconectar(db)

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
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql = (" INSERT INTO rubros " + 
               " VALUES (%s,%s,%s) ")
        tupla=(id, nombre, activo)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()
        conexionBD.desconectar(db)
        
    except Exception as e:        
        return jsonify({'result':'Error al registrar el rubro: '+str(e)})

    return jsonify({'result':'Rubro registrado correctamente'})
       



#------------------------ A QUIEN LLAMO? -------------------------------------------


@app.route('/crearAquienLlamo', methods=['POST'])
def crearAquienLlamo():
    
    try:
        Categoria=request.json['Categoria']
        Nombre=request.json['Nombre']
        Apellido=request.json['Apellido']
        Telefono=request.json['Telefono']
        Direccion=request.json['Direccion']
        Facebook=request.json['Facebook']
        Instagram=request.json['Instagram']        
    
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql = (" INSERT INTO a_quien_llamo " + 
               " VALUES (default,%s,%s,%s,%s,%s,%s,%s,'Si') ")
        tupla=(Categoria, Nombre, Apellido, Telefono, Direccion, Facebook, Instagram)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()       
        conexionBD.desconectar(db)
        
    except Exception as e:        
        return jsonify({'result':'Error', 'mensaje': 'Error al crear A quien Llamo?: '+str(e)})
    
    return jsonify({'result':'Success', 'mensaje':"A quien Llamo? creado correctamente"})


@app.route('/listarAquienLlamo', methods=['GET'])
def listarAquienLlamo():
    
    try:
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM a_quien_llamo FROM "+ DB + ";"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)
        columnasItem.append("Nombre_categoria")


        sql = (" SELECT a.*, NombreCategoria FROM a_quien_llamo a "+
                " INNER JOIN categorias c ON a.Categoria = c.Id "+
                " WHERE Activo='Si' ")
        cursor.execute(sql)
        AquienLlamoBusqueda = cursor.fetchall()
        cursor.close()
        conexionBD.desconectar(db)

        if not AquienLlamoBusqueda:
            return jsonify({'result':'Error' , 'mensaje': 'No se encontraron A_quien_llamo'})

        cantidadAquienLlamo=0
        AquienLlamo=[]
        for i in AquienLlamoBusqueda:
            elemento = {}
            for index in range(len(columnasItem)):
                elemento[columnasItem[index]] = i[index]
            AquienLlamo.append(elemento)      
            cantidadAquienLlamo=cantidadAquienLlamo+1     
        
    except Exception as e:        
        return jsonify({'result':'Error', 'mensaje': 'Error al buscar A_quien_llamo: '+str(e)})
    return jsonify({'result':'Success', 'A_quien_llamo':AquienLlamo, 'Cantidad_A_quien_llamo':cantidadAquienLlamo})


@app.route('/buscarAquienLlamo', methods=['GET'])
def buscarAquienLlamo():

    try:  
        Id = "%" + request.json['Id'] + "%"
        Categoria = "%" + request.json['Categoria'] + "%"
        Nombre = "%" + request.json['Nombre'] + "%"
        Apellido = "%" + request.json['Apellido'] + "%"
        Telefono = "%" + request.json['Telefono'] + "%"
        Direccion = "%" + request.json['Direccion'] + "%"
        Facebook = "%" + request.json['Facebook'] + "%"
        Instagram = "%" + request.json['Instagram'] + "%"
    
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM a_quien_llamo FROM "+ DB + ";"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)
        columnasItem.append("Nombre_categoria")

        sql = (" SELECT a.*, NombreCategoria FROM a_quien_llamo a "+
               " INNER JOIN categorias c ON a.Categoria = c.Id "+
               " WHERE a.Id like %s and Categoria like %s and Nombre like %s and Apellido like %s and "+
               " Direccion like %s and Telefono like %s and Facebook like %s and " +
               " Instagram like %s and Activo='Si' " ) 
        tupla=(Id, Categoria, Nombre, Apellido, Direccion, Telefono, Facebook, Instagram)     
        cursor.execute(sql,tupla)
        AquienLlamoBusqueda = cursor.fetchall()
        cursor.close()
        conexionBD.desconectar(db)

        if not AquienLlamoBusqueda:
            return jsonify({'result':'Error' , 'mensaje': 'No se encontraron A_quien_llamo'})

        cantidadAquienLlamo=0
        AquienLlamo=[]
        for i in AquienLlamoBusqueda:
            elemento = {}
            for index in range(len(columnasItem)):
                elemento[columnasItem[index]] = i[index]
            AquienLlamo.append(elemento)      
            cantidadAquienLlamo=cantidadAquienLlamo+1     
        
    except Exception as e:        
        return jsonify({'result':'Error', 'mensaje': 'Error al buscar A_quien_llamo: '+str(e)})
    return jsonify({'result':'Success', 'A_quien_llamo':AquienLlamo, 'Cantidad_A_quien_llamo':cantidadAquienLlamo})


@app.route('/buscarDatosAquienLlamo', methods=['GET'])
def buscarDatosAquienLlamo():
    
    try:
        Id=request.json['Id']

        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM a_quien_llamo FROM "+ DB + ";"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)

        sql = (" SELECT * FROM a_quien_llamo WHERE Id=%s ")       
        cursor.execute(sql, Id)
        ListaAquienLlamo = cursor.fetchone()
        cursor.close()
        conexionBD.desconectar(db)

        if not ListaAquienLlamo:
            return jsonify({'result':'Error' , 'mensaje': 'No se encontró el A_quien_llamo'})
       
        AquienLlamo={}
        for index in range(len(columnasItem)):
            AquienLlamo[columnasItem[index]] = ListaAquienLlamo[index]   
                     
    except Exception as e:        
        return jsonify({'result':'Error' , 'mensaje': 'Error al buscar el A_quien_llamo: '+str(e)})
    return jsonify({'result':'Success', 'Datos_A_quien_llamo':AquienLlamo})



@app.route('/modificarAquienLlamo', methods=['POST'])
def modificarAquienLlamo():

    try:
        Id=request.json['Id']
        Categoria=request.json['Categoria']
        Nombre=request.json['Nombre']
        Apellido=request.json['Apellido']
        Telefono=request.json['Telefono']
        Direccion=request.json['Direccion']
        Facebook=request.json['Facebook']
        Instagram=request.json['Instagram']  
     
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql = (" UPDATE a_quien_llamo " + 
               " SET Categoria=%s, Nombre=%s, Apellido=%s, Telefono=%s, Direccion=%s, Facebook=%s, Instagram=%s "+
               " WHERE Id=%s " )
        tupla=(Categoria, Nombre, Apellido,  Telefono, Direccion, Facebook, Instagram, Id)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()       
        conexionBD.desconectar(db)
        
    except Exception as e:        
        return jsonify({'result':'Error' , 'mensaje':'Error al modificar el A_quien_llamo: '+str(e)})
    
    return jsonify({'result':'Success', 'mensaje':"A_quien_llamo modificado correctamente"})


@app.route('/eliminarAquienLlamo', methods=['POST'])
def eliminarAquienLlamo():

    try:
        Id=request.json['Id']

        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql = (" UPDATE a_quien_llamo SET Activo='No' " + 
               " WHERE Id=%s " )
        tupla=(Id)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()   
        conexionBD.desconectar(db)    
        
    except Exception as e:        
        return jsonify({'result':'Error' , 'mensaje':'Error al eliminar el A_quien_llamo: '+str(e)})
    
    return jsonify({'result':'Success', 'mensaje':"A_quien_llamo eliminado correctamente"})
    


@app.route('/crearCategoria', methods=['POST'])
def crearCategoria():
    
    try:        
        NombreCategoria=request.json['NombreCategoria']              
    
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql = (" INSERT INTO categorias " + 
               " VALUES (default,%s) ")
        tupla=(NombreCategoria)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()       
        conexionBD.desconectar(db)
        
    except Exception as e:        
        return jsonify({'result':'Error', 'mensaje': 'Error al crear Categoria: '+str(e)})
    
    return jsonify({'result':'Success', 'mensaje':"Categoria creada correctamente"})
    

@app.route('/listarCategorias', methods=['GET'])
def listarCategorias():
    
    try:
        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM categorias FROM "+ DB + ";"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)
        
        sql = (" SELECT * FROM categorias ")
        cursor.execute(sql)
        CategoriasBusqueda = cursor.fetchall()
        cursor.close()
        conexionBD.desconectar(db)

        if not CategoriasBusqueda:
            return jsonify({'result':'Error' , 'mensaje': 'No se encontraron Categorias'})

        Categorias=[]
        for i in CategoriasBusqueda:
            elemento = {}
            for index in range(len(columnasItem)):
                elemento[columnasItem[index]] = i[index]
            Categorias.append(elemento)      
        
    except Exception as e:        
        return jsonify({'result':'Error', 'mensaje': 'Error al buscar Categorias: '+str(e)})
    return jsonify({'result':'Success', 'Categorias':Categorias})


@app.route('/modificarCategoria', methods=['POST'])
def modificarCategoria():

    try:
        Id=request.json['Id']
        NombreCategoria=request.json['NombreCategoria']       

        db = conexionBD.conectar(HOST, DB, USER, PASS)
        cursor=db.cursor()
        sql = (" UPDATE categorias " + 
               " SET NombreCategoria=%s "+
               " WHERE Id=%s " )
        tupla=(NombreCategoria, Id)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()       
        conexionBD.desconectar(db)
        
    except Exception as e:        
        return jsonify({'result':'Error' , 'mensaje':'Error al modificar la Categoria: '+str(e)})
    
    return jsonify({'result':'Success', 'mensaje':"Categoria modificada correctamente"})


if __name__ == "__main__":
    app.run(debug=True,
            port=4000)