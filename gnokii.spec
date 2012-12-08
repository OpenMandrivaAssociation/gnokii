%define	name	gnokii
%define	version	0.6.31
%define	rel	1
%define	release	%mkrel %{rel}
%define	Summary	Tool suite for Nokia mobile phones

%define	major	7
%define	libname			%mklibname %{name} %major
%define	libnamedev		%mklibname %{name} -d
%define	libnamestaticdev	%mklibname %{name} -d -s

Summary:	%{Summary}
Name:		%{name}
Version: 	%{version}
%if %mdkversion < 201000
%define subrel  1
%endif
Release:	%{release}
License:	GPLv2+
Url:		http://www.gnokii.org/
Group:		Communications
Source0:	http://www.gnokii.org/download/gnokii/%{name}-%{version}.tar.bz2
Source2:        %{name}-smsd.init
Source3:        %{name}-smsd.sysconfig
Source4:        %{name}-smsd.logrotate
Source5:        %{name}-smsd2mail.sh
Source6:        %{name}-smsd-README.smsd2mail
Patch3:		gnokii-0.6.8-fix-locking.patch
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Buildrequires:	xpm-devel gtk+2-devel bison bluez-devel
BuildRequires:	libusb-devel
BuildRequires:	libical-devel
BuildRequires:	mysql-devel postgresql-devel
BuildRequires:	sqlite3-devel
BuildRequires:	gettext-devel intltool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(pre):	rpm-helper
Requires(postun):	rpm-helper

%description
Gnokii is a Linux/Unix tool suite and (eventually) modem/fax driver for
Nokia's mobile phones, released under the GPL.

%package	xgnokii
Summary:	Graphical Linux/Unix tool suite for Nokia mobile phones
Group:		Communications
Requires:	%{name}
Requires:	xdg-utils

%description	xgnokii
Xgnokii is graphical Linux/Unix tool suite for Nokia's mobile phones. It
allows you to edit your contacts book, send/read SMS's from/in
computer and more other features.

%package        smsd
Summary:        Gnokii SMS daemon
Group:          Communications
Requires:       %{name} = %{version}-%{release}
Requires(post):  rpm-helper
Requires(preun):  rpm-helper

%description    smsd
The Gnokii SMS daemon receives and sends SMS messages.

%package        smsd-pgsql
Summary:        PostgreSQL support for Gnokii SMS daemon
Group:          Communications
Requires:       %{name}-smsd = %{version}-%{release}

%description    smsd-pgsql
%{summary}.

%package        smsd-mysql
Summary:        MySQL support for Gnokii SMS daemon
Group:          Communications
Requires:       %{name}-smsd = %{version}-%{release}

%description    smsd-mysql
%{summary}.

%package -n	%{libname}
Summary:	Linux/Unix tool suite for Nokia mobile phones
Group: 		System/Libraries

%description -n %{libname}
Gnokii is a Linux/Unix tool suite and (eventually) modem/fax driver for
Nokia's mobile phones, released under the GPL.

Libraries

%package -n	%{libnamedev}
Summary:	Development libraries and headers for gnokii
Group: 		Development/C
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Obsoletes:	%mklibname -d %name 3

%description -n %{libnamedev}
Gnokii is a Linux/Unix tool suite and (eventually) modem/fax driver for
Nokia's mobile phones, released under the GPL.

Development Libraries

%package -n	%{libnamestaticdev}
Summary:	Static library for gnokii
Group:		Development/C
Provides:	%{name}-static = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	lib%{name}-static = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Obsoletes:	%mklibname -d -s %name 3

%description -n	%{libnamestaticdev}
Static library for %{name}

%prep
%setup -q -n %{name}-%{version}
%patch3 -p1 -b .lock
autoreconf -fi

install -pm 644 %{SOURCE5} smsd2mail.sh
install -pm 644 %{SOURCE6} README.smsd2mail

%build
%configure2_5x	--enable-security \
		--with-pic \
		--enable-libusb
%make
cd xgnokii
%make

%install
rm -rf %{buildroot}
%{makeinstall_std}
cd xgnokii
%{makeinstall_std}
cd ..

# Rename smsd to gnokii-smsd
mv %buildroot%{_bindir}/{,gnokii-}smsd
mv %buildroot%{_mandir}/man8/{,gnokii-}smsd.8
sed -i 's,smsd ,gnokii-smsd ,' %buildroot%{_mandir}/man8/gnokii-smsd.8
sed -i 's,smsd.,gnokii-smsd.,' %buildroot%{_mandir}/man8/gnokii-smsd.8

install -d %{buildroot}%{_sysconfdir}
sed 's#/usr/local/sbin/#%{_sbindir}/#' <Docs/sample/gnokiirc >%{buildroot}%{_sysconfdir}/gnokiirc

# remove smsd libtool archives
rm -f %buildroot%_libdir/smsd/*.{la,a}

# install the configuration files
install -Dpm 755 %{SOURCE2} %{buildroot}%{_initrddir}/gnokii-smsd
install -Dpm 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/gnokii-smsd
install -Dpm 644 %{SOURCE4} \
  %{buildroot}%{_sysconfdir}/logrotate.d/gnokii-smsd

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/x%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/x%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/x%{name}.png

install -d %{buildroot}%{_var}/lock/gnokii

%find_lang %{name}

%pre
%_pre_groupadd %{name}

%postun
%_postun_groupdel %{name}

%pre smsd
%_pre_useradd gnokii / /sbin/nologin

%postun smsd
%_postun_userdel gnokii

%post smsd
%_post_service gnokii-smsd

%preun smsd
%_preun_service gnokii-smsd

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog TODO MAINTAINERS
%doc Docs/Bugs Docs/CREDITS Docs/DataCalls-QuickStart
%doc Docs/FAQ Docs/gnokii-IrDA-Linux Docs/gnokii-ir-howto
%doc Docs/gnokii.nol Docs/KNOWN_BUGS
%doc Docs/README* Docs/sample
%doc Docs/*.txt
%doc utils/*.sis
%{_bindir}/%{name}
%{_bindir}/sendsms
%{_bindir}/%{name}d
%{_sbindir}/m%{name}dev
%config(noreplace) %{_sysconfdir}/%{name}rc
%attr(777,root,gnokii) %{_var}/lock/gnokii
%{_mandir}/man1/gnokii.1*
%{_mandir}/man1/sendsms.1*
%{_mandir}/man8/gnokiid.8*
%{_mandir}/man8/mgnokiidev.8*

%files xgnokii -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/x%{name}
%{_datadir}/applications/xgnokii.desktop
%{_miconsdir}/x%{name}.png
%{_iconsdir}/x%{name}.png
%{_liconsdir}/x%{name}.png
%{_mandir}/man1/xgnokii*

%files smsd
%defattr(-,root,root,-)
%doc smsd/action smsd/ChangeLog smsd/README README.smsd2mail smsd2mail.sh
%attr(-,gnokii,gnokii) %config(noreplace) %{_sysconfdir}/sysconfig/gnokii-smsd
%config(noreplace) %{_sysconfdir}/logrotate.d/gnokii-smsd
%{_initrddir}/gnokii-smsd
%{_bindir}/gnokii-smsd
%{_mandir}/man8/gnokii-smsd.8*
%dir %{_libdir}/smsd/
%{_libdir}/smsd/libsmsd_file.so
%{_libdir}/smsd/libsmsd_sqlite.so

%files smsd-pgsql
%defattr(-,root,root,-)
%doc smsd/sms.tables.pq.sql
%{_libdir}/smsd/libsmsd_pq.so

%files smsd-mysql
%defattr(-,root,root,-)
%doc smsd/sms.tables.mysql.sql
%{_libdir}/smsd/libsmsd_mysql.so

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc Docs/gnokii-hackers-howto
%doc Docs/gettext-howto
%doc Docs/protocol
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/*.so
%if %mdvver <= 201100
%{_libdir}/*.la
%endif
%{_libdir}/pkgconfig/*

%files -n %{libnamestaticdev}
%defattr(-,root,root)
%{_libdir}/*.a


%changelog
* Mon Mar 19 2012 Götz Waschk <waschk@mandriva.org> 0.6.31-1mdv2012.0
+ Revision: 785530
- remove libtool archives on Cooker
- new major
- fix xgnokii build
- enable libical support
- spec cleanup
- new version

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.30-3
+ Revision: 664858
- mass rebuild

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.30-2
+ Revision: 645747
- relink against libmysqlclient.so.18

* Sun Jan 23 2011 Götz Waschk <waschk@mandriva.org> 0.6.30-1
+ Revision: 632446
- new version
- add sqlite module for smsd

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.29-3mdv2011.0
+ Revision: 626998
- rebuilt against mysql-5.5.8 libs, again

* Mon Dec 27 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.29-2mdv2011.0
+ Revision: 625419
- rebuilt against mysql-5.5.8 libs

* Wed Aug 04 2010 Funda Wang <fwang@mandriva.org> 0.6.29-1mdv2011.0
+ Revision: 565946
- new version 0.6.29

* Wed Feb 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.28.1-2mdv2010.1
+ Revision: 507029
- rebuild

* Sun Dec 27 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.6.28.1-1mdv2010.1
+ Revision: 482771
- update to new release and ditch all obsolete patches

* Mon Sep 14 2009 Götz Waschk <waschk@mandriva.org> 0.6.27-5mdv2010.0
+ Revision: 440016
- update build deps
- fix linking

* Wed Aug 12 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.6.27-4mdv2010.0
+ Revision: 415373
- push new release to fix wformat errors
- fix -Wformat warnings

  + Oden Eriksson <oeriksson@mandriva.com>
    - prepare for updates

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.27-3mdv2009.1
+ Revision: 311200
- rebuilt against mysql-5.1.30 libs

* Sun Nov 09 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.27-2mdv2009.1
+ Revision: 301573
- rebuilt against new libxcb

* Sun Oct 12 2008 Funda Wang <fwang@mandriva.org> 0.6.27-1mdv2009.1
+ Revision: 292708
- New version 0.6.27
- drop unused patch4 (fixed by upstream already)
- rediff brwoser patch

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jun 01 2008 Funda Wang <fwang@mandriva.org> 0.6.26-1mdv2009.0
+ Revision: 213876
- fix groups
- New version 0.6.26
- add smsd package ( files migrated from fedora )

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 25 2007 Funda Wang <fwang@mandriva.org> 0.6.22-1mdv2008.1
+ Revision: 111841
- New version 0.6.22
- clean old patches

* Fri Nov 16 2007 Funda Wang <fwang@mandriva.org> 0.6.21-2mdv2008.1
+ Revision: 109122
- disable parallel build
- bump release
- really fix pkgconfig install
- use xdg-open for help files
- fix gnokii.pc install

* Mon Nov 12 2007 Funda Wang <fwang@mandriva.org> 0.6.21-1mdv2008.1
+ Revision: 108080
- fix pkconfig file install
- New version 0.6.21

* Sat Nov 10 2007 Christiaan Welvaart <spturtle@mandriva.org> 0.6.20-1mdv2008.1
+ Revision: 107307
- 0.6.20
- patch5: do not run make in Docs dir as no Makefile is present there

* Sat Nov 03 2007 Christiaan Welvaart <spturtle@mandriva.org> 0.6.19-2mdv2008.1
+ Revision: 105564
- enable libusb
- patch4: fix a stack corruption for nk6510

* Wed Oct 10 2007 Funda Wang <fwang@mandriva.org> 0.6.19-1mdv2008.1
+ Revision: 96763
- New version 0.6.19

  + Thierry Vignaud <tv@mandriva.org>
    - fix man pages extension

* Wed Jul 25 2007 Funda Wang <fwang@mandriva.org> 0.6.18-1mdv2008.0
+ Revision: 55155
- New version 0.6.18
- New version

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - New version  0.6.15


* Sat Jan 13 2007 Jérôme Soyer <saispo@mandriva.org> 0.6.14-1mdv2007.0
+ Revision: 108284
- New release 0.6.14
- Import gnokii

* Thu Aug 17 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.13-6mdv2007.0
- fix menu icon
- add/remove %%doc
- do parallell build and work around brokeness

* Wed Aug 16 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.13-5mdv2007.0
- install man pages

* Sun Aug 13 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.6.13-4
- add BuildRequires: desktop-file-utils

* Wed Aug 09 2006 Laurent MONTEL <lmontel@mandriva.com> 0.6.13-3
- Rebuild

* Thu Jul 20 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.13-2mdv2007.0
- fix major

* Thu Jul 20 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.13-1mdv2007.0
- New release 0.6.13
- fix xdg menu and move it to xgnokii package
- fix macro-in-%%changelog

* Thu Jun 15 2006 Laurent MONTEL <lmontel@mandriva.com> 0.6.12-2
- Rebuild

* Thu Apr 06 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.12-1mdk
- New release 0.6.12

* Wed Mar 01 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.6.11-2mdk
- BuildRequires: gtk+-devel => gtk+2-devel

* Tue Feb 28 2006 Jerome Soyer <saispo@mandriva.org> 0.6.11-1mdk
- New release 0.6.11

* Tue Sep 06 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.8-2mdk
- "fix" problem with locking (P3, should fix #14601)

* Fri Aug 05 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.8-1mdk
- New release 0.6.8

* Fri Jul 08 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.7-1mdk
- 0.6.7
- regenerate P0
- drop P2 (fixed upstream)
- fix requires

* Fri May 13 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.6.5-1mdk
- 0.6.5
- fix build with gcc-4.0.0 (P2)
- drop P1 (merged upstream)
- %%mkrel

* Wed Feb 16 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 0.6.4-4mdk 
- Patch1 (CVS): fix crash with some locales (Mdk bug #13666)

* Fri Feb 11 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.4-3mdk
- fix deps
- libtool fixes to nuke lib64 rpaths

* Fri Nov 19 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.6.4-2mdk
- Fix provides

* Fri Nov 19 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.6.4-1mdk
- 0.6.4

* Fri Oct 01 2004 Buchan Milne <bgmilne@linux-mandrake.com> 0.6.3-2mdk
- ship the gnapplet.sis tool required by Symbian phones for bluetooth use
  (GPL, version dependent and not easily available anywhere else)
- make xgnokii require gnokii (needs a config file)
- fix menu file name and title

* Thu Aug 19 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.6.3-1mdk
- 0.6.3
- use %%configure macro

* Thu Apr 15 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.6.1-1mdk
- 0.6.1

* Wed Feb 11 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.5.10-2mdk
- Fix generate menu

* Mon Feb 02 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.5.10-1mdk
- 0.5.10
- use new menu section

