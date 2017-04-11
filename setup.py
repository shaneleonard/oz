from setuptools import setup

setup(name='oz-cli',
      version='0.2',
      description='Swiftly execute complex commands in the shell',
      url='https://github.com/shaneleonard/oz',
      author='Shane Leonard',
      author_email='shane.william.leonard@gmail.com',
      license='MIT',
      packages=['oz'],
      scripts=['bin/oz'],
      zip_safe=False)
