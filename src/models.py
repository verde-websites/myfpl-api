from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import TEXT, ForeignKey, TIMESTAMP, PrimaryKeyConstraint, String

Base = declarative_base()

class Season(Base):
    """Season model"""
    __tablename__ = "seasons"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    season_name: Mapped[str] = mapped_column(String(255))  # Added length for VARCHAR

class Player(Base):
    """Player model"""
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    fpl_tracker_id: Mapped[int]
    first_name: Mapped[str] = mapped_column(String(255))  # Added length
    second_name: Mapped[str] = mapped_column(String(255))  # Added length
    web_name: Mapped[str] = mapped_column(String(255))  # Added length
    status: Mapped[str] = mapped_column(String(50))  # Added length, status might not need 255
    player_type: Mapped[str] = mapped_column(String(50))  # Added length, adjusted for type
    price: Mapped[float]
    form: Mapped[float]
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

class Team(Base):
    """Team model"""
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    fpl_tracker_id: Mapped[int]
    team_name: Mapped[str] = mapped_column(String(255))  # Added length
    short_name: Mapped[str] = mapped_column(String(50))  # Added length, adjusted for shorter name

class Gameweek(Base):
    """Gameweek model"""
    __tablename__ = "game_weeks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gameweek_number: Mapped[int]
    name: Mapped[str] = mapped_column(String(255))  # Added length
    transfer_deadline: Mapped[datetime] = mapped_column(TIMESTAMP)
    gameweek_active: Mapped[bool]
    gameweek_finished: Mapped[bool]
    data_checked: Mapped[bool]

class Fixture(Base):
    """Fixture model"""
    __tablename__ = "fixtures"
    id: Mapped[int] = mapped_column(primary_key=True)
    fpl_tracker_id: Mapped[int]
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    game_week_id: Mapped[int] = mapped_column(ForeignKey("game_weeks.id"))
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    kickoff_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    minutes: Mapped[int]
    finished: Mapped[bool]
    finished_provisional: Mapped[bool]
    provisional_start_time: Mapped[bool]
    started: Mapped[bool]
    home_team_score: Mapped[int]
    away_team_score: Mapped[int]

class PlayerFixture(Base):
    """PlayerFixture model"""
    __tablename__ = "player_fixtures"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player_fpl_tracker_id: Mapped[int]
    fixture_id: Mapped[int] = mapped_column(ForeignKey("fixtures.id"))
    game_week_id: Mapped[int] = mapped_column(ForeignKey("game_weeks.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    minutes: Mapped[int]
    clean_sheet: Mapped[bool]
    goals_scored: Mapped[int]
    goals_conceded: Mapped[int]
    assists: Mapped[int]
    saves: Mapped[int]
    own_goals: Mapped[int]
    penalties_saved: Mapped[int]
    penalties_missed: Mapped[int]
    yellow_cards: Mapped[int]
    red_cards: Mapped[int]
    bonus_points: Mapped[int]
    bps_points: Mapped[int]
    influence: Mapped[float]
    creativity: Mapped[float]
    threat: Mapped[float]
    ict_index: Mapped[float]
    started: Mapped[bool]
    expected_goals: Mapped[float]
    expected_assists: Mapped[float]
    expected_goal_involvements: Mapped[float]
    expected_goals_conceded: Mapped[float]
    total_points: Mapped[int]


class PlayerFplSeason(Base):
    """PlayerFplSeason model"""
    __tablename__ = "player_fpl_seasons"
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))

    __table_args__ = (
        PrimaryKeyConstraint("season_id", "player_id"),
    )

class TeamFplSeason(Base):
    """TeamFplSeason model"""
    __tablename__ = "team_fpl_seasons"
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    __table_args__ = (
        PrimaryKeyConstraint("season_id", "team_id"),
    )

class FPLScraperAccount(Base):
    """FPLScraperAccount model"""
    __tablename__ = "fpl_scraper_accounts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255))  # Added length
    password: Mapped[str] = mapped_column(String(255))  # Added length
    manager_id: Mapped[str] = mapped_column(String(255))  # Added length
    cookies: Mapped[str] = mapped_column(TEXT())  # Added length
    in_use: Mapped[bool]
    last_used: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    cookies_last_updated: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    active: Mapped[bool]


