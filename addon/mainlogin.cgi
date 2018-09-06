#!/usr/bin/perl
#############################################################
#  功能: 1.对客人显示登录框, 2.对以登录者显示欢迎信息,
#
#  说明: 将本文件复制到 leobbs.cgi 同目录下,
#        在主页加上代码:
#        <SCRIPT type="text/javascript" language="javascript" src="论坛url地址/mainlogin.cgi"></SCRIPT>
#
#############################################################

#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
#  基于山鹰糊、花无缺制作的 LB5000 XP 2.30 免费版   #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBoard.com/          #
#      论坛地址： http://www.LeoBBS.com/            #
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
$LBCGI::POST_MAX=2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "mainlogin.cgi";
$query = new LBCGI;

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "客人" ) {
    $inmembername = "客人";
}
else {
    &getmember("$inmembername");
    $inmembername = "客人" if ($userregistered eq "no");
}

if ($inmembername eq "客人") {
    $str = qq~<FORM name=login action="$boardurl/loginout.cgi" method=post><INPUT type=hidden value=login name=action><INPUT type=hidden name=forum><BR>用户：<INPUT size=10 name=inmembername><BR>密码：<INPUT type=password size=10 name=inpassword><BR>Cookie <SELECT name=CookieDate><OPTION value="0" selected>不保存</OPTION><OPTION value=+1d>保存一天</OPTION><OPTION value=+30d>保存一月</OPTION><OPTION value=+20y>永久保存</OPTION></SELECT><BR><INPUT type=submit value=进入 name=Submit><INPUT type=reset value=取消 name=Submit></FORM><A target=_blank href="$boardurl/leobbs.cgi">参观</A> <A target=_blank href="$boardurl/register.cgi">注册</A> <A target=_blank href="$boardurl/profile.cgi?action=lostpassword">忘记密码</A><BR>~;
}
else {
    $str = qq~<BR>欢迎您<BR>$inmembername<BR><BR><A target=_blank href="$boardurl/leobbs.cgi">进入</A> <A target=_blank href="$boardurl/loginout.cgi">重登录</A> <A href="$boardurl/loginout.cgi?action=logout">退出</A><BR>~;
}

print header(-charset=>UTF-8);
print "document.write('$str')\n";
exit;
