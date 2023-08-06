import os
from setuptools import setup

# {name}
# {desc}


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="{name}",
    version="0.0.1",
    description="{desc}",
    author="{author}",
    author_email="{email}",
    license="{license}",
    keywords="{keywords}",
    url="{url}",
    packages=['{name}'],
    package_dir={{'{name}': '{name}'}},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        {license_long}
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
    ],
    entry_points={{
        'console_scripts': [
            '{name}={name}:main',
        ],
    }},
    # If you get errors running setup.py install:
    # zip_safe=False,
    #
    # For including non-python files:
    # package_data={{
    #     '{name}': ['templates/*.html'],
    # }},
    # include_package_data=True,
)
