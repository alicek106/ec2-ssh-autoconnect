# SSH Auto Connector for EC2 Instance

EC2 인스턴스의 IP를 자동으로 가져와서 SSH로 연결하는 간단한 스크립트입니다.

AWS Management Console에 들어가서 매번 인스턴스 IP 확인하고 SSH 붙는게 너무 귀찮아서 만들었습니다.

<p align="center"><img src="https://github.com/alicek106/ec2-ssh-autoconnect/blob/master/pic.gif" width="70%"></p>

이 스크립트는 아래의 기능들을 제공합니다.

- 단일 인스턴스의 시작과 동시에 SSH 접속하기
- 단일 인스턴스를 정지하기
- 여러 개의 인스턴스를 그룹으로 정의한 뒤, 그룹 인스턴스를 시작하기
- 그룹 인스턴스를 단체로 정지하기
- 인스턴스 상태, IP 출력

## Requirement

- python, pip 3+
- virtualenv (optional)

## Install

이 리포지터리를 내려받습니다.

```
$ git clone https://github.com/alicek106/ec2-ssh-autoconnect.git && \
    cd ec2-ssh-autoconnect && \
    virtualenv ec2-ssh-autoconnect && \
    source ec2-ssh-autoconnect/bin/activate && \
    pip install -r requirements.txt
```

config.ini 파일에서 EC2 인스턴스에 접근할 SSH 비밀 키의 경로를 설정합니다.

```
$ cat config.ini

[CONFIG]
EC2_SSH_PRIVATE_KEY = /Users/alice/Desktop/dev/keys/DockerEngineTestInstance.pem
```

또는, 그룹 인스턴스를 정의하려면 아래와 같이 설정할 수 있습니다. 아래의 예시는 그룹 이름을 kube로 입력했지만, 그룹 이름은 어떤 것이 되어도 상관이 없습니다.

```
[kube]
instance_list =
    controller-etcd-0
    worker-0
    worker-1
    worker-2
```

EC2 Credential 정보를 환경 변수로 설정합니다.

```
$ export AWS_ACCESS_KEY_ID=...
$ export AWS_SECRET_ACCESS_KEY=...
```

## How to use

EC2 인스턴스에 접속합니다. 커맨드에는 **connect, stop, group start, group stop**을 사용할 수 있습니다.

```
$ python __main__.py [커맨드] [인스턴스 이름]
```

- **connect** : 인스턴스가 정지중이라면 시작한 뒤 SSH로 연결합니다.
- **stop** : 인스턴스를 정지합니다.
- **group start, group stop** : 그룹 인스턴스를 시작하거나 정지할 수 있습니다.

사용 예시입니다. Test라는 이름의 인스턴스에 연결한 뒤 정지시킵니다.

```
$ python __main__.py connect Test

...
2019-04-13 16:05:10 INFO     Found credentials in environment variables.
2019-04-13 16:05:11 INFO     Starting EC2 instance : Test
2019-04-13 16:05:11 INFO     EC2 instance is in active.

Last login: Sat Apr 13 06:55:32 2019 from <DETACTED>
ubuntu@testbed:~$
```

```
$ python __main__.py stop Test

2019-04-13 16:07:42 INFO     Found credentials in environment variables.
2019-04-13 16:07:43 INFO     Stopping EC2 instance : Test
```

또는, config.ini에 직접 정의한 그룹을 시작하거나 정지할 수도 있습니다.

```
$ python __main__.py group start kube
2019-04-21 14:17:00 INFO     Found credentials in environment variables.
2019-04-21 14:17:01 INFO     Starting EC2 instance controller-etcd-0...
2019-04-21 14:17:01 INFO     Starting EC2 instance worker-0...
2019-04-21 14:17:01 INFO     Starting EC2 instance worker-1...
2019-04-21 14:17:02 INFO     Starting EC2 instance worker-2...
...
2019-04-21 14:17:49 INFO     EC2 instance is in active.
2019-04-21 14:17:50 INFO     EC2 instance is in active.
2019-04-21 14:17:50 INFO     All instances are ready. You can access the instances using below command
 -> ec2-connect connect [instance name]
```

모든 인스턴스의 상태와 IP를 출력할 수 있습니다. 이 때, 인스턴스는 고유한 Name 태그가 부여되어 있어야 합니다.
```
alicek106:dev alice$ ec2-connect list
2019-04-23 13:25:06 INFO     Found credentials in environment variables.
2019-04-23 13:25:07 INFO     List of EC2 instances :
Instance Name                 IP Address          Status
worker-1                      13.124.50.6         running
controller-etcd-0             13.125.158.31       running
worker-2                      13.125.226.103      running
worker-0                      52.79.173.246       running
Test                          Unknown             stopped
```

## 좀 더 쉽게 사용하기

~/.bashrc, ~/.bash_profile 등에 alias를 추가해 좀 더 편하게 사용해보세요. 저는 ec2-connect로 등록해 놓고 사용하고 있습니다.

```
$ cat ~/.bashrc

export EC2_SSH_AUTOCONNECT_DIR=/ec2-ssh-autoconnect
alias ec2-connect="$EC2_SSH_AUTOCONNECT_DIR/ec2-ssh-autoconnect/bin/python3 $EC2_SSH_AUTOCONNECT_DIR/__main__.py"
...
```

```
alicek106:~ alice$ ec2-connect connect Test

2019-04-13 16:41:59 INFO     Found credentials in environment variables.
2019-04-13 16:41:59 INFO     Starting EC2 instance : Test
2019-04-13 16:41:59 INFO     EC2 instance is in active.
Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-1079-aws x86_64)
..
Last login: Sat Apr 13 07:40:54 2019 from 222.117.216.29
ubuntu@testbed:~$
```

나중에 pip로 설치할 수 있도록 변경할 예정입니다.
