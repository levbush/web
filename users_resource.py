from flask import jsonify
from flask_restful import Resource, abort
import data.db_session as db_session
from data.user import User
from user_parser import parser


def abort_if_not_found(user_id):
    s = db_session.create_session()
    user = s.get(User, user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_not_found(user_id)
        s = db_session.create_session()
        user = s.get(User, user_id)
        return jsonify(
            user.to_dict(
                only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from')
            )
        )

    def put(self, user_id):
        abort_if_not_found(user_id)
        args = parser.parse_args()
        s = db_session.create_session()
        user = s.get(User, user_id)
        for key, value in args.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        s.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        abort_if_not_found(user_id)
        s = db_session.create_session()
        user = s.get(User, user_id)
        s.delete(user)
        s.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        s = db_session.create_session()
        users = s.query(User).all()
        return jsonify(
            [
                u.to_dict(
                    only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from')
                )
                for u in users
            ]
        )

    def post(self):
        args = parser.parse_args()
        s = db_session.create_session()
        user = User()
        for key, value in args.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        s.add(user)
        s.commit()
        return jsonify({'success': 'OK', 'id': user.id})
