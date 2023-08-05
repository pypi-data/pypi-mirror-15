from setuptools import setup

setup(name='jcore_api',
      version='1.0.dev1',
      description='jcore.io API',
      url='http://github.com/jcoreio/jcore-api-py',
      author='Andy Edwards',
      author_email='andy@jcore.io',
      license='MIT',
      packages=['jcore_api'],
      install_requires=[
        'six',
        'websocket-client'
      ],
      test_suite='nose2.collector.collector',
      tests_require=['nose2'],
      zip_safe=False)
