from datetime import datetime
from typing import Optional, TypeVar, List, Union

from sqlmodel import SQLModel, Field, Relationship

U = TypeVar("U", bound="User")
T = TypeVar("T", bound="Team")
UT = TypeVar("UT", bound="UserTeamLink")
US = TypeVar("US", bound="UserScore")


class UserTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="team.id")
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.id")
    date_create: datetime = Field(default_factory=datetime.now)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    username: str
    password: str
    date_create: datetime = Field(default_factory=datetime.now)
    teams: List["Team"] = Relationship(back_populates="users", link_model=UserTeamLink)
    scores: List["UserScore"] = Relationship(back_populates="user")

    @classmethod
    def get(cls, session, user_id: int) -> Union[U, None]:
        return session.query(User).filter(User.id == user_id).first()

    @classmethod
    def get_by_username(cls, session, username: str) -> Union[U, None]:
        return session.query(User).filter(User.username == username).first()

    @classmethod
    def get_all(cls, session) -> List[U]:
        return session.query(User).all()

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
    id: Optional[int] = Field(default=None, primary_key=True)
    research_stage: int
    users: List["User"] = Relationship(back_populates="teams", link_model=UserTeamLink)
    scores: List["UserScore"] = Relationship(back_populates="team")
    date_create: datetime = Field(default_factory=datetime.now)

    @classmethod
    def get(cls, session, team_id: int) -> Union[T, None]:
        return session.query(Team).filter(Team.id == team_id).first()

    @classmethod
    def get_all(cls, session) -> List[T] | None:
        return session.query(Team).all()

    @classmethod
    def get_by_stage(cls, session, stage: int) -> Union[T, None]:
        return session.query(Team).filter(Team.research_stage == stage).all()

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

    def delete(self, session) -> T:
        session.delete(self)
        session.commit()
        session.refresh(self)

        return self


class UserScore(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    team_id: int = Field(foreign_key="team.id")
    user: "User" = Relationship(back_populates="scores")
    team: "Team" = Relationship(back_populates="scores")
    score: int
    date_create: datetime = Field(default_factory=datetime.now)

    @classmethod
    def get_by_user(cls, session, user_id: int) -> list[US] | None:
        return session.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def get_by_team(cls, session, team_id: int) -> list[US] | None:
        return session.query(cls).filter(cls.team_id == team_id).all()

    @classmethod
    def get_all(cls, session) -> list[US] | None:
        return session.query(cls).all()

    @classmethod
    def get(cls, session, score_id: int) -> Union[US, None]:
        return session.query(cls).filter(cls.id == score_id).first()

    def create(self, session) -> US:
        session.add(self)
        session.commit()
        session.refresh(self)

        return self

    def update(self, session) -> US:
        session.add(self)
        session.commit()
        session.refresh(self)

        return self

    def delete(self, session) -> US:
        session.delete(self)
        session.commit()
        session.refresh(self)

        return self
