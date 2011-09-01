#
# Conditional build:
%bcond_without	gtk		# build without gtk-based frontend (fewer dependencies)
#
Summary:	ettercap - a ncurses-based sniffer/interceptor utility
Summary(pl.UTF-8):	ettercap - oparte o ncurses narzędzie do sniffowania/przechwytywania
Summary(pt_BR.UTF-8):	ettercap e um interceptador/sniffer paseado em ncurses
Name:		ettercap
Version:	0.7.3
Release:	12
Epoch:		1
License:	GPL
Group:		Networking/Utilities
Source0:	http://downloads.sourceforge.net/ettercap/%{name}-NG-%{version}.tar.gz
# Source0-md5:	28fb15cd024162c55249888fe1b97820
Patch1:		%{name}-build.patch
Patch2:		%{name}-as-needed.patch
Patch3:		%{name}-ncurses.patch
Patch4:		%{name}-libmissing.patch
Patch5:		%{name}-shlib_ext.patch
Patch6:		%{name}-flags.patch
URL:		http://ettercap.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_gtk:BuildRequires:	gtk+2-devel}
BuildRequires:	libltdl-devel
BuildRequires:	libnet-devel >= 1.1.2.1
BuildRequires:	libpcap-devel
BuildRequires:	libtool
BuildRequires:	ncurses-ext-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
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
%setup -q -n %{name}-NG-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{!?debug:dis}%{?debug:en}able-debug \
	--%{?with_gtk:en}%{!?with_gtk:dis}able-gtk \
	--enable-plugins \
	--enable-https
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGELOG AUTHORS TODO doc/*
%doc THANKS README.BUGS
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/ettercap
%attr(755,root,root) %{_libdir}/ettercap/*.so
%{_libdir}/ettercap/*.la
%{_datadir}/ettercap
%{_mandir}/man8/*
%{_mandir}/man5/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/etter.conf
