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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "whosonline.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
&ipbanned; #封杀一些 ip

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "客人" ) {
    $inmembername = "客人";
}
else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
     }
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
$membercodetemp = $membercode;

$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");
$current_time  = time;
$addtime = $timezone*3600 + $timedifferencevalue*3600;
$current_time  = &dateformatshort($current_time + $addtime);
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";

$helpurl = &helpfiles("在线用户");
$helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></a>~;

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t在线用户\tboth\t查看在线用户状态\t");
}
$freshtime= $query->cookie("freshtime");
if ($freshtime ne "") {
    $autofreshtime = $freshtime*60-1;
    $autofreshtime = 60 if ($autofreshtime < 60);
    $refreshnow = qq~<meta http-equiv="refresh" content="$autofreshtime;">~;
}
&mischeader("当前在线用户 (最后更新时间：$current_time)");

$output .= qq~$refreshnow
<p>
~;

$onlinedata = @onlinedata;
$output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=8 align=center><font face=$font color=$fontcolormisc><b>在线用户列表</b> (共 $onlinedata 人)</td></tr><tr>
<td bgcolor=$miscbackone align=center><font face=$font color=$fontcolormisc><b>头像</td>
<td bgcolor=$miscbackone align=center><font face=$font color=$fontcolormisc><b>用户名</td>
<td bgcolor=$miscbackone align=center><font face=$font color=$fontcolormisc><b>当前位置</td>
<td bgcolor=$miscbackone align=center><font face=$font color=$fontcolormisc><b>最后动作</td>
<td bgcolor=$miscbackone align=center><font face=$font color=$fontcolormisc><b>来访时间</td>
<td bgcolor=$miscbackone align=center><font face=$font color=$fontcolormisc><b>最近活动时间</td>
<td bgcolor=$miscbackone align=center><font face=$font color=$fontcolormisc><b>IP</td>
</tr>
~;
         
foreach (@onlinedata) {
    chomp $_;
    ($savedusername, $savedcometime, $savedtime, $savedwhere, $saveipaddresstemp, $saveosinfo, $savebrowseinfo, $savedwhere2, $fromwhere, $savemembercode, $savehidden) = split(/\t/, $_);
    $savedwhere2 =~ s/＊＃！＆＊//;
    $fromwhere     = "已设置保密" if (($pvtip ne "on")&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes"));
    $savedcometime = &dateformatshort($savedcometime + $addtime);
    $savedtime     = &dateformatshort($savedtime + $addtime);
    ($lookfor, $no) = split(/\(/,$savedusername);
    if ($lookfor eq "客人") { $savedusername = "客人"; $useravatar = "没有"; }
    else {
	my $checkhidden=0;
	if (((($savehidden eq 1)&&($membercodetemp ne "ad"))||($savedusername =~ /^客人/))&&(lc($savedusername) ne lc($inmembername))) {
	    $checkhidden=1;
	    $savedusername = "隐身会员"; $useravatar = "没有";
	}
	if ($checkhidden==0) {
#	    &getmember("$savedusername");
	    &getmember("$savedusername","no");
            if ($avatars eq "on") {
	        if (($personalavatar)&&($personalwidth)&&($personalheight)) { #自定义头像存在
	            $personalavatar =~ s/\$imagesurl/${imagesurl}/o;
	            if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
		        $personalavatar=uri_escape($personalavatar);
	                $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
	            }
	            else {
		        $personalavatar=uri_escape($personalavatar);
	                $useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>);
	            }
	        }
                elsif (($useravatar ne "noavatar") && ($useravatar)) {
		    $useravatar=uri_escape($useravatar);
                    $useravatar = qq(<br>&nbsp; <img src=$imagesurl/avatars/$useravatar.gif $defaultwidth $defaultheight>);
                }
        	else {
            	    if (($oicqnumber) && ($oicqnumber =~ /[0-9]/)) {
            		$useravatar=qq~<br>&nbsp; <img src=http://qqshow-user.tencent.com/$oicqnumber/11/00/ title="QQ 秀形象" border=0 width=70 height=113>~;
                    }
                    else {$useravatar="没有"; }
                }
            }
        }
    }

    ($saveipaddress, $none) = split(/=/,$saveipaddresstemp);
    ($ip1,$ip2,$ip3,$ip4)   = split(/\./,$saveipaddress);
    if ($membercodetemp eq "ad") {
        $saveipaddress="$ip1.$ip2.$ip3.$ip4";
    }
    elsif ($membercodetemp eq "smo") {
        if ($smocanseeip eq "no") { $saveipaddress="$ip1.$ip2.$ip3.$ip4"; }
        else {
	    if ($pvtip eq "on") { $saveipaddress="$ip1.$ip2.$ip3.$ip4"; }
	    else { $saveipaddress="已设置保密"; }
        }
    }
    elsif ($membercodetemp eq "mo") {
        if ($pvtip eq "on") { $saveipaddress="$ip1.$ip2.$ip3.*"; }
                       else { $saveipaddress="已设置保密"; }
    }
    else {
        if (($pvtip eq "on")&&($inmembername ne "客人")) {
	    $saveipaddress="$ip1.$ip2.*.*";
        }
        else { $saveipaddress="已设置保密"; }
    }
    unless (($savedusername eq "客人")||($savedusername eq "隐身会员")) {
	$ppp = qq~<a href="profile.cgi?action=show&member=~ . uri_escape($savedusername) . qq~" target=_blank><font face=$font color=$fontcolormisc><b>$savedusername</b></font></a>~;
    }
    else {
	$ppp = qq~<font face=$font color=$fontcolormisc><b>$savedusername</b></font>~;
    }

    $output .=qq~<tr><td bgcolor=$miscbackone nowrap align=center>$useravatar</td>
<td bgcolor=$miscbackone nowrap align=center>$ppp</td>
<td bgcolor=$miscbackone nowrap><font face=$font color=$fontcolormisc>$savedwhere</font></td>
<td bgcolor=$miscbackone><font face=$font color=$fontcolormisc>$savedwhere2</font></td>
<td bgcolor=$miscbackone nowrap align=center><font face=$font color=$fontcolormisc>$savedcometime</font></td>
<td bgcolor=$miscbackone nowrap align=center><font face=$font color=$fontcolormisc>$savedtime</font></td>
<td bgcolor=$miscbackone nowrap align=center><font face=$font color=$fontcolormisc>$saveipaddress</font></td>
</tr>~;
}
$output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;

print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output("$boardname - 论坛当前在线用户",\$output);
exit;
