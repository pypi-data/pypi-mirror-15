from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

def requirements():
    with open('requirements.txt') as f:
        return [line.rstrip('\n') for line in f]

setup(name='psychic_disco',
      version='0.6.3',
      description='Pythonic Microservices on AWS Lambda',
      long_description=readme(),
      url='http://github.com/robertdfrench/psychic-disco',
      author='Robert D. French',
      author_email='robert@robertdfrench.me',
      license='MIT',
      packages=['psychic_disco'],
      zip_safe=False,
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=requirements(),
      scripts=['bin/psychic_disco'])
