import sqlalchemy as sa
import datetime

from api.common.database import db

class EmailModel(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.func.now())
    sent_at = db.Column(db.DateTime, nullable=True)
    error = db.Column(db.String(255), nullable=True)


    @classmethod
    def find_not_sent(cls, total_threads = 1, thread_number = 1):
        return cls.query.filter(UserModel.sent_at == None).all

    @classmethod
    def find_not_sent_by_thread(cls, total_threads = 1, thread_number = 1):
        q = cls.query.filter(UserModel.sent_at == None)
        if number > 1:
            q.filter(EmailModel.id % number == 0)
        return q.all()

