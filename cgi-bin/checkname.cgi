#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / é›·å‚²æé…·è¶…çº§è®ºå›  #
#####################################################
# åŸºäºå±±é¹°(ç³Š)ã€èŠ±æ— ç¼ºåˆ¶ä½œçš„ LB5000 XP 2.30 å…è´¹ç‰ˆ  #
#   æ–°ç‰ˆç¨‹åºåˆ¶ä½œ & ç‰ˆæƒæ‰€æœ‰: é›·å‚²ç§‘æŠ€ (C)(R)2004    #
#####################################################
#      ä¸»é¡µåœ°å€ï¼š http://www.LeoBBS.com/            #
#      è®ºå›åœ°å€ï¼š http://bbs.LeoBBS.com/            #
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
require "data/styles.cgi";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "checkname.cgi";

$query = new LBCGI;
$inmembername = $query -> param('name');
$inmembername = &cleaninput($inmembername);
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

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

if ($bannedmember eq "yes") { $CheckR = "æˆ–å½“å‰çš„ IP è¢«ç®¡ç†¡£"; }

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
$CheckR="ÒÑ¾­±»±£Áô»òÕß±»½ûÖ¹×¢²á,Çë¸ü»»Ò»¸öÓÃ»§Ãû¡£" if ($noreg eq "yes");

$CheckR="ÓÃ»§ÃûÓĞÎÊÌâ£¬Çë¸ü»»£¡" if (($inmembername =~ /^m-/i)||($inmembername =~ /^s-/i)||($inmembername =~ /tr-/i)||($inmembername =~ /^y-/i)||($inmembername =~ /×¢²á/i)||($inmembername =~ /guest/i)||($inmembername =~ /qq-/i)||($inmembername =~ /qq/i)||($inmembername =~ /qw/i)||($inmembername =~ /q-/i)||($inmembername =~ /qx-/i)||($inmembername =~ /qw-/i)||($inmembername =~ /qr-/i)||($inmembername =~ /^È«Ìå/i)||($inmembername =~ /register/i)||($inmembername =~ /³ÏÆ¸ÖĞ/i)||($inmembername =~ /°ßÖñ/i)||($inmembername =~ /¹ÜÀíÏµÍ³Ñ¶Ï¢/i)||($inmembername =~ /leobbs/i)||($inmembername =~ /leoboard/i)||($inmembername =~ /À×°Á/i)||($inmembername =~ /LB5000/i)||($inmembername =~ /È«Ìå¹ÜÀíÈËÔ±/i)||($inmembername =~ /¹ÜÀíÔ±/i)||($inmembername =~ /ÒşÉí/i)||($inmembername =~ /¶ÌÏûÏ¢¹ã²¥/i)||($inmembername =~ /ÔİÊ±¿ÕÈ±/i)||($inmembername =~ /£ª£££¡£¦£ª/i)||($inmembername =~ /°æÖ÷/i)||($inmembername =~ /Ì³Ö÷/i)||($inmembername =~ /nodisplay/i)||($inmembername =~ /^system/i)||($inmembername =~ /---/i)||($inmembername eq "admin")||($inmembername eq "root")||($inmembername eq "copy")||($inmembername =~ /^sub/)||($inmembername =~ /^exec/)||($inmembername =~ /\@ARGV/i)||($inmembername =~ /^require/)||($inmembername =~ /^rename/i)||($inmembername =~ /^dir/i)||($inmembername =~ /^print/i)||($inmembername =~ /^con/i)||($inmembername =~ /^nul/i)||($inmembername =~ /^aux/i)||($inmembername =~ /^com/i)||($inmembername =~ /^lpt/i)||($inmembername =~ /^open/i));

$CheckR="ÓÃ»§ÃûÓĞÎÊÌâ£¬Çë¸ü»»£¡" if ($inmembername =~ /^q(.+?)-/ig || $inmembername =~ /^q(.+?)q/ig);


$tempinmembername =$inmembername;
$tempinmembername =~ s/ //g;
$tempinmembername =~ s/  //g;
if ($inmembername =~ /^¿ÍÈË/) { $CheckR="ÓĞµãÎÊÌâÓ´£¬Çë²»ÒªÔÚÓÃ»§ÃûµÄ¿ªÍ·ÖĞÊ¹ÓÃ¿ÍÈË×ÖÑù¡£"; }
if ($inmembername =~ /_/)     { $CheckR="ÓĞµãÎÊÌâÓ´£¬Çë²»ÒªÔÚÓÃ»§ÃûÖĞÊ¹ÓÃÏÂ»®Ïß£¡"; }
if ($inmembername =~ /\t/)    { $CheckR="ÓĞµãÎÊÌâÓ´£¬Çë²»ÒªÔÚÓÃ»§ÃûÖĞÊ¹ÓÃÌØÊâ×Ö·û£¡"; }
if (length($inmembername)>12) { $CheckR="Ì«³¤ÁË£¬Çë²»Òª³¬¹ı12¸ö×Ö·û£¨6¸öºº×Ö£©¡£"; }
if (length($inmembername)<2)  { $CheckR="Ì«¶ÌÁË£¬Çë²»ÒªÉÙì¶2¸ö×Ö·û£¨1¸öºº×Ö£©¡£"; }

#&getmember("$inmembername");
&getmember("$inmembername","no");
if ($userregistered ne "no") { $CheckR="ÒÑ¾­ÓĞÓÃ»§Ê¹ÓÃ£¬ÇëÑ¡ÔñÒ»¸öĞÂµÄÓÃ»§Ãû¡£"; }

if ($inmembername eq "") { $CheckR = "²»ÄÜÎª¿Õ"; }
if ($inmembername ne "") { $show   = qq~"<font color="red">$inmembername</font>"~; }
$CheckR = "¶Ô²»Æğ£¬ÄúÊäÈëµÄÓÃ»§ÃûÓĞÎÊÌâ£¬Çë²»ÒªÔÚÓÃ»§ÃûÖĞ°üº¬\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]ÕâÀà×Ö·û£¡" if ($inmembername =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/);

if ($CheckR eq "") {$CheckR="Ã»ÓĞÎÊÌâ£¬¿ÉÒÔÕı³£Ê¹ÓÃ¡£"; }
print qq~
<html>
<head> 
<title>$boardname</title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<!--end Java-->
<!--css info(editable)-->
<style>
A:visited{TEXT-DECORATION: none}
A:active{TEXT-DECORATION: none}
A:hover{TEXT-DECORATION: underline overline}
A:link{text-decoration: none;}
.t{LINE-HEIGHT: 1.4}
BODY{FONT-FAMILY: ĞÂÏ¸Ã÷Ìå; FONT-SIZE: 9pt;
SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
SCROLLBAR-SHADOW-COLOR: buttonface;
SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
SCROLLBAR-TRACK-COLOR: #eeeeee;
SCROLLBAR-DARKSHADOW-COLOR: buttonshadow}
TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: ĞÂÏ¸Ã÷Ìå; FONT-SIZE: 9pt} 
INPUT{BORDER-TOP-WIDTH: 1px; PADDING-RIGHT: 1px; PADDING-LEFT: 1px; BORDER-LEFT-WIDTH: 1px; FONT-SIZE: 9pt; BORDER-LEFT-COLOR: #cccccc; BORDER-BOTTOM-WIDTH: 1px; BORDER-BOTTOM-COLOR: #cccccc; PADDING-BOTTOM: 1px; BORDER-TOP-COLOR: #cccccc; PADDING-TOP: 1px; HEIGHT: 18px; BORDER-RIGHT-WIDTH: 1px; BORDER-RIGHT-COLOR: #cccccc}
textarea, select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: ĞÂÏ¸Ã÷Ìå; font-size: 9pt; font-style: bold;}
--> 
</style> 
<!--end css info-->
</head>
<body $lbbody>
<table width=100% align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$titleborder height="100%"><tr><td>
<table width=100% cellspacing=0 cellpadding=4 border=0 height="100%">
<tr><td align="center" bgcolor=$menubackground><font color=$menufontcolor>ÄãËùÑ¡µÄÓÃ»§Ãû$show$CheckR</font></td></tr></table></td></tr></table>
</body>
</html>
~;
exit;
