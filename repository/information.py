from data.base import session
from models import Information


class InformationRepository:
    def __init__(self):
        self.session = session

    def get_all(self):
        return self.session.query(Information).all()

    def get_by_subject(self, subject: str):
        return self.session.query(Information).filter(Information.subject == subject).first()

    def get_by_name(self, name: str):
        return self.session.query(Information).filter(Information.name == name).first()

    def create_information(self, information: Information):
        self.session.add(information)
        self.session.commit()
        self.session.refresh(information)
        return information

    def delete_information(self, information: Information):
        self.session.delete(information)
        self.session.commit()
        return information
