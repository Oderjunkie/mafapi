from distutils.core import setup

setup(
  name = 'mafapi',
  packages = ['mafapi'],
  version = '0.3',
  license='GNU GPLv3',
  description = 'A simple python interfact for mafia.gg to create bots and clients.',
  author = 'Otesunkie',
  author_email = 'trickytests@gmail.com',
  url = 'https://github.com/Oderjunkie/mafapi',
  download_url = 'https://github.com/Oderjunkie/mafapi/archive/refs/tags/v_012.tar.gz',
  keywords = ['mafia', 'bot', 'connection', 'async', 'client'],
  install_requires=[
    'aiohttp',
    'asyncinit',
    'python-dateutil',
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
