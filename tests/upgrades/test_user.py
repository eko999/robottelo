"""Test for User related Upgrade Scenario's

:Requirement: Upgraded Satellite

:CaseAutomation: NotAutomated

:CaseLevel: Acceptance

:CaseComponent: API

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""
from nailgun import entities
import paramiko
from robottelo.datafactory import gen_string
from robottelo.test import APITestCase
from upgrade_tests import pre_upgrade, post_upgrade
from upgrade_tests.helpers.scenarios import create_dict, get_entity_data


class Test_scenario_positive_create_sshkey_in_existing_users(APITestCase):

    """SSH Key can be created in existing user post upgrade

    :id: e4338daa-272a-42e3-be45-77e1caea607f

    :steps:

        1. From SuperAdmin create user with all the details preupgrade
            satellite version
        2. Upgrade Satellite to next/latest version
        3. Go to the user created in preupgrade satellite version
        4. Attempt to add SSH key in user

    :expectedresults: Satellite admin should be able to add SSH key in
        existing user post upgrade
    """
    @pre_upgrade
    def test_pre_create_sshkey_in_existing_user(self):
        """Create User in preupgrade version

        :steps: From SuperAdmin create user with all the details preupgrade
            satellite version

        :expectedresults: The user should be created successfully
        """
        login_name = gen_string('alpha')
        # Creating User
        user = entities.User(login=login_name).create()
        # Verify if created user exists
        self.assertEqual(user.login, login_name)
        # Adding the User details to dict
        create_dict(
            {self.__class__.__name__: {'user_login': user.login}})

    @post_upgrade
    def test_post_create_sshkey_in_existing_user(self):
        """SSH key can be added to existing user post upgrade

        :steps: Postupgrade, Add SSH key to the existing user

        :expectedresults: SSH Key should be added to the existing user
        """
        ssh_name = gen_string('alpha')
        ssh_key = 'ssh-rsa {}'.format(paramiko.RSAKey.generate(2048).get_base64())
        # Mapping the pre upgrade created user login
        user_dict = get_entity_data(self.__class__.__name__)
        # Check Same user exits
        user = entities.User().search(query={'search': 'login={}'.format(user_dict['user_login'])})
        self.assertEqual(user[0].login, user_dict['user_login'])
        # Create SSHKey for User
        user_sshkey = entities.SSHKey(
            user=user[0].id, name=ssh_name, key=ssh_key).create()
        # Check SSHKey assigned to same User
        self.assertEqual(user_sshkey.user.id, user[0].id)


class Test_scenario_positive_existing_user_passwordless_access_to_host:
    """Existing user can password-less access to provisioned host

    :id: d2d94447-5fc7-49cc-840e-06568d8a5141

    :steps:

        1. In preupgrade satellite, From SuperAdmin create user with all the
            details
        2. Upgrade Satellite to next/latest satellite version
        3. Go to the user created in preupgrade satellite
        4. Add SSH key in that user
        5. Choose provisioning template you would use to provision the host
            in feature and add 'create_users' snippet in template
        6. Provision a host through the existing user
        7. Attempt to access the provisioned host through user

    :expectedresults: Existing User should be able to passwordless access to
        provisioned host
    """

    @pre_upgrade
    def test_pre_existing_user_passwordless_access_to_host(self):
        """Create User in preupgrade version

        :steps: In preupgrade satellite, From SuperAdmin create user with all
            the required details

        :expectedresults: The user should be created successfully
        """

    @post_upgrade
    def test_post_existing_user_passwordless_access_to_host(self):
        """Existing user can passwordless access to provisioned host

        :steps:

            1. Go to the user created in preupgrade satellite
            2. Add SSH key in that user
            3. Choose provisioning template you would use to provision the host
                in feature and add 'create_users' snippet in template
            4. Provision a host through the existing user
            5. Attempt to access the provisioned host through user

        :expectedresults: Existing User should be able to passwordless access
            to provisioned host
        """