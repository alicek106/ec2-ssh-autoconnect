# SSH Auto Connector for EC2 Instance

Simple commands which connects to AWS EC2 Instances! 

You don't need to check your changed EC2 instance IP anymore. Just use **'ec2-connect'**

<p align="center"><img src="https://github.com/alicek106/ec2-ssh-autoconnect/blob/master/pic.gif" width="70%"></p>

# 1. Features

Features that this script provide is..

- Start and stop a EC2 instance
- Start and stop multiple EC2 instances as a group
- **Connect SSH to a EC2 instance automatically**
- List all EC2 instances

# 2. Requirements

- python, pip 3+
- virtualenv (optional)

# 3. Install

Clone this repository and install required packages. You can use virtualenv for it.

```
$ git clone https://github.com/alicek106/ec2-ssh-autoconnect.git && \
    cd ec2-ssh-autoconnect && \
    virtualenv ec2-ssh-autoconnect && \
    source ec2-ssh-autoconnect/bin/activate && \
    pip install -r requirements.txt
```

Create configuration file as **/etc/ec2_connect_config.ini** like below.

```
$ cat /etc/ec2_connect_config.ini
[CONFIG]
EC2_SSH_PRIVATE_KEY = /Users/alice/Desktop/dev/keys/DockerEngineTestInstance.pem

[kubeadm]
instance_list =
    kubeadm-master
    kubeadm-worker1
    kubeadm-worker2
    kubeadm-worker0
```

Configuration file contains..

- Path of EC2 private key when used to connect SSH to EC2 instance. 
- Custom groups of EC2 instances (optional)

After that, set AWS credentials in bash. It can also be set by ~/.aws/credentials 

```
$ export AWS_ACCESS_KEY_ID=...
$ export AWS_SECRET_ACCESS_KEY=...
```

Add ec2-connect command as alias in ~/.bashrc. It will be replaced as a pip install later. Please set proper path as EC2_SSH_AUTOCONNECT_DIR to your directory (git clone path).

```
$ cat ~/.bashrc

export EC2_SSH_AUTOCONNECT_DIR=/ec2-ssh-autoconnect
alias ec2-connect="$EC2_SSH_AUTOCONNECT_DIR/ec2-ssh-autoconnect/bin/python3 $EC2_SSH_AUTOCONNECT_DIR/__main__.py"
...
```



# 4. How to use (Easy!)

1. Check EC2 instance list using **ec2-connect list**

   ```
   $ ec2-connect list
   2019-05-15 12:11:16 INFO     Found credentials in environment variables.
   2019-05-15 12:11:17 INFO     List of EC2 instances :
   Instance ID              Instance Name       IP Address          Status
   i-0994dac6654fd59e1      Test                52.79.236.231       running
   i-04b2ad71fcbdae8c1      kubeadm-worker1     Unknown             stopped
   i-0f24c89be31ea8bc2      kubeadm-master      Unknown             stopped
   i-04c77d71fb7ac7867      kubeadm-worker0     Unknown             stopped
   i-0d27c6c0ed423f903      kubeadm-worker2     Unknown             stopped
   ```

2. Connect to EC2 instance by **ec2-connect connect [EC2 instance name]**. This command uses private key defined in /etc/ec2_connect_config.ini

   ```
   $ ec2-connect connect Test
   2019-05-15 12:11:21 INFO     Found credentials in environment variables.
   2019-05-15 12:11:21 INFO     Starting EC2 instance : Test
   2019-05-15 12:11:21 INFO     EC2 instance is in active.
   2019-05-15 12:11:21 INFO     EC2 instance is in active.
   Warning: Permanently added '52.79.236.231' (ECDSA) to the list of known hosts.
   Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-1079-aws x86_64)
   ...
   New release '18.04.2 LTS' available.
   Run 'do-release-upgrade' to upgrade to it.
   
   
   Last login: Tue May 14 13:46:24 2019 from 222.117.216.29
   ubuntu@testbed:~$ 
   ```

   > **Tip** : If a instance is in STOP, 'connect' command automatically start that instance and connect SSH. So you don't need to command 'start' actually. Just use **connect**!

3. Stop EC2 instance by **ec2-connect stop [EC2 instance name]**

   ```
   $ ec2-connect stop Test
   2019-05-15 12:28:36 INFO     Found credentials in environment variables.
   2019-05-15 12:28:36 INFO     Stopping EC2 instance : Test
   2019-05-15 12:28:36 INFO     Stopping EC2 instance Test (Instance ID : i-0994dac6654fd59e1)...
   ```

4. If you defined **custom group** in /etc/ec2_connect_config.ini, you can use 'group start' or 'group stop'

   ```
   $ ec2-connect group start kubeadm
   2019-05-15 12:39:58 INFO     Found credentials in environment variables.
   2019-05-15 12:39:59 INFO     Starting EC2 instance kubeadm-master (instance ID : ..)
   2019-05-15 12:40:00 INFO     Starting EC2 instance kubeadm-worker1 (instance ID : ..)
   2019-05-15 12:40:00 INFO     Starting EC2 instance kubeadm-worker2 (instance ID : ..)
   2019-05-15 12:40:00 INFO     Starting EC2 instance kubeadm-worker0 (instance ID : ..)
   ```

   ```
   $ ec2-connect group stop kubeadm
   2019-05-15 12:41:11 INFO     Found credentials in environment variables.
   2019-05-15 12:41:12 INFO     Stopping EC2 instance kubeadm-master (Instance ID : ..)
   2019-05-15 12:41:12 INFO     Stopping EC2 instance kubeadm-worker1 (Instance ID : ..)
   2019-05-15 12:41:13 INFO     Stopping EC2 instance kubeadm-worker2 (Instance ID : ..)
   2019-05-15 12:41:13 INFO     Stopping EC2 instance kubeadm-worker0 (Instance ID : ..)
   ```

# 5. Disclaimers

- Is it possible to use multiple private key?

  -> It will be supported later :D

- It seems that this script uses instance name (tag:Name). What happens when there are multiple instances which have same tag:Name?

  -> 'ec2-connect start' and 'ec2-connect stop' commands control **instances, not a instance.** For example, if you have instances A and A (but different instance ID), and try to 'ec2-connect start A', it will start both instance at the same time. But **if you try to 'ec2-connect connect A', it will fail**. I recommand to use 'ec2-connect connect' command when each instance has unique tag:Name. Later, SSH connect by instance ID will be supported.

- Do I have to set AWS credentials variable in bash shell manually? 

  -> Actually, I came up with to use credentials by defining in /etc/ec2_connect_config.ini at first. But I think It is not safe to save credentials in that file :D It is possible to update, but maybe later. 