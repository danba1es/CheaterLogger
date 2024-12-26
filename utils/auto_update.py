import git
import asyncio
import sys
import os
from datetime import datetime
import logging

logger = logging.getLogger('bot')

class AutoUpdater:
    def __init__(self, repo_url, branch='main'):
        self.repo_url = repo_url
        self.branch = branch
        self.repo = None
        self.initialize_repo()

    def initialize_repo(self):
        if not os.path.exists('.git'):
            self.repo = git.Repo.clone_from(self.repo_url, '.')
        else:
            self.repo = git.Repo('.')

    async def check_for_updates(self):
        try:
            origin = self.repo.remotes.origin
            origin.fetch()
            
            if self.repo.head.commit.hexsha != origin.refs[self.branch].commit.hexsha:
                logger.info("Updates found! Pulling changes...")
                origin.pull()
                logger.info("Restarting bot...")
                os.execv(sys.executable, ['python'] + sys.argv)
            
        except Exception as e:
            logger.error(f"Error during auto-update: {str(e)}")

    async def start_update_checker(self, interval=300):
        while True:
            await self.check_for_updates()
            await asyncio.sleep(interval)
