#
# Spec file for comtics-krb
#
Summary: MIT Kereros configuration 
Name: my-krb
#%define _topdir /home/utilisateur/Soft/rpmbuild
#%define _tmppath /home/utilisateur/Soft/rpmbuild/tmp
%define version 0.0
%define release 1
%define realm THALESGROUP.COM
%define dnsdomain thalesgroup.com
%define servername kerberos
%define password secret
Version: %{version}
Release: %{release}
License: LGPL
BuildArch: noarch
Group: System Environment/Daemons
Source0: %{name}-%{version}.%{release}.tar.gz
Vendor: Thales Communications & Security
Packager: Pascal Jakobi <pascal.jakobi@thalesgroup.com>
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: git
BuildRequires: sed
# kerberos
Requires: ntp
Requires: krb5-server
Requires: krb5-libs
Requires: krb5-workstation



%description
This rpm customizes kerberos (MIT) and provides a simplified installation.

%prep
%setup -q -n %{name}-%{version}.%{release}

%preun 
systemctl stop krb5kdc
systemctl stop kadmin
kdb5_util destroy -r %{realm} -f -P %{password}
sed -i "/%{realm}/d" /var/kerberos/krb5kdc/kadm5.acl
sed -i "/^%{realm}/,/}/d" /var/kerberos/krb5kdc/kdc.conf

%build
sed -i 's/###SERVERNAME###/%{servername}/' comtics.conf
sed -i 's/###DNSDOMAIN###/%{servername}/' comtics.conf
sed -i 's/###REALM###/%{realm}/' comtics.conf
sed -i 's/###REALM###/%{realm}/' kdc-comtics.conf

%install
install --directory $RPM_BUILD_ROOT/etc
install --directory $RPM_BUILD_ROOT/etc/krb5.conf.d
install -m 0755 comtics.conf $RPM_BUILD_ROOT/etc/krb5.conf.d/comtics.conf

install --directory $RPM_BUILD_ROOT/var
install --directory $RPM_BUILD_ROOT/var/kerberos
install --directory $RPM_BUILD_ROOT/var/kerberos/krb5kdc
install -m 0755 kdc-comtics.conf $RPM_BUILD_ROOT/var/kerberos/krb5kdc/kdc-comtics.conf

%post
kdb5_util create -r %{realm} -s -P %{password}
echo "*/admin@/%{realm} *" >> /var/kerberos/krb5kdc/kadm5.acl
cat /var/kerberos/krb5kdc/kdc-comtics.conf >> /var/kerberos/krb5kdc/kdc.conf

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.md TODO
%config /etc/krb5.conf.d/comtics.conf
%config /var/kerberos/krb5kdc/kdc-comtics.conf

%changelog
* Fri Mar 30 2018  Pascal Jakobi <pascal.jakobi@thalesgroup.com> 0.1.1
- Initial RPM release
