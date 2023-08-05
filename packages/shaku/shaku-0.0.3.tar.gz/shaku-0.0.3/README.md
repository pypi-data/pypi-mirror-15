
# Shaku 模块

---

Shaku 是一个脚本（命令等）定时执行的 WebService 框架，它提供了 RestAPI 来帮助开发人员更容易的将脚本设置成一个定时任务。

该模块为 Shaku-Cli，方便开发人员在命令行执行脚本的定制化调用。

---

## 安装

Shaku-Cli 已经上传到 Pypi，使用 pip 可以很容易的安装该脚本。

```Shell
pip install shaku
```

---

## 文档

Shaku-Cli 是有一个很简单的命令行工具，你可以使用 `shaku --help` 来查看帮助文档。

```Shell
$ shaku --help
Usage: shaku [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version
  --help         Show this message and exit.

Commands:
  cpu             show CPU message
  disk            show disk message
  machine         show machine message
  memory          show memory message
  network         show network message
  spider          show status of one spider
  spider_create   create one spider
  spider_modify   modify the time when starting one spider
  spider_start    start one spider
  spiders         show spider list
  spiders_delete  remove all spiders
```

### 综合信息

每个命令都需要提供 host, port, version, 含义如下

parameter | host | port | version
简介|域名|端口|版本号
默认|无|无|1

此三个参数我均在测试过程中采用了默认值，实际使用过成功中需要填写相对应的信息

以下命令简介不再提及以上参数

### CPU(DISK, MACHINE, MEMORY, NETWORK) 信息

```Shell
$ shaku cpu
{u'message': u'', u'code': 0, u'result': {u'count': 1, u'phy_count': 1, u'percent': u'2.3%', u'times': {u'system': 2527.84, u'iowait': 13145.04, u'idle': 854261.55, u'user': 4806.85, u'nice': 90.91}}}
```

和CPU类似，disk, machine, memory, network 都可以这样来操作以获取相关信息。

### 爬虫信息显示 `spider`

命令 `shaku spider --help` 可以显示爬虫命令的帮助信息。

```Shell
$ shaku spider --help
Usage: shaku spider [OPTIONS]

  show status of one spider

Options:
  -h, --host TEXT        host of shaku service
  -p, --port TEXT        port of shaku service
  -v, --version INTEGER  version of shaku service
  -n, --name TEXT        name of spider  [required]
  --help                 Show this message and exit.
```

需要提供爬虫名称来查看爬虫的相关信息

当没有爬虫时，显示:

```Shell
$ shaku spider -n test_not_found
{"message": "spider not found", "code": 10100, "result": null}
```

有爬虫时显示：

```Shell
$ shaku spider -n test
{"message": "Service not running now.", "code": 0, "result": {"comment": "test", "hour": "*", "days": "*", "month": "*", "command": "supervisorctl start test", "minute": "*"}}
```

或

```Shell
$ shaku spider -n test
{"message": "", "code": 0, "result": {"status": "sleeping", "username": "xingming", "cpu_times": {"children_user": 0.0, "children_system": 0.0, "system": 0.0, "user": 0.01}, "pid": 5681, "is_running": true, "cmdline": ["python", "spider-test.py"], "memory_info": {"lib": 0, "text": 2871296, "dirty": 0, "shared": 2408448, "data": 2531328, "vms": 28983296, "rss": 4739072}, "running_time": "0:00:20", "cpu_percent": 0.0, "create_time": "2016-05-03 02:03:38", "job_msg": {"comment": "test", "hour": "0", "days": "*", "month": "*", "command": "supervisorctl start test", "minute": "5"}}}
```

### 创建爬虫 `spider_create`

命令 `shaku spider_create --help` 查看需要的参数信息

```Shell
$ shaku spider_create --help
Usage: shaku spider_create [OPTIONS]

  create one spider

Options:
  -h, --host TEXT        host of shaku service
  -p, --port TEXT        port of shaku service
  -v, --version INTEGER  version of shaku service
  -n, --name TEXT        name of spider  [required]
  -f, --filename TEXT    script of spider  [required]
  -M, --mins TEXT        mins of running this spider
  -H, --hour TEXT        hour of running this spider
  -d, --days TEXT        days of running this spider
  -m, --month TEXT       month of running this spider
  -c, --command TEXT     command of running this spider  [required]
  --help                 Show this message and exit.
```

需要提供的内容如上，其中 name, filename, command 为必须提供的信息，默认爬虫执行时间为凌晨12点，如果需要修改，可以提供hour等参数

以下是创建爬虫的例子:

```Shell
$ shaku spider_create -n test -f spider-test.py -c 'python spider-test.py' -M '*' -H '*'
{"job": {"comment": "test", "hour": "*", "days": "*", "month": "*", "command": "supervisorctl start test", "minute": "*"}}
```

以上命令，脚本会在每分钟的时候都会执行一次，因为是测试脚本，所以设定执行时间比较近，你可以按照需求设置自己脚本的运行时间。

查看脚本信息命令在上面（爬虫信息显示部分)

### 修改爬虫执行时间 `spider_modify`

使用 `shaku spider_modify --help` 来查看帮助

```Shell
$ shaku spider_modify --help
Usage: shaku spider_modify [OPTIONS]

  modify the time when starting one spider

Options:
  -h, --host TEXT        host of shaku service
  -p, --port TEXT        port of shaku service
  -v, --version INTEGER  version of shaku service
  -n, --name TEXT        name of spider  [required]
  -M, --mins TEXT        mins of running this spider
  -H, --hour TEXT        hour of running this spider
  -d, --days TEXT        days of running this spider
  -m, --month TEXT       month of running this spider
  --help                 Show this message and exit.
```

提供对应的爬虫名称和需要修改的爬虫执行时间，即可修改爬虫的信息

```Shell
$ shaku spider_modify -n test -M 5
{"message": "", "code": 0, "result": {"comment": "test", "hour": "0", "days": "*", "month": "*", "command": "supervisorctl start test", "minute": "5"}}
```

### 启动爬虫 `spider_start`

使用 `shaku spider_start --help` 来查看帮助

```Shell
$ shaku spider_start --help
Usage: shaku spider_start [OPTIONS]

  start one spider

Options:
  -h, --host TEXT        host of shaku service
  -p, --port TEXT        port of shaku service
  -v, --version INTEGER  version of shaku service
  -n, --name TEXT        name of spider  [required]
  --help                 Show this message and exit.
```

指定爬虫名称即可将爬虫启动

```Shell
shaku spider_start -n test
{"message": "", "code": 0, "result": ["test", "RUNNING", "pid", "5681", "uptime", "0:00:03"]}
```

启动后的进程信息，参考以上爬虫信息查看部分

### 查看爬虫列表 `spiders`

使用 `shaku spiders --help` 查看帮助

```Shell
$ shaku spiders --help
Usage: shaku spiders [OPTIONS]

  show spider list

Options:
  -h, --host TEXT        host of shaku service
  -p, --port TEXT        port of shaku service
  -v, --version INTEGER  version of shaku service
  --help                 Show this message and exit.
```

例如：

```Shell
$ shaku spiders
{"message": "", "code": 0, "result": [{"comment": "test2", "hour": "0", "days": "*", "month": "*", "command": "supervisorctl start test2", "minute": "0"}, {"comment": "test5", "hour": "0", "days": "*", "month": "*", "command": "supervisorctl start test5", "minute": "0"}, {"comment": "test", "hour": "0", "days": "*", "month": "*", "command": "supervisorctl start test", "minute": "5"}]}
```

### 删除所有爬虫 `spiders_delete`

使用 `shaku spiders_delete --help` 来查看帮助

```Shell
$ shaku spiders_delete --help
Usage: shaku spiders_delete [OPTIONS]

  remove all spiders

Options:
  -h, --host TEXT        host of shaku service
  -p, --port TEXT        port of shaku service
  -v, --version INTEGER  version of shaku service
  --help                 Show this message and exit.
```

例如

```Shell
$ shaku spiders_delete
{"message": "", "code": 0, "result": null}
$ shaku spiders
{"message": "", "code": 0, "result": []}
```

---

## Contact

If you have any questions, welcome to send an email to <a class="email" href="mailto:xiaoh@about.me">xiaoh@about.me</a>

---

## Blog

Welcom to my blog: http://www.xiaoh.me

---

### END

