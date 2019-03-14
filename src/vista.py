# -*- coding: utf-8 -*-
import os
from flask import render_template, Flask, request, url_for, redirect
from src import modelo as mod
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.realpath(__file__))+"\\ficheros"

m = mod.modelo.getInstance()

@app.route('/', methods=["GET","POST"])
def index():
    error = ''
    if request.method == "POST":
        if("btn btn-selepub" not in request.files):
            error = "No se ha seleccionado ningún fichero"
            return render_template('index.html', error = error)
        fich = request.files["btn btn-selepub"]
        fullpath = os.path.join(app.config['UPLOAD_FOLDER'], fich.filename)
        fich.save(fullpath)
        if(zipfile.is_zipfile(fullpath)):
            if("btn btn-cargarepub" in request.form):
                m.obtTextoEpub(fullpath)
                return redirect(url_for('menu'))
        else: 
            error = "La ruta indicada no contiene un fichero epub"
            return render_template('index.html', error = error)
    return render_template('index.html')

@app.route('/Menu/', methods=["GET", "POST"])
def menu():
#    error = ''
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    if request.method == "POST":
        if("btn btn-dictauto" in request.form):
            return redirect(url_for('dictaut'))
        elif("btn btn-verdict" in request.form):
            return redirect(url_for('verdict'))
        elif("btn btn-moddict" in request.form):
            return redirect(url_for('moddict'))
        elif("btn btn-vacdict" in request.form):
            m.vaciarDiccionario()
        elif("btn btn-expdict" in request.form):
            print('Funcionalidad en desarrollo')
    return render_template('menu.html')
#    return 'Hola mundo'


@app.route('/Menu/Dicts-Automaticos/', methods=["GET", "POST"])
def dictaut():
    msg = ''
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    if request.method == "POST":
        if("cbx cbx-vacdit"  in request.form):
            m.vaciarDiccionario()
        if("btn btn-creadict" in request.form):
            m.crearDict()
            msg = "Diccionario creado con éxito"
        elif("btn btn-impdict" in request.form):
            return redirect(url_for('impdict'))
        elif("btn btn-obtdict" in request.form):
            return redirect(url_for('obtdict'))
    return render_template('dictaut.html', msg = msg)

@app.route('/Menu/Dicts-Automaticos/Importar-Dict/', methods=["GET","POST"])
def impdict():
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    error = ''
    if request.method == "POST":
        if("btn btn-selcsv" not in request.files):
            error = "No se ha seleccionado ningún fichero"
            return render_template('impdict.html', error = error)
#        fich = request.files["btn btn-selcsv"]
#        fullpath = os.path.join(app.config['UPLOAD_FOLDER'], fich.filename)
        if("btn btn-cargarcsv" in request.form):
            #Se deja para futuros sprint comprobar que el fichero introducido es csv
            # debido a que mimetype no reconoce si el archivo es csv
            if(True):
                # m.importDict(fullpath)
                error = "Fichero csv cargado"
                return render_template('impdict.html', error = error)
            else: 
                error = "La ruta indicada no contiene un fichero csv"
                return render_template('impdict.html', error = error)
    return render_template('impdict.html')

@app.route('/Menu/Dicts-Automaticos/Obtener-Dict/', methods=["GET","POST"])
def obtdict():
    error = ''
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    if request.method == "POST":
        url = request.form['txt txt-url']
        if(len(url)>0):
            m.scrapeWiki(url)
            #Se deja para futuros sprints comprobar que la url contenía información scrapeable
        else:
            error = 'No se permiten textos vacíos como url'
    return render_template('obtdict.html', error = error)
    
@app.route('/Menu/Ver-Diccionario/', methods=["GET", "POST"])
def verdict():
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    return render_template('verdict.html', pers = m.getPersonajes())

@app.route('/Menu/Modificar-Diccionario/', methods=["GET", "POST"])   
def moddict():
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    if request.method == "POST":
        if("btn btn-newpers" in request.form):
            return redirect(url_for('newpers'))
        elif("btn btn-delpers" in request.form):
            return redirect(url_for('delpers'))
        elif("btn btn-joinpers" in request.form):
            return redirect(url_for('joinpers'))
        elif("btn btn-newrefpers" in request.form):
            return redirect(url_for('newrefpers'))
        elif("btn btn-delrefpers" in request.form):
            return redirect(url_for('delrefpers'))
    return render_template('moddict.html', pers = m.getPersonajes())

@app.route('/Menu/Modificar-Diccionario/Anadir-Personaje/', methods=["GET", "POST"])    
def newpers():
    error = ''
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    if request.method == "POST":
        perso = request.form['txt txt-nombrepers']
        if(len(perso)>0):
            error = 'Se ha añadido correctamente el personaje: ' + str(perso)
            m.anadirPersonaje(perso)
        else:
            error = 'No se permiten textos vacíos como nombre de personaje'
    return render_template('newpers.html', error = error, pers = m.getPersonajes())

@app.route('/Menu/Modificar-Diccionario/Eliminar-Personaje/', methods=["GET", "POST"])    
def delpers():
    error = ''
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    if request.method == "POST":
        perso = request.form['txt txt-idpers']
        if(len(perso)>0):
            m.eliminarPersonaje(perso)
        else:
            error = 'No se permiten textos vacíos como id de personaje'
    return render_template('delpers.html', error = error, pers = m.getPersonajes())

@app.route('/Menu/Modificar-Diccionario/Juntar-Personajes/', methods=["GET", "POST"])    
def joinpers():
    error = ''
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    if request.method == "POST":
        id1p = request.form['txt txt-id1pers']
        id2p = request.form['txt txt-id2pers']
        if(len(id1p)>0 and len(id2p)>0):
            m.juntarPersonajes(id1p,id2p)
        else:
            error = 'No se permiten textos vacíos como id de personaje o nueva referencia'
    return render_template('joinpers.html', error = error, pers = m.getPersonajes())
   
@app.route('/Menu/Modificar-Diccionario/Nueva-Referencia/', methods=["GET", "POST"])    
def newrefpers():
    error = ''
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    if request.method == "POST":
        idp = request.form['txt txt-idpers']
        ref = request.form['txt txt-refpers']
        if(len(idp)>0 and len(ref)>0):
            m.anadirReferenciaPersonaje(idp,ref)
        else:
            error = 'No se permiten textos vacíos como id de personaje o nueva referencia'
    return render_template('newrefpers.html', error = error, pers = m.getPersonajes())

@app.route('/Menu/Modificar-Diccionario/Eliminar-Referencia/', methods=["GET", "POST"])    
def delrefpers():
    error = ''
    if(m.getTexto() == ''):
        return redirect(url_for('index'))
    if request.method == "POST":
        idp = request.form['txt txt-idpers']
        ref = request.form['txt txt-refpers']
        if(len(idp)>0 and len(ref)>0):
            m.eliminarReferenciaPersonaje(idp,ref)
        else:
            error = 'No se permiten textos vacíos como id de personaje o nueva referencia'
    return render_template('delrefpers.html', error = error, pers = m.getPersonajes())