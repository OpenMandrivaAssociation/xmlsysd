%define name    xmlsysd
%define version 1.0.4
%define release %mkrel 2
# The following should match PROGRAM, VERSION and RELEASE in the
# Makefile accompanying this program (and the .tgz defined in Source
# below.

Summary: XML-based system information daemon

Name: %name
Version: %version
Release: %release
Group: Monitoring
Url: http://www.phy.duke.edu/~rgb/Beowulf/xmlsysd.php
License: GPL
Source: http://www.phy.duke.edu/~rgb/wulfware/%{name}-%{version}.tgz
Source1: %{name}.xinetd
Buildroot: %{_tmppath}/%{name}root
BuildRequires: libxml2-devel, libwulf-devel
Patch0:	xmlsysd-proc-net.patch
Requires: xinetd

%description 
xmlsysd is a system information daemon that recognizes a simple command
language that causes it to execute certain systems calls and parse
various system information files in /proc, convert the information it
thus obtains into an xml encapsulation, and send the xml data out via a
socket connection.  It supports both a forking daemon mode that can be
run from userspace and an xinetd mode that can be run out of xinetd.  In
most situations the latter is more securable and controllable and this
rpm installs it in this mode.  

The xml encapsulation of system and proc data is documented within this
package to facilitate the construction of web or other applications that
connect to the daemon, retrieve the information it provides on some
polling loop, and extract the data for presentation.  In addition, the
source and xml itself is reasonably extensible so that it should be easy
to add new things to be monitored to the daemon in ways that don't break
existing applications (applications should always ignore any field tags
they don't recognize and should also be able to cope with missing field
tags that they expect to be there).  One monitoring application,
wulfstat, should generally be available in a separate rpm packaging.

The construction of xmlsysd is deliberately lightweight -- it is a
(hopefully) efficiently coded C-source binary application that tries to
make a minimal impact on the cpu, memory and network resources of the
host being monitored.  This design goal should be preserved if at all
possible by programmers seeking to add features or fields to be
monitored.

%prep
%setup -q -n %{name}
#%patch0 -p0

%build
make clean
%make

%install
%make PREFIX=%{buildroot}/usr install
mkdir -p %{buildroot}/%{_sysconfdir}/xinetd.d/
cp -vf %SOURCE1 %{buildroot}/%{_sysconfdir}/xinetd.d/xmlsysd

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
# The xmlsysd binary
%attr(755,root,root) %{_sbindir}/xmlsysd
# The xmlsysd man page
%attr(644,root,root) %{_mandir}/man8/xmlsysd.8.*
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}*

# The xmlsysd docs
%doc README TODO COPYING CHANGELOG DESIGN

%post
service xinetd condrestart

%postun
service xinetd condrestart

