## package settings
%define vault_user    vault
%define vault_group   %{vault_user}
%define vault_home    %{_localstatedir}/lib/vault
%define vault_confdir %{_sysconfdir}/vault.d
%define debug_package  %{nil}

Name:           vault
Version:        1.1.0
Release:        1%{?dist}
Summary:        Manage Secrets and Protect Sensitive Data.

Group:          System Environment/Daemons
License:        Mozilla Public License, version 2.0
URL:            http://www.vaultproject.io

Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source2:        %{name}.service
Source3:        %{name}.sysconfig

BuildRequires:  systemd-units

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
Secure, store and tightly control access to tokens, passwords,
certificates, encryption keys for protecting secrets and other
sensitive data using a UI, CLI, or HTTP API.

%package config
Summary:    Configuration files for %{name}
Group:      System Environment/Daemons
Requires:   vault

%description config
Example configuration for %{name}.

%prep
%setup -q -c

%build

%install
## directories
%{__install} -d -m 0750 %{buildroot}%{vault_home}

## sytem files
%{__install} -p -D -m 0640 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0640 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

## configuration
for svc in %{_sourcedir}/vault-config-*; do
	%{__install} -p -D -m 0644 $svc %{buildroot}%{vault_confdir}/$(echo $(basename $svc)|sed s/vault-config-//)
done

## main binary
%{__install} -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%pre
## add required user and group if needed
getent group %{vault_group} >/dev/null || \
	groupadd -r %{vault_group}
getent passwd %{vault_user} >/dev/null || \
	useradd -r -g %{vault_user} -d %{vault_home} \
	-s /sbin/nologin -c %{name} %{vault_user}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%{_unitdir}/%{name}.service
%caps(cap_ipc_lock=+ep) %attr(755,-,-) %{_bindir}/%{name}
%attr(-,%{vault_user},%{vault_group}) %dir %{vault_home}

%files config
%defattr(0644,root,root,0755)
%dir %{vault_confdir}
%config(noreplace) %{vault_confdir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
