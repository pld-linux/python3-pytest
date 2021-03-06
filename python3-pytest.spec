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
Name:		python3-%{module}
Version:	6.2.2
Release:	1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pytest/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest/pytest-%{version}.tar.gz
# Source0-md5:	828d15f426ce9740627a9b07e47a318a
Patch0:		%{name}-tests.patch
URL:		https://pytest.org/
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-py >= %{pylib_version}
BuildRequires:	python3-setuptools >= 1:40.0
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	pydoc3 >= 1:3.5
BuildRequires:	python3-argcomplete
BuildRequires:	python3-atomicwrites >= 1.0
BuildRequires:	python3-attrs >= 17.4.0
BuildRequires:	python3-hypothesis >= 3.56
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata >= 0.12
%endif
BuildRequires:	python3-initconfig
BuildRequires:	python3-more_itertools >= 4.0.0
BuildRequires:	python3-nose
BuildRequires:	python3-packaging
%if "%{py3_ver}" < "3.6"
BuildRequires:	python3-pathlib2 >= 2.2.0
%endif
BuildRequires:	python3-pluggy >= 0.12
BuildRequires:	python3-pluggy < 1.0
BuildRequires:	python3-requests
BuildRequires:	python3-six >= 1.10.0
BuildRequires:	python3-wcwidth
BuildRequires:	python3-xmlschema
BuildConflicts:	python3-pytest-benchmark < 3.2.1
# outdated
BuildConflicts:	python3-pytest-catchlog
# seems to break things
BuildConflicts:	python3-pytest-xdist
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-pygments_pytest
BuildRequires:	python3-sphinx_removed_in >= 0.2.0
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3 >= 1.8.2
%endif
Requires:	python3-modules >= 1:3.5
Requires:	python3-setuptools
Obsoletes:	python3-pytest-cache
Obsoletes:	python3-pytest-catchlog
Conflicts:	python-pytest < 4.6.11-2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
py.test is a simple and popular testing tool for Python.

%description -l pl.UTF-8
py.test to proste i popularne narzędzie testujące dla Pythona.

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
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
%py3_build

%if %{with tests}
# test_pdb_custom_cls_with_settrace fails without preinstalled pytest
# test_pdb_* which spawn pdb hang under some unclear conditions
# ...and most test_debugging tests require ptys
# test_spawn_uses_tmphome and some terminal tests require ptys
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest -k 'not (test_debugging or test_spawn_uses_tmphome or test_runtest_location_shown_before_test_starts or test_report_collect_after_half_a_second or test_trial_pdb)' testing
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

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/py.test{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pytest{,-3}

ln -sf py.test-3 $RPM_BUILD_ROOT%{_bindir}/py.test
ln -sf pytest-3 $RPM_BUILD_ROOT%{_bindir}/pytest

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/py.test
%attr(755,root,root) %{_bindir}/py.test-3
%attr(755,root,root) %{_bindir}/pytest
%attr(755,root,root) %{_bindir}/pytest-3
%{py3_sitescriptdir}/pytest
%{py3_sitescriptdir}/_pytest
%{py3_sitescriptdir}/pytest-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/en/_build/html/{_images,_modules,_static,announce,example,proposals,*.html,*.js}
%endif
