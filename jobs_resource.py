from flask import jsonify
from flask_restful import Resource, abort
import data.db_session as db_session
from data.job import Jobs
from job_parser import parser


def abort_if_not_found(job_id):
    s = db_session.create_session()
    job = s.get(Jobs, job_id)
    if not job:
        abort(404, message=f'Job {job_id} not found')


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_not_found(job_id)
        s = db_session.create_session()
        job = s.get(Jobs, job_id)
        return jsonify(
            job.to_dict(
                only=('id', 'job', 'work_size', 'collaborators', 'team_leader', 'is_finished', 'start_date', 'end_date')
            )
        )

    def put(self, job_id):
        abort_if_not_found(job_id)
        args = parser.parse_args()
        s = db_session.create_session()
        job = s.get(Jobs, job_id)
        for key, value in args.items():
            if value is not None and hasattr(job, key):
                setattr(job, key, value)
        s.commit()
        return jsonify({'success': 'OK'})

    def delete(self, job_id):
        abort_if_not_found(job_id)
        s = db_session.create_session()
        job = s.get(Jobs, job_id)
        s.delete(job)
        s.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        s = db_session.create_session()
        jobs = s.query(Jobs).all()
        return jsonify(
            [
                j.to_dict(
                    only=(
                        'id',
                        'job',
                        'work_size',
                        'collaborators',
                        'team_leader',
                        'is_finished',
                        'start_date',
                        'end_date',
                    )
                )
                for j in jobs
            ]
        )

    def post(self):
        args = parser.parse_args()
        if not args.get('job'):
            abort(400, message='Поле job обязательно')
        s = db_session.create_session()
        job = Jobs()
        for key, value in args.items():
            if value is not None and hasattr(job, key):
                setattr(job, key, value)
        s.add(job)
        s.commit()
        return jsonify({'success': 'OK', 'id': job.id})
