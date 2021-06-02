from distutils.core import setup

setup(
  name = 'mafapi',
  packages = ['mafapi'],
  version = '0.1',
  license='GNU GPLv3',
  description = 'A simple python interfact for mafia.gg to create bots and clients.',
  author = 'Otesunkie',
  author_email = 'trickytests@gmail.com',
  url = 'https://github.com/Oderjunkie/mafapi',
  download_url = 'https://github.com/Oderjunkie/mafapi/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['mafia', 'bot', 'connection', 'async', 'client'],
  install_requires=[            # I get to this in a second
    'aiohttp',
    'asyncinit',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
  ]
)