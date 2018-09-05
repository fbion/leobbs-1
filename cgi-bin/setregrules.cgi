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
require "bbs.lib.pl";
$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$thisprog = "setregrules.cgi";

$query = new LBCGI;

$rules        = $query -> param('therules');
$action       = $query -> param("action");
$action       = &cleaninput("$action");

$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
            
        &getmember("$inmembername","no");
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

if ($action eq "process") {
        
        $rules =~ s/\n\n/\n/ig;
        $rules =~ s/\s+/\n/ig;

        $filetomake = "$lbdir" . "data/register.dat";
        open (FILE, ">$filetomake");
        print FILE $rules;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font color=#333333><center><b>所有信息已经保存</b></center><br><br>
                <b>注册条款和声明已经保存.目前的注册条款和声明如下：</b><br><HR><ul>$rules</ul>
                <HR><br><br><br><center><a href="setregrules.cgi">修改注册条款和声明</a></center>);
                }
                else {
                    print qq(
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                    <font color=#333333><b>信息无法保存</b><br>文件或者目录不可写。
                    </td></tr></table></td></tr></table>
                    );
                    }
                }
        
    else {

                $filetoopen = "$lbdir" . "/data/register.dat";
                open (FILE, "$filetoopen") or $rules = "输入注册条款和声明";
                @rules = <FILE> if (!$rules);
                close (FILE);

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 注册条款和声明设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font color=#333333><b>输入注册条款和声明</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <br>
                <b>注意:</b>　可以使用 HTML ，但不能使用 LeoBBS 标签。<br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=70 rows=15 wrap="virtual" name="therules">);
		                foreach (@rules) {
		                   $rules = $_;
		                   #$rules =~ s/\n//isg;
		                   print qq($rules);
		                }
		                print qq(</textarea>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit name=submit value=提交></form></td></tr></table></td></tr></table>
                );
                
        }
                }
                else {
                    &adminlogin;
                    }

print qq~</td></tr></table></body></html>~;
exit;
