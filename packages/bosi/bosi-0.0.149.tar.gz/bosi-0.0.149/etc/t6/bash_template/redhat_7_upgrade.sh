#!/bin/bash

install_bsnstacklib=%(install_bsnstacklib)s
install_ivs=%(install_ivs)s
install_all=%(install_all)s
deploy_dhcp_agent=%(deploy_dhcp_agent)s
ivs_version=%(ivs_version)s
is_controller=%(is_controller)s
deploy_horizon_patch=%(deploy_horizon_patch)s
openstack_release=%(openstack_release)s
skip_ivs_version_check=%(skip_ivs_version_check)s


controller() {

    # bsnstacklib installed and property files updated. now perform live db migration
    echo "Performing live DB migration for Neutron.."
    if [[ $openstack_release == 'kilo' || $openstack_release == 'kilo_v2' ]]; then
        neutron-db-manage --service bsn_service_plugin upgrade head
    else
        neutron-db-manage upgrade heads
    fi

    systemctl restart httpd

    echo 'Restart neutron-server'
    rm -rf /etc/neutron/plugins/ml2/host_certs/*
    systemctl restart neutron-server
}

compute() {

    # install ivs
    if [[ $install_ivs == true ]]; then
        # check ivs version compatability
        pass=true
        ivs --version
        if [[ $? == 0 ]]; then
            old_version=$(ivs --version | awk '{print $2}')
            old_version_numbers=(${old_version//./ })
            new_version_numbers=(${ivs_version//./ })
            if [[ "$old_version" != "${old_version%%$ivs_version*}" ]]; then
                pass=true
            elif [[ $old_version > $ivs_version ]]; then
                pass=false
            elif [[ $((${new_version_numbers[0]}-1)) -gt ${old_version_numbers[0]} ]]; then
                pass=false
            fi
        fi

        if [[ $pass == true ]]; then
            rpm -ivh --force %(dst_dir)s/%(ivs_pkg)s
            if [[ -f %(dst_dir)s/%(ivs_debug_pkg)s ]]; then
                rpm -ivh --force %(dst_dir)s/%(ivs_debug_pkg)s
            fi
        elif [[ $skip_ivs_version_check == true ]]; then
            rpm -ivh --force %(dst_dir)s/%(ivs_pkg)s
            if [[ -f %(dst_dir)s/%(ivs_debug_pkg)s ]]; then
                rpm -ivh --force %(dst_dir)s/%(ivs_debug_pkg)s
            fi
        else
            echo "ivs upgrade fails version validation"
        fi
    fi

    # restart ivs, neutron-bsn-agent
    systemctl restart ivs
    systemctl restart neutron-bsn-agent
}


set +e

# Make sure only root can run this script
if [ "$(id -u)" != "0" ]; then
    echo -e "Please run as root"
    exit 1
fi

# install bsnstacklib
if [[ $install_bsnstacklib == true ]]; then
    #TODO install bsnstacklib, horizon-bsn
fi

if [[ $is_controller == true ]]; then
    controller
else
    compute
fi

set -e

exit 0

