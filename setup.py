import setuptools

setuptools.setup(
    name='imagerenamer',
    version='0.0.3',
    description='Image batch renaming package',
    py_modules=['imagerenamer'],
    entry_points = {
        'console_scripts': [
            'imagerenamer = imagerenamer:main'
        ]
    },
    install_requires=['exifread', 'fire', 'tqdm'],
    url='https://github.com/JSogaard/imagerenamer',
    packages=setuptools.find_packages()
)