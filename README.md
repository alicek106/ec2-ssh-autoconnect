# SSH Auto Connector for EC2 Instance

EC2 인스턴스의 IP를 자동으로 가져와서 SSH로 연결하는 간단한 스크립트입니다.

AWS Management Console에 들어가서 매번 인스턴스 IP 확인하고 SSH 붙는게 너무 귀찮아서 만들었습니다.

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

EC2 Credential 정보를 환경 변수로 설정합니다.

```
$ export AWS_ACCESS_KEY_ID=...
$ export AWS_SECRET_ACCESS_KEY=...
```

## How to use

EC2 인스턴스에 접속합니다. 커맨드에는 **connect, stop**을 사용할 수 있습니다.

```
$ python __main__.py [커맨드] [인스턴스 이름]
```

- **connect** : 인스턴스가 정지중이라면 시작한 뒤 SSH로 연결합니다.
- **stop** : 인스턴스를 정지합니다.

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

## 좀 더 쉽게 사용하기

~/.bashrc, ~/.bash_profile 등에 alias를 추가해 좀 더 편하게 사용해보세요.

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
