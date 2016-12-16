from distutils.core import setup

setup(
    name = 'ingressAPI',
    packages = ['ingressAPI'],
    version = '0.1',
    description = 'Game Ingress API',
    author = 'lc4t',
    author_email = 'lc4t0.0@gmail.com',
    keywords = ['ingress', 'api', 'google', 'intel', 'map'],
    install_requires = ['requests[socks]', 'lxml', 'beautifulsoup4'],
    license = 'GPL3.0',
    url = 'https://github.com/lc4t/ingress-api',
    download_url = 'https://github.com/lc4t/ingress-api/tarball/0.1',
)
