%define	name	gnokii
%define	version	0.6.30
%define	rel	1
%define	release	%mkrel %{rel}
%define	Summary	Tool suite for Nokia mobile phones

%define	major	6
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

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}

# Rename smsd to gnokii-smsd
mv %buildroot%{_bindir}/{,gnokii-}smsd
mv %buildroot%{_mandir}/man8/{,gnokii-}smsd.8
sed -i 's,smsd ,gnokii-smsd ,' %buildroot%{_mandir}/man8/gnokii-smsd.8
sed -i 's,smsd.,gnokii-smsd.,' %buildroot%{_mandir}/man8/gnokii-smsd.8

install -d $RPM_BUILD_ROOT%{_sysconfdir}
sed 's#/usr/local/sbin/#%{_sbindir}/#' <Docs/sample/gnokiirc >$RPM_BUILD_ROOT%{_sysconfdir}/gnokiirc

# remove smsd libtool archives
rm -f %buildroot%_libdir/smsd/*.{la,a}

# install the configuration files
install -Dpm 755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/gnokii-smsd
install -Dpm 640 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/gnokii-smsd
install -Dpm 644 %{SOURCE4} \
  $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/gnokii-smsd

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/x%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/x%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/x%{name}.png

install -d $RPM_BUILD_ROOT%{_var}/lock/gnokii

%find_lang %{name}

%pre
%_pre_groupadd %{name}

%postun
%_postun_groupdel %{name}

%if %mdkversion < 200900
%post xgnokii
%{update_menus}
%endif

%if %mdkversion < 200900
%postun xgnokii
%{clean_menus}
%endif

%pre smsd
%_pre_useradd gnokii / /sbin/nologin

%postun smsd
%_postun_userdel gnokii

%post smsd
%_post_service gnokii-smsd

%preun smsd
%_preun_service gnokii-smsd

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

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
%{_libdir}/*.la
%{_libdir}/pkgconfig/*

%files -n %{libnamestaticdev}
%defattr(-,root,root)
%{_libdir}/*.a
