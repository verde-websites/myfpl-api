from datetime import datetime
from src.models import FPLScraperAccount as FPLScraperAccountModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.fpl_scraper_account import FPLScraperAccountSchema

async def get_fpl_scraper_account_from_manager_id(session: AsyncSession, manager_id: str) -> FPLScraperAccountModel:
    """Get FPLScraperAccount by manager_id"""
    stmt = select(FPLScraperAccountModel).where(FPLScraperAccountModel.manager_id == manager_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_fpl_scraper_account_from_email(session: AsyncSession, email: str) -> FPLScraperAccountModel:
    """Get FPLScraperAccount by email"""
    stmt = select(FPLScraperAccountModel).where(FPLScraperAccountModel.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def update_fpl_scraper_account(session: AsyncSession, account_id: int, **kwargs):
    """Update specified fields for an FPLScraperAccount."""
    # Fetch the account by ID
    result = await session.execute(
        select(FPLScraperAccountModel).where(FPLScraperAccountModel.id == account_id)
    )
    account = result.scalar_one_or_none()

    if account is None:
        raise ValueError(f"No account found with ID {account_id}")

    # Update fields dynamically based on kwargs
    for key, value in kwargs.items():
        if hasattr(account, key):
            setattr(account, key, value)
        else:
            raise AttributeError(f"FPLScraperAccount has no attribute '{key}'")

    # Set last_used to now if in_use is set to True
    if kwargs.get("in_use") is True:
        account.last_used = datetime.utcnow()

    # Add the account back to the session and commit changes
    session.add(account)
    await session.commit()

async def create_fpl_scraper_account(session: AsyncSession, fpl_manager_session: FPLScraperAccountSchema):
    """Create FPLScraperAccount"""
    stmt = insert(FPLScraperAccountModel).values(
        email=fpl_manager_session.email,
        password=fpl_manager_session.password,
        manager_id=fpl_manager_session.manager_id,
        cookies=fpl_manager_session.cookies,
        in_use=fpl_manager_session.in_use,
        last_used=fpl_manager_session.last_used,
        cookies_last_updated=fpl_manager_session.cookies_last_updated,
        active=fpl_manager_session.active,
    )
    await session.execute(stmt)

async def get_next_available_fpl_scraper_account(session: AsyncSession) -> FPLScraperAccountSchema:
    """Get next available FPLScraperAccount."""
    result = await session.execute(
        select(FPLScraperAccountModel).where(
            (FPLScraperAccountModel.in_use == False) & (FPLScraperAccountModel.active == True)
        )
    )
    account = result.scalar_one_or_none()
    if account is None:
        raise Exception("No available scraper accounts")
    
    account.in_use = True
    account.last_used = datetime.utcnow()
    session.add(account)  # Mark the account as in use
    return FPLScraperAccountSchema.model_validate(account)
  #  """Get next available FPLScraperAccount"""
  #  async with session.begin():
  #      account = await session.execute(
  #              select(FPLScraperAccountModel).where(FPLScraperAccountModel.in_use == False and FPLScraperAccountModel.active == True)
  #          ).scalar_one_or_none()
  #      if account is None:
  #          raise Exception("No available scraper accounts")
  #      account.in_use = True
  #      account.last_used = datetime.timestamp.utcnow()
  #      session.add(account)
  #      return account