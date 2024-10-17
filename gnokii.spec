%define url_ver %(echo %{version}|cut -d. -f1,2).x
%define _disable_ld_no_undefined 1

%define major 7
%define libname %mklibname %{name} %major
%define devname %mklibname %{name} -d

Summary:	Summary Tool suite for Nokia mobile phones
Name:		gnokii
Version: 	0.6.31
Release:	16
License:	GPLv2+
Group:		Communications
Url:		https://www.gnokii.org/
Source0:	http://www.gnokii.org/download/gnokii/%{url_ver}/%{name}-%{version}.tar.bz2
Source2:	%{name}-smsd.init
Source3:	%{name}-smsd.sysconfig
Source4:	%{name}-smsd.logrotate
Source5:	%{name}-smsd2mail.sh
Source6:	%{name}-smsd-README.smsd2mail
Patch3:		gnokii-0.6.8-fix-locking.patch
Patch4:		gnokii-clang.patch
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png

BuildRequires:	bison
BuildRequires:	intltool
BuildRequires:	gettext-devel
BuildRequires:	mysql-devel
BuildRequires:	readline-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libical)
BuildRequires:	pkgconfig(libpcsclite)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(sqlite3)
Buildrequires:	pkgconfig(xpm)
Requires(pre,postun):	rpm-helper

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
Requires(post,preun):  rpm-helper

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
Libraries

%package -n	%{devname}
Summary:	Development libraries and headers for gnokii
Group: 		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}

%description -n %{devname}
Development Libraries

%prep
%setup -q
%autopatch -p1
#autoreconf -fi

install -pm 644 %{SOURCE5} smsd2mail.sh
install -pm 644 %{SOURCE6} README.smsd2mail

%build
%configure	\
	--disable-static \
	--enable-libusb \
	--enable-security \
	--with-pic
%make_build
cd xgnokii
%make_build

%install
%make_install
%make_install -C xgnokii

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

%files
%doc ChangeLog TODO MAINTAINERS
%doc %{_docdir}/gnokii
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
%{_bindir}/x%{name}
%{_datadir}/applications/xgnokii.desktop
%{_miconsdir}/x%{name}.png
%{_iconsdir}/x%{name}.png
%{_liconsdir}/x%{name}.png
%{_mandir}/man1/xgnokii*

%files smsd
%attr(-,gnokii,gnokii) %config(noreplace) %{_sysconfdir}/sysconfig/gnokii-smsd
%config(noreplace) %{_sysconfdir}/logrotate.d/gnokii-smsd
%{_initrddir}/gnokii-smsd
%{_bindir}/gnokii-smsd
%{_mandir}/man8/gnokii-smsd.8*
%dir %{_libdir}/smsd/
%{_libdir}/smsd/libsmsd_file.so
%{_libdir}/smsd/libsmsd_sqlite.so

%files smsd-pgsql
%{_libdir}/smsd/libsmsd_pq.so

%files smsd-mysql
%{_libdir}/smsd/libsmsd_mysql.so

%files -n %{libname}
%{_libdir}/libgnokii.so.%{major}*

%files -n %{devname}
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
