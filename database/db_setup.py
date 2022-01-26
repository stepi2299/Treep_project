from app import db
from database.models import ExperienceLevel, TypeOfInterests


class DbWorker:
    def __init__(self):
        pass

    def fill_db_with_default_values(self):
        pass

    def delete_singe_record(self, obj):
        try:
            db.session.delete(obj)
            db.session.commit()
        except:
            db.session.rollback()

    def delete_all_records_from_table(self, model):
        try:
            model.query.delete()
            db.session.commit()
        except:
            db.session.rollback()

    def add_into_db(self, obj):
        try:
            if isinstance(obj, list):
                db.session.add_all(obj)
            else:
                db.session.add(obj)
            db.session.commit()
        except:
            db.session.rollback()
