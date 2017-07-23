%define name node-app
%define version 1.0.0
%define release 1
%define buildroot %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Name: %{name}
Version: %{version}
Release: %{release}
Summary: node-app

Group: Installation Script
License: ISC
Source: %{name}.tar.gz
BuildRoot: %{buildroot}
Requires: nodejs >= 6.0
BuildRequires: nodejs >= 6.0
AutoReqProv: no

%description

%global debug_package %{nil}

%prep
%setup -q -c -n %{name}

%build

#It runs right before installation of rpm
%pre
getent group node-app >/dev/null || groupadd -r node-app
getent passwd node-app >/dev/null || useradd -r -g node-app -G node-app -d / -s /sbin/nologin -c "node-app" node-app

#it install rpm package in the build time
%install
mkdir -p %{buildroot}/usr/lib/node-app
cp -r ./ %{buildroot}/usr/lib/node-app
mkdir -p %{buildroot}/var/log/node-app

#Post installation
%post
cp /usr/lib/node-app/node-app.service /etc/systemd/system/node-app.service
systemctl daemon-reload
systemctl enable node-app
systemctl restart node-app

#runs on uninstallation or upgrade (uninstall previous version)
%postun
if [ $1 == 0 ] ; then
	#uninstall package
	systemctl stop node-app
	systemctl disable node-app
	rm /etc/systemd/system/node-app.service
fi


%clean
rm -rf %{buildroot}

%files
%defattr(644, node-app, node-app, 755)
/usr/lib/node-app
/var/log/node-app
