# comtics-krb
Kerberos installation RPM for COMTICS

# Set up
In order to create the RPM, 4 parameters are to be set in the spec file:
- The Kerberos database password
- The server's hostname for the KDC and Kerberos admin server
- The kerberos realm and DNS domain (same value, one in upper case, the other in lower case).
