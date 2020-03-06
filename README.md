# GitLab Community Edition数据迁移

使用`gitlab-ce` API进行私有仓库数据迁移，从`11.1.4`迁至`12.7.5`。因版本不同，无法使用`gitlab-rake`工具进行`backup`/`restore`

API参考：
- https://docs.gitlab.com/ee/api/README.html
- https://gitpython.readthedocs.io/en/stable/reference.html#


代码参考：https://github.com/THRAEX-70/gitlab-migrator
感谢THRAEX-70分享

优化：
- 迁移创建Users、Groups、Group-members、Projects、Repositories进行是否存在判定
- 查询增加了翻页支持（默认单页最大显示100）
- 修改部分代码逻辑
- 新用户默认密码：hellouser

## 环境依赖
`python 3`
`$ pip install -r requirements.txt`

## 配置

`src/config.py`:

- `SOURCE`: 老版本GitLab地址(端口)与访问令牌

- `TARGET`: 新版本GitLab(端口)地址与访问令牌

## 迁移数据列表

- [X] Users
- [X] Groups
- [X] Group members
- [X] Projects
- [X] Repositories
- [ ] Issues
- [ ] Merge requests
- [ ] SSH key
- [ ] Deploy Keys

## 用法

- 迁移
``` sh
$ cp src/config_example.py src/config.py
$ python3 src/main.py
```

- 清除目标库中的数据
``` sh
$ python3 src/clean.py
```
