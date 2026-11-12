#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Plugin for testing Cython extension modules
Summary(pl.UTF-8):	Wtyczka do testowania modułów rozszerzeń Cythona
Name:		python3-pytest-cython
Version:	0.4.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-cython/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-cython/pytest_cython-%{version}.tar.gz
# Source0-md5:	e65a2fdcf2e24cd047f5a22cffdedc0c
URL:		https://pypi.org/project/pytest-cython/
%{?with_tests:BuildRequires:	libstdc++-devel}
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-Cython >= 0.28
BuildRequires:	python3-pytest >= 8
# tests/example-project/pyproject.toml
BuildRequires:	python3-setuptools >= 1:74.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Pytest plugin allows for the doctesting of C extension modules
for Python, specifically created through Cython.

%description -l pl.UTF-8
Ta wtyczka Pytesta pozwala wykonywać doctesty modułów rozszerzeń w C
dla Pythona, w szczególności tych utworzonych przy pomocy Cythona.

%prep
%setup -q -n pytest_cython-%{version}

%build
%py3_build_pyproject

%if %{with tests}
cd tests/example-project
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
LDFLAGS="%{rpmldflags}" \
%{__python3} setup.py build_ext --inplace
cd ../..

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cython.plugin" \
PYTHONPATH=$(pwd)/src:$(pwd)/tests/example-project/src \
%{__python3} -m pytest tests/test_pytest_cython.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CONTRIBUTING.md LICENSE.md README.md
%{py3_sitescriptdir}/pytest_cython
%{py3_sitescriptdir}/pytest_cython-%{version}.dist-info
