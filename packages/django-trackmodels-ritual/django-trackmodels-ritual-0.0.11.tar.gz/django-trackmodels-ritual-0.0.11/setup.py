from setuptools import setup, find_packages

setup(
    name='django-trackmodels-ritual',
    version='0.0.11',
    namespace_packages=['grimoire', 'grimoire.django'],
    packages=find_packages(exclude=['trackmodels_proj', 'trackmodels_proj.*', 'sample', 'sample.*']),
    package_data={
        'grimoire.django.tracked': [
            'locale/*/LC_MESSAGES/*.*',
            'templates/admin/*.html',
            'templates/admin/tracked/*.html',
        ]
    },
    url='https://github.com/luismasuelli/django-trackmodels-ritual',
    license='LGPL',
    author='Luis y Anita',
    author_email='luismasuelli@hotmail.com',
    description='The trackmodels library is useful to set creation/update/delete dates on models and track by them',
    install_requires=['Django>=1.7', 'dateutils>=0.6.6']
)