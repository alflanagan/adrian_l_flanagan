"""A management command to read projects from github, and add them to the software app."""
import json
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from requests import Response, post, HTTPError
from requests.auth import HTTPBasicAuth
from software.models import Technology, SoftwareProject


class Command(BaseCommand):
    """Command definition for manage.py."""
    help = 'Retrieves data about github repos, adds them to software models.'

    @staticmethod
    def get_secret_key():
        """Reads github access token from a disk file."""
        try:
            with open('github_token.txt', 'r') as token_in:
                return token_in.read().strip()
        except IOError as ioe:
            raise CommandError("Unable to get github token from github_token.txt file.", ioe)

    def handle(self, *args, **options):
        """
        Implements the command.
        Retrieves a list of public repos from github, uses the data to create SoftwareProject
        objects if they do not already exist.
        """
        get_repos = """
        {
        "query": "query {
                    viewer {
                      login
                      repositories(first: 100, privacy: PUBLIC) {
                        nodes {
                          name
                          isFork
                          parent {
                            nameWithOwner
                          }
                          createdAt
                          description
                          diskUsage
                          forkCount
                          pushedAt
                          primaryLanguage {
                            name
                          }
                          licenseInfo {
                            name
                            nickname
                          }
                          issues {
                            totalCount
                          }
                          languages(first: 100) {
                            edges {
                              node {
                                name
                              }
                            }
                          }
                          stargazers {
                            totalCount
                          }
                          watchers {
                            totalCount
                          }
                        }
                        pageInfo {
                          hasNextPage
                        }
                      }
                    }
                  }"
        }
        """
        response: Response = post("https://api.github.com/graphql",
                                  data=get_repos.replace("\n", ''),
                                  auth=HTTPBasicAuth(
                                      'alflanagan',
                                      self.get_secret_key()),
                                  )
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            raise CommandError("Failed retrieval from github.", http_err)
        data = json.loads(response.content.decode('utf-8'))
        if data['data'] is None:
            for err in data['errors']:
                self.stderr.write(err['message'])
            raise CommandError('Github API returned error messages')
        repo_list = data['data']['viewer']['repositories']['nodes']
        self.stdout.write('Retrieved data on {} repositories.'.format(len(repo_list)))
        username = data['data']['viewer']['login']
        for repo in repo_list:
            self.save_repo(username, repo)
        if data['data']['viewer']['repositories']['pageInfo']['hasNextPage']:
            self.stderr.write('WARNING: there are more repos available than this command')
            self.stderr.write('         retrieves. Time to fix it!!')

    def save_repo(self, owner, repo_dict):
        """
        Use the values in `repo_dict` (from github) to construct a `SoftwareProject`, save
        it to the database if it doesn't exist. Writes status messages to ``self.stdout``, errors
        to ``self.stderr``.
        """
        title = repo_dict['name']
        is_fork = repo_dict['isFork']
        parent = repo_dict['parent']['nameWithOwner'] if is_fork else ''
        created_at = repo_dict['createdAt']
        blurb = repo_dict['description'] if repo_dict['description'] else ''
        starred = int(repo_dict['stargazers']['totalCount'])
        watchers = int(repo_dict['watchers']['totalCount'])
        fork_count = repo_dict['forkCount']
        pushed = repo_dict['pushedAt']
        primary_language = (repo_dict['primaryLanguage']['name'] if
                            repo_dict['primaryLanguage'] else None)
        proj_license = 'none'
        if repo_dict['licenseInfo'] is not None:
            proj_license = repo_dict['licenseInfo']['nickname']
            if proj_license is None or proj_license == '':
                proj_license = repo_dict['licenseInfo']['name']
        issue_count = repo_dict['issues']['totalCount']

        # self.stdout.write('Repo: {}/{}{} ({}) {} {} {} {}{}'.format(username,
                          # title, ' (fork of {})'.format(parent) if is_fork else '',
                          # created_at, starred, watchers, fork_count, proj_license,
                          # '\n\t' + blurb if blurb else ''))
        tech = self.tech_get_or_create(primary_language)

        project = SoftwareProject(title=title,
                                  github_repo=title,
                                  sync_github=True,
                                  created_at=created_at,
                                  starred=starred > 0,
                                  blurb=blurb,
                                  is_fork=is_fork,
                                  parent=parent,
                                  fork_count=fork_count,
                                  last_update=pushed,
                                  license=proj_license,
                                  issue_count=issue_count,
                                  stargazers=starred,
                                  watchers=watchers,
                                  primary_language=tech)
        try:
            project.full_clean()
            self.stdout.write("Adding new project {}".format(project.title))
            project.save()
        except ValidationError as validation_err:
            if set(validation_err.message_dict.keys()) == set(['title']):
                self.stdout.write("Skipping project {}/{}, it's already present.".format(
                    owner, title))
            else:
                self.stderr.write("Failed to save project {}/{}".format(owner, title))
                self.stderr.write(str(validation_err))

    @staticmethod
    def tech_get_or_create(tech_name):
        """
        Retrieves the technology named `tech_name` from db, or creates it if not there.

        @returns {Technology|None} Instance, or None if tech_name is falsey.
        """
        tech = None
        if tech_name:
            try:
                tech = Technology.objects.get(name=tech_name)
            except Technology.DoesNotExist:
                tech = Technology(name=tech_name, notes='', stars=0)
                tech.full_clean()
                tech.save()
        return tech
