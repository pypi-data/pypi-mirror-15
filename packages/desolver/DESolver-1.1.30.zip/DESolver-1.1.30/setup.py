#!/usr/bin/env python

from distutils.core import setup

setup(name='DESolver',
      version='1.1.30',
      description='Differential Equation System Solver',
      author='Ekin Ozturk',
      author_email='ekin.ozturk@mail.utoronto.ca',
      install_requires=['numpy'],
      license='MIT',
      keywords=['ode solver', 'differential equation', 'differential system', 'ode system', 'non-linear ode'],
      url='https://github.com/Microno95/desolver',
      packages=['desolver'],
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          'Environment :: Console',
          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Topic :: Scientific/Engineering :: Mathematics',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      )
