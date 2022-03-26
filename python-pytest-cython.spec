#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (one failing on py3)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Plugin for testing Cython extension modules
Summary(pl.UTF-8):	Wtyczka do testowania modułów rozszerzeń Cythona
Name:		python-pytest-cython
Version:	0.1.1.post0
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-cython/
#Source0:	https://files.pythonhosted.org/packages/source/p/pytest-cython/pytest-cython-%{version}.tar.gz
Source0:	https://files.pythonhosted.org/packages/45/12/39dba6aae3257d762ef56b0667971e71544ab1932825839666152c744c1e/pytest-cython-%{version}.tar.gz
# Source0-md5:	f24330785e961eed5f9a40716a977bae
URL:		https://pypi.org/project/pytest-cython/
%{?with_tests:BuildRequires:	libstdc++-devel}
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-Cython >= 0.20.2
BuildRequires:	python-pytest >= 2.7.3
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Cython >= 0.20.2
BuildRequires:	python3-pytest >= 2.7.3
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-Sphinx >= 1.3
BuildRequires:	python3-sphinx_py3doc_enhanced_theme
%endif
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Pytest plugin allows for the doctesting of C extension modules
for Python, specifically created through Cython.

%description -l pl.UTF-8
Ta wtyczka Pytesta pozwala wykonywać doctesty modułów rozszerzeń w C
dla Pythona, w szczególności tych utworzonych przy pomocy Cythona.

%package -n python3-pytest-cython
Summary:	Plugin for testing Cython extension modules
Summary(pl.UTF-8):	Wtyczka do testowania modułów rozszerzeń Cythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-pytest-cython
This Pytest plugin allows for the doctesting of C extension modules
for Python, specifically created through Cython.

%description -n python3-pytest-cython -l pl.UTF-8
Ta wtyczka Pytesta pozwala wykonywać doctesty modułów rozszerzeń w C
dla Pythona, w szczególności tych utworzonych przy pomocy Cythona.

%package apidocs
Summary:	API documentation for Python pytest-cython module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest-cython
Group:		Documentation

%description apidocs
API documentation for Python pytest-cython module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest-cython.

%prep
%setup -q -n pytest-cython-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
cd tests/example-project
%{__python} setup.py clean build_ext --inplace --use-cython
cd ../..
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cython.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests/test_pytest_cython.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
cd tests/example-project
%{__python3} setup.py clean build_ext --inplace --use-cython
cd ../..
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cython.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests/test_pytest_cython.py
%endif
%endif

%if %{with doc}
cd docs
PYTHONPATH=$(pwd)/../src \
%{__python3} -m sphinx -W . build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/pytest_cython
%{py_sitescriptdir}/pytest_cython-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pytest-cython
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/pytest_cython
%{py3_sitescriptdir}/pytest_cython-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,reference,*.html,*.js}
%endif
