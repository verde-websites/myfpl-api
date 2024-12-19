import asyncio
import yaml
from datetime import datetime
#from pathlib import Path

from sqlalchemy.future import select
from src.database import sessionmanager  # Import your database session manager
from src.models import FPLScraperAccount, Season  # Import the model

# Function to load fixtures from a YAML file
def load_fixture(file_path: str):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

async def seed_database():
    """Function to seed the database with fixtures from a YAML file."""
    await seed_seasons()
    #await seed_fpl_manager_sessions()

async def seed_seasons():
    """Function to seed the database with fixtures from a YAML file."""
    season_fixtures_path = "fixtures/seasons.yaml"  # Path to your fixture YAML file
    fpl_manager_sessions_path = "fixtures/fpl_manager_sessions.yaml"
    season_fixtures = load_fixture(season_fixtures_path)
    fpl_manager_sessions = load_fixture(fpl_manager_sessions_path)

    async with sessionmanager.session() as session:
        for fpl_manager_session in fpl_manager_sessions:
            new_fpl_manager_session = FPLScraperAccount(
                email=fpl_manager_session["email"],
                password=fpl_manager_session["password"],
                manager_id=fpl_manager_session["manager_id"],
                cookies=fpl_manager_session["cookies"],
                in_use=fpl_manager_session["in_use"],
                last_used=datetime.fromisoformat(fpl_manager_session["last_used"]) if fpl_manager_session["last_used"] else None,
                cookies_last_updated=datetime.fromisoformat(fpl_manager_session["cookies_last_updated"]) if fpl_manager_session["cookies_last_updated"] else None,
                active=fpl_manager_session["active"]
            )
            session.add(new_fpl_manager_session)
        await session.commit()
        await sessionmanager.close()

async def seed_fpl_manager_sessions():
    fixture_path = "fixtures/fpl_manager_sessions.yaml"  # Path to your fixture YAML file

    # Load the fixtures
    fixtures = load_fixture(fixture_path)

    async with sessionmanager.session() as session:
        for fixture in fixtures:
            # Check if the entry already exists
            stmt = select(FPLScraperAccount).where(FPLScraperAccount.email == fixture["email"])
            result = await session.execute(stmt)
            existing_entry = result.scalars().first()

            # If the entry doesn't exist, insert it
            if not existing_entry:
                new_manager = FPLScraperAccount(
                    email=fixture["email"],
                    password=fixture["password"],
                    manager_id=fixture["manager_id"],
                    cookies=fixture["cookies"],
                    in_use=fixture["in_use"],
                    last_used=datetime.fromisoformat(fixture["last_used"]) if fixture["last_used"] else None,
                    cookies_last_updated=datetime.fromisoformat(fixture["cookies_last_updated"]) if fixture["cookies_last_updated"] else None,
                    active=fixture["active"]
                )
                session.add(new_manager)

        # Commit the transaction
        await session.commit()
        await sessionmanager.close()
    
def main():
    """Main entry point to run the seed_database function and handle session cleanup."""
    asyncio.run(seed_database())

if __name__ == "__main__":
    # Run the seed database function asynchronously
    main()
