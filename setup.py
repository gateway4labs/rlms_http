from setuptools import setup

classifiers=[
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

cp_license="MIT"

# TODO: depend on gateway4labs

setup(name='g4l_rlms_http',
      version='0.1',
      description="HTTP plug-in in the gateway4labs RLMS",
      classifiers=classifiers,
      author='Dept. SCC at UNED',
      author_email='accaminero@scc.uned.es',
      url='http://github.com/gateway4labs/rlms_http/',
      packages=['g4l_rlms_http'],
      license=cp_license,
     )

