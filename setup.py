import setuptools

setuptools.setup(
    name='imagerenamer',
    version='0.0.1',
    description='Image batch renaming package',
    py_modules='imagerenamer',
    package_dir={'': 'src'},
    url='https://github.com/JSogaard/imagerenamer',
    packages=setuptools.find_packages(where='src')
)