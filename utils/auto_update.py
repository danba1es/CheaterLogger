import git
import asyncio
import sys
import os
from datetime import datetime
import logging

logger = logging.getLogger('bot')

class AutoUpdater:
    def __init__(self):
        self.repo_url = os.getenv('GIT_REPO_URL')
        if not self.repo_url:
            raise ValueError("GIT_REPO_URL environment variable is not set")
        self.branch = 'main'
        self.repo = None
        self.initialize_repo()

    def initialize_repo(self):
        try:
            if not os.path.exists('.git'):
                logger.info(f"Initializing new repository")
                self.repo = git.Repo.init('.')
                self.repo.create_remote('origin', self.repo_url)
                # Create initial commit if needed
                if not self.repo.head.is_valid():
                    open('.gitignore', 'a').close()  # Create .gitignore if it doesn't exist
                    self.repo.index.add(['.gitignore'])
                    self.repo.index.commit('Initial commit')
            else:
                self.repo = git.Repo('.')
                if 'origin' not in self.repo.remotes:
                    self.repo.create_remote('origin', self.repo_url)

            # Ensure we're on main branch
            if 'main' not in self.repo.heads:
                self.repo.create_head('main')
            self.repo.heads.main.checkout()

            # Try to pull from remote if it exists
            try:
                self.repo.remotes.origin.fetch()
                self.repo.remotes.origin.pull('main')
            except git.exc.GitCommandError as e:
                logger.warning(f"Could not pull from remote: {str(e)}")

            logger.info("Repository initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize repository: {str(e)}")
            raise

    async def check_for_updates(self):
        try:
            # Fetch latest changes
            self.repo.remotes.origin.fetch()

            # Check if remote main branch exists
            if 'origin/main' not in self.repo.refs:
                logger.info("Remote main branch not found, pushing local changes")
                self.repo.remotes.origin.push('main:main')
                return

            # Compare with remote and pull if needed
            if self.repo.head.commit.hexsha != self.repo.refs['origin/main'].commit.hexsha:
                logger.info("Updates found! Pulling changes...")
                self.repo.remotes.origin.pull()
                logger.info("Restarting bot...")
                os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            logger.error(f"Error during auto-update: {str(e)}")

    async def start_update_checker(self, interval=300):  # Check every 5 minutes
        while True:
            await self.check_for_updates()
            await asyncio.sleep(interval)