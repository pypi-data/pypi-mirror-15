from distutils.core import setup
import os

setup(name="LiPyc",
        version="0.2.3.dev1",
        description="",
        author="Laurent Prosperi",
        author_email="laurent.prosperi@ens-cachan.fr",
        url="https://github.com/severus21/LiPyc",
        platforms="",
        license="Apache 2.0",
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',  #https://pypi.python.org/pypi?%3Aaction=list_classifiers

            'Intended Audience :: End Users/Desktop',
            'Topic :: Multimedia :: Graphics :: Viewers',

            'License :: OSI Approved :: Apache Software License',

            'Programming Language :: Python :: 3.4',
        ],
        packages=["lipyc", "lipyc.panels"],
        #install_requires=['PIL', 'tkinter'],
        keywords= ["pciture", "managment"],
        package_dir = {"lipyc": "src"},
        requires=["PIL", "tkinter"],
        data_files=[
            ("", ["album_default.png", "file_default.png"]),
        ]
    )
