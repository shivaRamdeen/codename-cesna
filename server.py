from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Users, Items
from flask import Flask, request, jsonify, abort, g
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
auth = HTTPBasicAuth()

import pdb
app = Flask(__name__)

# DB connction setup
engine = create_engine('mysql://root:password@127.0.0.1/hustle')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# verify password for basic auth
@auth.verify_password
def verify_password(username_or_token,password):
	user_id = Users.verifyAuthToken(username_or_token)
	if user_id:
		user = session.query(Users).filter_by(id = user_id).one()
	else:
		user = session.query(Users).filter_by(email = username_or_token ).first()
		if not user or not user.verifyPass(password):
			return False
	g.user = user
	return True

# token
@app.route('/v1.0/token')
@auth.login_required
def get_auth_token():
	token = g.user.genAuthToken()
	return jsonify({'token':token.decode('ascii')})

#all users endpoint
@app.route('/v1.0/users', methods=['GET','POST','PUT','DELETE'])
def User():
	if request.method == 'GET':
		return getUsers()

	if request.method == 'POST':
		return createUser()

	if request.method == 'PUT':
		return updateUser()

	if request.method == 'DELETE':
		return deleteUser()

#all items endpoint
@app.route('/v1.0/items', methods=['GET','POST','PUT','DELETE'])
def Item():
	if request.method == 'GET':
		return getItems()

	if request.method == 'POST':
		return createItem()

	if request.method == 'PUT':
		return updateItem()

	if request.method == 'DELETE':
		return deleteItem()

#gets user accounts
def getUsers():
	# get user accounts
        userAccounts = session.query(Users).all()
	# return json formatted data
	return jsonify(Users=[user.serialize for user in userAccounts])

# create user account
def createUser():
	fname = request.json.get('fname')
	lname = request.json.get('lname')
	password = request.json.get('password')
	email = request.json.get('email')
	contact = request.json.get('contact')

	# check if params are valid
	if fname is None or lname is None or password is None or email is None or contact is None:
		print "Requred arguments not found"
		abort(400)

	# check if user already exits
	exists = session.query(Users).filter_by(email = email).first()
	if exists is not None:
		print "The email address is already associated with an existing account! \n"
		return jsonify({'message':'The email address is already associated with an existing account!'}), 200

	# create account
	newUser = Users(fname = fname, lname = lname, email = email, contact = contact, reports = 0)
	newUser.hashPass(password)
	session.add(newUser)
	session.commit()
	return jsonify({'message': 'Account Created for %s' % newUser.fname}), 201

# update user account
def updateUser():
	fname = request.json.get('fname')
	lname = request.json.get('lname')
	password = request.json.get('password')
	email = request.json.get('email')
	contact = request.json.get('contact')
	id = request.json.get('id')

	if id is not None:
		user = session.query(Users).filter_by(id = id).first()
		if user is None:
			print "The user does not exist \n"
			abort(400)
	else:
		print "No user id specified in the request \n"
		abort(400)

	if fname is not None:
		user.fname = fname
	if lname is not None:
		user.lname = lname
	if password is not None:
		user.hassPass(password)
	if contact is not None:
		user.contact = contact

	session.commit()
	return jsonify({'message':'Account %s updated sucessfully' % id}), 200

# delete user account
def deleteUser():
	# check for valid parameters
	id = request.json.get('id')
	if id is None:
		print "Required argument not found in request \n"
		abort(400)

	# delete account
	delUser = session.query(Users).filter_by(id = request.json.get('id')).first()

	if delUser is not None:
		session.delete(delUser)
		session.commit()
		return jsonify({'message':'Account %s was successfully deleted' % delUser.id}), 200

	return jsonify({'message':'The account does not exist'}), 200

# get all items
def getItems():
	return "Your Item is xxx"

# create item
def createItem():
	id = request.json.get('id')
	name = request.json.get('name')
	desc = request.json.get('description')
	price = request.json.get('price')
	negotiable = request.json.get('negotiable')
	# created = request.json.get('created') # not sure if client should handle this or server.

	if id is None or name is None or desc is None or price is None or negotiable is None:
		print "required arguments needed to create the item is not provided in the request \n"
		abort(400)

	#check if user ID is valid.
	validUser = session.query(Users).filter_by(id = id).first()
	if validUser is None:
		print("The user does not exist. To use the application please create an account.")
		abort(400)

	# create item
	newItem = Items(name = name, description = desc, price = price, negotiable = negotiable, user_id = id, created = datetime.now())
	session.add(newItem)
	session.commit()
	return jsonify({'message':'Item created successfully'}), 200

#delete item
def deleteItem():
	item_id = request.json.get('id')
	user_id = request.json.get('user_id')

	if item_id is None or user_id is None:
		print "User ID and Item ID must be specified to delete Item"
		abort(400)

	#check if user exists??? does this need to be done?

	#Check if item exists by id number
	validItem = session.query(Items).filter_by(id = item_id).first()

	if validItem is None:
		print "The item referenced in the delete request is not available"
		abort(400)

	#convert user_id string to int for proper converstion with database type
	user_id_int = int(user_id)
	#check if item belongs to user
	if validItem.user_id != user_id_int:
		print "The user that sent the request is not authorized to delete the item %s, %s" % (validItem.user_id, user_id)
		abort(400)

	#delete item
	session.delete(validItem)
	session.commit()
	return jsonify({'message':'Item Deleted'}), 200


# update item
def updateItem():
	item_name = request.json.get('name')
	item_desc = request.json.get('description')
	item_price = request.json.get('price')
	item_nego = request.json.get('negotiable')
	item_id = request.json.get('id')
	user_id = request.json.get('user_id')

	#check for required parameters
	if item_id is None or user_id is None:
		print "Requred parameters for the request are not provided"
		abort(400)

	#check if user exists
	validUser = session.query(Users).filter_by(id = user_id).first()
	if validUser is None:
		print "The user id that sent the request does not exist"
		abort(400)

	#check that the item to update exists
	validItem = session.query(Items).filter_by(id = item_id).first()
	if validItem is None:
		print "The item does not exist"
		abort(400)

	user_id_int = int(user_id)
	if validItem.user_id != user_id_int:
		print("The user is not authorized to modify this item")
		abort(400)

	# update required fields
	if item_name is not None:
		validItem.name = item_name

	if item_desc is not None:
		validItem.description = item_desc

	if item_price is not None:
		validItem.price = item_price

	if item_nego is not None:
		validItem.negotiable = item_nego

	session.commit()
	return jsonify({'message': 'Item Updated Successfully'}), 200


if __name__ == "__main__":
        app.debug = True
        app.run(host = '0.0.0.0', port = 80)
