#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_without	python3 # CPython 3.x module

%define		pylib_version	1.4.12
%define 	module	pytest
Summary:	Simple and popular testing tool for Python
Summary(pl.UTF-8):	Proste i popularne narzędzie testujące dla Pythona
Name:		python-%{module}
Version:	2.8.2
Release:	1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/pypi/pytest
Source0:	https://pypi.python.org/packages/source/p/pytest/pytest-%{version}.tar.gz
# Source0-md5:	96e77b3a2fb40e5d99a1cfba38ac7c6d
URL:		http://pytest.org/
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-py >= %{pylib_version}
BuildRequires:	python-setuptools >= 7.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg >= 1.0
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-py >= %{pylib_version}
BuildRequires:	python3-setuptools >= 7.0
%endif
Requires:	python-py >= %{pylib_version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
py.test is a simple and popular testing tool for Python.

%description -l pl.UTF-8
py.test to proste i popularne narzędzie testujące dla Pythona.

%package -n python3-pytest
Summary:	Simple powerful testing with Python
Summary(pl.UTF-8):	Proste, ale funkcjonalne narzędzie testujące dla Pythona
Group:		Development/Languages
Requires:	python3-py >= %{pylib_version}
Suggests:	python3-setuptools

%description -n python3-pytest
py.test provides simple, yet powerful testing for Python.

%description -n python3-pytest -l pl.UTF-8
py.test to proste, ale bardzo funkcjonalne narzędzie testujące dla
Pythona.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build

%if %{with python3}
%py3_build
%endif

%if %{with doc}
install -d _htmldocs/html
for l in doc/*; do
	PYTHONPATH=$(pwd) \
	%{__make} -C $l html
	# remove hidden file
	rm $l/_build/html/.buildinfo
	mv $l/_build/html _htmldocs/html/${l##doc/}
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install
%endif

%py_install

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.rst %{?with_doc:_htmldocs/html}
%attr(755,root,root) %{_bindir}/py.test
%attr(755,root,root) %{_bindir}/py.test-%{py_ver}
%{py_sitescriptdir}/pytest.py[co]
%{py_sitescriptdir}/_pytest
%{py_sitescriptdir}/pytest-%{version}-py*.egg-info

%if %{with python3}
%files -n python3-pytest
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.rst %{?with_doc:_htmldocs/html}
%attr(755,root,root) %{_bindir}/py.test-%{py3_ver}
%{py3_sitescriptdir}/pytest.py
%{py3_sitescriptdir}/_pytest
%{py3_sitescriptdir}/__pycache__/pytest.*.py[co]
%{py3_sitescriptdir}/pytest-%{version}-py*.egg-info
%endif
