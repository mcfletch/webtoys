import os

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name='toys',
        version='1.0.0',
        description='toys',
        long_description='toys',
        classifiers=[
            "Programming Language :: Python",
            "Framework :: Django",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
        author='VRPlumber Consulting Inc.',
        author_email='mcfletch@vrplumber.com',
        url='http://www.vrplumber.com/programming/project/toys',
        keywords='django',
        packages=find_packages(),
        include_package_data=True,
        license='MIT',
        # Dev-only requirements:
        # pychecker
        # coverage
        # globalsub
        package_data = {
            'toys': [
                'templates/toys/*.html',
                'static/js/*',
                'static/css/*',
                'static/img/*',
                'static/materialize/js/*', 
                'static/materialize/css/*', 
                'static/materialize/fonts/*', 
            ],
        },
        install_requires=[
            'django',
            'django-annoying',
        ],
        scripts = [
        ],
        entry_points = dict(
            console_scripts = [
            ],
        ),
    )

