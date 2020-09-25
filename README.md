# Jwt-cli

## 目录

- [安装](#安装)
- [使用](#使用)
- [作者](#作者)
- [描述](#描述)
- [License](#license)

## 安装

```
pip3 install pyjwt
```

## 使用

```
python3 jwt_cli.py jwt_string [options]

usage: jwt_cli.py [-h] [-D] [-A] [-s [SPOOFJWK [SPOOFJWK ...]]] [-d DICT] jwts

positional arguments:
  jwts                  JWT字符串

optional arguments:
  -h, --help            show this help message and exit
  -D, --decipher        解密JWT中的HEADER和PAYLOAD，无参数传输
  -A, --algnone         禁用加密算法，重新生成JWT字段，无参数传输
  -s [SPOOFJWK [SPOOFJWK ...]], --spoofjwk [SPOOFJWK [SPOOFJWK ...]]
                        修改PAYLOAD字段添加进原来的JWT字段，需要显示的说明修改的key:value，允许多个参数修改
  -d DICT, --dict DICT  指定密钥字典，爆破JWT密钥

User: python3 jwt_cli.py jwt_string -D
```

## 作者

[@Misakikata](https://github.com/Misakikata)

## 描述

在实际测试jwt的时候，目前使用的GitHub上的几个脚本有点不太理想，某些情况下还有谜之错误，所以就有这个脚本，为了更快的解决jwt的一些测试方式。

## License

GPL-2.0 © 2020 Misakikata

