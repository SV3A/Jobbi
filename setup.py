from setuptools import setup

setup(name='jobbi',
      version='0.2',
      description='Gets you tha jobs',
      url='http://github.com/SV3A/jobbi',
      author='Svend Andersen',
      author_email='sveas93@gmail.com',
      license='',
      packages=['jobbi'],
      install_requires=[
          'requests',
          'beautifulsoup4',
          'pyqt5'
      ],
      zip_safe=False)
