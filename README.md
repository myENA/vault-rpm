# RPM Spec for Vault

RPM build for creating [Vault](https://www.vaultproject.io) packages for use in the ENA environment.

# Building

The RPMs may be built with [Docker](#with-docker), [Vagrant](#with-vagrant), or [manual](#manual).

Whatever way you choose you will need to do a few basic things first.

```bash
git clone https://github.com/myENA/vault-rpm  ## check out this code
cd vault-rpm                                  ## uhh... you should know
mkdir -p artifacts                            ## prep the artifacts location
```

## With Docker

```bash
docker build -t ena/vault-rpm .                                ## build the image
docker run -v $PWD/artifacts:/tmp/artifacts -it ena/vault-rpm  ## run the image and build the RPMs
```

## With Vagrant

```bash
vagrant up       ## provision and build the RPMs
```

## Manual

```bash
cat build.sh     ## read the script
```

## Result

Two RPMs will be copied into the `artifacts` folder:
1. `vault-<version>-<release>.el7.centos.x86_64.rpm`         - The binary and systemd service definition (required)
2. `vault-config-<version>-<release>.el7.centos.x86_64.rpm`  - Example agent configuration (recommended)

# Running

1. Install the RPM(s) that you need
2. Review and edit (if needed) `/etc/sysconfig/vault` and associated config under `/etc/vault.d/*` (config package)
3. Start the service and tail the logs: `systemctl start vault.service` and `journalctl -f --no-pager -u vault`
4. Optionally start on reboot with: `systemctl enable vault.service`

## Configuring

Config files are loaded in lexicographical order from the `config` specified in `/etc/sysconfig/vault` (config package).
You may modify and/or add to the provided configuration as needed.

# Further reading

See the [vaultproject.io](https://www.vaultproject.io) website.
