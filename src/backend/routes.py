import json
from datetime import datetime
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
# from pydantic.schema import List
from typing import List, Annotated
from json import loads, dumps

from src.backend.database import User, Team, UserScore
from src.backend.intertnal import (
    UserRequest,
    UserResponse,
    UserResponseWithTeam,
    UserResponseWithScores,
    UserResponseWithTeamAndScores,
    UserSecureRequest,
    TeamRequest,
    TeamResponse,
    TeamResponseWithUsers,
    UserScoreRequest,
    UserScoreResponse,
    UserScoreResponseWithTeamAndUser, UserScorePatch, Stage,
)
from sqlmodel import Session
from src.backend.dependencies import engine, get_current_active_user, get_password_hash

users = APIRouter()
teams = APIRouter()
scores = APIRouter()
stages = APIRouter()

research_stage_config = Path(__file__).parent.parent.parent / "stage.json"

if not research_stage_config.exists():
    with research_stage_config.open('w') as f:
        f.write(dumps({"stage": 1}))


@users.get("/users/me", response_model=UserResponseWithTeamAndScores)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    with Session(engine) as session:
        user = User.get(session, current_user.id)
        teams_ = user.teams
        scores_ = user.scores

        user.teams = teams_
        user.scores = scores_

    return user


@users.get("/user/{user_id}", response_model=UserResponseWithTeamAndScores)
def get_user(user_id: int):
    with Session(engine) as session:
        user_get = User.get(session, user_id)

        if user_get is None:
            raise HTTPException(status_code=404, detail="User not found")

        teams_ = user_get.teams
        scores_ = user_get.scores

        user_get.teams = teams_
        user_get.scores = scores_

        return user_get


@users.get("/users", response_model=List[UserResponseWithTeamAndScores])
def get_users():
    with Session(engine) as session:
        users_ = User.get_all(session)

        for u in users_:
            teams_ = u.teams
            scores_ = u.scores

            u.teams = teams_
            u.scores = scores_

        return users_


@users.post("/user", response_model=UserResponse, status_code=201)
def create_user(user: UserSecureRequest):
    with Session(engine) as session:
        user_create = User.from_orm(user)
        user_create.password = get_password_hash(user.password)
        user_create.create(session)

        teams_ = user_create.teams
        user_create.teams = teams_

        return user_create


@users.patch("/user/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserRequest):
    with Session(engine) as session:
        user_update = User.get(session, user_id)

        if user_update is None:
            raise HTTPException(status_code=404, detail="User not found")

        if user.first_name is not None: user_update.first_name = user.first_name
        if user.last_name is not None: user_update.last_name = user.last_name
        user_update.update(session)

        return user_update


@users.delete("/user/{user_id}", response_model=UserResponse)
def delete_user(user_id: int):
    with Session(engine) as session:
        user_delete = User.get(session, user_id)

        if user_delete is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_delete.delete(session)

        return user_delete


@teams.get("/team/{team_id}", response_model=TeamResponseWithUsers)
def get_team(team_id: int):
    with Session(engine) as session:
        team_get = Team.get(session, team_id)

        if team_get is None:
            raise HTTPException(status_code=404, detail="Team not found")

        users_ = team_get.users

        for u in users_:
            scores_ = u.scores
            u.scores = scores_

        team_get.users = users_

        return team_get


@teams.get("/teams/{stage}", response_model=List[TeamResponseWithUsers])
def get_teams_by_stage(stage: int):
    with Session(engine) as session:
        _teams = Team.get_by_stage(session, stage)

        for t in _teams:
            users_ = t.users

            for u in users_:
                scores_ = u.scores
                u.scores = scores_

            t.users = users_

        return _teams


@teams.get("/teams", response_model=List[TeamResponseWithUsers])
def get_teams():
    with Session(engine) as session:
        teams_ = Team.get_all(session)

        for t in teams_:
            users_ = t.users

            for u in users_:
                scores_ = u.scores
                u.scores = scores_

            t.users = users_

        return teams_


@teams.patch("/team/{team_id}/join/{user_id}", response_model=TeamResponse)
def join_team(team_id: int, user_id: int):
    with Session(engine) as session:
        team_join = Team.get(session, team_id)
        user_join = User.get(session, user_id)

        if user_join is None:
            raise HTTPException(status_code=404, detail="User not found")

        if team_join is None:
            raise HTTPException(status_code=404, detail="Team not found")

        if user_join in team_join.users:
            raise HTTPException(status_code=409, detail="User already in team")

        team_join.users.append(user_join)
        team_join.update(session)

        users_ = team_join.users
        team_join.users = users_

        return team_join


@teams.patch("/team/{team_id}/leave/{user_id}", response_model=TeamResponse)
def leave_team(team_id: int, user_id: int):
    with Session(engine) as session:
        team_leave = Team.get(session, team_id)
        user_leave = User.get(session, user_id)

        if user_leave is None:
            raise HTTPException(status_code=404, detail="User not found")

        if team_leave is None:
            raise HTTPException(status_code=404, detail="Team not found")

        if user_leave not in team_leave.users:
            raise HTTPException(status_code=409, detail="User not in team")

        team_leave.users.remove(user_leave)
        team_leave.update(session)

        users_ = team_leave.users
        team_leave.users = users_

        return team_leave


@teams.post("/team", response_model=TeamResponse, status_code=201)
def create_team(team: TeamRequest):
    with Session(engine) as session:
        team_create = Team.from_orm(team)
        team_create.create(session)

        return team_create


@teams.patch("/team/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, team: TeamRequest):
    with Session(engine) as session:
        team_update = Team.get(session, team_id)

        if team_update is None:
            raise HTTPException(status_code=404, detail="Team not found")

        if team.research_stage is not None: team_update.research_stage = team.research_stage
        team_update.update(session)

        return team_update


@teams.delete("/team/{team_id}", response_model=TeamResponse)
def delete_team(team_id: int):
    with Session(engine) as session:
        team_delete = Team.get(session, team_id)

        if team_delete is None:
            raise HTTPException(status_code=404, detail="Team not found")

        team_delete.delete(session)

        return team_delete


@scores.get("/score/{user_id}", response_model=list[UserScoreResponseWithTeamAndUser])
def get_score(user_id: int):
    with Session(engine) as session:
        score_get = UserScore.get_by_user(session, user_id)

        for s in score_get:
            team_ = s.team
            s.team = team_

            user_ = s.user
            s.user = user_

        return score_get


@scores.get("/score/{team_id}", response_model=list[UserScoreResponseWithTeamAndUser])
def get_score(team_id: int):
    with Session(engine) as session:
        score_get = UserScore.get_by_team(session, team_id)

        for s in score_get:
            team_ = s.team
            s.team = team_

            user_ = s.user
            s.user = user_

        return score_get


@scores.get("/scores", response_model=list[UserScoreResponseWithTeamAndUser])
def get_scores():
    with Session(engine) as session:
        scores_ = UserScore.get_all(session)

        for s in scores_:
            team_ = s.team
            s.team = team_

            user_ = s.user
            s.user = user_

        return scores_


@scores.post("/score", response_model=UserScoreResponse, status_code=201)
def create_score(score: UserScoreRequest):
    with Session(engine) as session:
        # get recent user score
        scores_ = UserScore.get_by_user(session, score.user_id)

        if len(scores_) > 0:
            # check timedelta between last score and new score < 10 min
            if (datetime.now() - scores_[-1].date_create).total_seconds() < 600:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "message": "Вы можете отправлять результаты не чаще чем раз в 10 минут",
                        "estimated_time": 600 - (datetime.now() - scores_[-1].date_create).total_seconds()
                    })

        score_create = UserScore.from_orm(score)
        score_create.create(session)
        return score_create


@scores.patch("/score/{score_id}", response_model=UserScoreResponse)
def update_score(score_id: int, score: UserScorePatch):
    with Session(engine) as session:
        score_update = UserScore.get(session, score_id)

        if score_update is None:
            raise HTTPException(status_code=404, detail="Score not found")

        if score.score is not None: score_update.score = score.score
        score_update.update(session)
        return score_update


@scores.delete("/score/{score_id}", response_model=UserScoreResponse)
def delete_score(score_id: int):
    with Session(engine) as session:
        score_delete = UserScore.get(session, score_id)

        if score_delete is None:
            raise HTTPException(status_code=404, detail="Score not found")

        score_delete.delete(session)
        return score_delete


@scores.delete("/score/{user_id}", response_model=UserScoreResponse)
def delete_score(user_id: int):
    with Session(engine) as session:
        score_delete = UserScore.get_by_user(session, user_id)
        for s in score_delete:
            s.delete(session)

        return score_delete


@scores.post("/score/export")
def export_scores():
    with Session(engine) as session:
        scores_ = UserScore.get_all(session)

    df = pd.DataFrame([s.dict() for s in scores_], index=[s.id for s in scores_])
    df = df.drop(columns=["id"])
    df.to_csv("scores.csv")

    return FileResponse(path="scores.csv", status_code=200, media_type="text/csv", filename="scores.csv")


@stages.get("/stage", response_model=Stage)
def get_stage():
    with research_stage_config.open("r") as f:
        stage_json = loads(f.read())

    return stage_json


@stages.post("/stage")
def set_stage(stage: int):
    with research_stage_config.open("w") as f:
        f.write(dumps({"stage": stage}))

    return {"success": True}
