from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('surname', type=str)
parser.add_argument('name', type=str)
parser.add_argument('age', type=int)
parser.add_argument('position', type=str)
parser.add_argument('speciality', type=str)
parser.add_argument('address', type=str)
parser.add_argument('email', type=str)
parser.add_argument('hashed_password', type=str)
parser.add_argument('city_from', type=str)
