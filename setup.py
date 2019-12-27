from setuptools import setup

setup(
        name='Snapshotilizer9000',
        version='0.1',
        author='Melvin Patmon',
        author_email="patmonm@gmail.com",
        description="Shotty is a tool to manage EC2 instances and snapshots",
        license="GPLv3+",
        packages=['shotty'],
        url="github link",
        install_requires=[
            'click',
            'boto3'
            ],
        entry_points='''
            [console_scripts]
            shotty=shotty.shotty:cli
        ''',
        )
