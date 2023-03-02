Name:           hyperhdr
Version:        19.0.0.0
Release:        1%{?dist}
Summary:        Ambient lighting

License:        MIT
URL:            https://github.com/awawa-dev/HyperHDR
Source0:        %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/mjansson/mdns/1.4.2/mdns.h
Patch0:         fix.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  cmake
BuildRequires:  cmake(Qt6)
BuildRequires:  pkgconfig(libturbojpeg)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  cmake(Qt6SerialPort)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  mbedtls-devel
BuildRequires:  cmake(flatbuffers)
BuildRequires:  flatbuffers-compiler
BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils

%description
Open source ambient lighting implementation for television sets based on the
video and audio streams analysis, using performance improvements especially
for USB grabbers.

%prep
%autosetup -p1 -n HyperHDR-%{version}

mkdir dependencies/bonjour
cp %{SOURCE1} dependencies/bonjour/
sed -i  -e 's|file(DOWNLOAD "https://raw.githubusercontent.com/mjansson/mdns/${MJANSSON_MDNS_VERSION}/mdns.h"||' \
        -e 's|"${CMAKE_SOURCE_DIR}/dependencies/bonjour/mdns.h"||' \
        -e 's|STATUS MJANSSON_MDNS_STATUS_H)||' CMakeLists.txt

%cmake -G Ninja \
    -DCMAKE_CXX_STANDARD=17 \
    -DUSE_SYSTEM_FLATBUFFERS_LIBS:BOOL=ON \
    -DUSE_SYSTEM_MBEDTLS_LIBS:BOOL=ON \
    -DENABLE_MQTT:BOOL=OFF \
    -DBUILD_SHARED_LIBS:BOOL=OFF \
    -DPLATFORM=linux

%build
%cmake_build


%install
%cmake_install
mkdir -p %{buildroot}/usr/share/hyperhdr/lut/
tar -xf resources/lut/lut_lin_tables.tar.xz -C %{buildroot}%{_datadir}/%{name}/lut/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-remote
%{_libdir}/libsmart*.so*
%{_userunitdir}/%{name}.service
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png

%changelog
* Tue Feb 28 2023 Vasiliy Glazov <vascom2@gmail.com> - 19.0.0.0-1
- Initial packaging for Fedora
