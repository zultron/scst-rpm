# use --define "kver X.Y.Z" to build for different kernel
%{!?kernel:%define kver %(rpm -q kernel-devel --qf \\\
    "%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}\\n" | tail -1)}
%global kmod_install_dir /lib/modules/%{kver}.%{_target_cpu}/%{name}


Summary: Generic SCSI target mid-level for Linux (SCST)
Name: scst
Version: 2.2.1
Release: 0%{?dist}
License: GPL
Group: Applications/File
Source: %{name}-%{version}.tar.bz2
URL: http://scst.sourceforge.net/
BuildRequires: kernel-devel = %{kver}


%description
SCST is designed to provide unified, consistent interface between SCSI
target drivers and Linux kernel and simplify target drivers development
as much as possible. Detail description of SCST's features and internals
could be found in "Generic SCSI Target Middle Level for Linux" document
SCST's Internet page http://scst.sourceforge.net.
 

%package devel
Summary: Development files for scst
Group: Development/Libraries


%description devel
Kernel header files for scst


%package -n kmod-%{name}-%{kver}
Summary: Generic SCSI target mid-level for Linux (SCST) kernel modules
Group: System Environment/Kernel
Requires: kernel-%{_target_cpu} = %{kver}
Provides: kmod-scst = %{version}-%{release}


%description -n kmod-%{name}-%{kver}
SCST is designed to provide unified, consistent interface between SCSI
target drivers and Linux kernel and simplify target drivers development
as much as possible. Detail description of SCST's features and internals
could be found in "Generic SCSI Target Middle Level for Linux" document
SCST's Internet page http://scst.sourceforge.net.
This RPM contains kernel modules.

These modules were built for kernel %{kver}


%package -n kmod-%{name}-%{kver}-devel
Summary: Development files for scst kernel modules
Group: System Environment/Kernel
Requires: kernel-devel-%{_target_cpu} = %{kver}
Requires: %{name}-devel
Provides: kmod-scst-devel = %{version}-%{release}
Provides: kmod-scst-%{kver}-devel = %{version}-%{release}


%description -n kmod-%{name}-%{kver}-devel
This package provides the kernel module symbol file for building
against the SCST kernel modules, version %{kver}


%prep
%setup -q


%build
make DESTDIR=%{buildroot} INSTALL_DIR_H=%{buildroot}/usr/include/scst \
    INSTALL_MOD_PATH=%{buildroot} KVER=%{kver}.%{_target_cpu} \
    KDIR=/usr/src/kernels/%{kver}.%{_target_cpu}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} \
    INSTALL_DIR_H=%{buildroot}%{_includedir}/%{name} \
    INSTALL_DIR=%{buildroot}%{kmod_install_dir} \
    KVER=%{kver}.%{_target_cpu} \
    KDIR=/usr/src/kernels/%{kver}.%{_target_cpu}

# Install Module.symvers, needed by iscsi-scst package
mkdir -p %{buildroot}%{_usrsrc}/kernels/%{kver}.%{_target_cpu}/scst
mv %{buildroot}%{_includedir}/%{name}/Module.symvers \
    %{buildroot}%{_usrsrc}/kernels/%{kver}.%{_target_cpu}/scst


%clean
rm -rf %{buildroot}


%files devel
%{_includedir}/%{name}/scst*.h
%doc AskingQuestions COPYING ChangeLog README SysfsRules ToDo


%files -n kmod-%{name}-%{kver}
%dir %{kmod_install_dir}
%{kmod_install_dir}/scst.ko
%{kmod_install_dir}/dev_handlers


%files -n kmod-%{name}-%{kver}-devel
%{_usrsrc}/kernels/%{kver}.%{_target_cpu}/scst


%post -n kmod-%{name}-%{kver}
/sbin/depmod -aeF /boot/System.map-%{kver}.%{_target_cpu} \
	%{kver}.%{_target_cpu} > /dev/null || :


%postun -n kmod-%{name}-%{kver}
/sbin/depmod -aeF /boot/System.map-%{kver}.%{_target_cpu} \
	%{kver}.%{_target_cpu} > /dev/null || :


%changelog
* Mon Jul 28 2014 John Morris <john@zultron.com> - 2.2.1-0
- Update to 2.2.1
- Patch kernel source location for kernel-devel packages
- Fix macros
- Rename kernel-module-* packages to kmod-*
- Rename scst-kernel-headers to scst-devel
- Add kmod-*-devel pkg with Module.symvers
- Remove cruft
- Fix install path to /lib/modules/KVER/scst
- Remove %%ExclusiveArch: tags

* Mon Nov 23 2009  Jaroslaw Polok <jaroslaw.polok@cern.ch> 1.0.11-3.cern
- added CONFIG_SCST_STRICT_SERIALIZING option.

* Mon Nov 16 2009  Jaroslaw Polok <jaroslaw.polok@cern.ch> 1.0.11-2.cern
- 2nd attempt at packaging ;-)

* Fri Nov 13 2009  Andras HORVATH <andras.horvath@cern.ch> 1.0.11-1.cern
- first packaging attempt
