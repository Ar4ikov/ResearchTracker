from fastapi import APIRouter
from pydantic.schema import List

from src.backend.database import User, Team, UserScore
from src.backend.intertnal import (
    UserRequest,
    UserResponse,
    UserResponseWithTeam,
    UserSecure,
    TeamRequest,
    TeamResponse,
    TeamResponseWithUsers,
    UserScoreRequest,
    UserScoreResponse,
    UserScoreResponseWithTeamAndUser,
)
from sqlmodel import Session
from src.backend.dependencies import engine

users = APIRouter()
teams = APIRouter()
scores = APIRouter()


@users.get("/user/{user_id}", response_model=UserResponseWithTeam)
def get_user(user_id: int):
    with Session(engine) as session:
        user_get = User.get(session, user_id)
        teams_ = user_get.teams
        scores_ = user_get.scores

        user_get.teams = teams_
        user_get.scores = scores_

        return user_get


@users.get("/users", response_model=List[UserResponseWithTeam])
def get_users():
    with Session(engine) as session:
        users_ = User.get_all(session)

        for u in users_:
            teams_ = u.teams
            print(teams_)
            u.teams = teams_

        return users


@users.post("/user", response_model=UserResponse, status_code=201)
def create_user(user: UserSecure):
    with Session(engine) as session:
        user_create = User.from_orm(user)
        user_create.create(session)

        teams_ = user_create.teams
        user_create.teams = teams_

        return user_create


@users.patch("/user/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserRequest):
    with Session(engine) as session:
        user_update = User.get(session, user_id)
        if user.first_name is not None: user_update.first_name = user.first_name
        if user.last_name is not None: user_update.last_name = user.last_name
        user_update.update(session)

        teams_ = user_update.teams
        user_update.teams = teams_

        return user_update


@users.delete("/user/{user_id}", response_model=UserResponse)
def delete_user(user_id: int):
    with Session(engine) as session:
        user_delete = User.get(session, user_id)
        user_delete.delete(session)

        teams_ = user_delete.teams
        user_delete.teams = teams_

        return user_delete


@teams.get("/team/{team_id}", response_model=TeamResponseWithUsers)
def get_team(team_id: int):
    with Session(engine) as session:
        team_get = Team.get(session, team_id)
        users_ = team_get.users

        for u in users_:
            scores_ = u.scores
            u.scores = scores_

        team_get.users = users_

        return team_get


@teams.get("/teams", response_model=List[TeamResponseWithUsers])
def get_teams():
    with Session(engine) as session:
        teams_ = Team.get_all(session)

        for t in teams_:
            users_ = t.users

            for u in users_:
                scores_ = u.scores
                u.scores = scores_

            print(users_)
            t.users = users_

        return teams_


@teams.post("/team/{team_id}/join/{user_id}", response_model=TeamResponse)
def join_team(team_id: int, user_id: int):
    with Session(engine) as session:
        team_join = Team.get(session, team_id)
        user_join = User.get(session, user_id)

        team_join.users.append(user_join)
        team_join.update(session)

        users_ = team_join.users
        team_join.users = users_

        return team_join


@teams.post("/team", response_model=TeamResponse, status_code=201)
def create_team(team: TeamRequest):
    with Session(engine) as session:
        team_create = Team.from_orm(team)
        team_create.create(session)

        users_ = team_create.users
        team_create.users = users_

        return team_create


@teams.patch("/team/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, team: TeamRequest):
    with Session(engine) as session:
        team_update = Team.get(session, team_id)
        if team.research_stage is not None: team_update.research_stage = team.research_stage
        team_update.update(session)

        users_ = team_update.users
        team_update.users = users_

        return team_update


@teams.delete("/team/{team_id}", response_model=TeamResponse)
def delete_team(team_id: int):
    with Session(engine) as session:
        team_delete = Team.get(session, team_id)
        team_delete.delete(session)

        users_ = team_delete.users
        team_delete.users = users_

        return team_delete


@scores.get("/score/{user_id}", response_model=UserScoreResponseWithTeamAndUser)
def get_score(user_id: int):
    with Session(engine) as session:
        score_get = UserScore.get_by_user(session, user_id)

        for s in score_get:
            team_ = Team.get(session, s.team_id)
            s.team = team_

            user_ = s.user
            s.user = user_

        return score_get


@scores.get("/score/{team_id}", response_model=List[UserScoreResponseWithTeamAndUser])
def get_score(team_id: int):
    with Session(engine) as session:
        score_get = UserScore.get_by_team(session, team_id)

        for s in score_get:
            team_ = Team.get(session, s.team_id)
            s.team = team_

            user_ = s.user
            s.user = user_

        return score_get


@scores.get("/scores", response_model=List[UserScoreResponse])
def get_scores():
    with Session(engine) as session:
        scores_ = UserScore.get_all(session)
        return scores_


@scores.post("/score", response_model=UserScoreResponse, status_code=201)
def create_score(score: UserScoreRequest):
    with Session(engine) as session:
        score_create = UserScore.from_orm(score)
        score_create.create(session)
        return score_create


@scores.patch("/score/{user_id}", response_model=UserScoreResponse)
def update_score(user_id: int, score: UserScoreRequest):
    with Session(engine) as session:
        score_update = UserScore.get_by_user(session, user_id)
        if score.score is not None: score_update.score = score.score
        score_update.update(session)
        return score_update


@scores.delete("/score/{user_id}", response_model=UserScoreResponse)
def delete_score(user_id: int):
    with Session(engine) as session:
        score_delete = UserScore.get_by_user(session, user_id)
        score_delete.delete(session)
        return score_delete
