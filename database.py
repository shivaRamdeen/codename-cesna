import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# A class is the representation of a SQL table in python.
# Mapper code maps objects in python to colums in our database

# User table
class Users(Base):

	# columns
	__tablename__ = 'users'
	id = Column ( Integer, primary_key = True)
	fname = Column(String(80), nullable = False)
	email = Column(String(120))

	# function to enable flask jsonify	
	@property
	def serialize(self):
		return {
			'id': self.id,
			'fname': self.fname,
			'email': self.email
			}
# Item Table
class Items(Base):
	__tablename__ = 'items'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	description = Column(String(300), nullable = False)
	price = Column(Numeric, nullable = False)
	user_id = Column(Integer, ForeignKey('users.id'))
	users = relationship(Users)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'price': self.price,
			'user_id': self.user_id,
			}



# Connnection to SQL
# TODO: secure way of connecting to the database, password should not be in plain-text
engine = create_engine('mysql://root:password@127.0.0.1/hustle')
Base.metadata.create_all(engine)

