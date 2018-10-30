"""Models describing public software projects I authored or have been involved with."""
from django.db import models
#  pylint: disable=too-few-public-methods

class Category(models.Model):
    """A short name used to categorize 'something'."""

    class Meta:  # pylint: disable=missing-docstring
        ordering = ['name']
        verbose_name_plural = 'categories'
    name = models.CharField(max_length=20, help_text='Category title', primary_key=True)
    description = models.CharField(max_length=250, help_text='brief description', blank=True)
    def __str__(self):
        return "{} - ({})".format(self.name, self.description)


class Technology(models.Model):
    """Some piece of technology used in a software project.

    Might be a computer language, a library, a methodology, etc.
    """

    class Meta:  # pylint: disable=missing-docstring
        verbose_name_plural = 'technologies'
    name = models.CharField(max_length=30, primary_key=True, help_text='Short name of technology')
    notes = models.TextField(help_text='Notes to describe technology, my history with it, my '
                             'opinions, etc.', blank=True)
    stars = models.IntegerField(help_text='Totally subjective rating of the technology.',
                                null=True)
    def __str__(self):
        return self.name


class SoftwareProject(models.Model):
    """A public software project."""
    title = models.CharField(max_length=50,
                             help_text='Common name of the software project.', primary_key=True)
    github_repo = models.CharField(max_length=50,
                                   help_text='repo name in github (between "owner/" '
                                   'and ".git" in URL)',
                                   blank=True)
    # for github projects, much of this model is basically cached github data :)
    sync_github = models.BooleanField(default=True,
                                      help_text="Should this repo be automatically synchronized "
                                      "with Github?")
    created_at = models.DateTimeField(verbose_name="Date Created",
                                      help_text="Date repo first created or first document written")
    starred = models.BooleanField(default=False, help_text='Is the repo starred on github?')
    blurb = models.TextField(help_text='Short description of the project, about a paragraph.',
                             blank=True)
    is_fork = models.BooleanField(help_text='Is the repo a fork of a parent repo?')
    parent = models.CharField(max_length=250, blank=True,
                              help_text='Name of the parent repo, if any')
    fork_count = models.IntegerField(default=0, help_text='Count of forks of this repo')
    last_update = models.DateTimeField(null=True, help_text='Date/time of last push')
    license = models.CharField(max_length=50, help_text='The software license for the project')
    issue_count = models.IntegerField(default=0, help_text='Count of open github issues')
    stargazers = models.IntegerField(
        default=0, help_text='Count of users who starred this project')
    watchers = models.IntegerField(default=0, help_text='Count of users watching this project')
    primary_language = models.ForeignKey(Technology, models.PROTECT, help_text='Primary language',
                                         null=True, blank=True)
    categories = models.ManyToManyField('Category')
    def __str__(self):
        return "Project: {}".format(self.title)


class SoftwareTechUsed(models.Model):
    """Implements many-to-many relationship between SoftwareProject and Technology.

    Includes additional attributes of the relationship."""

    class Meta:  # pylint: disable=missing-docstring
        unique_together = ['project', 'tech']
        verbose_name_plural = 'software techs used'
    project = models.ForeignKey('SoftwareProject', models.CASCADE)
    tech = models.ForeignKey('Technology', models.CASCADE)
    version = models.CharField(max_length=40,
                               help_text='The version(s) of the tech used.',
                               blank=True)
    description = models.CharField(max_length=150,
                                   help_text='brief description of why/how tech is being used',
                                   blank=True)
    def __str__(self):
        return "{} USES {} {}".format(self.project.title, self.tech.name, self.version)
