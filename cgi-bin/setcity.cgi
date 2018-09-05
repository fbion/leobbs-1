#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

BEGIN {
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setcity.cgi";

$query = new LBCGI;

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
	$theparam =~ s/\\/\\\\/g;
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam =~ s/'//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \'$theparam\'\;\n";
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");
        
        
if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {

    
    if ($action eq "process") {

        
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/cityinfo.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 变量结构</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=宋体 color=#333333><center><b>以下信息已经成功保存</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 变量设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=宋体 color=#333333><b>所有信息没有保存</b><br>文件或者目录不可写<br>请检测你的 data 目录和 cityinfo.cgi 文件的属性！
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                $moneyname ="雷傲元" if ($moneyname eq "");
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 社区设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>社区货币设置</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>货币名称符号</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="moneyname" value="$moneyname" maxlength=6> 默认：雷傲元<BR>如果修改，请修改后到论坛初始化中清空 Cache 一次</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每推荐一个人增加的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjhb" value="$addtjhb"> 默认：100</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每个精华帖子增加的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addjhhb" value="$addjhhb"> 默认：100</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每推荐一个人增加的积分</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjjf" value="$addtjjf"> 默认：0</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每发一个主题折算的积分</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="ttojf" value="$ttojf"> 默认：2</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每发一个回复折算的积分</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="rtojf" value="$rtojf"> 默认：1</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次被删除贴子减去的积分</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="deltojf" value="$deltojf"> 默认：3</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>新用户注册分配的积分</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinjf" value="$joinjf"> 默认：10</td>
                </tr>  
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次发帖增加的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addmoney" value="$addmoney"> 默认：10</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次回复增加的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="replymoney" value="$replymoney"> 默认：8</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次登录增加的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="loginmoney" value="$loginmoney"> 默认：15</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次被删除贴子减去的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="delmoney" value="$delmoney"> 默认：20</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>新用户注册分配的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinmoney" value="$joinmoney"> 默认：1000</td>
                </tr> 

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>发送短消息时需要缴交的费用</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="msgmm" value="$msgmm" maxlength=4> 如不需要，请留空，此功能对版主和坛主无效</td>
                </tr>  

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>每次发小字报花费的货币</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="xzbcost" value="$xzbcost" maxlength=4> 如不需要，请留空</td>
                </tr>  
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
                ~;
                
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;
