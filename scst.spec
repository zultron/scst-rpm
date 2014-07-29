# use --define "kernel X.Y.Z" to build for different kernel
# use --target i686 on i386
%{!?kernel:%define kernel %(rpm -q kernel-source kernel-devel --qf "%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}\\n" | tail -1)}

Summary: Generic SCSI target mid-level for Linux (SCST)
Name: scst
Version: 1.0.1.1
Release: 3.cern
License: GPL
Buildroot: %{_tmppath}/%{name}-buildroot
Group: Applications/File
Source: %{name}-%{version}.tar.gz
Packager: Andras.Horvath@cern.ch
URL: http://scst.sourceforge.net/

%description
SCST is designed to provide unified, consistent interface between SCSI
target drivers and Linux kernel and simplify target drivers development
as much as possible. Detail description of SCST's features and internals
could be found in "Generic SCSI Target Middle Level for Linux" document
SCST's Internet page http://scst.sourceforge.net.
 
%package -n %{name}-kernel-headers
Summary: Generic SCSI target mid-level for Linux (SCST), header files
Group: Applications/File
%description -n %{name}-kernel-headers
SCST is designed to provide unified, consistent interface between SCSI
target drivers and Linux kernel and simplify target drivers development
as much as possible. Detail description of SCST's features and internals
could be found in "Generic SCSI Target Middle Level for Linux" document
SCST's Internet page http://scst.sourceforge.net.
This RPM contains header files.

%package -n kernel-module-%{name}-%{kernel}
Summary: Generic SCSI target mid-level for Linux (SCST), kernel module
Group: System Environment/Kernel
Requires: kernel-%{_target_cpu} = %{kernel}
BuildRequires: kernel-devel = %{kernel}
Provides: kernel-module
Provides: kernel-module-scst = %{version}-%{release}
ExclusiveArch: i686 x86_64 ia64

%description -n kernel-module-%{name}-%{kernel}
SCST is designed to provide unified, consistent interface between SCSI
target drivers and Linux kernel and simplify target drivers development
as much as possible. Detail description of SCST's features and internals
could be found in "Generic SCSI Target Middle Level for Linux" document
SCST's Internet page http://scst.sourceforge.net.
This RPM contains kernel modules.

These modules were built for kernel %{kernel} on architecture %{arch}


%prep

%setup
perl -p -i -e 's,/sbin/depmod,:,g' src/Makefile
perl -p -i -e 's,^#EXTRA_CFLAGS\s+\+=\s+\-DCONFIG_SCST_STRICT_SERIALIZING,EXTRA_CFLAGS += -DCONFIG_SCST_STRICT_SERIALIZING,g' src/Makefile

%build

make DESTDIR=%{buildroot} INSTALL_DIR_H=%{buildroot}/usr/include/scst INSTALL_MOD_PATH=%{buildroot} KVER=%{kernel}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} INSTALL_DIR_H=%{buildroot}/usr/include/scst INSTALL_MOD_PATH=%{buildroot} KVER=%{kernel}
mkdir -p %{buildroot}/usr/share/doc/%{name}-kernel-headers-%{version}
cp README ChangeLog COPYING AskingQuestions ToDo %{buildroot}/usr/share/doc/%{name}-kernel-headers-%{version}
# no we do want docs in modules (since it will clash with docs in devel ..)
#cp README ChangeLog COPYING AskingQuestions ToDo %{buildroot}/usr/share/doc/%{name}-%{version}-modules
# seems we do not need it really ?
#cd %{buildroot}/usr/include/; for i in scst*.h ; do ln -s /usr/include/scst/$i .; done

rm -f %{buildroot}/usr/include/scst/Module.symvers

%clean
rm -rf %{buildroot}

%files -n %{name}-kernel-headers
%defattr(-,root,root)
/usr/include/scst/scst*.h
%doc /usr/share/doc/%{name}-kernel-headers-%{version}

%files -n kernel-module-%{name}-%{kernel}
%defattr(-,root,root)
/lib/modules/%{kernel}/extra/scst.ko
/lib/modules/%{kernel}/extra/dev_handlers/scst_*.ko
#doc /usr/share/doc/%{name}-%{version}-modules

%post -n kernel-module-%{name}-%{kernel}

/sbin/depmod -aeF /boot/System.map-%{kernel} %{kernel} > /dev/null || :
# if we would need this in initrd we could add:
#/sbin/mkinitrd --allow-missing -f /boot/initrd-%{kernel}.img %{kernel} > /dev/null || :

%postun -n kernel-module-%{name}-%{kernel}

/sbin/depmod -aeF /boot/System.map-%{kernel} %{kernel} > /dev/null || :
# if we would need this in initrd we could add:
#/sbin/mkinitrd --allow-missing -f /boot/initrd-%{kernel}.img %{kernel} > /dev/null || :


%changelog
* Mon Nov 23 2009  Jaroslaw Polok <jaroslaw.polok@cern.ch> 1.0.11-3.cern
- added CONFIG_SCST_STRICT_SERIALIZING option.

* Mon Nov 16 2009  Jaroslaw Polok <jaroslaw.polok@cern.ch> 1.0.11-2.cern
- 2nd attempt at packaging ;-)

* Fri Nov 13 2009  Andras HORVATH <andras.horvath@cern.ch> 1.0.11-1.cern
- first packaging attempt
