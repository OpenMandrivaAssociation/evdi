%define major 1
%define libname %mklibname evdi
%define devname %mklibname evdi -d

Name: evdi
Version: 1.14.1
Release: 1
Source0: https://github.com/DisplayLink/evdi/archive/refs/tags/v%{version}.tar.gz
Patch0: pyevdi-detect-python-3.10+.patch
Summary: Extensible Virtual Display Interface
URL: https://github.com/evdi/evdi
License: MIT
Group: System/Libraries
BuildRequires: make
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(python3)
BuildRequires: python%{pyver}dist(pybind11)

%description
The Extensible Virtual Display Interface (EVDI) is a Linux kernel module that
enables management of multiple screens, allowing user-space programs to take
control over what happens with the image. It is essentially a virtual display
you can add, remove and receive screen updates for, in an application that
uses the libevdi library.

It is needed primarily for DisplayLink driver.

%package -n %{libname}
Summary: Extensible Virtual Display Interface
Group: System/Libraries

%description -n %{libname}
The Extensible Virtual Display Interface (EVDI) is a Linux kernel module that
enables management of multiple screens, allowing user-space programs to take
control over what happens with the image. It is essentially a virtual display
you can add, remove and receive screen updates for, in an application that
uses the libevdi library.

It is needed primarily for DisplayLink driver.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

The Extensible Virtual Display Interface (EVDI) is a Linux kernel module that
enables management of multiple screens, allowing user-space programs to take
control over what happens with the image. It is essentially a virtual display
you can add, remove and receive screen updates for, in an application that
uses the libevdi library.

It is needed primarily for DisplayLink driver.

%package -n python-%{name}
Summary: Python bindings for the EVDI library
Group: System/Libraries
Requires: %{libname} = %{EVRD}

%description -n python-%{name}
Python bindings for the EVDI library

The Extensible Virtual Display Interface (EVDI) is a Linux kernel module that
enables management of multiple screens, allowing user-space programs to take
control over what happens with the image. It is essentially a virtual display
you can add, remove and receive screen updates for, in an application that
uses the libevdi library.

It is needed primarily for DisplayLink driver.

%prep
%autosetup -p1

%build
CFLAGS="%{optflags} -I../module" %make_build -C library
%if "%{_lib}" != "lib"
sed -i -e 's,/usr/lib/py,%{_libdir}/py,' pyevdi/Makefile
%endif
CXXFLAGS="%{optflags} -I../module -I../library" %make_build -C pyevdi

%install
%make_install -C library LIBDIR=%{_libdir}
%make_install -C pyevdi

mkdir -p %{buildroot}%{_includedir}
cp library/*.h %{buildroot}%{_includedir}/

%files -n %{libname}
# The .so file is intentionally here, it's dlopened
# by DisplayLinkManager and possibly others
%{_libdir}/*.so
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*

%files -n python-%{name}
%{_libdir}/python*/lib-dynload/*
