Doormouse Core
==============
Doormouse is a library and CLI for managing your PKI without needing to memorize arcane OpenSSL commands and manual tracking. 

Quickstart
----------
1. Visit INSTALL.rst for 2-step instructions to get Doormouse on your system.
2. Get a configuration built using one of the following methods:
   a. Use the default testing config (Built-in default)
   b. Copy an example config from docs/ into ~/.doormouse/doormouse.conf
   c. Build your own config and pass it using ``-c <path_to_config>``
3. Call ``doormouse initialize`` to build the database.
4. Use ``doormouse create <nickname_from_conf> hello.world``

Security Consideration
~~~~~~~~~~~~~~~~~~~~~~
**NOTE:** Doormouse will store the private and public keys on the filesystem in your ~/.doormouse directory. For your security, you should carefully protect that directory.

Using Doormouse
---------------

**Revoke a Certificate**::

    doormouse revoke certificate SERIAL_NUMBER

**Refresh all CRLs**::

    doormouse revoke refresh

**Refresh a specific CRL**::

    doormouse revoke refresh ISSUER_NICKNAME

**List all entries in a CRLs**::

    doormouse revoke list

**List all entries in a specific CRL**::

    doormouse revoke list ISSUER_NICKNAME

**Initialize all CAs**::

    (can be run multiple times if new CAs added)
    doormouse initialize

**List all certificates**::

    doormouse list 

**List all certificates from a CA**::

    doormouse list ISSUER_NICKNAME

**Create a certificate and key**::

    doormouse create CERT_NICKNAME COMMON_NAME ALT_NAME_1 ...

**Sign a CSR**::

    doormouse sign CERT_NICKNAME CSRFILE

**Import an external certificate**::

    doormouse import PATH_TO_CERTFILE

**Forget a certificate**::

    doormouse forget SERIAL_NUMBER

**Print a list of expiring certificates**::

    doormouse warn DAYS

**Export a certificate public key**::

    doormouse export SERIAL [OUTFILE]

**Export a certificate with public and private key**::

    doormouse export -k SERIAL [OUTFILE]

**Export a certificate with public key and ca chain**::

    doormouse export -c SERIAL [OUTFILE]

Caveats
~~~~~~~
* PyOpenSSL does not provide a way to extract subjectAltNames from a CSR, therefore we do not
  support CSRs with subjectAltNames.  This is a bummer.
* PyOpenSSL does not provide a way to get interpreted data from X509 extensions, making it difficult
  to test extension settings in unit tests.

Who are you people?
-------------------

We're BrainGu! A multi-disciplined group of systems admins, software developers, devops and 
security engineers trying to make it easier to secure networks and systems.
