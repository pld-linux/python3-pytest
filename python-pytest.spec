#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	tests	# unit tests

%define		pylib_version	1.5.0
%define 	module	pytest
Summary:	Simple and popular testing tool for Python
Summary(pl.UTF-8):	Proste i popularne narzędzie testujące dla Pythona
Name:		python-%{module}
Version:	3.10.1
Release:	2
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pytest/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest/pytest-%{version}.tar.gz
# Source0-md5:	9afbcf5a86d4fea46024eb65994e7e69
Patch0:		%{name}-tests.patch
URL:		http://pytest.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-py >= %{pylib_version}
BuildRequires:	python-setuptools >= 1:40.0
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	pydoc >= 1:2.7
BuildRequires:	python-atomicwrites >= 1.0
BuildRequires:	python-attrs >= 17.4.0
BuildRequires:	python-funcsigs
BuildRequires:	python-hypothesis >= 3.56
BuildRequires:	python-mock
BuildRequires:	python-more_itertools >= 4.0.0
BuildRequires:	python-nose
BuildRequires:	python-pathlib2 >= 2.2.0
BuildRequires:	python-pluggy >= 0.7
BuildRequires:	python-requests
BuildRequires:	python-six >= 1.10.0
BuildConflicts:	python-backports.unittest_mock
BuildConflicts:	python-pyfakefs
BuildConflicts:	python-pytest-catchlog
# with xdist requires various modules source
BuildConflicts:	python-pytest-xdist
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-py >= %{pylib_version}
BuildRequires:	python3-setuptools >= 1:40.0
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	pydoc3 >= 1:3.4
BuildRequires:	python3-atomicwrites >= 1.0
BuildRequires:	python3-attrs >= 17.4.0
BuildRequires:	python3-hypothesis >= 3.56
BuildRequires:	python3-more_itertools >= 4.0.0
BuildRequires:	python3-nose
%if "%{py3_ver}" < "3.6"
BuildRequires:	python3-pathlib2 >= 2.2.0
%endif
BuildRequires:	python3-pluggy >= 0.7
BuildRequires:	python3-requests
BuildRequires:	python3-six >= 1.10.0
BuildConflicts:	python3-pyfakefs
BuildConflicts:	python3-pytest-catchlog
BuildConflicts:	python3-pytest-xdist
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3 >= 1.0
%endif
Requires:	python-modules >= 1:2.7
Requires:	python-setuptools
Obsoletes:	python-pytest-cache
Obsoletes:	python-pytest-catchlog
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
Requires:	python3-devel-tools >= 1:3.4
Requires:	python3-setuptools
Obsoletes:	python3-pytest-cache
Obsoletes:	python3-pytest-catchlog

%description -n python3-pytest
py.test provides simple, yet powerful testing for Python.

%description -n python3-pytest -l pl.UTF-8
py.test to proste, ale bardzo funkcjonalne narzędzie testujące dla
Pythona.

%package apidocs
Summary:	Documentation for py.test Pythona package
Summary(pl.UTF-8):	Dokumentacja pakietu Pythona py.test
Group:		Documentation

%description apidocs
Documentation for py.test Pythona package.

%description apidocs -l pl.UTF-8
Dokumentacja pakietu Pythona py.test.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
# test_pdb_custom_cls_with_settrace fails without preinstalled pytest
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest -k 'not test_pdb and not TestTerminal and not test_request_garbage' testing
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# test_pdb_custom_cls_with_settrace fails without preinstalled pytest
# test_pdb_* which spawn pdb hang under some unclear conditions
# test_request_garbage fails sometimes
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest -v -k 'not test_pdb and not TestTerminal and not test_request_garbage' testing
%endif
%endif

%if %{with doc}
for l in doc/*; do
	PYTHONPATH=$(pwd)/src \
	%{__make} -C $l html \
		SPHINXBUILD=sphinx-build-3
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/py.test{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pytest{,-3}
%endif

%if %{with python2}
%py_install

ln $RPM_BUILD_ROOT%{_bindir}/py.test{,-2}
ln $RPM_BUILD_ROOT%{_bindir}/pytest{,-2}

# pytest.py source seems required for "monkeypatching" tests
%py_postclean -x pytest.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/py.test
%attr(755,root,root) %{_bindir}/py.test-2
%attr(755,root,root) %{_bindir}/pytest
%attr(755,root,root) %{_bindir}/pytest-2
%{py_sitescriptdir}/pytest.py*
%{py_sitescriptdir}/_pytest
%{py_sitescriptdir}/pytest-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pytest
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/py.test-3
%attr(755,root,root) %{_bindir}/pytest-3
%{py3_sitescriptdir}/pytest.py
%{py3_sitescriptdir}/_pytest
%{py3_sitescriptdir}/__pycache__/pytest.*.py[co]
%{py3_sitescriptdir}/pytest-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/en/_build/html/{_images,_modules,_static,announce,example,proposals,*.html,*.js}
%endif
