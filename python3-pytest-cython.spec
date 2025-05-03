#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Plugin for testing Cython extension modules
Summary(pl.UTF-8):	Wtyczka do testowania modułów rozszerzeń Cythona
Name:		python3-pytest-cython
Version:	0.3.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-cython/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-cython/pytest-cython-%{version}.tar.gz
# Source0-md5:	23f8f72dea2206e607adc4bebe6e6c64
URL:		https://pypi.org/project/pytest-cython/
%{?with_tests:BuildRequires:	libstdc++-devel}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Cython >= 0.28
BuildRequires:	python3-pytest >= 4.6.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_py3doc_enhanced_theme
BuildRequires:	sphinx-pdg-3 >= 1.3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Pytest plugin allows for the doctesting of C extension modules
for Python, specifically created through Cython.

%description -l pl.UTF-8
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cython.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests/test_pytest_cython.py
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CONTRIBUTING.md LICENSE.md README.md
%{py3_sitescriptdir}/pytest_cython
%{py3_sitescriptdir}/pytest_cython-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
