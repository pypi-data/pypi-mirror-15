from distutils.core import setup
setup(
  name = 'courspider',
  packages = ['courspider'],
  version = '0.4',
  description = 'A webscraper API to scrape course data from u of t calenders',
  author = 'Tony Xiao',
  author_email = 'zylphrex@gmail.com',
  license = 'MIT',
  install_requires = [
    'beautifulsoup4',
  ],
  url = 'https://github.com/Zylphrex/courspider',
  download_url = 'https://github.com/Zylphrex/courspider/tarball/0.4',
  keywords = ['u of t', 'University', 'Toronto', 'course', 'data'],
  classifiers = [],
)
