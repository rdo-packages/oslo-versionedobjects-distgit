%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%package -n python3-%{pkg_name}
Summary:    OpenStack common versionedobjects library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
BuildRequires: git-core
# Required for tests
BuildRequires: python3-hacking
BuildRequires: python3-oslotest
BuildRequires: python3-testtools
BuildRequires: python3-fixtures
BuildRequires: python3-iso8601
BuildRequires: python3-mock
BuildRequires: python3-oslo-config
BuildRequires: python3-oslo-i18n
BuildRequires: python3-oslo-messaging
BuildRequires: python3-eventlet
# Required to compile translation files
BuildRequires: python3-babel
BuildRequires: python3-jsonschema

BuildRequires: python3-pytz

Requires:   python3-oslo-concurrency >= 3.26.0
Requires:   python3-oslo-config >= 2:5.2.0
Requires:   python3-oslo-context >= 2.19.2
Requires:   python3-oslo-messaging >= 5.29.0
Requires:   python3-oslo-serialization >= 2.18.0
Requires:   python3-oslo-utils >= 4.7.0
Requires:   python3-oslo-log >= 3.36.0
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-iso8601
Requires:   python3-netaddr
Requires:   python3-webob >= 1.7.1
Requires:   python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for OpenStack common versionedobjects library

BuildRequires: python3-oslo-config
BuildRequires: python3-openstackdocstheme
BuildRequires: python3-oslo-messaging
BuildRequires: python3-iso8601
BuildRequires: python3-sphinx

# Needed for autoindex which imports the code

%description -n python-%{pkg_name}-doc
Documentation for the oslo.versionedobjects library.
%endif

%package -n python3-%{pkg_name}-tests
Summary:    Tests for OpenStack common versionedobjects library

Requires: python3-%{pkg_name} = %{version}-%{release}
Requires: python3-hacking
Requires: python3-oslotest
Requires: python3-testtools
Requires: python3-pytz

%description -n python3-%{pkg_name}-tests
%{common_desc_tests}


%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo versionedobjects library

%description -n python-%{pkg_name}-lang
Translation files for Oslo versionedobjects library

%description
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{sname}-%{upstream_version} -S git

# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%{py3_build}

# Generate i18n files
python3 setup.py compile_catalog -d build/lib/oslo_versionedobjects/locale --domain oslo_versionedobjects


%install
%{py3_install}

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-3 -W -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_versionedobjects/locale/*/LC_*/oslo_versionedobjects*po
rm -f %{buildroot}%{python3_sitelib}/oslo_versionedobjects/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_versionedobjects/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_versionedobjects --all-name

%check
python3 setup.py test

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_versionedobjects
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_versionedobjects/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_versionedobjects/tests

%files -n python-%{pkg_name}-lang -f oslo_versionedobjects.lang
%license LICENSE

%changelog
