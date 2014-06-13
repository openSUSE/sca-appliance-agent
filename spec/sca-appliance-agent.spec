# spec file for package sca-appliance-agent
#
# Copyright (C) 2014 SUSE LLC
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Source developed at:
#  https://github.com/g23guy/sca-appliance-agent
#
# norootforbuild
# neededforbuild
%define sca_common sca

Name:         sca-appliance-agent
Summary:      Supportconfig Analysis Appliance Agent
URL:          https://github.com/g23guy/sca-appliance-agent
Group:        System/Monitoring
License:      GPL-2.0
Autoreqprov:  on
Version:      1.3
Release:      28
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
gzip -9f man/*8
gzip -9f man/*5

%install
pwd;ls -la
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/%{sca_common}
install -d $RPM_BUILD_ROOT/usr/sbin
install -d $RPM_BUILD_ROOT/usr/share/man/man8
install -d $RPM_BUILD_ROOT/usr/share/man/man5
install -d $RPM_BUILD_ROOT/usr/share/doc/packages/%{sca_common}
install -d $RPM_BUILD_ROOT/usr/lib/%{sca_common}/php
install -m 444 man/COPYING.GPLv2 $RPM_BUILD_ROOT/usr/share/doc/packages/%{sca_common}
install -m 644 config/*.conf $RPM_BUILD_ROOT/etc/%{sca_common}
install -m 644 config/* $RPM_BUILD_ROOT/usr/share/doc/packages/%{sca_common}
install -m 544 bin/sdagent* $RPM_BUILD_ROOT/usr/sbin
install -m 640 bin/reportfull.php $RPM_BUILD_ROOT/usr/lib/%{sca_common}/php
install -m 644 docs/* $RPM_BUILD_ROOT/usr/share/doc/packages/%{sca_common}
install -m 644 man/*.8.gz $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 man/*.5.gz $RPM_BUILD_ROOT/usr/share/man/man5

%files
%defattr(-,root,root)
%dir /etc/%{sca_common}
%dir /usr/share/doc/packages/%{sca_common}
%dir /usr/lib/%{sca_common}
%dir /usr/lib/%{sca_common}/php
/usr/lib/%{sca_common}/php/*
/usr/sbin/*
%config /etc/%{sca_common}/*
%doc /usr/share/man/man8/*
%doc /usr/share/man/man5/*
%doc /usr/share/doc/packages/%{sca_common}/*

%changelog

