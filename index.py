# -*- coding: utf-8 -*-

import os
from datetime import datetime
import json
from bson.json_util import dumps
from flask import Flask, session, render_template, request, redirect, url_for, escape, jsonify
from pymongo import MongoClient
from bson import json_util

# services = os.getenv('VCAP_SERVICES')
# services_json = json.loads(services)

# MONGO_URL = services_json["compose-for-mongodb"][0]["credentials"]["uri"] + '&ssl_cert_reqs=CERT_NONE'

MONGO_URL = 'mongodb://admin:KCBOGLJUGQATOBXA@sl-eu-lon-2-portal.1.dblayer.com:16948/admin?ssl=true&ssl_cert_reqs=CERT_NONE'

client = MongoClient(MONGO_URL)
db = client.get_default_database()

app = Flask(__name__)

@app.route('/')
def inicio():
    if ('username' in session):
        return render_template('home.html', username = session['username'], last_connection = session['last_connection'])
    return redirect(url_for('acceder'))

@app.route('/acceder', methods=['GET', 'POST'])
def acceder():
	error = None
	if request.method == 'POST':
		if usuarioValido(request.form['user'], request.form['password']):
			session['username'] = request.form['user']
			session['last_connection'] = getLastConnection(request.form['user'])
			updateLastConnection(request.form['user'])
			return redirect(url_for('inicio'))
		else:
			error = "Usuario y/o password incorrectos"
			return render_template('acceder.html', error = error)
	else:
		if ('username' in session):
			return render_template('home.html', username = session['username'], last_connection = session['last_connection'])
		else:
			return render_template('acceder.html', error = error)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    error = None
    if request.method == 'POST':
        if nuevoUsuarioValido(request.form['name'], request.form['user'], request.form['password']):
            if (usuarioExistente(request.form['user'])):
				error = "El identificador seleccionado ya existe en el servidor."
            else:
				altaNuevoUsuario(request.form['name'], request.form['user'], request.form['password'])
				session['username'] = request.form['user']
				session['last_connection'] = getLastConnection(request.form['user'])
				return redirect(url_for('inicio'))
        else:
            error = "Los datos deben contener, al menos, 3 caracteres."

    return render_template('acceder.html', error = error)

@app.route('/salir')
def salir():
    session.pop('username', None)
    return redirect(url_for('inicio'))

@app.route('/usuarios/<username>')
def obtener_usuario(username):
	return getUser(username)

@app.route('/usuarios/eliminar/<username>')
def eliminar_usuario(username):
	deleteUser(username)
	return redirect(url_for('salir'))

@app.route('/usuarios/')
def obtener_usuarios():
	return getUsers()

def usuarioValido(username, password):
    result = db.users.find( { '_id' : username, 'password' : password })
    if (result.count() == 1):
        return True
    else:
        return False

def nuevoUsuarioValido(name, username, password):
    if (len(name) < 3) or (len(username) < 3) or (len(password) < 3):
        return False
    else:
        return True

def usuarioExistente(username):
    result = db.users.find( { '_id' : username })
    if (result.count() > 0):
        return True
    else:
        return False

def altaNuevoUsuario(name, username, password):
    db.users.insert_one( { '_id' : username, 'name' : name, 'password' : password , 'last_connection' : datetime.now() } )


def updateLastConnection(username):
	db.users.update_one( { '_id': username }, { '$set' : { 'last_connection' : datetime.now() } } )

def deleteUser(username):
    db.users.delete_one( { '_id' : username } )

def getUser(username):
	result = db.users.find( { '_id' : username } )
	if (result.count() == 1):
		return jsonify(result[0])
	else:
		return "null"

def getUsers():
	result = db.users.find( {}, { 'last_connection' : 0 })
	return dumps(result)

def getLastConnection(username):
	result = db.users.find( { '_id' : username }, { 'last_connection' : 1, '_id' : 0 } )
	if (result.count() == 1):
		return dumps(result[0])
	else:
		return "null"

port = os.getenv('PORT', '5000')
if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(host='0.0.0.0', port=int(port), debug=True)