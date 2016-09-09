import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.hash import pbkdf2_sha256
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

# A class is the representation of a SQL table in python.
# Mapper code maps objects in python to colums in our database

# User table
class Users(Base):

	# columns
	__tablename__ = 'users'
	id = Column ( Integer, primary_key = True)
	fname = Column(String(80), nullable = False)
	lname = Column(String(80), nullable = False)
	email = Column(String(120))
	pass_hash = Column(String(120))
	contact = Column(String(11), nullable = False)
	reports = Column(Integer)

	# function to enable flask jsonify	
	@property
	def serialize(self):
		return {
			'id': self.id,
			'fname': self.fname,
			'lname': self.lname,
			'email': self.email,
			'contact': self.contact,
			}
	# function to hash the password befor storing
	def hashPass(self,password):
		self.pass_hash = pbkdf2_sha256.encrypt(password)

	# function to verify passwords with hashes
	def verifyPass(self,password):
		return pbkdf2_sha256.verify(password,self.pass_hash)

	def genAuthToken(self, expiration=600)
		s = Serializer(secret_key, expires_in = expiration)
		return s.dump({'id':self.id})


	@staticmethod
	def verifyAuthToken(token):
		s = Serializer(secret_key)
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user_id = data['id']
		return user_id

# Item Table
class Items(Base):
	__tablename__ = 'items'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	description = Column(String(300), nullable = False)
	price = Column(Numeric, nullable = False)
	negotiable = Column(Boolean(create_constraint = True))
	user_id = Column(Integer, ForeignKey('users.id'))
	users = relationship(Users)
	created = Column(Date) # check python data and time module to determine how to set this value

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'price': self.price,
			'negotiable': self.negotiable,
			'user_id': self.user_id,
			'created': self.created,
			}



# Connnection to SQL
# TODO: secure way of connecting to the database, password should not be in plain-text
engine = create_engine('mysql://root:password@127.0.0.1/hustle')
Base.metadata.create_all(engine)

