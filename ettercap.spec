Summary:	ettercap - a ncurses-based sniffer/interceptor utility
Summary(pl):	ettercap - oparte o ncurses narz�dzie do sniffowania/przechwytywania
Summary(pt_BR):	ettercap e um interceptador/sniffer paseado em ncurses
Name:		ettercap
Version:	0.6.b
Release:	2
Epoch:		1
License:	GPL
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/ettercap/%{name}-%{version}.tar.gz
# Source0-md5:	f665cf82347a91f216184537f8f2c4bd
Patch0:		%{name}-dont_require_root.patch
Patch1:		%{name}-ncurses.patch
Patch2:		%{name}-plugin_dir.patch
Patch3:		%{name}-kernel_version.patch
URL:		http://ettercap.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.7c
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl
ettercap jest wieloczynno�ciowym snifferem/przechwytywaczem/loggerem
dla sieci LAN (opartych na switchach lub hubach). Obs�uguje aktywn� i
pasywn� analiz� wielu protoko��w (nawet szyfrowanych, jak SSH czy
HTTPS). Mo�liwe jest tak�e wstrzykiwanie lub filtrowanie danych
(podmiana lub usuni�cie pakietu) w locie, przy podtrzymaniu
synchronizacji po��czenia. Program ma zaimplementowane wiele tryb�w
sniffowania, aby da� pot�ne i kompletne narz�dzie. Obs�ugiwane s�
wtyczki. Program ma mo�liwo�� sprawdzania, czy pracuje w sieci ze
switchami oraz u�ywania odcisk�w system�w (aktywnego lub pasywnego)
do poznania geometrii sieci. Pasywne skanowanie sieci uzyskuje
informacje o: hostach w sieci, otwartych portach, wersjach us�ug,
rodzajach host�w (bramki, routery lub zwyk�e komputery) oraz
przybli�onych odleg�o�ciach (w hopach).

%description -l pt_BR
ettercap � um sniffer/interceptor/logger de rede para redes locais
(com uso de switches ou n�o). Suporta opera��es ativas e passivas de
v�rios protocolos (mesmo os criptografados, como SSH e HTTPS). Tamb�m
� poss�vel inje��o de dados em uma conex�o estabelecida e filtragem
(substitui��o ou descarte de um pacote) em tempo real mantendo a
conex�o sincronizada. Muitos modos de sniffing foram implementadas
para proporcionar a voc� um completo conjunto de sniffing. Plugins s�o
suportados. Tem a habilidade de verificar se voc� est� em uma rede
local com switches ou n�o. Utiliza fingerprints do Sistema Operacional
(ativo ou passivo) para permitir que voc� conhe�a a geometria da rede
local. A varredura passiva da rede local obt�m informa��es sobre:
hosts na rede local, portas abertas, vers�o de servi�os, tipo de host
(gateway, router ou um computador) e a dist�ncia estimada no hop.

%prep
%setup -q
#%patch0 -p1
%patch1
#%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
##%{__autoconf}
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
%configure \
	--%{!?debug:dis}%{?debug:en}able-debug \
	--enable-ncurses \
	--disable-gtk
%{__make}
%{__make} plug-ins

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} plug-ins_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.PLUGINS HISTORY CHANGELOG AUTHORS TODO
%doc THANKS KNOWN-BUGS PORTINGS
%doc plugins/{H03_hydra1/HYDRA.HOWTO,H01_zaratan/ZARATAN.HOWTO,H09_roper/ROPER.HOWTO}
%attr(755,root,root) %{_sbindir}/*
%{_libdir}/ettercap
%{_datadir}/ettercap
%{_mandir}/man8/*
