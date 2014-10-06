import os

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name='webtoys',
        version='1.0.0',
        description='Web Toys',
        long_description='Web Toys Site',
        classifiers=[
            "Programming Language :: Python",
            "Framework :: Django",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
        author='VRPlumber Consulting Inc.',
        author_email='mcfletch@vrplumber.com',
        url='http://www.vrplumber.com/programming/project/{{app_name}}',
        keywords='django',
        packages=find_packages(),
        include_package_data=True,
        license='MIT',
        # Dev-only requirements:
        # nose
        # pychecker
        # coverage
        # globalsub
        package_data = {
            'webtoys': [
            ],
        },
        install_requires=[
            'django',
            'django-annoying',
            'south',
        ],
        scripts = [
        ],
        entry_points = dict(
            console_scripts = [
            ],
        ),
    )

