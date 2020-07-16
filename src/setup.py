
from setuptools import setup, find_packages

setup(name='login-html-hydra',
          version='0.0.1',
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
                            #'gunicorn',
                            'requests',
                            'Flask',
                            'flask-wtf',
                            'users-model',
                            'login-model',
                            'SQLAlchemy'
                            #'flask_jsontools'
                            #'flask-cors',
                            #'Flask-OIDC',
                            #'microservices_common>=2.0.7a1'
                          ],
          entry_points={
          }

      )
