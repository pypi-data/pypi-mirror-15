from distutils.core import setup
from distutils.command.install import install
from distutils import log
import json
import os
import sys

kernel_json = {
    "argv": [sys.executable, "-m", "postgres_kernel", "-f", "{connection_file}"],
    "display_name": "PostgreSQL",
    "language": "postgresql",
    "codemirror_mode": "sql"
}


class install_with_kernelspec(install):
    def run(self):
        # Regular installation
        install.run(self)

        # Now write the kernelspec
        from IPython.kernel.kernelspec import install_kernel_spec
        from IPython.utils.tempdir import TemporaryDirectory
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755)  # Starts off as 700, not user readable
            with open(os.path.join(td, 'kernel.json'), 'w') as f:
                json.dump(kernel_json, f, sort_keys=True)
            # TODO: Copy resources once they're specified

            log.info('Installing IPython kernel spec')
            install_kernel_spec(td, 'postgres', user=self.user, replace=True)

with open('README.rst') as f:
    readme = f.read()

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)

setup(name='postgres_kernel',
      version='0.1',
      description='A PostgreSQL kernel for IPython',
      long_description=readme,
      author='Brian Schiller',
      author_email='bgschiller@gmail.com',
      url='https://github.com/bgschiller/postgres_kernel',
      download_url='https://github.com/bgschiller/postgres_kernel/tarball/0.1',
      packages=['postgres_kernel'],
      keywords=['postgres', 'ipython', 'jupyter'],
      cmdclass={'install': install_with_kernelspec},
      install_requires=['psycopg2>=2.6', 'tabulate==0.7.5'],
      classifiers=[
          'Framework :: IPython',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Shells',
      ])
