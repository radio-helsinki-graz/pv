from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='helsinki.program',
      version=version,
      description="Program Management for Radio Helsinki, Graz",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "CHANGES.rst")).read(),
      # Get more strings from http://www.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='django radio',
      author='Ernesto Rico-Schmidt',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Django',
          'python-dateutil',
          'PyYAML',
          'MySQL-python',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
