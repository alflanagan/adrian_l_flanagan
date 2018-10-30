"""A management command to read the list of languages used in projects from github, and add them
to the Technology model.
"""
import json
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from requests import Response, post, HTTPError
from requests.auth import HTTPBasicAuth
from software.models import Technology


class Command(BaseCommand):
    """Command definition for manage.py."""
    help = 'Retrieves languages used from github repos, adds to Technology if not already there.'

    def get_secret_key(self):
        try:
            with open('github_token.txt', 'r') as token_in:
                return token_in.read().strip()
        except IOError as ioe:
            raise CommandError("Unable to get github token from github_token.txt file.", ioe)

    def handle(self, *args, **options):
        get_languages = """
        {
        "query": "query {
                  viewer {
                    repositories(first: 100, privacy: PUBLIC) {
                      nodes {
                        languages(first: 20) {
                          edges {
                            node {
                              name
                            }
                          }
                        }
                      }
                    }
                  }
                }"
    }
        """
        response: Response = post("https://api.github.com/graphql",
                                  data=get_languages.replace("\n", ''),
                                  auth=HTTPBasicAuth(
                                      'alflanagan',
                                      self.get_secret_key()),
                                  )
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            raise CommandError("Failed retrieval from github.", http_err)
        data = json.loads(response.content.decode('utf-8'))
        repo_list = data['data']['viewer']['repositories']['nodes']
        lang_set = set()
        for repo in repo_list:
            nodes = repo["languages"]["edges"]
            for node in nodes:
                lang_set.add(node['node']['name'])
        for lang_name in lang_set:
            newtech = Technology(name=lang_name, notes='', stars=0)
            try:
                newtech.full_clean()
                self.stdout.write("Adding new technology {}".format(newtech.name))
                newtech.save()
            except ValidationError as validation_err:
                if set(validation_err.message_dict.keys()) == set(['name']):
                    self.stdout.write("Skipping language {}, it's already present.".format(
                        lang_name))
                else:
                    self.stderr.write("Failed to save language {}".format(lang_name))
                    self.stderr.write(str(validation_err))
