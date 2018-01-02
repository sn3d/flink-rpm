%define __jar_repack %{nil}

Name:           wd-flink
Version:        1.4.0
Release:        1%{?dist}
Summary:        Flink

Group:          Java
License:        Apache License 2.0
URL:            https://flink.apache.org
#Source0:        http://www-eu.apache.org/dist/flink/flink-1.4.0/flink-1.4.0-bin-scala_2.11.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Flink

%prep
rm -rf ./*
wget http://www-eu.apache.org/dist/flink/flink-1.4.0/flink-1.4.0-bin-scala_2.11.tgz
gzip -dc flink-1.4.0-bin-scala_2.11.tgz | tar -xvvf -

%install
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/flink
mkdir -p $RPM_BUILD_ROOT/etc/flink
mkdir -p $RPM_BUILD_ROOT/var/log/flink

cp -R $RPM_BUILD_DIR/flink-%{version}/* $RPM_BUILD_ROOT/usr/share/flink
cp -R $RPM_BUILD_DIR/flink-%{version}/conf/* $RPM_BUILD_ROOT/etc/flink
rm -rf $RPM_BUILD_ROOT/usr/share/flink/conf

%clean
%{__rm} -rf %{buildroot}

%post
ln -s -f /etc/flink /usr/share/flink/conf
ln -s -f /var/log/flink /usr/share/flink/log

%postun
%{__rm} -f /usr/share/flink/conf
%{__rm} -f /usr/share/flink/log

%files
%defattr(-,flink,flink)
/usr/share/flink/*
/etc/flink/*
/var/log/flink
