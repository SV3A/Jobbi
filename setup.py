from setuptools import setup

setup(name='get_job',
      version='0.1',
      description='Get you the jobs',
      url='http://github.com/SV3A/get-job',
      author='Svend Andersen',
      author_email='sveas93@gmail.com',
      license='',
      packages=['get_job'],
      install_requires=[
          'requests',
          'beautifulsoup4',
          'pyqt5'
      ],
      zip_safe=False)
