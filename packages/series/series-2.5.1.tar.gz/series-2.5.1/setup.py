from setuptools import setup, find_packages

from tek.config.write import write_pkg_config

version_parts = (2, 5, 1)
version = '.'.join(map(str, version_parts))

write_pkg_config('.', 'series.conf', 'series')
setup(
    name='series',
    version=version,
    author='Torsten Schmits',
    author_email='torstenschmits@gmail.com',
    license='GPLv3',
    packages=find_packages(exclude=['tests', 'tests.*', 'unit', 'unit.*']),
    data_files=[('share/series/config', ['series.conf'])],
    package_data={
        '': ['alembic/env.py', 'alembic.ini', 'alembic/versions/*.py'],
    },
    install_requires=[
        'tryp>=7.4.0',
        'requests',
        'tek<=3.2.0',
        'tek-utils>=3.0.2',
        'sqlpharmacy',
        'crystalmethod',
        'lxml',
        'feedparser',
        'flask',
        'alembic',
        'tvrampage',
        'python-dateutil'
    ],
    entry_points={
        'console_scripts': [
            'serieslibd = series.library.cli:libd',
            'serieslibc = series.library.cli:libc',
            'seriesgetd = series.get.cli:getd',
            'seriesgetc = series.get.cli:getc',
            'subsync_dir = series.subsync:subsync_dir_cli',
            'subsync_cwd = series.subsync:subsync_cwd',
            'subsync_auto = series.subsync:subsync_auto',
            'handle_episode = series.handle_episode:handle_episode_cli',
            'store_episode = series.store_episode:store_episode_cli',
        ]
    }
)
