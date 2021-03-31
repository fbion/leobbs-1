论坛用户库结构和修改方法 

雷傲极酷超级论坛 LeoBBS X 说明文档

.

  
**论坛用户库结构和修改方法：**　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　[**返回上一页**](leobbs.md)  
  
**1. 用户库存放位置**  
LeoBBS X 的用户文件都是存放在 cgi-bin 目录下的 membersXXXXXX 目录(XXXXXX 是随机安全字符串)内的 0 - 512 之间的一个数字子目录中。  
其中数字子目录名是根据用户名的前两个字符按照算法转换而成的。  
  
**2. 用户库文件目录规则**  
用户的文件存在被分在了５１２个目录中，为了确定某个用户文件应该存放在什么目录下，需要用下面的程序段：  
$namenumber = &getnamenumber($username);  
这样得到的 $namenumber 就是目录名，要注意的是，其中的 $username 是已经经过下面第３点处理过的。  
  
**3. 用户库文件名规则**  
用户输入的用户名必须经过简单处理，主要是为了防止非法字符等问题。比如你  
输入的用户名保存在变量 $username 中的话，那么需要用下面程序来处理：  
$username = &unHTML("$username")  
$username =~ s/ /\\\_/g;  
$username =~ tr/A-Z/a-z/;  
这样处理后的 $username 就是最终的用户文件名。  
  
**4. 用户库文件名**  
文件名为 经过处理的用户名.cgi，存放在相应的用户库目录中。  
  
**5. 用户库文件的内部结构**  
你打开一个用户库文件的时候，里面的内容如下：  
$membername\\t$password\\t$membertitle\\t$member_code\\t$numberofposts\\t$emailaddress\\t$showemail\\t$ipaddress\\t$homepage\\t$oicqnumber\\t  
$icqnumber\\t$location\\t$interests\\t$joineddate\\t$lastpostdate\\t$signature\\t$timedifference\\t$privateforums\\t$useravatar\\t$userflag\\t  
$userxz\\t$usersx\\t$personalavatar\\t$personalwidth\\t$personalheight\\t$rating\\t$lastgone\\t$visitno\\t$useradd04\\t$useradd02\\t$mymoney\\t$postdel\\t  
$sex\\t$education\\t$marry\\t$work\\t$born\\t$chatlevel\\t$chattime\\t$jhmp\\t$jhcount\\t$ebankdata\\t$onlinetime\\t$userquestion\\t$awards\\t  
$jifen\\t$userface\\t$soccerdata\\t$useradd5\\t  
  
用户库文件内的每个字段是由 \\t (就是 tab 表格符)分割的，下面是每个字段的具体解释：

$membername     用户名（未处理过的）
$password       密码（先经过 MD5 加密，然后在最前面添加 lEO 标志字样，长度为固定的３５个字节）
$membertitle    自定义头衔（如果内容是 member 或者空的话表示无头衔）
$member_code     用户类型（坛主：ad，总斑竹：smo，斑竹：mo，副斑竹：amo，认证用户：rz 和 rz1 rz2 ... rz5，普通用户：me，
                禁言用户：banned，屏蔽贴子用户：masked）
$numberofposts  发贴数（格式：主题数|回复数，中间是用"|"符号隔开的）
$emailaddress   电子邮件地址
$showemail      是否允许在贴子中显示邮件地址（显示：yes，不显示：no，显示为 MSN：msn，显示为网易泡泡：popo）
$ipaddress      注册时使用的 IP 地址
$homepage       主页地址
$oicqnumber     QQ 号码
$icqnumber      ICQ 号码
$location       来自
$interests      自我简介
$joineddate     注册日期
$lastpostdate   最后发贴（格式：最后发贴时间%%%最后发布的贴子地址%%%最后发布贴子的标题）
$signature      签名 (原始签名和经过 LBCODE 转换后的签名用 aShDFSiod 隔开)
$timedifference 时区
$privateforums  私密区访问权限
$useravatar     头像（如果没有，则内容为noavatar）
$userflag       国家名称
$userxz         星座
$usersx         生肖
$personalavatar 自定义头像
$personalwidth  头像宽度
$personalheight 头像高度
$rating         威望（最大默认是 5，可设置，最小 -5，如果是 -6，则无法发言）
$lastgone       最后访问时间
$visitno        访问次数
$useradd04      保留，未使用
$useradd02      保留，未使用
$mymoney        附加金钱数
$postdel        贴子被删除数
$sex            性别（m=帅哥、f=美女、no=保密）
$education      教育状况
$marry          婚否
$work           职业
$born           生日（格式：年/月/日，其中年份为4位数字，月份和日为2位数字）
$chatlevel      聊天室级别（目前尚未使用）
$chattime       聊天室停留时间（目前尚未使用）
$jhmp           江湖门派
$jhcount        用户精华帖个数
$ebankdata      银行相关数据
$onlinetime     用户在线时间
$userquestion   取回密码要问的问题和答案（格式：问题|答案，中间是用"|"符号隔开的）
$awards         用户奖章
$jifen          用户积分
$userface       虚拟形象
$soccerdata     体育彩票（预留给彩票插件，官方版未使用）
$useradd5       保留，未使用

如果你需要制作某些特别的扩展功能，可以使用用户库中的保留字段($chatlevel，$chattime也可以使用)！  
  
  
**6. 和用户库有关的系统调用**  
你只需在你程序的开头用下面命令包含部分必须的库文件，  
　　　 require "data/boardinfo.cgi";  
　　　 require "data/styles.cgi";  
　　　 require "data/cityinfo.cgi";  
　　　 require "bbs.lib.pl";  
　　　 require "plugin.lib.pl";  
然后你可以直接使用下面的系统功能（不断增加中）  
  
**a)** &whosonline("$username\\t插件名\\tnone\\t功能名\\t");  
可以更新 $username 的最后登陆时间，登陆次数，并且在在线名单中显示此用户在使用某插件的某功能（插件名和功能名可填写一样）  
比如：  
&whosonline("$username\\t论坛银行\\tnone\\t存款\\t");  
  
**b)** &getmember("$username",参数);  
可以得到 $username 的所有资料，放置在５所示的变量中，如果执行后，$userregistered 的值为 "no"，则表明没有这个用户。  
参数可以是 "no"，这个是可选的，表明不锁定，如果是仅仅读用户，可以加上，如果得到的数据是需要写回用户库的，则千万不要加。  
参数可以是 "check"，这个是可选的，表明仅仅用于检查用户是否存在，不改变５中任何变量，返回 1 表明用户存在，返回 0 表明用户不存在。  
比如：  
&getmember("$username"); # 读取 $username 这个用户的用户数据  
&getmember("$username","no"); # 读取 $username 这个用户的用户数据，不进行数据锁定  
&getmember("$username","check"); # 检查 $username 这个用户是否存在  
  
**c)** &updateuserinfo("$username",发贴变化,回复变化,威望变化,经验变化,魅力变化,金钱变化,被删数变化,精华贴变化,在线时间变化,积分变化);  
可以根据你写的变化量更新 $username 用户的资料信息（注意：参数全部是变化量！如果不变化，相应参数就写 0，但千万不要缺少任何参数）  
比如：  
&updateuserinfo("$username",0,0,0,0,0,1000,0,0,0,0); # 给用户加 1000 元虚拟货币  
  
**d)** &upinfodata( name => "要更改的用户名", emailaddress =>"改变后的值", showemail =>"改变后的值", ………… );  
使用散列方式来更新用户文件库的任何字段。  
注意： name 参数是必须的，其他参数根据需要修改的数据相应增减，程序忽略空白散列值和用户库（上面５中的）不存在的散列变量。  
　　　用户名字段是不能更新的，而密码字段更新后会暂时变成明文。  
比如：  
&upinfodata( name => "$username", homepage =>"http://www.leobbs.org", icqnumber =>"123456789", ………… );  
\# 更新 $username 用户的主页和 ICQ 号码，其他数据不变。  
  
**c) 和 d) 函数都有返回值的，规定如下**：  
\# 返回 -1，没有用户  
\# 返回 0 ，用户数据有问题，写入失败  
\# 返回 1 ，成功  
  

[**返 回**](leobbs.md)

  
  

* * *

版权所有：[雷傲科技](http://www.leobbs.org) & [雷傲极酷超级论坛](http://bbs.leobbs.org)　　Copyright 2000-2005