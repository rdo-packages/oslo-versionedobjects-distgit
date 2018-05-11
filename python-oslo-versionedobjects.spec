%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global sname oslo.versionedobjects
%global pkg_name oslo-versionedobjects

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
Version:    1.31.3
Release:    1%{?dist}
Summary:    OpenStack common versionedobjects library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:  noarch

%package -n python2-%{pkg_name}
Summary:    OpenStack common versionedobjects library
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-pbr
BuildRequires: git
# Required for tests
BuildRequires: python2-hacking
BuildRequires: python2-oslotest
BuildRequires: python2-testtools
BuildRequires: python2-fixtures
BuildRequires: python2-iso8601
BuildRequires: python2-mock
BuildRequires: python2-oslo-config
BuildRequires: python2-oslo-i18n
BuildRequires: python2-oslo-messaging
BuildRequires: python2-eventlet
# Required to compile translation files
BuildRequires: python2-babel
%if 0%{?fedora} > 0
BuildRequires: python2-d2to1
BuildRequires: python2-pytz
BuildRequires: python2-jsonschema
%else
BuildRequires: python-d2to1
BuildRequires: pytz
BuildRequires: python-jsonschema
%endif

Requires:   python2-six >= 1.10.0
Requires:   python2-oslo-concurrency >= 3.25.0
Requires:   python2-oslo-config >= 2:5.1.0
Requires:   python2-oslo-context >= 2.19.2
Requires:   python2-oslo-messaging >= 5.29.0
Requires:   python2-oslo-serialization >= 2.18.0
Requires:   python2-oslo-utils >= 3.33.0
Requires:   python2-oslo-log >= 3.36.0
Requires:   python2-oslo-i18n >= 3.15.3
Requires:   python2-mock
Requires:   python2-fixtures
Requires:   python2-iso8601
%if 0%{?fedora} > 0
Requires:   python2-netaddr
Requires:   python2-webob >= 1.7.1
%else
Requires:   python-netaddr
Requires:   python-webob >= 1.7.1
%endif
Requires:   python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
%{common_desc}

%package -n python-%{pkg_name}-doc
Summary:    Documentation for OpenStack common versionedobjects library

BuildRequires: python2-oslo-config
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-oslo-messaging
BuildRequires: python2-iso8601
BuildRequires: python2-sphinx

# Needed for autoindex which imports the code

%description -n python-%{pkg_name}-doc
Documentation for the oslo.versionedobjects library.

%package -n python2-%{pkg_name}-tests
Summary:    Tests for OpenStack common versionedobjects library

Requires: python2-%{pkg_name} = %{version}-%{release}
Requires: python2-hacking
Requires: python2-oslotest
Requires: python2-testtools
%if 0%{?fedora} > 0
Requires: python2-pytz
%else
Requires: pytz
%endif

%description -n python2-%{pkg_name}-tests
%{common_desc_tests}


%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:    OpenStack common versionedobjects library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
BuildRequires: python3-d2to1
# Required for tests
BuildRequires: python3-hacking
BuildRequires: python3-oslotest
BuildRequires: python3-testtools
BuildRequires: python3-pytz
BuildRequires: python3-fixtures
BuildRequires: python3-iso8601
BuildRequires: python3-mock
BuildRequires: python3-oslo-config
BuildRequires: python3-oslo-i18n
BuildRequires: python3-oslo-messaging
BuildRequires: python3-eventlet

Requires:   python3-setuptools
Requires:   python3-six >= 1.10.0
Requires:   python3-oslo-concurrency >= 3.25.0
Requires:   python3-oslo-config >= 2:5.1.0
Requires:   python3-oslo-context >= 2.19.2
Requires:   python3-oslo-messaging >= 5.29.0
Requires:   python3-oslo-serialization >= 2.18.0
Requires:   python3-oslo-utils >= 3.33.0
Requires:   python3-oslo-log >= 3.36.0
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-mock
Requires:   python3-fixtures
Requires:   python3-iso8601
Requires:   python3-webob >= 1.7.1
Requires:   python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%package -n python3-%{pkg_name}-tests
Summary:    Tests for OpenStack common versionedobjects library

Requires: python3-%{pkg_name} = %{version}-%{release}
Requires: python3-hacking
Requires: python3-oslotest
Requires: python3-testtools
Requires: python3-pytz

%description -n python3-%{pkg_name}-tests
%{common_desc_tests}
%endif

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
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_versionedobjects/locale


%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_versionedobjects/locale/*/LC_*/oslo_versionedobjects*po
rm -f %{buildroot}%{python2_sitelib}/oslo_versionedobjects/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_versionedobjects/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_versionedobjects/locale
%endif

# Find language files
%find_lang oslo_versionedobjects --all-name

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_versionedobjects
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_versionedobjects/tests

%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_versionedobjects/tests

%files -n python-%{pkg_name}-lang -f oslo_versionedobjects.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_versionedobjects
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_versionedobjects/tests

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_versionedobjects/tests
%endif

%changelog
* Fri May 11 2018 RDO <dev@lists.rdoproject.org> 1.31.3-1
- Update to 1.31.3

* Sat Feb 10 2018 RDO <dev@lists.rdoproject.org> 1.31.2-1
- Update to 1.31.2

