import base64
from datetime import datetime
import pickle
from curl_cffi import requests 

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from ...crud.fpl_scraper_account import (
    get_fpl_scraper_account_from_manager_id, 
    get_next_available_fpl_scraper_account, 
    update_fpl_scraper_account
)

from endpoints import FPLEndpoints
from ...schemas.fpl.bootstrap_static import BootstrapStaticFPLResponse
from ...schemas.fpl_scraper_account import FPLScraperAccountSchema

class FPLScraperClient:
    """FPL API Scraper Client"""
    def __init__(self, db: AsyncSession):
        print('Initializing FPL Scraper Client')
        self.db = db
        self.fpl_scraper_account = FPLScraperAccountSchema
        self.account_session = requests.Session()
    
    async def start(self):
        """Retrieve FPL Scraper Account from the database"""
        account = await get_next_available_fpl_scraper_account(self.db)
        self.fpl_scraper_account = account
        if self.fpl_scraper_account.cookies == "":
            print("No cookies for scraper account. Logging in to FPL...")
            await self.login()
        else:
            print("Cookies found for scraper account. Verifying they are still valid...")
            pickled_cookies = pickled_cookies = base64.b64decode(self.fpl_scraper_account.cookies.encode("utf-8"))
            self.account_session.cookies.jar._cookies.update(pickle.loads(pickled_cookies))
            await self.verify_cookies_are_valid()
            ## Need to login
        

    async def stop(self):
        """Stop the client"""
        self.fpl_scraper_account.in_use = False
        self.fpl_scraper_account.last_used = datetime.utcnow()
        pickled_cookies = pickle.dumps(self.account_session.cookies.jar._cookies)
        cookies_base64 = base64.b64encode(pickled_cookies).decode("utf-8")
        await update_fpl_scraper_account(self.db, self.fpl_scraper_account.id, in_use=self.fpl_scraper_account.in_use, last_used=self.fpl_scraper_account.last_used, cookies=cookies_base64)

    async def retrieveNextBestScraperAccount(self):
        """Retrieve next best scraper account"""
        fpl_scraper_account = await get_fpl_scraper_account_from_manager_id(self.db, self.fpl_scraper_account.manager_id, )
        if fpl_scraper_account is None:
            raise Exception("FPL Scraper Account not found")
    
    async def login(self):
        """Login to FPL"""

        data = {
            "login": self.fpl_scraper_account.email,
            "password": self.fpl_scraper_account.password,
            "app": "plfpl-web",
            "redirect_uri": FPLEndpoints.LOGIN_REDIRECT.value
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.account_session.post(FPLEndpoints.LOGIN.value, data=data, headers=headers, impersonate="chrome")

        if not response.ok:
            raise Exception("Login failed")

    async def verify_cookies_are_valid(self):
        """Verify cookies are valid"""
        response = self.account_session.get(FPLEndpoints.ME.value, headers={"Accept": "application/json"}, impersonate="chrome")
        if response.ok and response.json()["player"]:
            print("Cookies are valid")
        else:
            print("Cookies are not valid, attempting to log in again")
            await self.login()

    async def save_cookies(self, cookies):
        """Save cookies to the database"""
        self.fpl_scraper_account.cookies = cookies
        await update_fpl_scraper_account(self.db, self.fpl_scraper_account.id, cookies=cookies)
    
    async def get_bootstrap_static(self):
        """Get bootstrap static"""
        try:
            response = self.account_session.get(FPLEndpoints.BOOTSTRAP_STATIC.value, headers={"Accept": "application/json"}, impersonate="chrome")
            response.raise_for_status()

            data = response.json()
            boostrap_static = BootstrapStaticFPLResponse(**data)
            return boostrap_static
        except ValidationError as e:
            print("Failed to parse response into BootstrapStaticFPLResponse", e)
        except requests.RequestError as e:
            print("Failed to get bootstrap static", e)
    
    async def get_bootstrap_static_players(self):
        """Get bootstrap static players"""
        bootstrap_static = await self.get_bootstrap_static()
        return bootstrap_static.players
    
    async def get_bootstrap_static_teams(self):
        """Get bootstrap static teams"""
        bootstrap_static = await self.get_bootstrap_static()
        return bootstrap_static.teams
    
    async def get_bootstrap_static_gameweeks(self):
        """Get bootstrap static gameweeks"""
        bootstrap_static = await self.get_bootstrap_static()
        return bootstrap_static.gameweeks

