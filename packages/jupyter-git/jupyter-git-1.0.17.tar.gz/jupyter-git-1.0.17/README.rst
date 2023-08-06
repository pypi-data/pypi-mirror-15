Follow steps on https://packaging.python.org/en/latest/distributing/#requirements-for-packaging-and-distributing

One time things:
  1. Make account on PyPI
  2. pip install twine

To Update Package:
  1. Update version number in setup.py
  2. rm dist/*
  3. python setup.py sdist
  4. Use the form on the PyPI website, to upload your PKG-INFO info located in your local project tree at myproject.egg-info   /PKG-INFO. If you don’t have that file or directory, then run python setup.py egg_info to have it generated.
  5. twine upload dist/*
