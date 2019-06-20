# SSH Auto Connector for EC2 Instance

AWS EC2 인스턴스에 SSH로 자동으로 연결해주는 간단한 명령어 스크립트입니다.

더 이상 변경된 인스턴스 IP를 확인하러 AWS 관리 콘솔에 들어가지 않아도 됩니다. **'ec2-connect'** 명령어를 사용해보세요!

<p align="center"><img src="https://github.com/alicek106/ec2-ssh-autoconnect/blob/master/pic.gif" width="70%"></p>

# 1. Features

이 스크립트 명령어는 아래와 같은 기능들을 제공합니다.

- **IP 대신 인스턴스 이름 (tag:Name) 을 이용해 SSH로 접속하는 기능**
- EC2 인스턴스의 시작, 정지 기능
- 여러 개의 EC2 인스턴스를 그룹으로 정의해, 동시에 여러 개의 인스턴스 시작 및 정지 기능
- 인스턴스 목록 출력 기능

# 2. Requirements

- python, pip 3+
- virtualenv (선택 사항)

# 3. Install

이 리포지터리를 클론한 다음, 필요한 패키지를 설치합니다. 이 과정에서 virtualenv를 사용할 수 있습니다. (선택 사항)

```
$ git clone https://github.com/alicek106/ec2-ssh-autoconnect.git && \
    cd ec2-ssh-autoconnect && \
    virtualenv ec2-ssh-autoconnect && \
    source ec2-ssh-autoconnect/bin/activate && \
    pip install -r requirements.txt
```

이 스크립트가 사용하는 설정 파일인 **/etc/ec2_connect_config.ini** 을 아래와 같이 생성합니다.

```
$ cat /etc/ec2_connect_config.ini
[CONFIG]
EC2_SSH_PRIVATE_KEY_DEFAULT = /Users/alice/Desktop/dev/keys/DockerEngineTestInstance.pem
mykey = /Users/alice/Desktop/dev/keys/mykey.pem

[kubeadm]
instance_list =
    kubeadm-master
    kubeadm-worker1
    kubeadm-worker2
    kubeadm-worker0
```

설정 파일은 다음의 내용을 포함합니다.

- EC2 인스턴스에 SSH 접속할 때 사용될 비밀 키
- 여러 개의 EC2 인스턴스를 정의하는 사용자 정의 그룹 (선택 사항)



Bash 쉘에서, 아래와 같이 AWS 접근 키를 환경 변수로서 내보냅니다.

```
$ export AWS_ACCESS_KEY_ID=...
$ export AWS_SECRET_ACCESS_KEY=...
```

ec2-connect 명령어를 ~/.bashrc 등과 같은 파일에 alias로 추가합니다. 가능하다면 나중에 pip로 교체해볼까 생각하고 있습니다. 여러분이 git clone한 디렉터리를 EC2_SSH_AUTOCONNECT_DIR 에 적절하게 입력해주시면 됩니다.

```
$ cat ~/.bashrc

export EC2_SSH_AUTOCONNECT_DIR=/ec2-ssh-autoconnect
alias ec2-connect="$EC2_SSH_AUTOCONNECT_DIR/ec2-ssh-autoconnect/bin/python3 $EC2_SSH_AUTOCONNECT_DIR/__main__.py"
...
```

~/.bashrc 파일을 적용시킵니다.

```
$ source ~/.bashrc
```

# 4. How to use (Easy!)

1. **ec2-connect list** 명령어로 EC2 인스턴스 목록을 출력합니다.

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

2. **ec2-connect start** 명령어로 EC2 인스턴스를 시작합니다.

   ```
   $ ec2-connect start Test
   2019-05-15 13:04:10 INFO     Found credentials in environment variables.
   2019-05-15 13:04:10 INFO     Starting EC2 instance : Test
   2019-05-15 13:04:11 INFO     Starting EC2 instance Test (instance ID : i-0994dac6654fd59e1)...
   ```

3. **ec2-connect connect [EC2 instance name]** 명령어를 이용해 자동으로 EC2 인스턴스에 SSH로 연결할 수 있습니다. 이 명령어는 /etc/ec2_connect_config.ini 에 정의된 비밀 키를 사용하므로, 설정 파일에서 반드시 적절한 비밀 키의 경로를 설정해야 합니다.

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

   > **Tip** : 인스턴스가 정지 상태에 있을 때 'connect' 명령어로 SSH 접근을 시도할 경우, 자동으로 인스턴스를 시작한 뒤 SSH 접속이 수행됩니다. 따라서 SSH로 붙어야 할 필요가 있을 때는 'start' 명령어를 사용할 필요가 없습니다.
   
   또는 --key=mykey와 같이 옵션을 정의함으로써 기본 키 외의 다른 키를 사용할 수도 있습니다. 아래의 예시는 설정 파일에 mykey를 정의한 경우이며, --key를 사용하지 않으면 EC2_SSH_PRIVATE_KEY_DEFAULT 항목을 읽어들여 사용합니다.
      ```
   $ ec2-connect connect Test --key=mykey
   ```
4. **ec2-connect stop [EC2 instance name]** 명령어로 EC2 인스턴스를 정지할 수 있습니다.

   ```
   $ ec2-connect stop Test
   2019-05-15 12:28:36 INFO     Found credentials in environment variables.
   2019-05-15 12:28:36 INFO     Stopping EC2 instance : Test
   2019-05-15 12:28:36 INFO     Stopping EC2 instance Test (Instance ID : i-0994dac6654fd59e1)...
   ```

5. 만약 **커스텀 그룹**을 /etc/ec2_connect_config.ini 설정 파일에 정의했다면, 'group start' 나 'group stop' 명령어를 통해 여러 개의 인스턴스를 동시에 시작하고 정지할 수 있습니다.

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

- 비밀 키를 여러 개 사용하는건 안되나요?

  -> 업데이트 되었습니다 :D

- 이 명령어 스크립트는 인스턴스 이름을 사용하는 것 같은데 (tag:Name), 만약 같은 이름을 가지는 여러 개의 인스턴스가 존재하면 어떻게 되죠?

  -> 'ec2-connect start' 와 'ec2-connect stop' 커맨드는 사실 **단일 인스턴스가 아닌, 여러 개의 인스턴스에 대해서 사용될 수 있습니다**. 예를 들어, A라는 이름을 가지는 인스턴스가 2개 존재할 때 'ec2-connect start A' 를 실행할 경우, A 이름을 가지는 2개의 인스턴스가 동시에 시작됩니다. 그러나 **'ec2-connect connect A' 와 같이, 같은 이름을 가지는 여러 개의 인스턴스에 SSH 연결을 시도하면.. 당연히 안되도록 막아놨습니다.** 그렇기 때문에 'ec2-connect connect' 명령어는, 각 인스턴스가 고유한 이름 (tag:Name) 을 가지는 경우에만 사용하는 것을 권장합니다. 나중에는 인스턴스 ID로 SSH 연결하는 기능도 추가할 예정입니다.

- AWS 접근 키 (AWS_SECRET_KEY) 변수를 매번 터미널에서 변수로 내보내야 하나요? 너무 귀찮은데.

  -> 사실 개발을 시작할 때는 설정 파일에 함께 접근 키도 정의하려고 했는데, /etc 에 민감한 정보를 저장해 놓는 것이 과연 안전한가? 라는 생각이 들어 쉘 환경 변수로 사용하도록 개발했습니다 :D 아마 나중에 설정 파일에서 읽어오도록 개발할 수도 있겠네요.