#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

BEGIN {
    $startingtime = (times)[0] + (times)[1];
    foreach ($0, $ENV{'PATH_TRANSLATED'}, $ENV{'SCRIPT_FILENAME'}) {
        my $LBPATH = $_;
        next if ($LBPATH eq '');
        $LBPATH =~ s/\\/\//g;
        $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC, $LBPATH);
    }
}

use warnings;
use strict;
use diagnostics;
use LBCGI;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "data/membertitles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setmembertitles.cgi";

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

$in_member_name = $query->cookie("adminname");
$in_password = $query->cookie("adminpass");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;

if ($action eq "process") {
    &getmember("$in_member_name", "no");

    if (($member_code eq "ad") && ($in_password eq $password) && ($password ne "") && ($in_member_name ne "") && (lc($in_member_name) eq lc($membername))) {

        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/membertitles.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        if (-e $filetomake && -w $filetomake) {
            print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 用户等级</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>所有信息已保存</b>
                </td></tr></table></td></tr></table>
                ~;
        }
        else {
            print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>所有的信息没有保存</b><br>有文件或目录为不可写，请设置属性 777 ！
                </td></tr></table></td></tr></table>
                ~;
        }

    }
    else {
        &adminlogin;
    }

}
else {

    &getmember("$in_member_name", "no");

    if (($member_code eq "ad") && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {

        $in_member_name =~ s/\_/ /g;

        print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 用户等级</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>用户等级设置</b>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <b>如果你不需要这么多的级别，那么可以把等于和高于你定义的最高级别的积分数全部改为 999999999 即可以屏蔽掉高级别。比如：你定义最高级别是5，那么你就应该把 5 以上和最高级这些级别的积分数目全部改 999999999 即可。<BR><BR>
                如果修改这里的任何一部分，那么请修改后到论坛初始化中清空 Cache 一次</b>
                </td>
                </tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>初级的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>初级的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle0" value="$mtitle0"></td>
                </tr>

               <tr>
               <td bgcolor=#FFFFFF valign=middle align=left width=40%>
               <font face=宋体 color=#333333><b>初级的图像</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text size=40 name="mgraphic0" value="$mgraphic0"></td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级一的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级一的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark1" value="$mpostmark1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级一的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle1" value="$mtitle1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级一的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic1" value="$mgraphic1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级二的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级二的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark2" value="$mpostmark2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级二的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle2" value="$mtitle2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级二的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic2" value="$mgraphic2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级三的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级三的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark3" value="$mpostmark3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级三的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle3" value="$mtitle3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级三的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic3" value="$mgraphic3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级四的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级四的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark4" value="$mpostmark4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级四的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle4" value="$mtitle4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级四的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic4" value="$mgraphic4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级五的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级五的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark5" value="$mpostmark5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级五的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle5" value="$mtitle5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级五的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic5" value="$mgraphic5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级六的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级六的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark6" value="$mpostmark6"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级六的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle6" value="$mtitle6"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级六的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic6" value="$mgraphic6"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级七的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级七的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark7" value="$mpostmark7"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级七的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle7" value="$mtitle7"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级七的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic7" value="$mgraphic7"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级八的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级八的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark8" value="$mpostmark8"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级八的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle8" value="$mtitle8"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级八的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic8" value="$mgraphic8"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级九的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级九的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark9" value="$mpostmark9"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级九的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle9" value="$mtitle9"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级九的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic9" value="$mgraphic9"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark10" value="$mpostmark10"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle10" value="$mtitle10"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic10" value="$mgraphic10"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十一的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十一的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark11" value="$mpostmark11"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十一的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle11" value="$mtitle11"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十一的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic11" value="$mgraphic11"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十二的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十二的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark12" value="$mpostmark12"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十二的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle12" value="$mtitle12"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十二的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic12" value="$mgraphic12"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十三的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十三的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark13" value="$mpostmark13"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十三的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle13" value="$mtitle13"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十三的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic13" value="$mgraphic13"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十四的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十四的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark14" value="$mpostmark14"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十四的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle14" value="$mtitle14"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十四的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic14" value="$mgraphic14"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十五的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十五的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark15" value="$mpostmark15"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十五的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle15" value="$mtitle15"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十五的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic15" value="$mgraphic15"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十六的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十六的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark16" value="$mpostmark16"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十六的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle16" value="$mtitle16"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十六的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic16" value="$mgraphic16"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十七的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十七的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark17" value="$mpostmark17"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十七的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle17" value="$mtitle17"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十七的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic17" value="$mgraphic17"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十八的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十八的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark18" value="$mpostmark18"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十八的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle18" value="$mtitle18"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十八的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic18" value="$mgraphic18"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>等级十九的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十九的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark19" value="$mpostmark19"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十九的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle19" value="$mtitle19"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>等级十九的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic19" value="$mgraphic19"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>最高等级的详细资料</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>最高等级的最大积分数 (达到就升级)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmarkmax" value="$mpostmarkmax"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>最高等级的名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitlemax" value="$mtitlemax"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>最高等级的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphicmax" value="$mgraphicmax"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=宋体 color=#990000><b>管理员专用的名称和图像 (如果不想要，请全部留空)</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>副版主的等级名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="amotitle" value="$amotitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>副版主的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="amodgraphic" value="$amodgraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>版主的等级名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="motitle" value="$motitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>版主的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="modgraphic" value="$modgraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>分类区版主的等级名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="cmotitle" value="$cmotitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>分类区版主的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="cmodgraphic" value="$cmodgraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>总版主的等级名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="smotitle" value="$smotitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>总版主的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="smodgraphic" value="$smodgraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>坛主的等级名称</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adtitle" value="$adtitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=宋体 color=#333333><b>坛主的图像</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="admingraphic" value="$admingraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit name=submit value="提 交"></td></form></tr></table></td></tr></table>
                ~;

    }
    else {
        &adminlogin;
    }

}

print qq~</td></tr></table></body></html>~;
exit;
