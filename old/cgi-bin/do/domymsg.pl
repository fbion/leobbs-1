#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

use strict;
use warnings;
use diagnostics;

open(MSGIN, "${lbdir}$msgdir/in/${memberfilename}_msg.cgi");
sysread(MSGIN, $totalmessages, (stat(MSGIN))[7]);
close(MSGIN);
$totalmessages =~ s/\r//isg;
my @allmessages = split(/\n/, $totalmessages);
$totalmessages = @allmessages;
my @newmessages = grep (/^(.+)\tno\t/, @allmessages);
$unread = @newmessages;
if ($unread && $allowusemsg ne "off") {
    my $intanchumsg = $query->cookie("tanchumsg");
    my $popnew = qq~<script>if (confirm("你有新的短消息，是否打开收件箱查看？")) openScript("messanger.cgi?action=inbox",600,400);</script>~ if ((($newmsgpop eq "on") || ($newmsgpop eq "popup")) && ($intanchumsg eq ""));
    my $lightnew = qq~<script language="JavaScript">pmBox.bgColor='Lightblue';setInterval("Timer()", 500);x=1;function Timer(){set=1;if(x==0 && set==1){pmBox.bgColor='Lightblue';x=1;set=0;}if(x==1 && set==1){pmBox.bgColor='';x=0;set=0;}}</script>~ if ((($newmsgpop eq "on") || ($newmsgpop eq "light")));
    $newmail = qq(<table width=$tablewidth cellpadding=2 cellspacing=0 align=center><tr><td width="*"></td><td align=right id="pmBox" width=215><bgsound src=$imagesurl/images/mail.wav border=0>$lightnew$popnew<span style="cursor:hand" onClick="javascript:openScript('messanger.cgi?action=inbox',600,400)"><img src=$imagesurl/images/newmail.gif border=0><font color=$fonthighlight>你有 <B>$unread</B> 条新的短信息，请注意查收</font></span></td></tr></table>);
}
#写入 cache
open(FILE, ">${lbdir}cache/mymsg/$memberfilename.pl");
print FILE qq~\$totalmessages = $totalmessages;\n~;
print FILE qq~\$unread = $unread;\n~;
print FILE qq~\$newmail = qq($newmail);\n~;
print FILE "1;\n";
close(FILE);
1;
