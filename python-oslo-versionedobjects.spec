%{!?_licensedir:%global license %%doc}
%global sname oslo.versionedobjects

Name:       python-oslo-versionedobjects
Version:    0.7.0
Release:    1%{?dist}
Summary:    OpenStack common versionedobjects library

License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    https://pypi.python.org/packages/source/o/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:  noarch
Requires:   python-setuptools
Requires:   python-six >= 1.7
Requires:   python-babel
Requires:   python-oslo-concurrency
Requires:   python-oslo-context
Requires:   python-oslo-messaging
Requires:   python-oslo-serialization
Requires:   python-oslo-utils
Requires:   python-oslo-log
Requires:   python-oslo-i18n
Requires:   python-mock
Requires:   python-fixtures
Requires:   python-iso8601

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-d2to1

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

Oslo versionedobjects library deals with DB schema being at different versions
than the code expects, allowing services to be operated safely during upgrades.

%package doc
Summary:    Documentation for OpenStack common versionedobjects library

BuildRequires: python-sphinx
BuildRequires: python-oslo-config
BuildRequires: python-oslo-sphinx
BuildRequires: python-oslo-messaging
BuildRequires: python-iso8601

# Needed for autoindex which imports the code

%description doc
Documentation for the oslo.versionedobjects library.

%prep
%setup -q -n %{sname}-%{version}

# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests


%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_versionedobjects
%{python2_sitelib}/*.egg-info

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Tue Aug 18 2015 Alan Pevec <alan.pevec@redhat.com> 0.7.0-1
- Update to upstream 0.7.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 26 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 0.1.1-1
- Upstream 0.1.1
- Based on Derekh Higgins package from Delorean
