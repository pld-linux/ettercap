Summary:	ettercap is a ncurses-based sniffer/interceptor utility
Name:		ettercap
Version:	0.5.4
Release:	1
Source0:	http://ettercap.sourceforge.net/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-dont_require_root.patch
Patch1:		%{name}-ncurses.patch
Patch2:		%{name}-plugin_dir.patch
URL:		http://ettercap.sourceforge.net/
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narz�dzia
Group(pt_BR):	Rede/Utilit�rios
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ettercap is a multipurpose sniffer/interceptor/logger for switched or
"hubbed" LAN.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
aclocal
autoconf
%configure \
	--disable-debug \
	--enable-ncurses
%{__make}
%{__make} plug-ins

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__make} plug-ins_install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf \
	README README.PLUGINS HISTORY CHANGELOG AUTHORS TODO \
	THANKS KNOWN-BUGS PORTINGS

install -d $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT{%{_datadir},%{_libdir}}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_mandir}/man8/*
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_libdir}/ettercap
