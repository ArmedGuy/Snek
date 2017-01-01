from distutils.core import setup
setup(
  name = 'snek-orm',
  packages = ['snek', 'snek.processors','snek.models'], # this must be the same as the name above
  version = '0.0.7',
  description = 'ORM library created just for fun',
  author = 'Johan Jatko',
  author_email = 'armedguy@ludd.ltu.se',
  url = 'https://github.com/ArmedGuy/Snek', # use the URL to the github repo
  download_url = 'https://github.com/ArmedGuy/Snek/tarball/0.0.7',
  keywords = ['no','step','on','snek','orm'], # arbitrary keywords
  classifiers = []
)
