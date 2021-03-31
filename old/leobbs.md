LeoBBS X 雷傲超级论坛说明文档 

雷傲极酷超级论坛 LeoBBS X 说明文档

.

  
**特别声明：**  
　　本论坛为共享软件(shareware)，仅提供给个人网站免费使用，请勿非法修改、转载、散播、或用于其他图利行为，并请勿删除或修改任何版权标示和图标！  
　　一切商业网站和收费网站必须经过注册以后才可以继续使用本论坛，注册后可获得完善的售后服务和升级服务，具体注册相关事项请看：**[商业版注册说明](reg.md)** 或联系 **[http://www.leobbs.org/](http://www.leobbs.org/)** 。  
　　**如果您的页面中添加有 3721 和百度的浏览器控件下载的话，那么请勿使用本论坛，谢谢合作！**  
　　当您的网站使用本论坛后，您论坛内容中所涉及的一切法律责任均与雷傲科技无关。  
  
  
**论坛安装说明：**  
　**1.** 完整上传 cgi-bin 和 non-cgi 目录，不要缺少任何文件。  
　**2.** 如果使用 Windows 类主机，请跳过此步骤。如果是 Unix 类主机，请[**按照属性设置说明**](filemod.md)，正确设置好所有文件和目录的属性。  
　**3.** 运行 install.cgi 文件，按照显示信息中的提示进行安装（记得要建立管理员账号哦）。  
　**4.** 进入管理区进行论坛初始化操作，然后进行基本变量设置和默认风格设置，最后在论坛设置和管理中建立您的论坛。  
　**5.** 安装完成，进入论坛吧。 ^\_^  
  
  
**论坛升级说明：**  

**升级步骤较多，请耐心看，认真做，千万不要遗漏步骤，也不要做错任何步骤，切记！**  
　**1.** 完整上传 non-cgi 下除了 usr 和 usravatars 目录以外所有目录、目录下的子目录和全部文件。  
　**2.** 检查 cgi-bin 下是否有 cache 目录，如果有，请把此目录和目录下的所有目录及文件全部删除。  
　**3.** 完整上传 cgi-bin 下除了 data、members、messages、record、search、memfav 目录以外的所有目录和目录下的目录  
　　　及文件（使用ASCII 模式），如果原来有此目录或文件，一律覆盖。  
　**4.** 检查以下五个目录：以 members、messages、record、search、memfav 开头的目录是不是都各只有一个，如果有多个，请  
　　　判断并删除掉多余的（一般做法是保留一个目录内文件数最多的），请务必小心操作，最终应该是这五个目录各有一个保留！  
　**5.** 对 data 目录下的文件，请务必上传覆盖这些文件：template.cgi、styles.cgi、skincache.pl、mpic.cgi、QQWry.Dat、  
　　　leoskin.cgi、emoticons.pl、emot.pl、ebankinfo.cgi，特别注意，删除掉所有 styleXX.cgi 文件（XX是数字）和  
　　　所有的 数字.txt 文件（如：10.txt、61.txt、210.txt 等）。  
　**6.** 删除掉 data 下的 skin 目录，然后完整上传 myskin、skin、template 三个子目录到 data 目录下。  
　**7.** 将最新的 cgi-bin 下的 \*.cgi \*.pl \*.pm 上传覆盖掉原来的文件（使用 ASCII 模式，千万不要上传任何子目录内的文件）。  
　**8.** 如果使用 Windows 类主机，请跳过此步骤。如果是 Unix 类主机，请[**按照属性设置说明**](filemod.md)，正确设置好所有文件和目录的属性。  
　**9.** 运行 install.cgi 进行安装（可以不用建立管理员账号，运行前请删除掉 data 下的 install.lock 文件）。  
　**10.**使用管理员账号进入管理区，设置 默认风格设置 和 基本变量设置中的所有空白变量，保存一次。  
　　　重建所有论坛一次（或者对每个论坛进行修复/重新计算一次）。  
　　　在初始化论坛数据中，对用户数据整理一次。  
　　　随便编辑一个分论坛，直接保存一次。  
　　　随便编辑一个联盟论坛，直接保存一次。  
　　　每个分论坛的公告都任选一个编辑，然后直接保存一次。  
　　　论坛插件设定，保存一次。  
　　　表情转换设置管理，任意编辑一个表情，保存一次。  
　　　初始化表情图片和 EMOT 图片一次。  
　　　在用户管理/排名中，更新用户排名一次。  
　　　由于在第 5 步骤的最后，删除了所有的 styleXX.cgi 文件，所以，你需要重新对每个分论坛进行相应的风格设置。  
　**11.**好了，运行 leobbs.cgi 吧，升级成功。  
  
  
**注意：**如果升级新版本(050706及后续版本)后造成论坛整体出错，任何程序都不能运行的话，请用 ASCII 方式完整上传 addon 目录下的 CGI 目录和 CGI.pm 文件(均传到论坛的程序目录下，和 data 、boarddata 等目录放一起)，传好后，请设置 CGI.pm 属性为 755, CGI 目录属性是 777, CGI 目录下的所有文件属性为 755 (Windows 类主机就不用设置属性了)。  
  
  
  
**特别注意：**  
　**1.** 由于 LeoBBS 程序完整兼容了 LB5000 的数据格式(包括 MX 和 XP)，即使对于需要特别转换的数据，程序也会在使用的过程中  
　　　自动进行转化，**所以无需使用任何转化程序，只需要按照升级说明来做既可**。  
　**2.** 所有其他非 LeoBBS 的论坛，[**请都先用 conv 目录中的相应程序转换成 LeoBBS**](convert.md)，然后按照升级说明来操作即可。  
　**3.** 由于以前 LB5000 的帖子格式不统一，所以会造成某些版本的 LB5000 在转换用 LeoBBS 后，会发生丢失第一次回复的  
　　　内容的问题（仅仅是第一次的回复，以后的回复不会丢失），请做好用户工作，让他们重新回复一次就好了。  
　**4.** 如果需要 分论坛新贴子、显示整个论坛的最新贴、首页登陆口、精华显示、公告显示等程序，请去 addon 目录查看，把需要  
　　　的程序上传即可（每个程序的开头都有详细的使用说明的）。  
　**5.** 如果论坛发送邮件使用的是94cool特快专递，那么请把 addon 下的 Net 目录完整上传到 cgi-bin 下，否则此功能会不正常。  
　**6.** LeoBBS 不兼容所有为 LB5000 制作的 hack 程序，如果需要，请联系 hack 作者更新。  
  
　**7.** 如果需要下载最新版本的论坛程序，请访问 **[http://www.leobbs.org/download/](http://www.leobbs.org/download/)**，或者点击您论坛最下面的版本号。  
　**8.** 如果需要安装协助、升级协助、漏洞通知等商业客户服务，[请联系雷傲科技进行商业版或者个人版的注册](reg.md)！  
  
  
**特别感谢(排名按照第一个字符的 ASCII 大小排序)：**  

LeoBBS X Develop Team 全体成员和雷傲科技全体员工  
Anthony、auron、bbser、Bigjim、cnangel、hztz、iJOE、异灵、maiweb、qxbug、RoyRoy、thegirl  
阿强、花无缺、路杨、麻辣、山鹰(糊)、一窍不通。  
程序中 Gzip 模块源自 [Dmitry Koteroff](mailto:koteroff@cpan.org) ， Exif 模块源自 [Phil Harvey](mailto:phil@owl.phy.queensu.ca) ，部分公共模块源自 [http://www.cpan.org/](http://www.cpan.org/)  
部分程序思路和代码源自 [http://www.leohacks.com/](http://www.leohacks.com/) ，部分 JavaScript 代码源自 [http://www.dynamicdrive.com/](http://www.dynamicdrive.com/)  
  
  
**论坛的其他说明文档联接：**  
[论坛属性设置完整说明](filemod.md)  
[论坛数据转换说明](convert.md)  
[论坛用户库结构和修改方法](userformat.md)  
[论坛功能列表](function.md)  
[LeoBBBS X 论坛皮肤制作说明](skin.md)  
[制作 BitTorrent 下载区的说明](bittorrent.md)  
[论坛安全手册](safe.md)  
[LeoBBBS X 论坛商业版注册说明](reg.md)  
[雷傲论坛插件和雷傲论坛商业插件版说明](plug.md)  
[LeoBBBS X 论坛虚拟主机选购说明](vhost.md)  
  
  
  
**开发团队技术演示及支持论坛：**  
**[雷傲极酷超级论坛](http://bbs.leobbs.org/)**  
**[LeoBBS X Develop Team](http://bbs.leobbs.org/cgi-bin/forums.cgi?forum=2)**  
  
  
  

  
  

* * *

版权所有：[雷傲科技](http://www.leobbs.org) & [雷傲极酷超级论坛](http://bbs.leobbs.org)　　Copyright 2000-2005