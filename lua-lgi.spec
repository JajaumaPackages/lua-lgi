%if 0%{?fedora} >= 22
%global luaver 5.3
%else
%if 0%{?fedora} > 19
%global luaver 5.2
%else
%global luaver 5.1
%endif
%endif
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

Name:		lua-lgi
Version:	0.9.0
Release:	3%{?dist}
Summary:	Lua bindings to GObject libraries
License:	MIT
URL:		https://github.com/pavouk/lgi
Source0:	https://github.com/pavouk/lgi/archive/%{version}/lgi-%{version}.tar.gz
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.10.8
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	lua >= %{luaver}
BuildRequires:	lua-devel >= %{luaver}
BuildRequires:	lua-markdown
# for the testsuite:
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(cairo-gobject)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	Xvfb xauth

Requires:	lua >= %{luaver}

%global __requires_exclude_from %{_docdir}
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
LGI is gobject-introspection based dynamic Lua binding to GObject
based libraries. It allows using GObject-based libraries directly from
Lua.


%package samples
Summary:    Examples of lua-lgi usage
# gtk-demo is LGPLv2+
License:    LGPLv2+ and MIT
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description samples
%{summary}


%prep
%setup -q -n lgi-%{version}


%build
CFLAGS="%{optflags} -DLUA_COMPAT_APIINTCASTS"
%configure || :
make %{?_smp_mflags}

# generate html documentation
markdown.lua README.md docs/*.md


%install
make install \
  "PREFIX=%{_prefix}" \
  "LUA_LIBDIR=%{lualibdir}" \
  "LUA_SHAREDIR=%{luapkgdir}" \
  "DESTDIR=%{buildroot}"

# install docs
mkdir -p %{buildroot}%{_pkgdocdir}
cp -av README.html docs/*.html \
  %{buildroot}%{_pkgdocdir}
cp -av samples %{buildroot}%{_pkgdocdir}
find %{buildroot}%{_pkgdocdir} -type f \
  -exec chmod -x {} \;


%check
%configure || :
# report failing tests, don't fail the build
xvfb-run -a -w 1 make check || :


%files
%dir %{_pkgdocdir}
%license LICENSE
%{_pkgdocdir}/*.html
%{luapkgdir}/lgi.lua
%{luapkgdir}/lgi
%{lualibdir}/lgi


%files samples
%{_pkgdocdir}/samples


%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.0-1
- Update to 0.9.0.

* Sat Mar 14 2015 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-4
- Mark license with %%license.

* Fri Jan 16 2015 Tom Callaway <spot@fedoraproject.org> - 0.8.0-3
- rebuild for lua 5.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul  4 2014 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-1
- Update to 0.8.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Thomas Moschny <thomas.moschny@gmx.de> - 0.7.2-1
- Update to 0.7.2.
- Use a single package doc dir.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 12 2013 Tom Callaway <spot@fedoraproject.org> - 0.7.1-2
- rebuild for lua 5.2

* Thu Mar 21 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.7.1-1
- Update to 0.7.1.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.6.2-5
- Update license tag.

* Mon Jan  7 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.6.2-4
- Remove unnecessary patch.
- Update license tag: gtk-demo is licensed under LGPLv2+.
- Put fully versioned dependency in subpackage.

* Wed Jan  2 2013 Thomas Moschny <thomas.moschny@gmx.de> - 0.6.2-3
- Move samples to separate package.
- Generate HTML documentation from markdown docs.

* Sun Dec 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.6.2-2
- Add gtk3 as BR, required by the testsuite.

* Sun Dec 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.6.2-1
- New package.
