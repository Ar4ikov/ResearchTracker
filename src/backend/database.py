from datetime import datetime
from typing import Optional, TypeVar, List, Union

from sqlmodel import SQLModel, Field, Relationship

U = TypeVar("U", bound="User")
T = TypeVar("T", bound="Team")
UT = TypeVar("UT", bound="UserTeamLink")


class UserTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="teams.id")
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="users.id")
    date_create: datetime = Field(default_factory=datetime.now)


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    username: str
    password: str
    teams: List["Team"] = Relationship(back_populates="users", link_model=UserTeamLink)
    scores: List["UserScore"] = Relationship(back_populates="user_scores")

    @classmethod
    def get(cls, session, user_id: int) -> Union[U, None]:
        return session.get(User, user_id=user_id)

    def create(self, session) -> U:
        session.add(self)
        session.commit()
        session.refresh(self)

        return self

    def update(self, session) -> U:
        session.add(self)
        session.commit()
        session.refresh(self)

        return self

    def delete(self, session):
        session.delete(self)
        session.commit()
        session.refresh(self)

        return self


class Team(SQLModel, table=True):
    __tablename__ = "teams"
    id: Optional[int] = Field(default=None, primary_key=True)
    research_stage: int
    users: List["User"] = Relationship(back_populates="teams", link_model=UserTeamLink)

    @classmethod
    def get(cls, session, team_id: int) -> Union[T, None]:
        return session.get(Team, team_id=team_id)

    def create(self, session) -> T:
        session.add(self)
        session.commit()
        session.refresh(self)

        return self

    def update(self, session) -> T:
        session.add(self)
        session.commit()
        session.refresh(self)

        return self

    def delete(self, session):
        session.delete(self)
        session.commit()
        session.refresh(self)

        return self


class UserScore(SQLModel, table=True):
    __tablename__ = "user_scores"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    team_id: int = Field(foreign_key="teams.id")
    score: int
    date_create: datetime = Field(default_factory=datetime.now)

    @classmethod
    def get_by_user(cls, session, user_id: int):...

