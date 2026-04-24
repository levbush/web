from flask import Blueprint, jsonify, request, make_response
import data.db_session as db_session
from data.user import User

blueprint = Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify([u.to_dict() for u in users])


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(user.to_dict())


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    if not data:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    user = User()
    for k in data:
        if hasattr(user, k):
            setattr(user, k, data[k])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = request.json
    if not data:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    for k in data:
        if hasattr(user, k):
            setattr(user, k, data[k])
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
