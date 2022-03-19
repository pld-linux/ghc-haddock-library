#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	haddock-library
Summary:	Library exposing some functionality of Haddock
Name:		ghc-%{pkgname}
Version:	1.9.0
Release:	2
License:	BSD-like
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/haddock-library
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	27cbfc7dbd7f4294cee44c876bbc57f9
URL:		http://hackage.haskell.org/package/haddock-library
BuildRequires:	ghc >= 6.12.3
%if %{with prof}
BuildRequires:	ghc-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Haddock is a documentation-generation tool for Haskell libraries.
These modules expose some functionality of it without pulling in the
GHC dependency. Please note that the API is likely to change so be
sure to specify upper bounds in your projects. For interacting with
Haddock itself, see the haddock package.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Documentation/
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Documentation/Haddock
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Documentation/Haddock/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Documentation/Haddock/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Documentation/Haddock/Parser
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Documentation/Haddock/Parser/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Documentation/Haddock/Parser/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Documentation/Haddock/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Documentation/Haddock/Parser/*.p_hi
%endif
