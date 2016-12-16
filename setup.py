from distutils.core import setup
setup(
    name='ingressAPI',
    packages=['requests[socks]', 'lxml', 'beautifulsoup4'],
    version='0.1',
    description='Game Ingress API',
    author='lc4t',
    author_email='lc4t0.0@gmail.com',
    url='https://github.com/lc4t/ingress-api',  # use the URL to the github repo
    download_url='https://github.com/lc4t/ingress-api/tarball/0.1',  # I'll explain this in a second
    keywords=['ingress', 'api', 'google', 'intel', 'map'],  # arbitrary keywords
    classifiers=[],
)
