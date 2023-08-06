from distutils.core import setup

setup(
    name='angr-management',
    version='4.6.6.15',
    description='GUI for angr',
    url='https://github.com/angr/angr-management',
    packages=['angrmanagement', 'angrmanagement.ui', 'angrmanagement.data'],
    package_data={
        'angrmanagement.ui': ['*.enaml']
    },
    install_requires=[
        'angr',
        'enaml==0.9.8',
        'pygments',
        'websocket-client'
    ]
)
