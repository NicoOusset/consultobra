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



#------------------------ A QUIEN LLAMO? -------------------------------
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
    
        cursor=db.cursor()
        sql = (" INSERT INTO a_quien_llamo " + 
               " VALUES (default,%s,%s,%s,%s,%s,%s,%s,'Si') ")
        tupla=(Categoria, Nombre, Apellido, Telefono, Direccion, Facebook, Instagram)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()       
        
    except Exception as e:        
        return jsonify({'result':'Error', 'mensaje': 'Error al crear A quien Llamo?: '+str(e)})
    
    return jsonify({'result':'Success', 'mensaje':"A quien Llamo? creado correctamente"})


@app.route('/listarAquienLlamo', methods=['GET'])
def listarAquienLlamo():
    
    try:
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM a_quien_llamo FROM consultobra;"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)

        sql = (" SELECT * FROM a_quien_llamo WHERE Activo='Si' ")
        cursor.execute(sql)
        AquienLlamoBusqueda = cursor.fetchall()
        cursor.close()

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
    
        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM a_quien_llamo FROM consultobra;"
        cursor.execute(sql0)
        columnas = cursor.fetchall()        
        columnasItem = []
        for c in columnas:
            nombreColumna = c[0]
            columnasItem.append(nombreColumna)

        sql = (" SELECT * FROM a_quien_llamo "+
               " WHERE Id like %s and Categoria like %s and Nombre like %s and Apellido like %s and "+
               " Direccion like %s and Telefono like %s and Facebook like %s and " +
               " Instagram like %s and Activo='Si' " ) 
        tupla=(Id, Categoria, Nombre, Apellido, Direccion, Telefono, Facebook, Instagram)     
        cursor.execute(sql,tupla)
        AquienLlamoBusqueda = cursor.fetchall()
        cursor.close()

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

        cursor=db.cursor()
        sql0 = "SHOW COLUMNS FROM a_quien_llamo FROM consultobra;"
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
     
        cursor=db.cursor()
        sql = (" UPDATE a_quien_llamo " + 
               " SET Categoria=%s, Nombre=%s, Apellido=%s, Telefono=%s, Direccion=%s, Facebook=%s, Instagram=%s "+
               " WHERE Id=%s " )
        tupla=(Categoria, Nombre, Apellido,  Telefono, Direccion, Facebook, Instagram, Id)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()       
        
    except Exception as e:        
        return jsonify({'result':'Error' , 'mensaje':'Error al modificar el A_quien_llamo: '+str(e)})
    
    return jsonify({'result':'Success', 'mensaje':"A_quien_llamo modificado correctamente"})


@app.route('/eliminarAquienLlamo', methods=['POST'])
def eliminarAquienLlamo():

    try:
        Id=request.json['Id']
    
        cursor=db.cursor()
        sql = (" UPDATE a_quien_llamo SET Activo='No' " + 
               " WHERE Id=%s " )
        tupla=(Id)
        cursor.execute(sql,tupla)
        db.commit()
        cursor.close()       
        
    except Exception as e:        
        return jsonify({'result':'Error' , 'mensaje':'Error al eliminar el A_quien_llamo: '+str(e)})
    
    return jsonify({'result':'Success', 'mensaje':"A_quien_llamo eliminado correctamente"})
        

@app.route('/listarCategorias', methods=['GET'])
def listarCategorias():
    
    try:
        cursor=db.cursor()
        
        sql = (" SELECT DISTINCT Categoria FROM a_quien_llamo WHERE Activo='Si' ")
        cursor.execute(sql)
        CategoriasBusqueda = cursor.fetchall()
        cursor.close()

        if not CategoriasBusqueda:
            return jsonify({'result':'Error' , 'mensaje': 'No se encontraron Categorias'})
        
        Categorias=[]
        for i in CategoriasBusqueda:
            elemento = {}           
            elemento['nombre_categoria'] = i[0]
            Categorias.append(elemento)                
        
    except Exception as e:        
        return jsonify({'result':'Error', 'mensaje': 'Error al buscar Categorias: '+str(e)})
    return jsonify({'result':'Success', 'Categorias':Categorias})

