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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "code.cgi";
require "bbs.lib.pl";
require "postjs.cgi";
$|++;
$thisprog	= "xzbadmin.cgi";
$query		= new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

if (int($hownews) < 50)
{	#å­—æ•°é¢„è®¾å€¼
	$hownews = 100;
}
#å–å¾—æ•°æ®
for ('forum','membername','password','action','inpost','message','xzbid','checked') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inforum		= $forum;
if (($inforum eq "")||($inforum !~ /^[0-9]+$/))
{	#éªŒè¯åˆ†è®ºå›ç¼–å·
	&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼");
}
if (-e "${lbdir}data/style${inforum}.cgi")
{	#è¯»å–ä¸“å±é£æ ¼
	require "${lbdir}data/style${inforum}.cgi";
}
$inmembername	= $membername;			#è½¬æ¢å˜æ•°
$inpassword	= $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$currenttime	= time;
$inmembername	= &stripMETA($inmembername);

#ä¸ªäººé£æ ¼
$inselectstyle	= $query->cookie("selectstyle");	#è¯»å–èµ„æ–™
$inselectstyle   = $skinselected if ($inselectstyle eq "");
if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./))
{	#ä¸ªäººé£æ ¼ä¸æ­£ç¡®
	&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼");	#è¾“å‡ºé”™è¯¯é¡µ
}
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi"))
{	#æœ‰æŒ‡å®šä¸ªäººé£æ ¼
	require "${lbdir}data/skin/${inselectstyle}.cgi";	#è¯»å–ä¸ªäººé£æ ¼
}
#ä¼šå‘˜å¸å·
if ($inmembername eq "")
{	#æ²¡æä¾›ä¼šå‘˜åç§°
	$inmembername	= $query->cookie("amembernamecookie");	#ä» COOKIE è¯»å–
}
if ($inpassword eq "")
{	#æ²¡æä¾›å¯†ç 
	$inpassword		= $query->cookie("apasswordcookie");	#ä» COOKIE è¯»å–
}
$inmembername	=~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;	#å­—ä¸²å¤„ç†
$inpassword		=~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

#æ£€æŸ¥å¸å·
if (($inmembername eq "")||($inmembername eq "å®¢äºº"))
{	#å®¢äºº
	&error("æ™®é€šé”™è¯¯&åªé™ä¼šå‘˜è¿›å…¥ï¼");	#ç¦æ­¢è¿›å…¥
}
else
{	#ä¼šå‘˜
	&getmember("$inmembername","no");	#è¯»å–å¸å·èµ„æ–™
	if ($userregistered eq "no")
	{	#æœªæ³¨å†Œå¸å·
		&error("æ™®é€šé”™è¯¯&æ­¤ç”¨æˆ·æ ¹æœ¬ä¸å­˜åœ¨ï¼");				#ç¦æ­¢è¿›å…¥
	}
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("æ™®é€šé”™è¯¯&å¯†ç ä¸ç”¨æˆ·åä¸ç›¸ç¬¦ï¼Œè¯·é‡æ–°ç™»å½•ï¼");
     }
}
$addtimes		= ($timedifferencevalue + $timezone)*3600;	#æ—¶å·®
#è®ºå›çŠ¶æ€
&doonoff;  #è®ºå›å¼€æ”¾ä¸å¦

&error("è¿›å…¥è®ºå›&ä½ çš„è®ºå›ç»„æ²¡æœ‰æƒé™è¿›å…¥è®ºå›ï¼") if ($yxz ne '' && $yxz!~/,$membercode,/);
    if ($allowusers ne '') {
	&error('è¿›å…¥è®ºå›&ä½ ä¸å…è®¸è¿›å…¥è¯¥è®ºå›ï¼') if (",$allowusers," !~ /\Q,$inmembername,\E/i);
    }

#è¯»å–åˆ†è®ºå›èµ„æ–™
my $forumdata	= "${lbdir}forum${inforum}/foruminfo.cgi";
if (-e $forumdata)
{	#æ‰¾åˆ°è¯¥åˆ†è®ºå›èµ„æ–™
	&getoneforum("$inforum");							#è¯»å–èµ„æ–™
}
else
{	#æ‰¾ä¸åˆ°èµ„æ–™
	&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼");	#è¾“å‡ºé”™è¯¯é¡µ
}
#éªŒè¯æƒé™
if (($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"))
{	#æœ‰æƒé™çš„äººï¼šå›ä¸»ï¼Œæ€»ç‰ˆä¸»ï¼Œç‰ˆä¸»æ ä¸­çš„
	&error("åˆ é™¤å°å­—æŠ¥&ä½ æ²¡æƒåŠ›åˆ é™¤ï¼");					#è¾“å‡ºé”™è¯¯é¡µ
}
#è¯´æ˜è¿ç»“
$helpurl		= &helpfiles("é˜…è¯»æ ‡è®°");
$helpurl		= qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;
#æŒ‡å®šæ¨¡å¼
my %Mode = (
	'delete'		=> \&deletexzb,		#åˆ é™¤
	'deleteover'	=> \&deleteoverxzb,	#åˆ é™¤ 2
	'edit'			=> \&editxzb,		#ç¼–è¾‘
);
#è¾“å‡ºæ¡£å¤´
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
#éªŒè¯æ¨¡å¼
if (defined $Mode{$action})
{	#æœ‰è¯¥æ¨¡å¼
	$Mode{$action}->();		#æ‰§è¡Œæ¨¡å¼
}
else
{	#æ²¡æœ‰è¯¥æ¨¡å¼
	&toppage;				#æ‰§è¡Œé¢„è®¾æ¨¡å¼ -> é¦–é¡µ
}
#è¾“å‡ºé¡µé¢
&output("$forumname - å°å­—æŠ¥ç®¡ç†",\$output);
#å¤„ç†ç»“æŸ
exit;
#æ¨¡å¼å†…å®¹
sub toppage
{	#æ¨¡å¼ -> é¦–é¡µ
	#è¾“å‡ºé¡µé¢å¤´
	&mischeader("å°å­—æŠ¥ç®¡ç†");
	#è¯»å–èµ„æ–™
	my @xzbdata = ();								#åˆå§‹åŒ–
	open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");	#å¼€å¯æ–‡ä»¶
	while (my $line = <FILE>)
	{	#æ¯æ¬¡è¯»å–ä¸€è¡Œå†…å®¹ loop 1
		chomp $line;			#å»æ‰æ¢è¡Œç¬¦
		push(@xzbdata,$line);	#æ”¾è¿›ç»“æœ ARRAY
	}#loop 1 end
	close(FILE);									#å…³é—­æ–‡ä»¶

	#é¡µé¢è¾“å‡º
	$output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post" id="1">
<input type="hidden" name="action" value="delete">
<input type="hidden" name="forum" value="$inforum">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="7%" $catbackpic align="center">
		</td>
		<td bgcolor="$titlecolor" width="*" $catbackpic align="center">
			<font color="$titlefontcolor"><b>æ ‡é¢˜</b></font>
		</td>
		<td bgcolor="$titlecolor" width="10%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>å‘å¸ƒè€…</b></font>
		</td>
		<td bgcolor="$titlecolor" width="20%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>å‘å¸ƒæ—¶é—´</b></font>
		</td>
		<td bgcolor="$titlecolor" width="15%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>å†…å®¹å­—èŠ‚æ•°</b></font>
		</td>
		<td bgcolor="$titlecolor" width="3%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>é€‰</b></font>
		</td>
	</tr>~;
	#è¾“å‡ºæ•°æ®
	my $i = 0;	#ç¼–å·
	foreach my $line(@xzbdata)
	{	#å›åœˆå¤„ç†æ•°æ® loop 1
		#   æ²¡ç”¨   , æ ‡é¢˜   , å‘å¸ƒè€…  , å†…å®¹ , å‘å¸ƒæ—¶é—´
		my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);		#åˆ†å‰²æ•°æ®
		#èƒŒæ™¯è‰²
		if ($i%2 == 0) {
			$postbackcolor = $postcolorone;
		} else {
			$postbackcolor = $postcolortwo;
		}
		my $admini		= qq~<div align="right"><font color="$titlecolor">|<a href="$thisprog?action=edit&forum=$inforum&xzbid=$posttime"><font color="$titlecolor">ç¼–è¾‘</font></a>|<a href="$thisprog?action=delete&forum=$inforum&xzbid=$posttime"><font color="$titlecolor">åˆ é™¤</font></a>|</font></div>~;		#ç®¡ç†è¿ç»“
		my $postdate		= &dateformat($posttime+$addtimes);						#å‘å¸ƒæ—¶é—´
		my $msgbytes	= length($msg);												#å­—èŠ‚æ•°
		my $startedby	= uri_escape($postid);		#ä¼šå‘˜å
		$iuu = $i + 1;
		$output .= qq~
	<tr>
		<td bgcolor="$postbackcolor" width="7%" align="center">
			<font color="$postfontcolorone">No.<i>$iuu</i></font>
		</td>
		<td bgcolor="$postbackcolor" width="*" align="left">
			&nbsp;&nbsp;<font color="$postfontcolorone">$title</font>$admini
		</td>
		<td bgcolor="$postbackcolor" width="10%" align="center">
			<font color="$postfontcolorone"><span style=cursor:hand onClick=javascript:O9('$startedby')>$postid</span></font>
		</td>
		<td bgcolor="$postbackcolor" width="20%" align="center">
			<font color="$postfontcolorone">$postdate</font>
		</td>
		<td bgcolor="$postbackcolor" width="15%" align="center">
			<font color="$postfontcolorone"><i>$msgbytes</i> byte(s)</font>
		</td>
		<td bgcolor="$postbackcolor" width="3%" align="center">
			<input type="checkbox" name="xzbid" value="$posttime">
		</td>
	</tr>~;
		$i++;																		#ç¼–å·é€’å¢
	}#loop 1 end
	#é¡µé¢è¾“å‡º
	$output .= qq~
	</table>
	</td>
</tr>
</table><SCRIPT>valignend()</SCRIPT>
<table cellpadding="0" cellspacing="2" width="$tablewidth" align="center" border="0">
<tr>
	<td align="right" width="75%">
		<input type="submit" value="åˆ é™¤é€‰æ‹©">
	</td>
</form id="1 end">
<form action="$thisprog" method="post" id="2">
<input type="hidden" name="action" value="deleteover">
<input type="hidden" name="forum" value="$inforum">
	<td align="right">
		<input type="submit" value="åˆ é™¤è¶…è¿‡ï¼”ï¼˜å°æ—¶çš„å°å­—æŠ¥">
	</td>
</tr>
</form id="2 end">
</table><BR>~;
}
sub editxzb
{	#æ¨¡å¼ -> ç¼–è¾‘
	#è¾“å‡ºé¡µé¢å¤´
	&mischeader("ç¼–è¾‘å°å­—æŠ¥");
	#æ‰¾å¯»è¦ç¼–è¾‘çš„å°å­—æŠ¥
	my $findresult	= -1;	#åˆå§‹åŒ–
	my @xzbdata		= ();
	my $xzbno		= 0;
	open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");	#å¼€å¯æ–‡ä»¶
	while (my $line = <FILE>)
	{	#æ¯æ¬¡è¯»å–ä¸€è¡Œå†…å®¹ loop 1
		chomp $line;															#å»æ‰æ¢è¡Œç¬¦
		my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);	#åˆ†å‰²æ•°æ®
		if ($posttime eq $xzbid)
		{	#å°±æ˜¯è¿™ä¸ª
			$findresult = $xzbno;		#æ¿€æ´»æ‰¾å¯»ç»“æœ
		}
		elsif ($findresult == -1)
		{	#ä¸æ˜¯çš„æ—¶å€™
			$xzbno++;				#ç¼–å·é€’å¢
		}
		push(@xzbdata,$line);													#æ”¾è¿›æ•°æ® ARRAY
	}#loop 1 end
	close(FILE);
	if ($findresult == -1)
	{	#æ‰¾ä¸åˆ°
		&error("ç¼–è¾‘å°å­—æŠ¥&æ‰¾ä¸åˆ°ç›®æ ‡å°å­—æŠ¥ï¼");										#è¾“å‡ºé”™è¯¯é¡µ
	}
	if ($checked ne 'yes')
	{	#æœªè¿›è¡Œç¡®è®¤
		#ç›®å‰æ•°æ®
		#   æ²¡ç”¨   , æ ‡é¢˜   , å‘å¸ƒè€…  , å†…å®¹ , å‘å¸ƒæ—¶é—´
		my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$xzbdata[$xzbno]);	#åˆ†å‰²æ•°æ®
	    $msg =~ s/\<p\>/\n\n/ig;															#å­—ä¸²å¤„ç†
	    $msg =~ s/\<br\>/\n/ig;
		my $startedby	=  uri_escape($postid);				#ä¼šå‘˜å
		#é¡µé¢è¾“å‡º
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post" id="1">
<input type="hidden" name="action" value="edit">
<input type="hidden" name="checked" value="yes">
<input type="hidden" name="forum" value="$inforum">
<input type="hidden" name="xzbid" value="$posttime">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center" colspan="2">
			<font color="$titlefontcolor"><b>ç¼–è¾‘æ‰€é€‰å°å­—æŠ¥</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolortwo" alin="center" colspan="2">
			<table cellpadding="0" cellspacing="0" width="100%" bgcolor="$tablebordercolor" align="center" border="0">
			<tr>
				<td>
					<table cellpadding="3" cellspacing="1" border="0" width="100%">
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>æ‚¨ç›®å‰çš„èº«ä»½æ˜¯ï¼š <font color=$fonthighlight><B><u>$inmembername</u></B></font> ï¼Œè¦ä½¿ç”¨å…¶ä»–ç”¨æˆ·èº«ä»½ï¼Œè¯·è¾“å…¥ç”¨æˆ·åå’Œå¯†ç ã€‚æœªæ³¨å†Œå®¢äººè¯·è¾“å…¥ç½‘åï¼Œå¯†ç ç•™ç©ºã€‚</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·å</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">æ‚¨æ²¡æœ‰æ³¨å†Œï¼Ÿ</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„å¯†ç </font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">å¿˜è®°å¯†ç ï¼Ÿ</a></font></td></tr>
					<tr>
						<td bgcolor=$miscbackone valign=top>
							<font color="$fontcolormisc"><b>å°å­—æŠ¥å‘å¸ƒè€…</b></font>
						</td>
						<td bgcolor="$miscbackone">
							<font color="$postfontcolorone"><u><span style=cursor:hand onClick=javascript:O9('$startedby')>$postid</span></u></font>
						</td>
					</tr>
					<tr>
						<td bgcolor=$miscbackone valign=top>
							<font color="$fontcolormisc"><b>å°å­—æŠ¥æ ‡é¢˜</b> (æœ€å¤§ 80 å­—)</font>
						</td>
						<td bgcolor="$miscbackone">
							<input type="text" maxlength="80" name=inpost onkeydown=ctlent() value="$title" size=80>
						</td>
					</tr>
					<tr>
						<td bgcolor=$miscbacktwo valign=top>
							<font color="$fontcolormisc"><b>å°å­—æŠ¥å†…å®¹</b> (æœ€å¤š $hownews å­—)<p>
							åœ¨æ­¤è®ºå›ä¸­ï¼š
							<li>HTML æ ‡ç­¾: <b>ä¸å¯ç”¨</b>
							<li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS æ ‡ç­¾</a>: <b>å¯ç”¨</b></font>
						</td>
						<td bgcolor=$miscbacktwo valign=top>
							<TEXTAREA cols=58 name=message rows=6 wrap=soft onkeydown=ctlent()>$msg</TEXTAREA>
						</td>
					</tr>
					</table>
				</td>
			</tr>
			</table>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="right" width="51%">
			<input type="submit" value="æäº¤ç¼–è¾‘">&nbsp;
		</td>
</form id="1">
<form action="$thisprog" method="get" id="2">
<input type="hidden" name="forum" value="$inforum">
		<td bgcolor="$postcolorone" align="left">
			&nbsp;<input type="submit" value="è¿”å›ä¸»é¡µé¢">
		</td>
</form id="2">
	</tr>
	</table>
	</td>
</tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
	else
	{	#å·²è¿›è¡Œç¡®è®¤
		#newfile;								#Ğ´ÈëĞÂÎÄ¼şÄÚÈİ
		close(FILE);										#¹Ø±ÕÎÄ¼ş
		#Ò³ÃæÊä³ö
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="get">
<input type="hidden" name="forum" value="$inforum">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>ÒÑ¾­±à¼­¸ÃĞ¡×Ö±¨ÄÚÈİ</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="center">
			<input type="submit" value="·µ»ØÖ÷Ò³Ãæ">
		</td>
	</tr>
	</table>
	</td>
</tr>
</form>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
}
sub deletexzb
{	#Ä£Ê½ -> É¾³ı
	#Êä³öÒ³ÃæÍ·
	&mischeader("É¾³ıĞ¡×Ö±¨");
	#¶ÁÈ¡¸´Ñ¡Êı¾İ
	my @noarray		= ();	#³õÊ¼»¯
	my %nohash		= ();
	my $xzbidcount	= 0;
	my $novalue		= '';	# HIDDEN µÄÊäÈëÀ¸
	if ($xzbid ne "")
	{	#ÓĞ¶¨ÒåµÚÒ»¸ö ID
		@noarray = $query->param('xzbid');	#ËùÓĞ ID
		foreach my $xzbid(@noarray)
		{	#´¦ÀíËùÓĞ ID loop 1
			$novalue .= '<input type="hidden" name="xzbid" value="'.$xzbid.'">'."\n";	#Ôö¼ÓÀ¸Î»
			$nohash{$xzbid} = $xzbid;													#·ÅÈë HASH
			$xzbidcount++;																#ÊıÄ¿µİÔö
		}#loop 1 end 
		chomp $novalue;						#È¥³ı×îáá»»ĞĞ
	}
	if ($xzbidcount == 0)
	{	#Ã»Ñ¡ÈÎºÎĞ¡×Ö±¨
		&error("É¾³ıĞ¡×Ö±¨&Ã»ÓĞÑ¡ÈÎºÎĞ¡×Ö±¨£¡");			#Êä³ö´íÎóÒ³
	}

	if ($checked ne 'yes')
	{	#Î´½øĞĞÈ·ÈÏ
		#Ò³ÃæÊä³ö
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post" id="1">
<input type="hidden" name="action" value="delete">
<input type="hidden" name="checked" value="yes">
<input type="hidden" name="forum" value="$inforum">
$novalue
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center" colspan="2">
			<font color="$titlefontcolor"><b>È·ÈÏÉ¾³ıËùÑ¡µÄ $xzbidcount ¸öĞ¡×Ö±¨£¿</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="right" width="51%">
			<input type="submit" value="È·ÈÏÉ¾³ı">&nbsp;
		</td>
</form id="1">
<form action="$thisprog" method="get" id="2">
<input type="hidden" name="forum" value="$inforum">
		<td bgcolor="$postcolorone" align="left">
			&nbsp;<input type="submit" value="·µ»ØÖ÷Ò³Ãæ">
		</td>
</form id="2">
	</tr>
	</table>
	</td>
</tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
	else
	{	#ÒÑ½øĞĞÈ·ÈÏ
		#É¾³ı´¦Àí
		my $newfile	= '';									#³õÊ¼»¯ÎÄ¼ş
		my $delbyte	= '';									#É¾³ıµÄ×Ö½Ú
		open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");		#¿ªÆôÎÄ¼ş
		while (my $line = <FILE>)
		{	#Ã¿´Î¶ÁÈ¡Ò»ĞĞÄÚÈİ loop 1
			chomp $line;			#È¥µô»»ĞĞ·û
			my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);		#·Ö¸îÊı¾İ
			if(($line eq "") || (defined $nohash{$posttime}))
			{	#¿Õ°×ĞĞ»òÉ¾³ıÄ¿Â¼
				$delbyte += length($line);	#¼ÓÉÏÉ¾³ıµÄ×Ö½Ú
				next;						#Ìø¹ı
			}
			$newfile .= $line."\n";														#·ÅÈëĞÂÎÄ¼şÄÚ
		}#loop 1 end
		close(FILE);										#¹Ø±ÕÎÄ¼ş
		open(FILE,'>'."${lbdir}boarddata/xzb$inforum.cgi");	#¿ªÆôÖ»Ğ´ÎÄ¼ş
		print FILE $newfile;								#Ğ´ÈëĞÂÎÄ¼şÄÚÈİ
		close(FILE);										#¹Ø±ÕÎÄ¼ş
		#Ò³ÃæÊä³ö
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="get">
<input type="hidden" name="forum" value="$inforum">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>ËùÑ¡µÄ $xzbidcount ¸öĞ¡×Ö±¨ÒÑ±»É¾³ı</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolortwo" align="center">
			×Ü¹²É¾³ı $delbyte  byte(s)
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="center">
			<input type="submit" value="·µ»ØÖ÷Ò³Ãæ">
		</td>
	</tr>
	</table>
	</td>
</tr>
</form>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
}
sub deleteoverxzb
{	#Ä£Ê½ -> É¾³ı 2
	#Êä³öÒ³ÃæÍ·
	&mischeader("É¾³ıĞ¡×Ö±¨");
	#¶ÁÈ¡³¬Ê±×ÊÁÏ
	my @delxzbid	= ();	#³õÊ¼»¯
	if($checked ne 'yes')
	{	#Î´½øĞĞÈ·ÈÏ
		open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");	#¿ªÆôÎÄ¼ş
		while (my $line = <FILE>)
		{	#Ã¿´Î¶ÁÈ¡Ò»ĞĞÄÚÈİ loop 1
			chomp $line;															#È¥µô»»ĞĞ·û
			my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);	#·Ö¸îÊı¾İ
			if ($currenttime-$posttime > 3600*48)
			{	#³¬¹ı£´£¸Ğ¡Ê±
				push(@delxzbid,$posttime);		#·Åµ½ĞèÉ¾ ID
			}
		}#loop 1 end
		close(FILE);									#¹Ø±ÕÎÄ¼ş
	}
	else
	{	#ÒÑ½øĞĞÈ·ÈÏ
		@delxzbid = $query->param('xzbid');				#ĞèÉ¾ ID
	}
	if (@delxzbid == 0)
	{	#Ã»ÈÎºÎĞ¡×Ö±¨ĞèÒªÉ¾
		&error("É¾³ıĞ¡×Ö±¨&Ã»ÓĞĞ¡×Ö±¨ĞèÒªÉ¾³ı£¡");			#Êä³ö´íÎóÒ³
	}
	#¶ÁÈ¡¸´Ñ¡Êı¾İ
	my %nohash		= ();
	my $xzbidcount	= 0;
	my $novalue		= '';	# HIDDEN µÄÊäÈëÀ¸
	foreach my $xzbid(@delxzbid)
	{	#´¦ÀíËùÓĞ ID loop 1
		unless ($currenttime-$posttime > 3600*48)
		{	#ÔÙ¼ì²éÊ±¼ä£¬²»Í¨¹ı
			next;		#Ìø¹ı
		}
		$novalue .= '<input type="hidden" name="xzbid" value="'.$xzbid.'">'."\n";	#Ôö¼ÓÀ¸Î»
		$nohash{$xzbid} = $xzbid;													#·ÅÈë HASH
		$xzbidcount++;																#ÊıÄ¿µİÔö
	}#loop 1 end 
	chomp $novalue;						#È¥³ı×îáá»»ĞĞ
	
	if ($checked ne 'yes')
	{	#Î´½øĞĞÈ·ÈÏ
		#Ò³ÃæÊä³ö
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post">
<input type="hidden" name="action" value="delete">
<input type="hidden" name="checked" value="yes">
<input type="hidden" name="forum" value="$inforum">
$novalue
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>È·ÈÏÉ¾³ıËùÑ¡µÄ $xzbidcount ¸öĞ¡×Ö±¨£¿</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="center">
			<input type="submit" value="È·ÈÏÉ¾³ı">
		</td>
	</tr>
	</table>
	</td>
</tr>
</form>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
}