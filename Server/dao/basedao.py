from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional


class BaseDAO(ABC):
    @abstractmethod
    def connect_to_database(self):
        pass

    @abstractmethod
    def disconnect_from_database(self):
        pass

    @abstractmethod
    def drop_tables(self):
        pass

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def add_user(
            self,
            user_name: str,
            first_name: str,
            last_name: str,
            password: str,
    ):
        pass

    @abstractmethod
    def get_user_id(
            self,
            user_name: str,
    ) -> Optional[str]:
        pass

    @abstractmethod
    def login_user(
            self,
            user_name: str,
            password: str,
    ) -> Optional[str]:
        pass

    @abstractmethod
    def add_rating(
            self,
            score: int,
            timestamp: datetime,
            foundtain_id: str,
            user_id: str,
    ):
        pass

    @abstractmethod
    def get_average_rating(
            self,
            foundtain_id: str,
            fountain_id: str,
    ) -> Optional[float]:
        pass

    @abstractmethod
    def add_fountain(
            self,
            building_id: str,
            fountain_name: str,
    ):
        pass

    @abstractmethod
    def lookup_fountain(
            self,
            fountain_name: str,
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def add_building(
            self,
            building_name: str,
            latitude: float,
            longitude: float,
            campus_id: str,
    ):
        pass

    @abstractmethod
    def get_building_id(
            self,
            building_name: str,
    ) -> Optional[str]:
        pass

    @abstractmethod
    def add_campus(
            self,
            city: str,
            state: str,
            campus_name: str,
    ):
        pass

    @abstractmethod
    def get_campus_id(
            self,
            campus_name: str,
    ) -> Optional[str]:
        pass

    @abstractmethod
    def list_fountains(
            self,
            building_name: str,
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def list_buildings(
            self,
            campus_name: str,
    ) -> List[Dict[str, Any]]:
        pass
