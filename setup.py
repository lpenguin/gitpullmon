from setuptools import setup

setup(name='gitpullmon',
      version='0.1',
      license='MIT',
      packages=['gitpullmon'],
      zip_safe=False,
      entry_points={
          'console_scripts': [
                'gitpullmon=gitpullmon.cli:main',
          ]
      },
       install_requires=[
          'gitpython',
      ],
)