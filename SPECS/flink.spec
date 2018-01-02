%define __jar_repack %{nil}

Name:           flink
Version:        1.4.0
Release:        1%{?dist}
Summary:        Flink

Group:          Applications/Apache
License:        Apache License 2.0
URL:            https://flink.apache.org
Source0:        flink_taskmanager.sh
Source1:        flink_jobmanager.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel

%description
Apache Flink

%prep
rm -rf ./*
wget http://www-eu.apache.org/dist/flink/flink-1.4.0/flink-1.4.0-bin-scala_2.11.tgz
gzip -dc flink-1.4.0-bin-scala_2.11.tgz | tar -xvvf -

cp $RPM_SOURCE_DIR/* ./

%install
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/flink
mkdir -p $RPM_BUILD_ROOT/etc/flink
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/var/log/flink

cp -R $RPM_BUILD_DIR/flink-%{version}/* $RPM_BUILD_ROOT/usr/share/flink
cp -R $RPM_BUILD_DIR/flink-%{version}/conf/* $RPM_BUILD_ROOT/etc/flink
rm -rf $RPM_BUILD_ROOT/usr/share/flink/conf
rm -rf $RPM_BUILD_ROOT/usr/share/flink/log

cp $RPM_SOURCE_DIR/flink_taskmanager.sh $RPM_BUILD_ROOT/etc/init.d/flink_taskmanager
cp $RPM_SOURCE_DIR/flink_jobmanager.sh $RPM_BUILD_ROOT/etc/init.d/flink_jobmanager

%clean
%{__rm} -rf %{buildroot}

%pre
/usr/bin/getent group flink > /dev/null || /usr/sbin/groupadd -r flink
/usr/bin/getent passwd flink > /dev/null || /usr/sbin/useradd -r -d /usr/share/flink -s /sbin/nologin -g flink flink

%post
ln -s -f /etc/flink /usr/share/flink/conf
ln -s -f /var/log/flink /usr/share/flink/log

%postun
case "$1" in
   0) # yum remove.
      /usr/sbin/userdel myservice
      %{__rm} -f /usr/share/flink/conf
      %{__rm} -f /usr/share/flink/log
   ;;
   1) # yum upgrade.
      # do nothing
   ;;
 esac

%files
%defattr(-,flink,flink)
/usr/share/flink/*
/var/log/flink
%config(noreplace)   /etc/flink/*
%attr(755,root,root) /etc/init.d/*

