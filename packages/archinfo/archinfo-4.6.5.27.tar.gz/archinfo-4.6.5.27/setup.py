from distutils.core import setup
setup(
    name='archinfo',
    version='4.6.5.27',
    packages=['archinfo'],
    install_requires=[ 'capstone', 'pyelftools' ]
)
