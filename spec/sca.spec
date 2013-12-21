# Copyright (C) 2013 SUSE LLC
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# norootforbuild
# neededforbuild

##################################################################
## Update REPO_URL, FPAT_URL in sdagent.conf before release
## Update FPAT_URL in reportfull.php before release
##################################################################

# test updating the rpm

Name:         sca
Summary:      Supportconfig Analysis Appliance
Group:        Documentation/SuSE
Distribution: SUSE Linux Enterprise
Vendor:       SUSE Support
License:      GPLv2
Autoreqprov:  on
Version:      1.2
Release:      1.131220.PTF.1
Source:       %{name}-%{version}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-%{version}
Buildarch:    noarch

%description
Source for sca-broker, sca-agent and sca-pattern-devel subpackages. The 
tool uses the Supportconfig Analysis patterns to analyze supportconfig 
archives identifying known issues. 

Authors:
--------
    Jason Record <jrecord@suse.com>

##################################################################
# Broker
##################################################################

%package broker
Summary:      Supportconfig Analysis Broker
Group:        Documentation/SuSE
Requires:     apache2
Requires:     curl
Requires:     php5, php5-bz2, php5-mbstring, php5-mcrypt, php5-mysql, php5-zip, php5-zlib
Requires:     /usr/bin/ssh
Requires:     /usr/bin/dos2unix
Requires:     /bin/logger
Requires:     /usr/bin/mysql
Requires:     /usr/sbin/mysqld
Requires:     /usr/bin/sed
Requires:     /usr/bin/awk
Requires:     /bin/ping

%description broker
Monitors inbound supportconfig archives and is responsible for assigning new and retry 
archives to appropriate agents for analysis. 

Authors:
--------
    Jason Record <jrecord@suse.com>

%prep broker
%setup -q

%build broker
gzip -9f scatool.8

%install broker
pwd;ls -la
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/opt/%{name}
install -d $RPM_BUILD_ROOT/opt/%{name}/bin
install -d $RPM_BUILD_ROOT/srv/www/htdocs/sca
install -d $RPM_BUILD_ROOT/srv/www/htdocs/sdp
install -d $RPM_BUILD_ROOT/usr/sbin
install -d $RPM_BUILD_ROOT/usr/share/man/man1
install -d $RPM_BUILD_ROOT/usr/share/man/man5
install -d $RPM_BUILD_ROOT/usr/share/doc/packages/%{name}
install -d $RPM_BUILD_ROOT/var/opt/%{name}
install -m 644 config/sdbroker.conf $RPM_BUILD_ROOT/etc/opt/%{name}
install -m 544 bin/scadb $RPM_BUILD_ROOT/opt/%{name}/bin
install -m 544 bin/sdbroker $RPM_BUILD_ROOT/opt/%{name}/bin
install -m 544 bin/sdbroker-monitor $RPM_BUILD_ROOT/opt/%{name}/bin
install -m 544 bin/setup-sca $RPM_BUILD_ROOT/opt/%{name}/bin
install -m 544 bin/setup-sdagent $RPM_BUILD_ROOT/opt/%{name}/bin
install -m 544 bin/setup-sdbroker $RPM_BUILD_ROOT/opt/%{name}/bin
install -m 644 websca/* $RPM_BUILD_ROOT/srv/www/htdocs/sca
install -m 644 websca/index.html $RPM_BUILD_ROOT/usr/share/doc/packages/%{name}
install -m 544 bin/scadb $RPM_BUILD_ROOT/usr/sbin
install -m 544 bin/setup-sca $RPM_BUILD_ROOT/usr/sbin
install -m 644 schema/ServerDiagnostics* $RPM_BUILD_ROOT/usr/share/doc/packages/%{name}
install -m 644 config/combined.cron $RPM_BUILD_ROOT/usr/share/doc/packages/%{name}
install -m 644 config/sdbroker.cron $RPM_BUILD_ROOT/usr/share/doc/packages/%{name}
install -m 644 docs/README.sdbroker $RPM_BUILD_ROOT/usr/share/doc/packages/%{name}
install -m 644 man/scadb.1.gz $RPM_BUILD_ROOT/usr/share/man/man1
install -m 644 man/sdbroker.1.gz $RPM_BUILD_ROOT/usr/share/man/man1
install -m 644 man/setup-sdagent.1.gz $RPM_BUILD_ROOT/usr/share/man/man1
install -m 644 man/setup-sdbroker.1.gz $RPM_BUILD_ROOT/usr/share/man/man1
install -m 644 man/sdbroker.conf.5.gz $RPM_BUILD_ROOT/usr/share/man/man5

%files broker
%defattr(-,root,root)
%dir /opt
%dir /etc/opt
%dir /var/opt
%dir /srv/www/htdocs/sca
%dir /opt/%{name}/bin
%dir /opt/%{name}
%dir /etc/opt/%{name}
%dir /var/opt/%{name}
%dir /usr/share/doc/packages/%{name}
%attr(0744,root,root) /usr/sbin/setup-sca
/opt/%{name}/bin/sdbroker
/opt/%{name}/bin/sdbroker-monitor
/opt/%{name}/bin/setup-sdbroker
/opt/%{name}/bin/setup-sdagent
/opt/%{name}/bin/setup-sca
/opt/%{name}/bin/scadb
/usr/sbin/scadb
%config /etc/opt/%{name}/sdbroker.conf
/usr/share/man/man1/sdbroker*.1.gz
/usr/share/man/man1/setup-sdbroker.1.gz
/usr/share/man/man1/setup-sdagent.1.gz
/usr/share/man/man1/scadb.1.gz
/usr/share/man/man5/sdbroker.conf.5.gz
%attr(-,wwwrun,www) /srv/www/htdocs/sca
%attr(-,wwwrun,www) /usr/share/doc/packages/%{name}/index.html
%doc /usr/share/doc/packages/%{name}/README.broker
%doc /usr/share/doc/packages/%{name}/ServerDiagnostic*sql
%doc /usr/share/doc/packages/%{name}/sdbroker.cron
%doc /usr/share/doc/packages/%{name}/combined.cron

%post broker
if [ -s /srv/www/htdocs/index.html ]; then
	if grep -i '<html><body><h1>It works!</h1></body></html>' /srv/www/htdocs/index.html &>/dev/null; then
		cp -a /usr/share/doc/packages/%{name}/index.html /srv/www/htdocs/
	else
		echo
		echo "WARNING: File already exists: /srv/www/htdocs/index.html"
		echo " Redirector /usr/share/doc/packages/%{name}/index.html will not be installed."
		echo
	fi
else
	cp -a /usr/share/doc/packages/%{name}/index.html /srv/www/htdocs/
fi

##################################################################
# Agent
##################################################################

%package agent
Summary:      Supportconfig Analysis Agent
Group:        Documentation/SuSE
Requires:     curl
Requires:     /bin/logger
Requires:     /usr/bin/mysql
Requires:     /usr/bin/perl
Requires:     /usr/bin/sed
Requires:     /usr/bin/awk
Requires:     /bin/ping
Requires:     /usr/bin/vmstat

%description agent
Analyzes supportconfig archives using the Support Advisor patterns. The results are
posted in a MySQL database and can be posted or emailed as an html report. 

Authors:
--------
    Jason Record <jrecord@suse.com>

%files agent
%defattr(-,root,root)
%dir /opt
%dir /etc/opt
%dir /var/opt
/opt/%{name}/bin/sdagent
/opt/%{name}/bin/sdagent-worker
/opt/%{name}/bin/sdagent-config
/opt/%{name}/bin/sdagent-monitor
/opt/%{name}/bin/sdagent-health
/opt/%{name}/bin/sdagent-patterns
/opt/%{name}/patterns
/opt/%{name}/%{name}
%dir /opt/%{name}/bin
%dir /opt/%{name}
%config /etc/opt/%{name}/sdagent.conf
%dir /etc/opt/%{name}
%dir /var/opt/%{name}/patterns
%dir /var/opt/%{name}
/usr/share/man/man1/sdagent*.1.gz
/usr/share/man/man5/sdagent*.5.gz
%doc /usr/share/doc/packages/%{name}/README.agent
%doc /usr/share/doc/packages/%{name}/sdagent.cron
%doc /usr/share/doc/packages/%{name}/curl.codes.txt
%dir /usr/share/doc/packages/%{name}

##################################################################
# Pattern Database
##################################################################

%package pattern-devel
Summary:      Supportconfig Analysis Pattern Database
Group:        Documentation/SuSE
Requires:     apache2
Requires:     /usr/bin/mysql
Requires:     /usr/sbin/mysqld
Requires:     php5, php5-bz2, php5-mbstring, php5-mcrypt, php5-mysql, php5-zip, php5-zlib

%description pattern-devel
Database to keep track of custom SCA patterns 

Authors:
--------
    Jason Record <jrecord@suse.com>

%files pattern-devel
%defattr(-,root,root)
%dir /opt
%dir /etc/opt
%dir /srv/www/htdocs/sdp
%dir /opt/%{name}/bin
%dir /opt/%{name}
%dir /etc/opt/%{name}
%dir /var/opt/%{name}
%dir /usr/share/doc/packages/%{name}
/opt/%{name}/bin/setup-sdp
/opt/%{name}/bin/sdpdb
/usr/sbin/sdpdb
/usr/share/man/man1/setup-sdp.1.gz
/usr/share/man/man5/sdp.conf.5.gz
%doc /usr/share/doc/packages/%{name}/README.patterns
%config /etc/opt/%{name}/sdp.conf
%attr(-,wwwrun,www) /srv/www/htdocs/sdp
%doc /usr/share/doc/packages/%{name}/SCA*sql

##################################################################
# Final processing
##################################################################

%changelog
* Mon Dec 18 2013 jrecord@suse.com
- fixed SDP XSS and SQL injection vulnerabilities

* Thu Dec 12 2013 jrecord@suse.com
- sends email for pattern updates when $EMAIL_LEVEL -gt $EMAIL_MIN
- SCA reports page sorts by all columns
- correctly checks for SUSE Linux Enterpise archives only
- sdagent-patterns now updates from the OBS pattern repo
  * using -u prevents updates
- fixed SCA XSS vulnerabilities
- fixed SCA SQL injection vulnerabilities

* Wed Dec 04 2013 jrecord@suse.com
- forgot to update all versions to 1.0.0
- added report link to SUSE Studio home page

* Tue Dec 03 2013 jrecord@suse.com
- initial release

