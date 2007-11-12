%define	name	gnokii
%define	version	0.6.21
%define	rel	1
%define	release	%mkrel %{rel}
%define	Summary	Tool suite for Nokia mobile phones

%define	major	3
%define	libname			%mklibname %{name} %major
%define	libnamedev		%mklibname %{name} -d
%define	libnamestaticdev	%mklibname %{name} -d -s

Summary:	%{Summary}
Name:		%{name}
Version: 	%{version}
Release:	%{release}
License:	GPL
Url:		http://www.gnokii.org/
Group:		Communications
Source0:	http://www.gnokii.org/download/gnokii/%{name}-%{version}.tar.bz2
# (gb) directly applies to aclocal.m4, don't bother with aclocal
#Patch0:		gnokii-0.6.7-libtool.patch.bz2
# (fc) 0.6.4-4mdk fix crash with some locales (Mdk bug 13666) (CVS)
#Patch1:		gnokii-0.6.4-fixcrash.patch.bz2
#Patch2:		gnokii-0.6.5-gcc4-fix.patch.bz2
Patch3:		gnokii-0.6.8-fix-locking.patch
Patch4:		gnokii-0.6.19-stack-corruption-fix.patch
Patch5:		gnokii-0.6.20-no-docs-install-rules.patch
Patch6:		gnokii-0.6.21-fix-pkgconfig-install.patch
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Buildrequires:	xpm-devel gtk+2-devel bison bluez-devel
BuildRequires:	autoconf2.5 >= 2.52
BuildRequires:	desktop-file-utils
BuildRequires:	libusb-devel
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

%description	xgnokii
Xgnokii is graphical Linux/Unix tool suite for Nokia's mobile phones. It
allows you to edit your contacts book, send/read SMS's from/in
computer and more other features.

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
%setup -q 
#%patch0 -p1 -b .libtool
#%patch1 -p1 -b .fixcrash
#%patch2 -p1 -b .gcc4
%patch3 -p1 -b .lock
%patch4 -p1 -b .stack-corruption
%patch5 -p1 -b .docs-install
%patch6 -p0 -b .pkgconfig

#needed by patch0
autoconf
mv Docs/man man
rm Docs/Makefile

%build
%configure2_5x	--enable-security \
		--with-pic \
		--enable-libusb
%make -k || make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall}-devel

install -d $RPM_BUILD_ROOT%{_sysconfdir}
sed 's#/usr/local/sbin/#%{_sbindir}/#' <Docs/sample/gnokiirc >$RPM_BUILD_ROOT%{_sysconfdir}/gnokiirc

desktop-file-install	--vendor="" \
			--remove-category="Application" \
			--add-category="X-MandrivaLinux-Office-Communications-Phone" \
			--dir $RPM_BUILD_ROOT%{_datadir}/applications \
			$RPM_BUILD_ROOT%{_datadir}/applications/*

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/x%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/x%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/x%{name}.png

# for now remove sis file
rm -rf $RPM_BUILD_ROOT%{_docdir}/gnokii/*.sis

install -d $RPM_BUILD_ROOT%{_var}/lock/gnokii

cd man
for i in *.1*; do install -m644 $i -D %{buildroot}%{_mandir}/man1/$i; done
for i in *.8*; do install -m644 $i -D %{buildroot}%{_mandir}/man8/$i; done
cd -


%find_lang %{name}

%pre
%_pre_groupadd %{name}

%postun
%_postun_groupdel %{name}

%post xgnokii
%{update_menus}

%postun xgnokii
%{clean_menus}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Docs/* ChangeLog TODO
%doc utils/*.sis
%{_bindir}/%{name}
%{_bindir}/sendsms
%{_sbindir}/%{name}d
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
%{_datadir}/x%{name}
%{_datadir}/applications/xgnokii.desktop
%{_miconsdir}/x%{name}.png
%{_iconsdir}/x%{name}.png
%{_liconsdir}/x%{name}.png
%{_mandir}/man1/xgnokii.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*

%files -n %{libnamestaticdev}
%defattr(-,root,root)
%{_libdir}/*.a
