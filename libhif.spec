Summary:   Simple package library built on top of hawkey and librepo
Name:      libhif
Version:   0.2.1
Release:   2%{?dist}
License:   LGPLv2+
URL:       https://github.com/hughsie/libhif
Source0:   http://people.freedesktop.org/~hughsient/releases/libhif-%{version}.tar.xz

BuildRequires: glib2-devel >= 2.16.1
BuildRequires: libtool
BuildRequires: docbook-utils
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel
BuildRequires: hawkey-devel >= 0.4.6
BuildRequires: rpm-devel >= 4.11.0
BuildRequires: librepo-devel >= 1.7.11
BuildRequires: libsolv-devel

# Bootstrap build requirements
BuildRequires: automake autoconf libtool

# backport from master branch
Patch0:    support-subscription-manager.patch

%description
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package devel
Summary: GLib Libraries and headers for libhif
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
GLib headers and libraries for libhif.

%prep
%setup -q
%patch0 -p1 -b .subscription-manager

%build
# Support builds of both git snapshots and tarballs
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
%configure \
        --enable-gtk-doc \
        --disable-static \
        --disable-silent-rules
)

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libhif*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.md AUTHORS NEWS COPYING
%{_libdir}/libhif.so.1*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_libdir}/libhif.so
%{_libdir}/pkgconfig/libhif.pc
%dir %{_includedir}/libhif
%{_includedir}/libhif/*.h
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/*.gir

%changelog
* Mon Jul 27 2015 Richard Hughes <rhughes@redhat.com> 0.2.1-2
- Support enrollment engines such as subscription-manager.
- Resolves: #1223417

* Mon Jul 13 2015 Richard Hughes <rhughes@redhat.com> 0.2.1-1
- Rebase to latest upstream version to pick up upstreamed patches.
- Resolves: #1220484

* Thu May 28 2015 Richard Hughes <rhughes@redhat.com> 0.2.0-3
- Initial import
- Resolves: #1220484
