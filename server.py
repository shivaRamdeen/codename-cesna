from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Users, Items
from flask import Flask, request, jsonify
app = Flask(__name__)

# DB connction setup
engine = create_engine('mysql://root:password@127.0.0.1/hustle')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#all users endpoint
@app.route('/v1.0/users', methods=['GET','POST','PUT','DELETE'])
def User():
	if request.method == 'GET':
		return getUsers()

	if request.method == 'POST':
		return createUser()

	if request.method == 'PUT':
		return updateUser()

#all items endpoint
@app.route('/v1.0/items', methods=['GET','POST','PUT','DELETE'])
def Items():
	if request.method == 'GET':
		return getItems()

	if request.method == 'POST':
		return createItem()

	if request.method == 'PUT':
		return updateItem()

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
	contact = requenst.json.get('contact')

	# check if params are valid
	if fname is None or lname is None or password is None or email is None or contact is None:
		print "Requred arguments not found"
		abort(400)

	# check if user already exits
	if session.query(User).filter_by(email = email).first() is not None:
		print "The email address is already associated with an existing account!"
		return jsonify({'message':'The email address is already associated with an existing account!'}), 200

	# create account
	newUser = Users(fname = fname, lname = lname, email = email, contact = contact, reports = 0)
	newUser.hashPass(password)
	session.add(newUser)
	session.commit()
	return jsonify({'message': 'Account Created for %s %s' % newUser.fname, newUser.lname}),201

# update user account
def updateUser():
	return "Account Updated Successfully"

# get all items
def getItems():
	return "Your Item is xxx"

# create item
def createItem():
	return "Item Created Successfully"

# update item
def updateItem():
	return "Item Updated Successfully"

if __name__ == "__main__":
        app.debug = True
        app.run(host = '0.0.0.0', port = 80)
