"""Models to define navigation links for site (overkill?)."""
from django.db import models

# Create your models here.

class Section(models.Model):
    """A section heading in a list of links."""

    title = models.CharField(max_length=50, primary_key=True,
                             help_text="A section heading in a menu.")
    description = models.CharField(max_length=255,
                                   help_text="A longer description of the section, for e.g. a"
                                   " tooltip")

class Link(models.Model):
    """A navigation link."""

    target = models.CharField(max_length=150)
    title = models.CharField(max_length=80)
