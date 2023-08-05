#!/bin/bash

install_bsnstacklib=%(install_bsnstacklib)s
install_ivs=%(install_ivs)s
deploy_dhcp_agent=%(deploy_dhcp_agent)s
ivs_version=%(ivs_version)s
is_controller=%(is_controller)s
is_ceph=%(is_ceph)s
is_cinder=%(is_cinder)s
is_mongo=%(is_mongo)s
deploy_horizon_patch=%(deploy_horizon_patch)s
fuel_cluster_id=%(fuel_cluster_id)s
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

    echo 'Restart neutron-server'
    rm -rf /etc/neutron/plugins/ml2/host_certs/*
    service neutron-server restart
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
            dpkg --force-all -i %(dst_dir)s/%(ivs_pkg)s
            if [[ -f %(dst_dir)s/%(ivs_debug_pkg)s ]]; then
                modinfo openvswitch | grep "^version"
                dpkg --force-all -i %(dst_dir)s/%(ivs_debug_pkg)s
            fi
        elif [[ $skip_ivs_version_check == true ]]; then
            dpkg --force-all -i %(dst_dir)s/%(ivs_pkg)s
            if [[ -f %(dst_dir)s/%(ivs_debug_pkg)s ]]; then
                modinfo openvswitch | grep "^version"
                dpkg --force-all -i %(dst_dir)s/%(ivs_debug_pkg)s
            fi
        else
            echo "ivs upgrade fails version validation"
        fi
    fi

    echo 'Restart ivs, neutron-bsn-agent'
    systemctl restart ivs
    service neutron-bsn-agent restart
}

ceph() {
}

cinder() {
}

mongo() {
}


set +e

# Make sure only root can run this script
if [[ "$(id -u)" != "0" ]]; then
   echo -e "Please run as root"
   exit 1
fi

# install bsnstacklib
if [[ $install_bsnstacklib == true ]]; then
    #TODO: install bsnstacklib
fi

if [[ $is_controller == true ]]; then
    controller
elif [[ $is_ceph == true ]]; then
    ceph
elif [[ $is_cinder == true ]]; then
    cinder
elif [[ $is_mongo == true ]]; then
    mongo
else
    compute
fi

set -e

exit 0

