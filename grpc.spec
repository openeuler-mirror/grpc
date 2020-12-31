Name:          grpc
Version:       1.31.0
Release:       2
Summary:       A modern, open source high performance RPC framework that can run in any environment
License:       ASL 2.0
URL:           https://www.grpc.io
Source0:       https://github.com/grpc/grpc/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:       abseil-20200225.tar.gz 
Source2:       benchmark-v1.5.1.tar.gz  
Source4:       googletest-release-1.10.0.tar.gz

Patch0000:     Copy-channel-args-hash-before-appending-ruby-user-ag.patch
Patch0001:     Ran-generate_proto_ruby.sh-to-update-generated-files.patch
Patch0002:     Add-ABSL_RANDOM_HWAES_FLAGS.patch
Patch0003:     Fix-destruction-race-between-subchannel-and-client_c.patch
Patch0004:     Fix-use-after-free-by-removing-stream-from-transport.patch
Patch0005:     repair-gflags-compile-error-with-cmake.patch 
Patch0006:     repair-pkgconfig-path.patch
Patch0007:     add-secure-compile-option-in-Makefile.patch
Patch0008:     fix-re2-build-error.patch
Patch0009:     allow-grpcio-to-be-build-against-system-re2.patch

BuildRequires: gcc-c++ pkgconfig protobuf-devel protobuf-compiler gdb
BuildRequires: openssl-devel c-ares-devel gflags-devel gtest-devel zlib-devel gperftools-devel
BuildRequires: python3-devel python3-setuptools python3-Cython
BuildRequires: cmake >= 3.13.0
BuildRequires: pkgconfig(re2)
Requires:      protobuf-compiler gflags 

Provides:      %{name}-plugins = %{version}-%{release}
Provides:      %{name}-cli = %{version}-%{release}
Obsoletes:     %{name}-plugins < %{version}-%{release}
Obsoletes:     %{name}-cli < %{version}-%{release}

%description
gRPC is a modern open source high performance RPC framework that can run in any environment.
It can efficiently connect services in and across data centers with pluggable support for
load balancing, tracing, health checking and authentication. It is also applicable in last
mile of distributed computing to connect devices, mobile applications and browsers to backend services.

%package       devel
Summary:       gRPC library development files
Requires:      %{name} = %{version}-%{release}
Requires:      pkgconfig(re2)

%description   devel
Development headers and files for gRPC libraries.

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
tar -zxf %{SOURCE1} --strip-components 1 -C %{_builddir}/%{name}-%{version}/third_party/abseil-cpp/
tar -zxf %{SOURCE2} --strip-components 1 -C %{_builddir}/%{name}-%{version}/third_party/benchmark/
tar -zxf %{SOURCE4} --strip-components 1 -C %{_builddir}/%{name}-%{version}/third_party/googletest/

%build
mkdir -p cmake/build
cd cmake/build
cmake ../../ -DgRPC_INSTALL=ON\
             -DgRPC_CARES_PROVIDER=package \
             -DgRPC_PROTOBUF_PROVIDER=package \
             -DgRPC_SSL_PROVIDER=package      \
             -DgRPC_ZLIB_PROVIDER=package     \
             -DgRPC_RE2_PROVIDER=package      \
             -DgRPC_GFLAGS_PROVIDER=package   \
             -DgRPC_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
             -DgRPC_INSTALL_BINDIR=%{buildroot}%{_bindir} \
             -DgRPC_INSTALL_INCLUDEDIR=%{buildroot}%{_includedir} \
             -DgRPC_INSTALL_CMAKEDIR=%{buildroot}%{_prefix}/lib/cmake/%{name} \
             -DgRPC_INSTALL_SHAREDIR=%{buildroot}%{_datadir}/%{name} \
             -DgRPC_INSTALL_PKGCONFIGDIR=%{buildroot}%{_libdir}/pkgconfig \
             -DCMAKE_INSTALL_PREFIX=%{_prefix} \
             -DgRPC_BUILD_TESTS=ON \
             -DBUILD_SHARED_LIBS=ON
make -j24 V=1

# build python module
export GRPC_PYTHON_BUILD_WITH_CYTHON=True
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=True
export GRPC_PYTHON_BUILD_SYSTEM_CARES=True
export GRPC_PYTHON_BUILD_SYSTEM_RE2=True
export CFLAGS="%optflags"
cd ../..
%py3_build

%install
cd cmake/build
make install/local
cp grpc_cli %{buildroot}%{_bindir}
cp libgrpc++_test_config.so*  %{buildroot}%{_libdir}
rm -rf %{buildroot}%{_prefix}/lib

%delete_la_and_a
cd ../..
%py3_install

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE

%{_bindir}/grpc_cli
%{_bindir}/grpc_*_plugin

%{_libdir}/*.so.1*
%{_libdir}/*absl*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%exclude %{_libdir}/*absl*
%{_libdir}/pkgconfig/*
%{_includedir}/grpc
%{_includedir}/grpc++
%{_includedir}/grpcpp

%files -n python3-grpcio
%defattr(-,root,root)
%{python3_sitearch}/grpc
%{python3_sitearch}/grpcio-%{version}-py?.?.egg-info

%changelog
* Wed Dec 09 2020 gaihuiying <gaihuiying1@huawei.com> - 1.31.0-2
- Type:requirement
- ID:NA
- SUG:NA
- DESC:separate re2 from grpc source

* Mon Aug 28 2020 liuxin <liuxin264@huawei.com> - 1.31.0-1
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
