# my-krb
Kerberos simplified RPM installation.
Build an RPM with default realm set, use it many times.

# Set up
- Before anything, create a build environment for RPMs (see rpmbuild documentation).
- Then download the my-krb project ('git clone https://github.com/pjakobi/my-krb my-krb-0.0.1')
- You now need to set the RPM parameters : realm, DNS domain... Also the topdir variable might need a change. All these parameters are at the top of the my-krb.spec file.
- Then create a tar file in the SOURCES directory 'tar cvfz (...)/rpmbuild/SOURCES/my-krb-0.0.1.tar.gz my-krb-0.0.1/*'
- 

