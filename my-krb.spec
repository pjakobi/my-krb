#
# Spec file for comtics-krb
#
Summary: MIT Kereros configuration 
Name: my-krb
#%define _topdir /home/utilisateur/Soft/rpmbuild
#%define _tmppath /home/utilisateur/Soft/rpmbuild/tmp
%define version 0.0
%define release 2
%define realm THALESGROUP.COM
%define dnsdomain %(echo %{realm} | tr '[:upper:]' '[:lower:]')
%define servername dumbo.home
%define password secret
%define dbpassword thales
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
sed -i "/%{realm} =/,/^}/d" /var/kerberos/krb5kdc/kdc.conf
sed -i "/default_realm/s/= \(.*\)/ = EXAMPLE\.COM/" /etc/krb5.conf
sed -i "/%{realm} = /,/}/d" /etc/krb5.conf
sed -i "/= %{realm}$/d" /etc/krb5.conf

%build



%install


%post



# 
# Create realm supplementing /etc/krb5.conf 
#
sed -i "/default_realm/s/= \(.*\)/ = %{realm}/" /etc/krb5.conf
sed -i '/^\[realms\]/a\
%{realm} = {\
    admin_server = %{servername}\
    kdc = %{servername}\n}' /etc/krb5.conf

sed -i '/^\[domain_realm\]/a\
%{dnsdomain} = %{realm}\
.%{dnsdomain} = %{realm}' /etc/krb5.conf

#
# kdc.conf updates
#
tmpfile=`mktemp %{_tmppath}/kerberos.XXXX`
export tmpfile
sed -n "/EXAMPLE\.COM/,/\}/p" /var/kerberos/krb5kdc/kdc.conf > $tmpfile
sed -i "s/EXAMPLE\.COM/%{realm}/" $tmpfile
cat $tmpfile >> /var/kerberos/krb5kdc/kdc.conf
#rm $tmpfile

#
# Create realm in kerberos
#
rm -rf /var/kerberos/krb5kdc/principal*
kdb5_util create -r %{realm} -s -P %{dbpassword}
echo "*/admin@/%{realm} *" >> /var/kerberos/krb5kdc/kadm5.acl
kadmin.local -q "addprinc -pw %{password} root"
kadmin.local -q "addprinc -pw %{password} root/admin"

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.md TODO



%changelog
* Sun Apr 22 2018  Pascal Jakobi <pascal.jakobi@thalesgroup.com> 0.0.3
- SASL
* Fri Mar 30 2018  Pascal Jakobi <pascal.jakobi@thalesgroup.com> 0.1.1
- Initial RPM release
