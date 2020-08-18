Name:          grpc
Version:       1.28.1
Release:       2
Summary:       A modern, open source high performance RPC framework that can run in any environment
License:       ASL 2.0
URL:           https://www.grpc.io
Source0:       https://github.com/grpc/grpc/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:       abseil-cpp-b832dce8489ef7b6231384909fd9b68d5a5ff2b7.tar.gz 

Patch9000:     0001-cxx-Arg-List-Too-Long.patch
Patch9001:     0002-add-secure-compile-option-in-Makefile.patch

BuildRequires: gcc-c++ pkgconfig protobuf-devel protobuf-compiler gdb
BuildRequires: openssl-devel c-ares-devel gflags-devel gtest-devel zlib-devel gperftools-devel
BuildRequires: python3-devel python3-setuptools python3-Cython
Requires:      protobuf-compiler

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

%description   devel
Development headers and files for gRPC libraries.

%package -n python3-grpcio
Summary:       Python3 language bindings for gRPC
Requires:      %{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-grpcio
Python3 bindings for gRPC.

%prep
%autosetup -p1
sed -i 's:^prefix ?= .*:prefix ?= %{_prefix}:' Makefile
sed -i 's:$(prefix)/lib:$(prefix)/%{_lib}:' Makefile
sed -i 's:^GTEST_LIB =.*::' Makefile
tar -zxf %{SOURCE1} --strip-components 1 -C %{_builddir}/%{name}-%{version}/third_party/abseil-cpp/

%build
%make_build shared plugins

# build python module
export GRPC_PYTHON_BUILD_WITH_CYTHON=True
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=True
export GRPC_PYTHON_BUILD_SYSTEM_CARES=True
export CFLAGS="%optflags"
%py3_build

%install
make install prefix="%{buildroot}%{_prefix}"
make install-grpc-cli prefix="%{buildroot}%{_prefix}"
%delete_la_and_a
%py3_install

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE

%{_bindir}/grpc_cli
%{_bindir}/grpc_*_plugin

%{_libdir}/*.so.1*
%{_libdir}/*.so.9*
%{_datadir}/grpc

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
%{python3_sitearch}/grpcio-%{version}-py?.?.egg-info

%changelog
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
