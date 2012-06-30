try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

dependencies = [
            'PyYAML >= 3.10'
        ]

setup( name='redline'
      ,version='0.0.1'
      ,packages=['redline',]
      ,entry_points={
            'console_scripts':[
                'redline = redline.cli:begin'
            ]
          }
      ,install_requires=dependencies
      )
