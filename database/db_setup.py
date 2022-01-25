from app import db
from database.models import ExperienceLevel, TypeOfInterests


class DbWorker:
    def __init__(self):
        pass

    def add_into_db(self, obj):
        db.session.add(obj)
        db.session.commit()

    def add_several_into_db(self, obj_list):
        db.session.add_all(obj_list)
        db.session.commit()

    def delete_from_db(self, obj):
        db.session.delete(obj)
        db.session.commit()

db_worker = DbWorker()
exp = ExperienceLevel(experience="E")
t1 = TypeOfInterests(name="ww")
t2 = TypeOfInterests(name="ww2")
t3 = TypeOfInterests(name="ww3")
db_worker.add_several([t1, t2, t3])
print(exp.id)
