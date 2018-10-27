from api.common.database import db
from sqlalchemy.dialects.mysql import JSON

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    summary = db.Column(db.String(300), nullable=False)
