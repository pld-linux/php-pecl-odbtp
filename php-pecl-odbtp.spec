%define		php_name	php%{?php_suffix}
%define		modname	odbtp
%define		status		stable
Summary:	%{modname} - ODBTP client functions
Summary(pl.UTF-8):	%{modname} - funkcjonalność klienta ODBTP
Name:		%{php_name}-pecl-%{modname}
Version:	1.1.4
Release:	4
License:	LGPL
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	0ae71132e80c1bacb8ecc8d8221358f1
Patch0:		php-pecl-%{modname}-shared.patch
Patch1:		php-pecl-%{modname}-shared64.patch
Patch2:		php-pecl-%{modname}-confpath.patch
URL:		http://pecl.php.net/package/odbtp/
BuildRequires:	odbtp-devel = %{version}
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Provides:	php(odbtp)
Obsoletes:	php-odbtp
Obsoletes:	php-pear-odbtp
Conflicts:	php-mssql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides a set of ODBTP, Open Database Transport
Protocol, client functions. ODBTP allows any platform to remotely use
the ODBC facilities installed on a Win32 host to connect to a
database. Linux and UNIX clients can use this extension to access
Win32 databases like MS SQL Server, MS Access and Visual FoxPro.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
To rozszerzenie dostarcza zestaw funkcji klienta ODBTP, Otwartego
Protokołu Transportu Baz Danych (Open Database Transport Protocol).
ODBTP pozwala na zdalny dostęp do ODBC zainstalowanego na komputerze z
systemem Windows. Umożliwia to dostęp do baz danych takich jak MS SQL
Server, MS Access czy Visual FoxPro z poziomu systemu Linux/Unix.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%if "%{_lib}" == "lib64"
%patch1 -p1
%else
%patch0 -p1
%endif
%patch2 -p1

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
