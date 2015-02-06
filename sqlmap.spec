Name:           sqlmap
Version:        0.9
Release:        5
Summary:        Automatic SQL injection and database takeover tool
Group:          Monitoring
License:        GPL
URL:            http://sqlmap.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sqlmap/sqlmap-%{version}.tar.gz

%description
sqlmap is an open source penetration testing tool that automates the process of
detecting and exploiting SQL injection flaws and taking over of database
servers. It comes with a powerful detection engine, many niche features for the
ultimate penetration tester and a broad range of switches lasting from database
fingerprinting, over data fetching from the database, to accessing the
underlying file system and executing commands on the operating system via
out-of-band connections.

%prep
%setup -q -n sqlmap
find . -name .svn | xargs rm -rf
# Drop shebang from non-executable python files
find . -type f -and -name '*.py' -and ! -executable -exec  sed -i "sa#!/usr/bin/env pythonaa" {} \;
# Dro non-Linux stuff
rm -rf lib/contrib/upx/macosx
rm -rf lib/contrib/upx/windows
rm -rf udf/mysql/windows
rm -rf udf/postgresql/windows
rm -rf extra/udfhack/windows
%ifarch x86_64
rm -rf udf/mysql/linux/32
rm -rf udf/postgresql/linux/32
rm -rf extra/udfhack/linux/32
%else
rm -rf udf/mysql/linux/64
rm -rf udf/postgresql/linux/64
rm -rf extra/udfhack/linux/64
%endif

%install
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 755 sqlmap.py %{buildroot}%{_datadir}/%{name}
cp -pr extra %{buildroot}%{_datadir}/%{name}
cp -pr lib %{buildroot}%{_datadir}/%{name}
cp -pr plugins %{buildroot}%{_datadir}/%{name}
cp -pr shell %{buildroot}%{_datadir}/%{name}
cp -pr txt %{buildroot}%{_datadir}/%{name}
cp -pr udf %{buildroot}%{_datadir}/%{name}
cp -pr xml %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/sqlmap <<EOF
#!/bin/sh
cd %{_datadir}/%{name}
exec ./sqlmap.py \$@
EOF
chmod +x %{buildroot}%{_bindir}/sqlmap

install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 sqlmap.conf %{buildroot}%{_sysconfdir}
pushd %{buildroot}%{_datadir}/%{name}
ln -s ../../..%{_sysconfdir}/sqlmap.conf .
popd

%files
%doc doc/*
%{_datadir}/%{name}
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
