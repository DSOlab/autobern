import setuptools

setuptools.setup(name='pybern',
    version='1.0-r1',
    description='Python Modules to Assist Bernese-based GNSS processing',
    url='',
    author='Xanthos Papanikolaou, Dimitris Anastasiou',
    author_email='xanthos@mail.ntua.gr, danast@mail.ntua.gr',
    packages=setuptools.find_packages(),#['pystrain', 'pystrain.geodesy', 'pystrain.iotools'],
    install_requires=['requests','paramiko', 'scp']
    )
