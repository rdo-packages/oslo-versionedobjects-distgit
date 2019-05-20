# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname oslo.versionedobjects
%global pkg_name oslo-versionedobjects

%global with_doc 1

%global common_desc \
The Oslo project intends to produce a python library containing \
infrastructure code shared by OpenStack projects. The APIs provided \
by the project should be high quality, stable, consistent and generally \
useful. \
 \
Oslo versionedobjects library deals with DB schema being at different versions \
than the code expects, allowing services to be operated safely during upgrades.

%global common_desc_tests \
Tests for the oslo.versionedobjects library.

Name:       python-oslo-versionedobjects
Version:    XXX
Release:    XXX
Summary:    OpenStack common versionedobjects library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:  noarch

%package -n python%{pyver}-%{pkg_name}
Summary:    OpenStack common versionedobjects library
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}

BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-pbr
BuildRequires: git
# Required for tests
BuildRequires: python%{pyver}-hacking
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-testtools
BuildRequires: python%{pyver}-fixtures
BuildRequires: python%{pyver}-iso8601
BuildRequires: python%{pyver}-mock
BuildRequires: python%{pyver}-oslo-config
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-oslo-messaging
BuildRequires: python%{pyver}-eventlet
# Required to compile translation files
BuildRequires: python%{pyver}-babel
BuildRequires: python%{pyver}-jsonschema

# Handle python2 exception
%if %{pyver} == 2
BuildRequires: python-d2to1
BuildRequires: pytz
%else
BuildRequires: python%{pyver}-d2to1
BuildRequires: python%{pyver}-pytz
%endif

Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-oslo-concurrency >= 3.26.0
Requires:   python%{pyver}-oslo-config >= 2:5.2.0
Requires:   python%{pyver}-oslo-context >= 2.19.2
Requires:   python%{pyver}-oslo-messaging >= 5.29.0
Requires:   python%{pyver}-oslo-serialization >= 2.18.0
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-oslo-log >= 3.36.0
Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-iso8601
Requires:   python%{pyver}-netaddr
Requires:   python%{pyver}-webob >= 1.7.1
Requires:   python-%{pkg_name}-lang = %{version}-%{release}

%description -n python%{pyver}-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for OpenStack common versionedobjects library

BuildRequires: python%{pyver}-oslo-config
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-oslo-messaging
BuildRequires: python%{pyver}-iso8601
BuildRequires: python%{pyver}-sphinx

# Needed for autoindex which imports the code

%description -n python-%{pkg_name}-doc
Documentation for the oslo.versionedobjects library.
%endif

%package -n python%{pyver}-%{pkg_name}-tests
Summary:    Tests for OpenStack common versionedobjects library

Requires: python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires: python%{pyver}-hacking
Requires: python%{pyver}-oslotest
Requires: python%{pyver}-testtools
%if %{pyver} == 2
Requires: pytz
%else
Requires: python%{pyver}-pytz
%endif

%description -n python%{pyver}-%{pkg_name}-tests
%{common_desc_tests}


%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo versionedobjects library

%description -n python-%{pkg_name}-lang
Translation files for Oslo versionedobjects library

%description
%{common_desc}

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%{pyver_build}

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_versionedobjects/locale


%install
%{pyver_install}

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/oslo_versionedobjects/locale/*/LC_*/oslo_versionedobjects*po
rm -f %{buildroot}%{pyver_sitelib}/oslo_versionedobjects/locale/*pot
mv %{buildroot}%{pyver_sitelib}/oslo_versionedobjects/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_versionedobjects --all-name

%check
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{pkg_name}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/oslo_versionedobjects
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/oslo_versionedobjects/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_versionedobjects/tests

%files -n python-%{pkg_name}-lang -f oslo_versionedobjects.lang
%license LICENSE

%changelog
