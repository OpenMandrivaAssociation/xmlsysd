%define name    xmlsysd
%define version 1.0.4
%define release 8
# The following should match PROGRAM, VERSION and RELEASE in the
# Makefile accompanying this program (and the .tgz defined in Source
# below.

Summary: XML-based system information daemon

Name: %name
Version: %version
Release: %release
Group: Monitoring
Url: https://www.phy.duke.edu/~rgb/Beowulf/xmlsysd.php
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



%changelog
* Wed Sep 09 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.0.4-7mdv2010.0
+ Revision: 435153
- rebuild

* Sun Aug 03 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.0.4-6mdv2009.0
+ Revision: 262463
- rebuild

* Thu Jul 31 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.0.4-5mdv2009.0
+ Revision: 257186
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.0.4-3mdv2008.1
+ Revision: 168512
- rebuild
- fix summary
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Aug 19 2007 Pascal Terjan <pterjan@mandriva.org> 1.0.4-2mdv2008.0
+ Revision: 66503
- Fix BuildRequires for x86_64


* Fri Sep 23 2005 Erwan Velu <erwan@seanodes.com> 1.0.4-1mdk
- 1.0.4

* Tue Mar 22 2005 Antoine Ginies <aginies@n1.mandrakesoft.com> 0.2.6-2mdk
- rebuild

* Thu Oct 07 2004 Erwan Velu <erwan@mandrakesoft.com> 0.2.6-1mdk
- 0.2.6

* Fri Aug 13 2004 Erwan Velu <erwan@mandrakesoft.com> 0.2.5-1mdk
- 0.2.5

* Wed Jun 23 2004 Erwan Velu <erwan@mandrakesoft.com> 0.2.3-1mdk
- 0.2.3

* Fri Jun 18 2004 Erwan Velu <erwan@mandrakesoft.com> 0.2.2-2mdk
- Adding proc-net patch
- Removing group entry in /etc/xinetd.d/xmlsysd
- Cleaning xinetd configuration

* Fri Jun 18 2004 Erwan Velu <erwan@mandrakesoft.com> 0.2.2-1mdk
- Initial relase
- Adding buildrequires

* Mon Apr 29 2002 Robert G. Brown <rgb@duke.edu>
- Releasing v 0.1.0 beta -- this has now been "stable" for weeks.

* Wed Mar 13 2002 Robert G. Brown <rgb@duke.edu>
- set up and built for RH 7.2

