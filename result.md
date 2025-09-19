#### CPU使用情况
**返回的结果**
```
11:48:49 up 71 days, 14:42,  6 users,  load average: 0.15, 0.57, 0.70
```
**分析的结论**
系统运行71天，负载较低（0.15, 0.57, 0.70），CPU使用情况正常

---
#### 内存使用情况
**返回的结果**
```
               total        used        free      shared  buff/cache   available
Mem:            7426        4224         203           7        2998        2890
Swap:              0           0           0
```
**分析的结论**
内存使用率约57%（4224/7426），可用内存2890MB，内存使用情况正常

---
#### 磁盘使用情况
**返回的结果**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda2        99G   73G   22G  77% /
```
**分析的结论**
磁盘使用率77%（73G/99G），剩余22G，磁盘空间使用较高，建议关注

---
#### 节点状态
**返回的结果**
```
NAME             STATUS   ROLES           AGE    VERSION
vm-0-14-ubuntu   Ready    control-plane   146d   v1.30.12
```
**分析的结论**
节点状态正常，运行146天，Kubernetes版本v1.30.12

---
#### Pod状态
**返回的结果**
```
```
**分析的结论**
未发现异常Pod

---
#### 系统时间
**返回的结果**
```
Fri Sep 19 11:48:50 AM CST 2025
```
**分析的结论**
系统时间正常

---
#### Kafka状态
**返回的结果**
```
```
**分析的结论**
未发现Kafka相关信息

---
#### Zookeeper状态
**返回的结果**
```
```
**分析的结论**
未发现Zookeeper相关信息

---
#### MySQL状态
**返回的结果**
```
default         my-mysql-0                                      1/1     Running   1          67d
```
**分析的结论**
MySQL运行正常，运行67天

---
#### Redis状态
**返回的结果**
```
default         my-redis-master-0                               1/1     Running   2          71d
```
**分析的结论**
Redis运行正常，运行71天，重启过2次

---
#### Glusterd状态
**返回的结果**
```
```
**分析的结论**
未发现Glusterd相关信息

---
#### MongoDB状态
**返回的结果**
```
```
**分析的结论**
未发现MongoDB相关信息

---
#### 最终总结
项目运行状态总体正常，CPU和内存使用率正常，但磁盘使用率较高（77%），建议关注磁盘空间。MySQL和Redis中间件运行正常，节点状态良好。未发现Kafka、Zookeeper、Glusterd和MongoDB相关组件。