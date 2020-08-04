
from setuptools import setup, find_packages

setup(name='login-html-hydra',
          version='0.0.4',
          description='aplicación de consent y logín de hydra',
          url='https://github.com/pablodanielrey/login-html-hydra',
          author='Desarrollo DiTeSi, FCE',
          author_email='ditesi@econo.unlp.edu.ar',
          classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6'
          ],
          packages=find_packages(exclude=['contrib', 'docs', 'test*']),
          install_requires=[
                            'users-model',
                            'login-model',
                            'requests',
                            'Flask',
                            'flask-wtf',
                            'SQLAlchemy',
                            'redis',
                            'google-api-python-client',
                            #'google_auth_oauthlib',
                            'google-auth',
                            'google-auth-httplib2',
                            'oauth2client'
                          ],
          entry_points={
          }

      )
