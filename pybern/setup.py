import setuptools

setuptools.setup(name='pybern',
    version='1.4-b1',
    description='Python Modules to Assist Bernese-based GNSS processing (upd for BERN54)',
    url='',
    author='Xanthos Papanikolaou, Dimitris Anastasiou',
    author_email='xanthos@mail.ntua.gr, danastasiou@mail.ntua.gr',
    packages=setuptools.find_packages(),#['pystrain', 'pystrain.geodesy', 'pystrain.iotools'],
    install_requires=['requests','paramiko', 'scp']
    )
