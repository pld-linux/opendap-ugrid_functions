#
# Conditional build:
%bcond_with	tests	# make check (requires BES server)
#
Summary:	ugrid functions handler for the OPeNDAP data server
Summary(pl.UTF-8):	Moduł obsługi funkcji ugrid dla serwera danych OPeNDAP
Name:		opendap-ugrid_functions
Version:	1.0.1
Release:	1
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/ugrid_functions-%{version}.tar.gz
# Source0-md5:	8ab724ae7a8629a2414311eb75a013de
Patch0:		%{name}-sh.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.10
%{?with_tests:BuildRequires:	bes >= 3.13.0}
BuildRequires:	bes-devel >= 3.13.0
%{?with_tests:BuildRequires:	cppunit-devel >= 1.12.0}
BuildRequires:	gridfields-devel >= 1.0.3
BuildRequires:	libdap-devel >= 3.13.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	bes >= 3.13.0
Requires:	libdap >= 3.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the ugrid (Unstructured Grid or irregular mesh) subsetting
function handler for Hyrax. This Hyrax server function will subset a
compliant ugrid mesh and return a mesh that is also compliant. The
subset can be specified using latitude, longitude and time.

%description -l pl.UTF-8
Ten pakiet zawiera moduł ugrid (Unstructured Grid - tablicy bez
struktury lub maski nieregularnej) obsługujący funkcję podzbioru dla
serwera Hyrax. Funkcja serwera wyliczy podzbiór zgodny z siatką ugrid
i zwróci także zgodną siatkę. Podzbiór może być określony przy użyciu
szerokości, długości i czasu.

%prep
%setup -q -n ugrid_functions-%{version}
%patch0 -p1

%build
# rebuild autotools for -as-needed to work
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bes/modules/ugrid_functions.conf
%attr(755,root,root) %{_libdir}/bes/libugrid_functions.so
