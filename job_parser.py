from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('job', type=str)
parser.add_argument('work_size', type=int)
parser.add_argument('collaborators', type=str)
parser.add_argument('team_leader', type=int)
parser.add_argument('is_finished', type=bool)
