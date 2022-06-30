%global c_so_version 19
%global cpp_so_version 1.41

Name:          grpc
Version:       1.41.1
Release:       3
Summary:       A modern, open source high performance RPC framework that can run in any environment
License:       ASL 2.0
URL:           https://www.grpc.io
Source0:       https://github.com/grpc/grpc/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0006:     repair-pkgconfig-path.patch
Patch0007:     add-secure-compile-option-in-Makefile.patch
Patch0010:     backport-grpc-1.41.1-python-grpcio-use-system-abseil.patch

BuildRequires: gcc-c++ pkgconfig protobuf-devel protobuf-compiler
BuildRequires: openssl-devel c-ares-devel gtest-devel zlib-devel gperftools-devel
BuildRequires: python3-devel python3-setuptools python3-Cython
BuildRequires: cmake >= 3.13.0
BuildRequires: pkgconfig(re2)
BuildRequires: abseil-cpp-devel
Requires:      protobuf-compiler

%description
gRPC is a modern open source high performance RPC framework that can run in any environment.
It can efficiently connect services in and across data centers with pluggable support for
load balancing, tracing, health checking and authentication. It is also applicable in last
mile of distributed computing to connect devices, mobile applications and browsers to backend services.

%package       devel
Summary:       gRPC library development files
Requires:      %{name} = %{version}-%{release}
Requires:      pkgconfig(re2)
Requires:      abseil-cpp-devel

%description   devel
Development headers and files for gRPC libraries.

%package plugins
Summary:        Protocol buffers compiler plugins for gRPC
# License:        same as base package
Requires:       grpc = %{version}-%{release}
Requires:       protobuf-compiler
 
%description plugins
Plugins to the protocol buffers compiler to generate gRPC sources.

%package -n python3-grpcio
Summary:       Python3 language bindings for gRPC
Requires:      %{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-grpcio
Python3 bindings for gRPC.

%prep
%autosetup -p1 -n %{name}-%{version} 
sed -i 's:^prefix ?= .*:prefix ?= %{_prefix}:' Makefile
sed -i 's:$(prefix)/lib:$(prefix)/%{_lib}:' Makefile
sed -i 's:^GTEST_LIB =.*::' Makefile

%build
mkdir -p cmake/build
cd cmake/build
cmake ../../ -DgRPC_INSTALL=ON\
             -DgRPC_CARES_PROVIDER=package \
             -DgRPC_PROTOBUF_PROVIDER=package \
             -DgRPC_SSL_PROVIDER=package      \
             -DgRPC_ZLIB_PROVIDER=package     \
             -DgRPC_RE2_PROVIDER=package      \
             -DgRPC_ABSL_PROVIDER=package     \
             -DgRPC_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
             -DgRPC_INSTALL_BINDIR=%{buildroot}%{_bindir} \
             -DgRPC_INSTALL_INCLUDEDIR=%{buildroot}%{_includedir} \
             -DgRPC_INSTALL_CMAKEDIR=%{buildroot}%{_prefix}/lib/cmake/%{name} \
             -DgRPC_INSTALL_SHAREDIR=%{buildroot}%{_datadir}/%{name} \
             -DgRPC_INSTALL_PKGCONFIGDIR=%{buildroot}%{_libdir}/pkgconfig \
             -DCMAKE_INSTALL_PREFIX=%{_prefix} \
             -DBUILD_SHARED_LIBS=ON
make -j24 V=1

# build python module
export GRPC_PYTHON_BUILD_WITH_CYTHON=True
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=True
export GRPC_PYTHON_BUILD_SYSTEM_CARES=True
export GRPC_PYTHON_BUILD_SYSTEM_RE2=True
export GRPC_PYTHON_BUILD_SYSTEM_ABSL=True
export CFLAGS="%optflags"
cd ../..
%py3_build

%install
cd cmake/build
make install/local
rm -rf %{buildroot}%{_prefix}/lib

%delete_la_and_a
cd ../..
%py3_install

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE

%{_datadir}/%{name}
%{_libdir}/libaddress_sorting.so.%{c_so_version}*
%{_libdir}/libgpr.so.%{c_so_version}*
%{_libdir}/libgrpc.so.%{c_so_version}*
%{_libdir}/libgrpc_unsecure.so.%{c_so_version}*
%{_libdir}/libupb.so.%{c_so_version}*
%{_libdir}/libgrpc++.so.%{cpp_so_version}*
%{_libdir}/libgrpc++_alts.so.%{cpp_so_version}*
%{_libdir}/libgrpc++_error_details.so.%{cpp_so_version}*
%{_libdir}/libgrpc++_reflection.so.%{cpp_so_version}*
%{_libdir}/libgrpc++_unsecure.so.%{cpp_so_version}*
%{_libdir}/libgrpc_plugin_support.so.%{cpp_so_version}*
%{_libdir}/libgrpcpp_channelz.so.%{cpp_so_version}*

%files plugins
%{_bindir}/grpc_*_plugin

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/grpc
%{_includedir}/grpc++
%{_includedir}/grpcpp

%files -n python3-grpcio
%defattr(-,root,root)
%{python3_sitearch}/grpc
%{python3_sitearch}/grpcio-%{version}-py*

%changelog
* Sat Apr 16 2022 xingwei <xingwei14@h-partners.com> - 1.41.1-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:delete useless so files

* Wed Mar 30 2022 xihaochen <xihaochen@h-partners.com> - 1.41.1-2
- Type:requirement
- ID:NA
- SUG:NA
- DESC:remove gflags

* Tue Mar 29 2022 xihaochen <xihaochen@h-partners.com> - 1.41.1-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update grpc to 1.41.1

* Mon Jul 19 2021 lijingyuan <lijingyuan3@huawei.com> - 1.31.0-6
- Type:requirement
- ID:NA
- SUG:NA
- DESC:cancel gdb in buildrequires

* Tue Jul 06 2021 gaihuiying <gaihuiying1@huawei.com> - 1.31.0-5
- Type:requirement
- ID:NA
- SUG:NA
- DESC:separate abseil-cpp from grpc source

* Wed Jun 23 2021 gaihuiying <gaihuiying1@huawei.com> - 1.31.0-4
- Type:requirement
- ID:NA
- SUG:NA
- DESC:delete benchmark and googletest sources in grpc and rebase to 1.31.0-4

* Wed Dec 09 2020 gaihuiying <gaihuiying1@huawei.com> - 1.31.0-2
- Type:requirement
- ID:NA
- SUG:NA
- DESC:separate re2 from grpc source

* Fri Aug 28 2020 liuxin <liuxin264@huawei.com> - 1.31.0-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update grpc version to 1.31.0

* Tue Aug 18 2020 chenyaqiang <chenyaqiang@huawei.com> - 1.28.1-3
- rebuild for package build and clarify last changelog info

* Mon May 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.28.1-2
- Type:rebuild
- ID:NA
- SUG:NA
- DESC:update to 1.28.2

* Mon May 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.28.1-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update to 1.28.1

* Fri Mar 20 2020 songnannan <songnannan2@huawei.com> - 1.22.0-3
- add gdb in buildrequires 

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.22.0-2
- Delete unused patch

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.22.0-1
- Package init
