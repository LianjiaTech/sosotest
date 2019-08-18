# sosotest自动化测试平台介绍

sosotest自动化测试平台的功能：<br>
1、http接口、dubbo接口的测试。（其他类型类型接口测试可通过二次开发支持）<br>
2、支持多环境、多服务配置。<br>
3、支持数据业务分离。<br>
4、支持数据驱动。<br>
5、支持mock。<br>
6、支持CI。<br>
7、支持自定义封装。<br>
8、支持mysql数据库操作、redis操作、mongo操作、kafka等。<br>
9、分布式任务处理，可并发支持多任务。<br>
sosotest是一个简单易用且功能强大的自动化测试平台。<br>
目前sosotest已经为贝壳找房提供了稳定的后端接口自动化服务，服务于贝壳找房的各个重要业务线，
为业务线后端自动化赋能，有效提高了后端接口自动化效率。<br>

## 多服务、多环境、多模式支持
可以灵活的配置被测服务，配置测试环境和请求地址。<br>
普通模式、关键字模式和python模式的多模式支持，适合不同能力的测试人员。<br>
可自定义关键字、自定义python函数和类，实现更好的封装。

## 数据业务分离
全局变量、组合文本功能，实现了平台的数据与业务的分离。

## 数据驱动
python模式支持接口级的数据驱动。<br>
任务优先变量，实现了任务级的数据驱动。

## HTTP/DUBBO测试
支持HTTP接口测试。<br>
支持DUBBO接口测试(telnet invoke方式)。

## 可结合CI工具完成CI
提供了invoke接口和CI示例，能够跟CI工具结合进行持续集成。

## 多功能HTTP MOCK服务
提供了mock服务，支持restful规范的接口，支持使用python自定义流程，动态返回mock响应结果。

## 多种用例导入模式（postman导入、日志导入）
http支持postman导入，日志导入。<br>
dubbo支持日志导入。

## 多种录制方式（Chrome扩展、报文生成、MOCK代理）
http支持多种录制方式。<br>
Chrome扩展，一键点击生成接口和业务流用例。<br>
复制原始请求报文，一键生成接口用例。<br>
设置app的mock代理，直接生成mock数据后，一键转为接口用例。

## 分布式异步执行任务，支持多任务高并发。
任务执行采用了master-slave的分布式方案，能够接入多个slave实现任务执行的高并发。

# 安装部署&使用文档
gitbook: [sosotest_docs](https://github.com/truelovesdu/sosotest_docs) 

# 联系我们
交流反馈QQ群：284333313<br>
作者邮箱：wangjilianglong@163.com<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;liyc_self@163.com 

# 鸣谢
sosotest测试平台是从2017年初开始做的一个项目，期间经历了各种改版，到贝壳找房后，又进行了更多的功能开发和完善，
尤其在贝壳找房期间开发的python模式，让平台功能更加完善，使得平台可以更好的服务于经验丰富的pythoner。
在此向感谢一下在sosotest的成长过程中给予支持的各位领导和一起付出努力和做出贡献的各位同事。<br><br>
首先感谢sosotest起步时给予大力支持的技术总监金梁，是您的支持才有了sosotest的诞生。<br><br>
然后感谢销售易的技术总监杨松给予的大力支持，是您的支持，才有了sosotest的第二次改版，
从一个简陋的平台，到功能逐步完善，是您的强力推进落地，才有了平台在公司落地为研发团队赋能，
并且获得了公司创新大赛的第一名，如果不是因为一些特殊原因，应该还会跟您一起战斗。<br><br>
再然后是在贝壳的leader何立春，为sosotest在贝壳找房的落地和推进提供了很大的帮助，
在贝壳找房期间也大力支持sosotest的开发工作，使得sosotest在贝壳期间再一次产生了质的飞跃，
任务分布式执行让平台能够承担更大的执行压力，
python模式支持让平台能更好的封装，
以及其他一些主要能力例如mock服务等都是在贝壳期间开发完成的，
在贝壳让sosotest真正的完善，成为一个可使用的功能完善的产品。<br><br>
接下来重点要感谢的是一起开发平台的小伙伴李亚超，从sosotest的第一行代码开始，我们共同探讨平台功能设计，探讨实现方案，
哪怕我们已经不在一个公司了，依然一起对sosotest进行开发和维护，多少个周末我们一起合并代码，
都是为了sosotest的每一次成长，感谢李亚超这两年对sosotest的贡献。<br><br>
最后还要感谢一下对平台做出其他贡献的朋友和同事，<br>
感谢李成龙开发的sosotest的jenkins的插件，让jenkins能够更方便的调度sosotest的任务执行。<br>
感谢岳令为sosotest提供的docker file，让sosotest的部署执行更加方便。
（由于一些特殊原因，未能合入本次开源）<br>
感谢王蕾以及房源团队的小伙伴们一起对sosotest_docs进行完善。<br>
感谢使用sosotest的各位同事在使用过程中的不断反馈，平台也是在大家的使用和反馈中不断完善的。

## License

[MIT](http://opensource.org/licenses/MIT)

Copyright(c) 2017 Lianjia, Inc. All Rights Reserved