#
# Conditional build:
%bcond_without	doc	# HTML documentation build
#
Summary:	Simple and popular testing tool for Python
Summary(pl.UTF-8):	Proste i popularne narzędzie testujące dla Pythona
Name:		python-pytest
Version:	2.2.4
Release:	1
License:	MIT
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/p/pytest/pytest-%{version}.zip
# Source0-md5:	73ed098e39978890b83cbea1f1ab2a74
URL:		http://pytest.org/
BuildRequires:	python-devel >= 2.4
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with doc}
BuildRequires:	python-py >= 1.4.8
BuildRequires:	sphinx-pdg >= 1.0
%endif
Requires:	python-py >= 1.4.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
py.test is a simple and popular testing tool for Python.

%description -l pl.UTF-8
py.test to proste i popularne narzędzie testujące dla Pythona.

%prep
%setup -q -n pytest-%{version}

%build
%{__python} setup.py build

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.txt %{?with_doc:doc/_build/html}
%attr(755,root,root) %{_bindir}/py.test
%attr(755,root,root) %{_bindir}/py.test-%{py_ver}
%{py_sitescriptdir}/pytest.py[co]
%{py_sitescriptdir}/_pytest
%{py_sitescriptdir}/pytest-%{version}-py*.egg-info
