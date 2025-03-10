#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	tests	# unit tests

%define 	module	pytest
Summary:	Simple and popular testing tool for Python
Summary(pl.UTF-8):	Proste i popularne narzędzie testujące dla Pythona
Name:		python3-%{module}
Version:	8.3.4
Release:	4
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pytest/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest/pytest-%{version}.tar.gz
# Source0-md5:	542c4e802eeac1d196482e90a36533ed
Patch0:		pytest-dev-bug-12624.patch
URL:		https://pytest.org/
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-py >= 1.8.2
BuildRequires:	python3-setuptools >= 1:45.0
BuildRequires:	python3-setuptools_scm >= 6.2.3
%if "%{py3_ver}" != "3.11"
BuildRequires:	python3-tomli
%endif
%if %{with tests}
BuildRequires:	pydoc3 >= 1:3.6
BuildRequires:	python3-argcomplete
BuildRequires:	python3-attrs >= 19.2.0
%if "%{py3_ver}" != "3.11"
BuildRequires:	python3-exceptiongroup >= 1.0.0
%endif
BuildRequires:	python3-hypothesis >= 3.56
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata >= 0.12
%endif
BuildRequires:	python3-iniconfig
BuildRequires:	python3-nose
BuildRequires:	python3-packaging
BuildRequires:	python3-pluggy >= 1.5.0
BuildRequires:	python3-pluggy < 2.0
BuildRequires:	python3-pygments >= 2.7.2
BuildRequires:	python3-requests
BuildRequires:	python3-xmlschema
BuildConflicts:	python3-pytest-benchmark < 3.2.1
# outdated
BuildConflicts:	python3-pytest-catchlog
# seems to break things
BuildConflicts:	python3-pytest-xdist
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-packaging
BuildRequires:	python3-pallets-sphinx-themes
BuildRequires:	python3-pluggy >= 1.5.0
BuildRequires:	python3-pygments_pytest >= 2.3.0
BuildRequires:	python3-sphinx_removed_in >= 0.2.3
BuildRequires:	python3-sphinxcontrib-svg2pdfconverter
BuildRequires:	python3-sphinxcontrib-towncrier
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3 >= 4.5
%endif
Requires:	python3-modules >= 1:3.7
# no egg dependency (pytest comes with minimal replacement, we don't package it)
Requires:	python3-py >= 1.11.0
Requires:	python3-setuptools >= 1:42.0
Obsoletes:	python3-pytest-cache < 1.1
Obsoletes:	python3-pytest-catchlog < 1.2.3
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
%patch -P0 -p1

%build
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

%py3_build_pyproject

%if %{with tests}
# test_trial_pdb and most test_debugging tests require ptys
# test_spawn_uses_tmphome and some terminal tests require ptys
# test_code_highlight and test_color_yes has some terminal sequence mismatch
# test_version_* have some exception string mismatch
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest -k 'not (test_code_highlight or test_color_yes or test_debugging or test_header_trailer_info or test_spawn_uses_tmphome or test_runtest_location_shown_before_test_starts or test_report_collect_after_half_a_second or test_trial_pdb or test_version_less_verbose or test_version_verbose)' testing
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

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/py.test{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pytest{,-3}

ln -sf py.test-3 $RPM_BUILD_ROOT%{_bindir}/py.test
ln -sf pytest-3 $RPM_BUILD_ROOT%{_bindir}/pytest

# rely on system python3-py instead
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/py.py \
	$RPM_BUILD_ROOT%{py3_sitescriptdir}/__pycache__/py.*.py[co]

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
%{py3_sitescriptdir}/pytest-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/en/_build/html/{_images,_modules,_static,announce,example,proposals,*.html,*.js}
%endif
