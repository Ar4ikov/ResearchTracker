from datetime import datetime

from pydantic import BaseModel, validator
from typing import Optional
from re import fullmatch

from pydantic.schema import List


class UserScoreRequest(BaseModel):
    score: int
    user_id: int
    team_id: int


class UserScoreResponse(UserScoreRequest):
    id: Optional[int] = None
    date_create: datetime


class UserRequest(BaseModel):
    first_name: str
    last_name: str


class UserResponse(UserRequest):
    id: Optional[int] = None
    date_create: datetime


class UserResponseWithScores(UserResponse):
    scores: list[UserScoreResponse] | None = []


class TeamRequest(BaseModel):
    research_stage: int


class TeamResponse(TeamRequest):
    id: Optional[int] = None
    date_create: datetime


class UserResponseWithTeam(UserResponse):
    teams: list[TeamResponse] | None = []


class TeamResponseWithUsers(TeamResponse):
    users: list[UserResponseWithScores] | None = []


class UserScoreResponseWithTeamAndUser(UserScoreResponse):
    user: UserResponseWithScores
    team: TeamResponse


class UserSecure(UserRequest):
    username: str
    password: str

    @validator("username")
    def username_regexp_latin(cls, v: str):
        if not v.isalnum():
            raise ValueError("Username must be latin letters and numbers")
        return v

    @validator("password")
    def password_strong_regexp(cls, v: str):
        if not fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", v):
            raise ValueError("Password must be latin letters and numbers")
        return v
