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
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "remmail.cgi";

$query = new LBCGI;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

@params = $query->param;
foreach $param (@params) {
    $theparam = $query->param($param);
    $theparam = &unHTML("$theparam");
    ${$param} = $theparam;
}

$inmembername = $query->cookie("amembernamecookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$member =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$member = "" if (length($member) > 16);

if (lc($inmembername) eq lc($member)) {
    $filetoopen = "$lbdir" . "data/remmem.cgi";
    open(FILE, "$filetoopen");
    flock(FILE, 2);
    @members = <FILE>;
    close(FILE);

    foreach $removed (@members) {
        chomp($removed);
        if ($removed eq $member) {
            $output = qq~
   <tr bgcolor="#FFFFFF">
   <td align="center">
   你好，$member：你已经退出 LeoBBS 邮件列表了。
   </td>
   </tr>
  ~;
            &displayoutput;
        }
    }

    $filetoopen = "$lbdir" . "data/remmem.cgi";
    open(FILE, ">>$filetoopen");
    print FILE "$member\n";
    close(FILE);

    $adminemail_out = &encodeemail($adminemail_out);
    $output = qq~
 <tr bgcolor="#FFFFFF">
 <td align="center">
 你好，$member：你已经退出 LeoBBS 邮件列表了。
 <br>如果你想重新加入，请联系 <a href="mailto:$adminemail_out">坛主</a> 。
 </td>
 </tr>
~;
    &displayoutput;

}
else {

    $output = qq~
 <tr bgcolor="#FFFFFF">
 <td align="center">
 对不起，你的 Cookie 不匹配。<br>如果你想退出此邮件列表，那么必须首先登录论坛。
 <br><a href="loginout.cgi">按此登录后重试</a>
 </td>
 </tr>
~;
    &displayoutput;
}

sub displayoutput {

    print qq~
 <html>
 <head>
 <title></title>
 </head>
 <body bgcolor="#FFFFFF">
 <table border="0" align="center" width="456">
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333 size=3><b>欢迎使用 LeoBBS 邮件列表</td>
 </tr>
 $output
 </table>
 </body>
 </html>~;
    exit;
}
