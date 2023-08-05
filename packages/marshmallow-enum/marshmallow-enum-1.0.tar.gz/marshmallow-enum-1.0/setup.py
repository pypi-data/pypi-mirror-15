from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

try:
    import enum
    extra_requires = []
except ImportError:
    extra_requires = ['enum34']

REQUIRES = ['marshmallow>=2.0.0'] + extra_requires


class ToxTest(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        args = []
        if self.tox_args:
            args = shlex.split(self.tox_args)

        errno = tox.cmdline(args=args)
        sys.exit(errno)


if __name__ == '__main__':
    setup(
        name='marshmallow-enum',
        version='1.0',
        author='Alec Nikolas Reiter',
        author_email='alecreiter@gmail.com',
        url="https://github.com/justanr/marshmallow_enum",
        description='Enum field for Marshmallow',
        license='MIT',
        packages=['marshmallow_enum'],
        install_requires=REQUIRES,
        test_suite='test',
        tests_require=['tox'],
        cmdclass={'test': ToxTest},
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: Implementation :: PyPy"
        ]
    )
