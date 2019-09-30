Name:            grpc
Version:         1.17.1
Release:         5
Summary:         A modern, open source high performance RPC framework that can run in any environment
License:         ASL 2.0
URL:             https://www.grpc.io
Source0:         https://github.com/grpc/grpc/archive/v%{version}.tar.gz
BuildRoot:       %{_tmppath}/%{name}-%{version}

BuildRequires:   gcc-c++ pkgconfig protobuf-devel protobuf-compiler
BuildRequires:   openssl-devel c-ares-devel gflags-devel gtest-devel zlib-devel gperftools-devel
BuildRequires:   python3-devel python3-setuptools python3-Cython

#patch0000 and patch0001 come from fedora
Patch0000:       0001-enforce-system-crypto-policies.patch
Patch0001:       0002-patch-from-15532.patch
# patch0002 comes from upstream community
Patch0002:       0003-Do-not-build-the-Ruby-plugin.patch
Patch9000:       0001-cxx-Arg-List-Too-Long.patch
Patch9001:       grpc-add-secure-compile-option-in-Makefile.patch

%description
gRPC is a modern open source high performance RPC framework that can run in any environment.
It can efficiently connect services in and across data centers with pluggable support for
load balancing, tracing, health checking and authentication. It is also applicable in last
mile of distributed computing to connect devices, mobile applications and browsers to backend services.

%package plugins
Summary: Compiler plugins for gRPC protoc
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: protobuf-compiler

%description plugins
With the gRPC plugin, you get generated gRPC client and server code, as well as the regular
protocol buffer code for populating, serializing, and retrievingyour message types.

%package devel
Summary: gRPC library development files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and files for gRPC libraries.

%package cli
Summary: Cli for gRPC
Requires: %{name}%{?_isa} = %{version}-%{release} gflags

%description cli
Provides normal cli for gRPC.

%package -n python3-grpcio
Summary: Python3 language bindings for gRPC
Requires: %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-grpcio
Python3 bindings for gRPC.

%prep
%autosetup -p1

sed -i 's:^prefix ?= .*:prefix ?= %{_prefix}:;s:$(prefix)/lib:$(prefix)/%{_lib}:;s:^GTEST_LIB =.*::' Makefile

%build
%make_build shared plugins

export GRPC_PYTHON_BUILD_WITH_CYTHON=True
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=True
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=True
export GRPC_PYTHON_BUILD_SYSTEM_CARES=True
export CFLAGS="%optflags"
%py3_build

%install
%make_install prefix="%{buildroot}%{_prefix}"
make install-grpc-cli prefix="%{buildroot}%{_prefix}"
%delete_la_and_a
%py3_install

%ldconfig_post
%ldconfig_postun

%files
%doc README.md
%license LICENSE
%{_libdir}/*.so.1*
%{_libdir}/*.so.7*
%{_datadir}/grpc

%files plugins
%{_bindir}/grpc_*_plugin

%files cli
%{_bindir}/grpc_cli

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/grpc
%{_includedir}/grpc++
%{_includedir}/grpcpp

%files -n python3-grpcio
%{python3_sitearch}/grpc
%{python3_sitearch}/grpcio-%{version}-py?.?.egg-info

%changelog
* Wed Sep 25 2019 wangli<wangli221@huawei.com> - 1.17.1-5
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:add secure compile option in Makefile

* Sun Sep 15 2019 liyongqiang<liyongqiang10@huawei.com> - 1.17.1-4
- Package init
