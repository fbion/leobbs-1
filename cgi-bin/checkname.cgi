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

use strict;
use warnings;
use LBCGI;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/styles.cgi";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;
my $thisprog = "checkname.cgi";

my $query = new LBCGI;
my $inmembername = $query -> param('name');
$inmembername = &cleaninput($inmembername);
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

$CheckR="";
$bannedmember = "no";
($ipaddress,$trueipaddress) = split(/\=/,&myip);

$filetoopen = "$lbdir" . "data/baniplist.cgi";
open(FILE,"${lbdir}data/baniplist.cgi");
my $bannedips = <FILE>;
close(FILE);
chomp $bannedips;
$bannedips = "\t$bannedips\t";
$bannedips =~ s/\t\t/\t/isg;
my $ipaddresstemp     = "\t$ipaddress\t";
my $trueipaddresstemp = "\t$trueipaddress\t";
$bannedmember = "yes" if (($bannedips =~ /$ipaddresstemp/i)||($bannedips =~ /$trueipaddresstemp/i));

if ($bannedmember eq "yes") { $CheckR = "或当前的 IP 被管理員设置成禁止注册新用户了，请更换或者联络管理員以便解决。"; }

open(THEFILE,"${lbdir}data/noreglist.cgi");
$userarray = <THEFILE>;
close(THEFILE);
chomp $userarray;
@saveduserarray = split(/\t/,$userarray);
$noreg = "no";
foreach (@saveduserarray) {
    chomp $_;
    if ($inmembername =~ m/$_/isg) {
        $noreg = "yes";
	last;
    }
}
$CheckR="已经被保留或者被禁止注册,请更换一个用户名。" if ($noreg eq "yes");

$CheckR="用户名有问题，请更换！" if (($inmembername =~ /^m-/i)||($inmembername =~ /^s-/i)||($inmembername =~ /tr-/i)||($inmembername =~ /^y-/i)||($inmembername =~ /注册/i)||($inmembername =~ /guest/i)||($inmembername =~ /qq-/i)||($inmembername =~ /qq/i)||($inmembername =~ /qw/i)||($inmembername =~ /q-/i)||($inmembername =~ /qx-/i)||($inmembername =~ /qw-/i)||($inmembername =~ /qr-/i)||($inmembername =~ /^全体/i)||($inmembername =~ /register/i)||($inmembername =~ /诚聘中/i)||($inmembername =~ /斑竹/i)||($inmembername =~ /管理系统讯息/i)||($inmembername =~ /leobbs/i)||($inmembername =~ /leoboard/i)||($inmembername =~ /雷傲/i)||($inmembername =~ /LB5000/i)||($inmembername =~ /全体管理人员/i)||($inmembername =~ /管理员/i)||($inmembername =~ /隐身/i)||($inmembername =~ /短消息广播/i)||($inmembername =~ /暂时空缺/i)||($inmembername =~ /＊＃！＆＊/i)||($inmembername =~ /版主/i)||($inmembername =~ /坛主/i)||($inmembername =~ /nodisplay/i)||($inmembername =~ /^system/i)||($inmembername =~ /---/i)||($inmembername eq "admin")||($inmembername eq "root")||($inmembername eq "copy")||($inmembername =~ /^sub/)||($inmembername =~ /^exec/)||($inmembername =~ /\@ARGV/i)||($inmembername =~ /^require/)||($inmembername =~ /^rename/i)||($inmembername =~ /^dir/i)||($inmembername =~ /^print/i)||($inmembername =~ /^con/i)||($inmembername =~ /^nul/i)||($inmembername =~ /^aux/i)||($inmembername =~ /^com/i)||($inmembername =~ /^lpt/i)||($inmembername =~ /^open/i));

$CheckR="用户名有问题，请更换！" if ($inmembername =~ /^q(.+?)-/ig || $inmembername =~ /^q(.+?)q/ig);


$tempinmembername =$inmembername;
$tempinmembername =~ s/ //g;
$tempinmembername =~ s/  //g;
if ($inmembername =~ /^客人/) { $CheckR="有点问题哟，请不要在用户名的开头中使用客人字样。"; }
if ($inmembername =~ /_/)     { $CheckR="有点问题哟，请不要在用户名中使用下划线！"; }
if ($inmembername =~ /\t/)    { $CheckR="有点问题哟，请不要在用户名中使用特殊字符！"; }
if (length($inmembername)>12) { $CheckR="太长了，请不要超过12个字符（6个汉字）。"; }
if (length($inmembername)<2)  { $CheckR="太短了，请不要少於2个字符（1个汉字）。"; }

#&getmember("$inmembername");
&getmember("$inmembername","no");
if ($userregistered ne "no") { $CheckR="已经有用户使用，请选择一个新的用户名。"; }

if ($inmembername eq "") { $CheckR = "不能为空"; }
if ($inmembername ne "") { $show   = qq~"<font color="red">$inmembername</font>"~; }
$CheckR = "对不起，您输入的用户名有问题，请不要在用户名中包含\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]这类字符！" if ($inmembername =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/);

if ($CheckR eq "") {$CheckR="没有问题，可以正常使用。"; }
print qq~
<html>
<head> 
<title>$boardname</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<!--end Java-->
<!--css info(editable)-->
<style>
A:visited{TEXT-DECORATION: none}
A:active{TEXT-DECORATION: none}
A:hover{TEXT-DECORATION: underline overline}
A:link{text-decoration: none;}
.t{LINE-HEIGHT: 1.4}
BODY{FONT-FAMILY: 新细明体; FONT-SIZE: 9pt;
SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
SCROLLBAR-SHADOW-COLOR: buttonface;
SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
SCROLLBAR-TRACK-COLOR: #eeeeee;
SCROLLBAR-DARKSHADOW-COLOR: buttonshadow}
TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: 新细明体; FONT-SIZE: 9pt} 
INPUT{BORDER-TOP-WIDTH: 1px; PADDING-RIGHT: 1px; PADDING-LEFT: 1px; BORDER-LEFT-WIDTH: 1px; FONT-SIZE: 9pt; BORDER-LEFT-COLOR: #cccccc; BORDER-BOTTOM-WIDTH: 1px; BORDER-BOTTOM-COLOR: #cccccc; PADDING-BOTTOM: 1px; BORDER-TOP-COLOR: #cccccc; PADDING-TOP: 1px; HEIGHT: 18px; BORDER-RIGHT-WIDTH: 1px; BORDER-RIGHT-COLOR: #cccccc}
textarea, select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: 新细明体; font-size: 9pt; font-style: bold;}
--> 
</style> 
<!--end css info-->
</head>
<body $lbbody>
<table width=100% align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$titleborder height="100%"><tr><td>
<table width=100% cellspacing=0 cellpadding=4 border=0 height="100%">
<tr><td align="center" bgcolor=$menubackground><font color=$menufontcolor>你所选的用户名$show$CheckR</font></td></tr></table></td></tr></table>
</body>
</html>
~;
exit;