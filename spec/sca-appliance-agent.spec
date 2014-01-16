# Copyright (C) 2013,2014 SUSE LLC
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# norootforbuild
# neededforbuild
%define sca_common sca

Name:         sca-appliance-agent
Summary:      Supportconfig Analysis Appliance Agent
URL:          https://bitbucket.org/g23guy/sca-appliance-agent
Group:        Documentation/SuSE
Distribution: SUSE Linux Enterprise
Vendor:       SUSE Support
License:      GPL-2.0
Autoreqprov:  on
Version:      1.3
Release:      0
Source:       %{name}-%{version}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-%{version}
Buildarch:    noarch
Requires:     /usr/bin/vmstat
Requires:     sca-appliance-common
Requires:     sca-patterns-base

%description
Analyzes supportconfig archives using the Supportconfig Analysis patterns. The results are
posted in a MySQL database and can be posted or emailed as an html report. 

Authors:
--------
    Jason Record <jrecord@suse.com>

%prep
%setup -q

%build
gzip -9f man/*

%install
pwd;ls -la
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/%{sca_common}
install -d $RPM_BUILD_ROOT/var/tmp/%{sca_common}
install -d $RPM_BUILD_ROOT/usr/sbin
install -d $RPM_BUILD_ROOT/usr/share/man/man1
install -d $RPM_BUILD_ROOT/usr/share/man/man5
install -d $RPM_BUILD_ROOT/usr/share/doc/packages/%{sca_common}
install -m 644 config/*.conf $RPM_BUILD_ROOT/etc/%{sca_common}
install -m 644 config/* $RPM_BUILD_ROOT/usr/share/doc/packages/%{sca_common}
install -m 544 bin/* $RPM_BUILD_ROOT/usr/sbin
install -m 644 docs/* $RPM_BUILD_ROOT/usr/share/doc/packages/%{sca_common}
install -m 644 man/*.1.gz $RPM_BUILD_ROOT/usr/share/man/man1
install -m 644 man/*.5.gz $RPM_BUILD_ROOT/usr/share/man/man5

%files
%defattr(-,root,root)
%dir /etc/%{sca_common}
%dir /var/tmp/%{sca_common}
%dir /usr/share/doc/packages/%{sca_common}
/usr/sbin/*
%config /etc/%{sca_common}/*
%doc /usr/share/man/man1/*
%doc /usr/share/man/man5/*
%doc /usr/share/doc/packages/%{sca_common}/*

%changelog
* Thu Jan 16 2014 jrecord@suse.com
- SCADIAG_HOME renamed to SCA_WORK
- SPRSRC renamed to PATTERN_LIBRARY_BASE
- relocated files according to FHS

* Thu Jan 07 2014 jrecord@suse.com
- updated pattern filter in sdagent-patterns
- sdagent-patterns has more explicit zypper startup options
- separated sca-appliance-common files

* Tue Dec 24 2013 jrecord@suse.com
- annotated sdagent.conf
- added ARCH_LOCATION to sdagent.conf
- sdagent-worker inserts ARCH_LOCATION into SQL import file

* Thu Dec 20 2013 jrecord@suse.com
- separated as individual RPM package
- sends email for pattern updates when $EMAIL_LEVEL -gt $EMAIL_MIN
- correctly checks for SUSE Linux Enterpise archives only
- sdagent-patterns now updates from the OBS pattern repo
  * using -u prevents updates

