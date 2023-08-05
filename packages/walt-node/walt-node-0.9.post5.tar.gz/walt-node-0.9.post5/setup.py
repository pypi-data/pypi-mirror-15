from setuptools import setup, find_packages
setup(
    name = "walt-node",
    version = "0.9-5",
    packages = find_packages(),
    install_requires = ['rpyc>=3.3','plumbum>=1.4.2','walt-common'],

    # metadata for upload to PyPI
    author = "Etienne Duble",
    author_email = "etienne.duble@imag.fr",
    description = "WalT (Wireless Testbed) node daemon.",
    license = "LGPL",
    keywords = "WalT wireless testbed",
    url = "http://walt.forge.imag.fr/",

    namespace_packages = ['walt'],
    entry_points = {
        'console_scripts': [
            'walt-node-daemon = walt.node.daemon:run',
            'walt-node-install = walt.node.install:run',
            'walt-serial-autolog = walt.node.serial.autolog:run'
        ]
    },
    scripts = [ 'sh/walt-monitor', 'sh/walt-echo' ]
)

