#
# Conditional build:
%bcond_without	geoip	# GeoIP support
%bcond_without	gtk	# gtk-based frontend
%bcond_with	gtk2	# use GTK+ 2.x instead of 3.x
%bcond_with	lua	# experimental Lua support
#
Summary:	ettercap - a ncurses-based sniffer/interceptor utility
Summary(pl.UTF-8):	ettercap - oparte o ncurses narzędzie do sniffowania/przechwytywania
Summary(pt_BR.UTF-8):	ettercap e um interceptador/sniffer paseado em ncurses
Name:		ettercap
Version:	0.8.3
Release:	2
Epoch:		1
License:	GPL v2+ with OpenSSL exception
Group:		Networking/Utilities
#Source0Download: https://github.com/Ettercap/ettercap/releases
Source0:	https://github.com/Ettercap/ettercap/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6b27d329a509e65fef9044c95a2dde35
Patch0:		%{name}-buildtype.patch
Patch1:		%{name}-gtk3.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-no-common.patch
URL:		https://www.ettercap-project.org/
%{?with_geoip:BuildRequires:	GeoIP-devel}
BuildRequires:	bison
BuildRequires:	cmake >= 2.8
BuildRequires:	curl-devel >= 7.26.0
BuildRequires:	flex
%if %{with gtk}
%{?with_gtk2:BuildRequires:	gtk+2-devel >= 2:2.10}
%{!?with_gtk2:BuildRequires:	gtk+3-devel >= 3.12.0}
%endif
BuildRequires:	libbsd-devel
BuildRequires:	libnet-devel >= 1:1.1.5
BuildRequires:	libpcap-devel
%{?with_lua:BuildRequires:	luajit-devel >= 2.0.0}
BuildRequires:	ncurses-ext-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	curl-libs >= 7.26.0
%if %{with gtk}
%{?with_gtk2:Requires:	gtk+2 >= 2:2.10}
%{!?with_gtk2:Requires:	gtk+3 >= 3.12.0}
%endif
Requires:	libnet >= 1:1.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fomit-frame-pointer

%description
ettercap is a network sniffer/interceptor/logger for ethernet LANs
(both switched or not). It supports active and passive dissection of
many protocols (even ciphered ones, like SSH and HTTPS). Data
injection in an established connection and filtering (substitute or
drop a packet) on the fly is also possible, keeping the connection
synchronized. Many sniffing modes were implemented to give you a
powerful and complete sniffing suite. Plugins are supported. It has
the ability to check whether you are in a switched LAN or not, and to
use OS fingerprints (active or passive) to let you know the geometry
of the LAN. The passive scan of the LAN retrieves infos about: hosts
in the lan, open ports, services version, type of the host (gateway,
router or simple host) and extimated distance in hop.

%description -l pl.UTF-8
ettercap jest wieloczynnościowym snifferem/przechwytywaczem/loggerem
dla sieci LAN (opartych na switchach lub hubach). Obsługuje aktywną i
pasywną analizę wielu protokołów (nawet szyfrowanych, jak SSH czy
HTTPS). Możliwe jest także wstrzykiwanie lub filtrowanie danych
(podmiana lub usunięcie pakietu) w locie, przy podtrzymaniu
synchronizacji połączenia. Program ma zaimplementowane wiele trybów
sniffowania, aby dać potężne i kompletne narzędzie. Obsługiwane są
wtyczki. Program ma możliwość sprawdzania, czy pracuje w sieci ze
switchami oraz używania odcisków systemów (aktywnego lub pasywnego) do
poznania geometrii sieci. Pasywne skanowanie sieci uzyskuje informacje
o: hostach w sieci, otwartych portach, wersjach usług, rodzajach
hostów (bramki, routery lub zwykłe komputery) oraz przybliżonych
odległościach (w hopach).

%description -l pt_BR.UTF-8
ettercap é um sniffer/interceptor/logger de rede para redes locais
(com uso de switches ou não). Suporta operações ativas e passivas de
vários protocolos (mesmo os criptografados, como SSH e HTTPS). Também
é possível injeção de dados em uma conexão estabelecida e filtragem
(substituição ou descarte de um pacote) em tempo real mantendo a
conexão sincronizada. Muitos modos de sniffing foram implementadas
para proporcionar a você um completo conjunto de sniffing. Plugins são
suportados. Tem a habilidade de verificar se você está em uma rede
local com switches ou não. Utiliza fingerprints do Sistema Operacional
(ativo ou passivo) para permitir que você conheça a geometria da rede
local. A varredura passiva da rede local obtém informações sobre:
hosts na rede local, portas abertas, versão de serviços, tipo de host
(gateway, router ou um computador) e a distância estimada no hop.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
install -d build
cd build
%cmake .. \
	-DBUNDLED_LIBS=OFF \
	%{!?with_geoip:-DENABLE_GEOIP=OFF} \
	%{!?with_gtk:-DENABLE_GTK=OFF} \
	-DENABLE_IPV6=ON
	%{?with_lua:-DENABLE_LUA=ON} \
	%{?with_gtk2:-DGTK_BUILD_TYPE=GTK2}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libettercap*.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG LICENSE.OPENSSL README README.{BINARIES,BUGS} THANKS TODO doc/*
%attr(755,root,root) %{_bindir}/ettercap
%attr(755,root,root) %{_bindir}/ettercap-pkexec
%attr(755,root,root) %{_bindir}/etterfilter
%attr(755,root,root) %{_bindir}/etterlog
%attr(755,root,root) %{_libdir}/libettercap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libettercap.so.0
%attr(755,root,root) %{_libdir}/libettercap-ui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libettercap-ui.so.0
%dir %{_libdir}/ettercap
%attr(755,root,root) %{_libdir}/ettercap/ec_*.so
%dir %{_sysconfdir}/ettercap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ettercap/etter.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ettercap/etter.dns
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ettercap/etter.mdns
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ettercap/etter.nbns
%{_datadir}/appdata/ettercap.appdata.xml
%{_datadir}/ettercap
%{_datadir}/polkit-1/actions/org.pkexec.ettercap.policy
%{_desktopdir}/ettercap.desktop
%{_pixmapsdir}/ettercap.svg
%{_mandir}/man5/etter.conf.5*
%{_mandir}/man8/ettercap.8*
%{_mandir}/man8/ettercap-pkexec.8*
%{_mandir}/man8/ettercap_curses.8*
%{_mandir}/man8/ettercap_plugins.8*
%{_mandir}/man8/etterfilter.8*
%{_mandir}/man8/etterlog.8*
