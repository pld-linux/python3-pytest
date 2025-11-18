#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	tests	# unit tests

%define		module	pytest
Summary:	Simple and popular testing tool for Python
Summary(pl.UTF-8):	Proste i popularne narzędzie testujące dla Pythona
Name:		python3-%{module}
Version:	8.4.2
Release:	1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pytest/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest/pytest-%{version}.tar.gz
# Source0-md5:	a1b847e1f079dfc5d26a63bc02f47fb7
Patch0:		pytest-dev-bug-12624.patch
URL:		https://pytest.org/
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-py >= 1.8.2
BuildRequires:	python3-setuptools >= 1:61
BuildRequires:	python3-setuptools_scm >= 6.2.3
%if "%{_ver_lt %{py3_ver} 3.11}" == "1"
BuildRequires:	python3-tomli >= 1
%endif
%if %{with tests}
BuildRequires:	pydoc3 >= 1:3.6
BuildRequires:	python3-argcomplete
BuildRequires:	python3-attrs >= 19.2.0
%if "%{_ver_lt %{py3_ver} 3.11}" == "1"
BuildRequires:	python3-exceptiongroup >= 1.0.0
%endif
BuildRequires:	python3-hypothesis >= 3.56
BuildRequires:	python3-iniconfig >= 1
BuildRequires:	python3-packaging >= 20
BuildRequires:	python3-pluggy >= 1.5.0
BuildRequires:	python3-pluggy < 2.0
BuildRequires:	python3-pygments >= 2.7.2
BuildRequires:	python3-requests
BuildRequires:	python3-xmlschema
BuildConflicts:	python3-pytest-benchmark < 3.2.1
# outdated
BuildConflicts:	python3-pytest-catchlog
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	inkscape
BuildRequires:	python3-furo
BuildRequires:	python3-packaging >= 20
BuildRequires:	python3-pluggy >= 1.5.0
BuildRequires:	python3-pygments_pytest >= 2.3.0
BuildRequires:	python3-sphinx_issues
BuildRequires:	python3-sphinx_removed_in >= 0.2.3
BuildRequires:	python3-sphinxcontrib-svg2pdfconverter
BuildRequires:	python3-sphinxcontrib-towncrier
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3 >= 7
%endif
Requires:	python3-modules >= 1:3.9
# no egg dependency (pytest comes with minimal replacement, we don't package it)
Requires:	python3-py >= 1.11.0
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
# test_stop_iteration_runtest_protocol, test_fail_setup, test_fail_teardown, test_fail_call: different exception message format
# test_disable_plugin_autoload, test_version_verbose, test_version_less_verbose, test_random_report_log_xdist, test_runs_twice_xdist, test_xdist_normal, test_xdist_normal_count, test_xdist_verbose, test_xdist_times: interfere with our plugin disabling and/or too many plugins installed
# test_header_trailer_info: some slow code warning?
# test_pdb_unittest_postmortem: timeout?
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest -k 'not (test_stop_iteration_runtest_protocol or test_fail_setup or test_fail_teardown or test_fail_call or test_disable_plugin_autoload or test_version_verbose or test_version_less_verbose or test_random_report_log_xdist or test_runs_twice_xdist or test_xdist_normal or test_xdist_normal_count or test_xdist_verbose or test_xdist_times or test_header_trailer_info or test_pdb_unittest_postmortem)'
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
%attr(755,root,root) %{_bindir}/py.test-3
%attr(755,root,root) %{_bindir}/pytest-3
%{_bindir}/py.test
%{_bindir}/pytest
%{py3_sitescriptdir}/pytest
%{py3_sitescriptdir}/_pytest
%{py3_sitescriptdir}/pytest-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/en/_build/html/{_images,_modules,_static,announce,example,explanation,how-to,proposals,reference,*.html,*.js}
%endif
