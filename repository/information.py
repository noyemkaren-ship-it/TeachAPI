from typing import List, Optional, Union
from data.base import session
from models import Information
from sqlalchemy.exc import SQLAlchemyError


class InformationRepository:
    def __init__(self):
        self.session = session

    def get_all(self) -> List[Information]:
        return self.session.query(Information).all()

    def get_by_subject(self, subject: str) -> Optional[Information]:
        return self.session.query(Information).filter(Information.subject == subject).first()

    def get_by_name(self, name: str) -> Optional[Information]:
        return self.session.query(Information).filter(Information.name == name).first()

    def create_information(self, information: Information) -> Union[Information, dict]:
        try:
            self.session.add(information)
            self.session.commit()
            self.session.refresh(information)
            return information
        except SQLAlchemyError as e:
            self.session.rollback()
            return {"Message": f"Information is not created: {str(e)}"}

    def delete_information(self, information: Information) -> Union[Information, dict]:
        try:
            self.session.delete(information)
            self.session.commit()
            return information
        except SQLAlchemyError as e:
            self.session.rollback()
            return {"Message": f"Information is not deleted: {str(e)}"}

    def delete_by_name(self, name: str) -> dict:
        try:
            information = self.get_by_name(name)
            if information is None:
                return {"Message": "Information not found"}

            self.session.delete(information)
            self.session.commit()
            return {"Message": f"Information '{name}' deleted successfully"}
        except SQLAlchemyError as e:
            self.session.rollback()
            return {"Message": f"Information is not deleted: {str(e)}"}

    def delete_by_subject(self, subject: str) -> dict:
        try:
            information = self.get_by_subject(subject)
            if information is None:
                return {"Message": "Information not found"}

            self.session.delete(information)
            self.session.commit()
            return {"Message": f"Information for subject '{subject}' deleted successfully"}
        except SQLAlchemyError as e:
            self.session.rollback()
            return {"Message": f"Information is not deleted: {str(e)}"}

    def get_all_subjects(self) -> List[str]:
        """Получение списка всех уникальных предметов"""
        subjects = self.session.query(Information.subject).distinct().all()
        return [subject[0] for subject in subjects if subject[0]]