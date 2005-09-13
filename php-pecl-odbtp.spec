%define		_modname	odbtp
%define		_status		stable

Summary:	%{_modname} - ODBTP client functions
Summary(pl):	%{_modname} - funkcjonalno¶æ klienta ODBTP
Name:		php-pecl-%{_modname}
Version:	1.1.2
Release:	1
License:	LGPL
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	28c3076fefccdca9e07548b8291d41b4
Patch0:		%{name}-shared.patch
Patch1:		%{name}-shared64.patch
URL:		http://pecl.php.net/package/odbtp/
BuildRequires:	odbtp-devel
BuildRequires:	php-devel
Requires:	php-common
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
This extension provides a set of ODBTP, Open Database Transport
Protocol, client functions. ODBTP allows any platform to remotely use
the ODBC facilities installed on a Win32 host to connect to a
database. Linux and UNIX clients can use this extension to access
Win32 databases like MS SQL Server, MS Access and Visual FoxPro.

In PECL status of this extension is: %{_status}.

%description -l pl
To rozszerzenie dostarcza zestaw funkcji klienta ODBTP, Otwartego
Protoko³u Transportu Baz Danych (Open Database Transport Protocol).
ODBTP pozwala na zdalny dostêp do ODBC zainstalowanego na komputerze z
systemem Windows. Umo¿liwia to dostêp do baz danych takich jak MS SQL
Server, MS Access czy Visual FoxPro z poziomu systemu Linux/Unix.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
%if "%{_lib}" == "lib64"
%patch1 -p1
%else
%patch0 -p1
%endif

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
