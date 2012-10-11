import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
VERSION = open(os.path.join(here, 'VERSION.txt')).read()

requires = setup(name='zf.githubreceiver',
      version=VERSION.strip(),
      description='zf.githubreceiver',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      namespace_packages=('zf',),
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[ 'setuptools'
                       , 'pyramid'
                       , 'pyramid_mailer'
                       , 'pyramid_tm'
                       , 'github.event'
                       , 'requests'
                       ],
      test_suite="zf.githubreceiver",
      entry_points = """\
      [paste.app_factory]
      main = zf.githubreceiver:main
      """,
      paster_plugins=['pyramid'],
      )

