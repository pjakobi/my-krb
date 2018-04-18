# my-krb
Kerberos simplified RPM installation : build an RPM with default realm set, use it many times.

## Creating the RPM
- Before anything, create a build environment for RPMs : rpmbuild/SPECS, rpmbuild/SOURCES, etc. (see rpmbuild documentation).
- Then download the my-krb project (`git clone https://github.com/pjakobi/my-krb my-krb-0.0.1`)
- You now need to set the RPM parameters : realm, DNS domain... Also the topdir variable might need a change. All these parameters are at the top of the my-krb.spec file.
- Then create a tar file in the SOURCES directory `tar cvfz (...)/rpmbuild/SOURCES/my-krb-0.0.1.tar.gz my-krb-0.0.1/*`
- At last run `rpmbuild my-krb.spec` - this should create a my-krb RPM in the (...)/rpmbuild/RPMS/noarch directory.

## Installation
Just run `yum localinstall` and that should do the trick.
