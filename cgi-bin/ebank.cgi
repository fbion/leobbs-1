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
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/mpic.cgi";
require "data/cityinfo.cgi";
require "data/ebankinfo.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "ebank.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
#&ipbanned;
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else
{
	$boardurltemp =$boardurl;
	$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath = $boardurltemp;
	$cookiepath =~ s/\/$//;
}

$inmembername = $query->cookie("amembernamecookie") if (!$inmembername);
$inpassword = $query->cookie("apasswordcookie") if (!$inpassword);
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "å®¢äºº" ) #å¿…é¡»ç™»å½•æ‰èƒ½è®¿é—®é“¶è¡Œ
{
	&error("æ™®é€šé”™è¯¯&ä½ ç°åœ¨çš„èº«ä»½æ˜¯è®¿å®¢ï¼Œå¿…é¡»ç™»é™†ä»¥åæ‰èƒ½è®¿é—®é“¶è¡Œï¼");
}

else
{
	&getmember($inmembername);
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("æ™®é€šé”™è¯¯&å¯†ç ä¸ç”¨æˆ·åä¸ç›¸ç¬¦ï¼Œè¯·é‡æ–°ç™»å½•ï¼");
     }
	&error("æ™®é€šé”™è¯¯&æ­¤ç”¨æˆ·æ ¹æœ¬ä¸å­˜åœ¨ï¼") if ($userregistered eq "no");
}

$cleanmembername = $inmembername;
$cleanmembername =~ s/ /\_/sg;
$cleanmembername =~ tr/A-Z/a-z/;
$currenttime = time;

#é¿å…æ¶æ„ç”¨æˆ·åŒæ—¶æäº¤å¤šä¸ªäº¤æ˜“è¯·æ±‚é€ æˆçš„è´Ÿå€ºå­˜æ¬¾ç­‰ç°è±¡
$ebanklockfile = $lbdir . "lock/" . $cleanmembername . "_ebank.lck";
if (-e $ebanklockfile)
{
	&myerror("é“¶è¡Œé”™è¯¯&è¯·ä¸è¦åŒæ—¶åœ¨é“¶è¡Œè¿›è¡Œå¤šç¬”äº¤æ˜“ï¼") if ($currenttime < (stat($ebanklockfile))[9] + 3);
}
open(LOCKCALFILE, ">$ebanklockfile");
print LOCKCALFILE "1;";
close(LOCKCALFILE);
#ENDé˜²åˆ·

#ç”¨æˆ·é‡‘é’±
$myallmoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

#ä¾æ¬¡ä¸ºè´¦æˆ·çŠ¶æ€ï¼ˆç©ºå€¼ï¼šæœªå¼€æˆ·ï¼Œ1ï¼›æ­£å¸¸ï¼Œ-1ï¼šè´¦æˆ·å†»ç»“ï¼‰ï¼Œå­˜æ¬¾ï¼Œå­˜æ¬¾æ—¶é—´ï¼Œè´·æ¬¾ã€è´·æ¬¾æ—¶é—´ï¼Œè´·æ¬¾æŠµæŠ¼ç§¯åˆ†å€¼ï¼Œæœ€è¿‘æ•°æ¬¡äº¤æ˜“æ—¶é—´ï¼Œé¢„ç•™äº†äº”ä¸ªå˜é‡ä»¥ä¾¿ä»¥åå¼€å‘æ–°åŠŸèƒ½æ¯”å¦‚å®šæœŸå­˜æ¬¾ã€ç”¨æˆ·æ˜¯å¦ä¿å¯†è‡ªå·±çš„å­˜æ¬¾
($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
unless ($mystatus eq "1" || $mystatus eq "-1" || $ebankdata eq "")
{
	($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = "";
}
if ($mystatus)
{
	$mysavedays = &getbetween($mysavetime, $currenttime);
	$mysaveaccrual = int($mysaves * $banksaverate * $mysavedays);
	if ($myloan)
	{
		$myloandays = &getbetween($myloantime, $currenttime) + 1;
		if ($myloandays > $bankloanmaxdays)
		{#å¦‚æœè´·æ¬¾è¿‡æœŸ
			&dooutloan($cleanmembername);
			$myallmoney -= $myloan;
			$rating -= $myloanrating;
			$myloan = 0;
		}
		else
		{
			$myloanaccrual = int($myloan * $bankloanrate * $myloandays);
		}
	}
}		

#è‡ªåŠ¨å†»ç»“å‘è¨€è¢«å±è”½ç”¨æˆ·ã€ç¦è¨€ç”¨æˆ·ï¼ˆç›‘ç‹±ä¸­çš„çŠ¯äººå‰¥å¤ºé‡‘èæƒåˆ©ï¼Ÿ:Dï¼‰
$mystatus = -1 if (($membercode eq "banned" || $membercode eq "masked") && $mystatus == 1);

#æ£€æŸ¥è¿‡æœŸè´·æ¬¾
if (-e $lbdir . "ebankdata/allloan.cgi")
{
	&winlock($lbdir . "ebankdata/allloan.cgi") if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	open(FILE, $lbdir . "ebankdata/allloan.cgi");
	flock(FILE, 1) if ($OS_USED eq "Unix");
	@allloan = <FILE>;
	close(FILE);
	foreach (@allloan)
	{
		chomp;
		($loaner, $loantime) = split(/,/, $_);
		if (&getbetween($loantime, $currenttime) >= $bankloanmaxdays)
		{
			shift(@allloan);
			push(@outloan, $loaner);
		}
		else
		{
			last;
		}
	}
	if (@outloan)
	{
		open(FILE, ">" . $lbdir . "ebankdata/allloan.cgi");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@allloan)
		{
			chomp;
			print FILE $_ . "\n" if ($_);
		}
		close(FILE);
	}
	&winunlock($lbdir . "ebankdata/allloan.cgi") if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	foreach (@outloan)
	{
		&dooutloan($_);
	}
}
#Endè¿‡æœŸè´·æ¬¾

&title;
$action = $query->param('action');
my %Mode = (
	'changepass' => \&changepass,	#ä¿®æ”¹å–æ¬¾å¯†ç 
	'open' => \&open,     #å¼€æˆ·
	'logoff' => \&logoff, #é”€æˆ·
	'get' => \&get,       #å–æ¬¾
	'save' => \&save,     #å­˜æ¬¾
	'btrans' => \&btrans, #è½¬å¸
	'post' => \&post,     #æ±‡æ¬¾
	'loan' => \&loan,     #è´·æ¬¾
	'repay' => \&repay    #å¿è¿˜
	);

if ($Mode{$action})
{
	$Mode{$action} -> ();
}
else
{
	&display;             #è¥ä¸šå…
}

unlink($ebanklockfile); #è§£é™¤é”å®š

print header(-cookie=>[$onlineviewcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&output($pagetitle,\$output);
exit;

sub display #è¥ä¸šå…
{
	my $onlineview = $query->cookie("onlineview");
	$onlineview = 0 if ($onlineview eq "");
	$onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
	$onlineviewcookie = cookie(-name => "onlineview", -value => "$onlineview", -path => "$cookiepath/", -expires => "+30d");
	my $onlinetitle = $onlineview == 1 ? "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>å…³é—­è¯¦ç»†åˆ—è¡¨</font></a>]" : "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>æ˜¾ç¤ºè¯¦ç»†åˆ—è¡¨</font></a>]";

	#å–å¾—æ€»å­˜æ¬¾ä¿¡æ¯
	my $allusers = 0;
	my $allsaves = 0;
	if (-e $lbdir . "ebankdata/allsaves.cgi")
	{
		open(FILE, $lbdir . "ebankdata/allsaves.cgi");
		my $allinfo = <FILE>;
		close(FILE);
		chomp($allinfo);
		($allusers, $allsaves) = split(/,/, $allinfo);
	}

	#å–å¾—æ’åä¿¡æ¯
	my @maxusers;
	my @maxsaves;
	if (-e $lbdir . "ebankdata/order.cgi")
	{
		open(FILE, $lbdir . "ebankdata/order.cgi");
		my @orders = <FILE>;
		close(FILE);
		for ($i = 0; $i < @orders && $i < $bankmaxdisplay; $i++)
		{
			chomp($orders[$i]);
			($maxusers[$i], $maxsaves[$i]) = split(/\t/, $orders[$i]);
		}
	}

	my $banksave100rate = $banksaverate * 100;
	my $bankloan100rate = $bankloanrate * 100;
	my $banktrans100rate = $banktransrate * 100;
	my $bankpost100rate = $bankpostrate * 100;

	my $helpurl = &helpfiles("é“¶è¡Œ");
	$helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></span>~;

	my $freshtime = $query->cookie("freshtime");
	if ($freshtime ne "")
	{
		my $autofreshtime = $freshtime * 60 - 1;
		$autofreshtime = 60 if ($autofreshtime < 60);
		my $refreshnow = qq~<meta http-equiv="refresh" content="$autofreshtime;">~;
	}

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	unless(-e "$filetoopens.lck")
	{
		$screenmode = $query->cookie("screenmode");
		$screenmode = 8 if ($screenmode eq "");
		&whosonline("$inmembername\t$bankname\t$bankname\té“¶è¡Œè¥ä¸šå¤§å…");
		$membertongji =~ s/æœ¬åˆ†è®ºå›/$bankname/o;
		undef $memberoutput if ($onlineview != 1);
	}
	else
	{
		$memberoutput = "";
		$membertongji = " <b>ç”±äºæœåŠ¡å™¨ç¹å¿™ï¼Œæ‰€ä»¥é“¶è¡Œè¥ä¸šå¤§å…çš„åœ¨çº¿æ•°æ®æš‚æ—¶ä¸æä¾›æ˜¾ç¤ºã€‚</b>";
		$onlinetitle = "";
	}

	$output .= qq~$refreshnow
	<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=$navfontcolor><a href=leobbs.cgi>$boardname</a> â†’ $bankname</td><td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center><font face=$font color=$fontcolormisc><b>æ¬¢è¿å…‰ä¸´$banknameè¥ä¸šå¤§å…</b></font></td></tr>
<tr>
	<td bgcolor=$forumcolorone width=92%><font color=$titlefontcolor>$membertongjiã€€ $onlinetitle</td>
	<td bgcolor=$forumcolorone width=8% align=center><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 width=40 height=12></a></td>
</tr>~;
	$output .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><table cellPadding=1 cellSpacing=0 border=0>$memberoutput</table><script language="JavaScript"> function O9(id) {if(id != "") window.open("profile.cgi?action=show&member=" + id);}</script></td></tr>~ if ($onlineview == 1 && $memberoutput);
	my $waitress = int(&myrand(10)) + 1;
	$waitress = "$imagesurl/ebank/mm$waitress.gif";
	if ($bankgetpass ne "")
	{
		$promptpassword = qq~prompt("è¯·è¾“å…¥ä½ çš„å–æ¬¾å¯†ç :", "")~;
		$promptchange = "ä¿®æ”¹ä¸ªäººå–æ¬¾å¯†ç ";
	}
	else
	{
		$promptpassword = '1';
		$promptchange = "åˆ›å»ºä¸ªäººå–æ¬¾å¯†ç ";
	}
	$output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><br>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 border=0 width=100%>
<tr><td bgcolor=$forumcolortwo valign=middle colspan=2 align=center $catbackpic><font face=$font color=$fontcolormisc>
<script language="JavaScript" src="$imagesurl/ebank/fader.js"></script>
<script language="JavaScript" type="text/javascript">
prefix="";
arNews = ["$bankmessage", "", "<b><font color=#99ccff>å•ç¬”äº¤æ˜“é¢ï¼š æœ€ä½ <i>$bankmindeal</i> $moneynameï¼Œæœ€é«˜ <i>$bankmaxdeal</i> $moneynameã€€24å°æ—¶æœ€å¤§äº¤æ˜“æ¬¡æ•°ï¼š $bankmaxdaydo</font></b>", "", "<b><font color=#885200>å½“å‰å­˜æ¬¾æ—¥åˆ©ç‡ï¼š <i>$banksave100rate</i>%ã€€å½“å‰è´·æ¬¾æ—¥åˆ©ç‡ï¼š <i>$bankloan100rate</i>%ã€€è´·æ¬¾å¿è¿˜æœŸé™ï¼š <i>$bankloanmaxdays</i> å¤©ä»¥å†…</font></b>", "", "<b><font color=green>è½¬è´¦æ‰‹ç»­è´¹ç‡ï¼š <i>$banktrans100rate</i>%ã€€æ±‡æ¬¾æ‰‹ç»­è´¹ç‡ï¼š <i>$bankpost100rate</i>%ã€€(æœ€ä½ <i>$bankmindeal</i> $moneyname)</font></b>", ""];
</script>
<span id="elFader" style="position:relative;visibility:hidden; height:16" ></span></font>
</td></tr>
<tr>
	<td bgcolor=$miscbacktwo width=260 rowspan=4 valign=top>
		<table><tr><td><font face=$font color=$fontcolormisc><br>ã€€ç°ä»»è¡Œé•¿ï¼š <font color=#990000>$bankmanager</font><br><br>ã€€å®¢æˆ·æ•°é‡ï¼š $allusers<br><br>ã€€å­˜æ¬¾æ€»é¢ï¼š<br>ã€€ <font color=#000099><i>$allsaves</i></font> $moneyname<br></td><td width=40% align=center><img src=$waitress width=90 height=90 alt="è¿™æ˜¯æ­£åœ¨ç»™æ‚¨æœåŠ¡çš„å½“ç­è¥ä¸šå‘˜MM:)" OnClick="DoKiss()"></td></tr>
		<tr><td colspan=2><br>ã€€å½“å‰æ—¶é—´ï¼š <span id=showtime></span></td></tr>
<script language="JavaScript" src="$imagesurl/ebank/ebank.js">
</script>
<script language="JavaScript"><!--
displaytime();
function PromptGetPass(formname)
{
	var input = eval(formname + ".getpass");
	if (mypass = $promptpassword)
	{
		input.value = mypass;
		return true;
	}
	else
		return false;
}
function PromptLogOff()
{
	if (confirm('è¿™å°†æŠŠä½ æ‰€æœ‰çš„å­˜æ¬¾å’Œç´¯è®¡åˆ©æ¯åŠ åˆ°ä½ çš„ç°é‡‘ä¸Šï¼Œ\\nå¦‚æœä½ åœ¨æœ¬è¡Œæœ‰è´·æ¬¾ï¼Œå¿…é¡»å…ˆè¿˜è´·ä»¥åæ‰èƒ½é”€æˆ·ã€‚\\næ˜¯å¦çœŸçš„è¦é”€æˆ·ï¼Ÿ'))
		if (mypass = $promptpassword)
			location.href = "$thisprog?action=logoff&getpass=" + mypass;
}
function PromptChangePass()
{
	if (mypass = $promptpassword)
		if (newpass = prompt("è¯·è¾“å…¥æ–°çš„å–æ¬¾å¯†ç :", ""))
			if (newpass2 = prompt("è¯·å†æ¬¡è¾“å…¥æ–°çš„å–æ¬¾å¯†ç :", ""))
				if (newpass != newpass2) alert("ä¸¤æ¬¡è¾“å…¥çš„æ–°å¯†ç ä¸ä¸€è‡´ï¼");
				else location.href = "$thisprog?action=changepass&getpass=" + mypass + "&newpass=" + newpass;
}
--></script>~;

	if ($mystatus)
	{
		$output .= qq~<tr><td align=center colspan=2><br><table border=1 cellPadding=10 cellSpacing=3><tr><td style="line-height: 140%"><font color=#000066>ä¸ªäººè´¢åŠ¡çŠ¶å†µ</font>ã€€ã€€ã€€ã€€<a href=# OnClick="PromptChangePass()"><font color=blue>$promptchange</font></a><br>~;
		if ($mystatus == 1)
		{
			$output .= qq~<font color=green>è´¦æˆ·çŠ¶æ€ã€€ã€€ã€€ã€€ã€€ã€€æ­£å¸¸ä½¿ç”¨</font><br>~;
		}
		else
		{
			$output .= qq~<font color=red>è´¦æˆ·çŠ¶æ€ã€€ã€€ã€€ã€€ã€€ã€€æš‚æ—¶å†»ç»“</font><br>~;
		}
		$output .= qq~å½“å‰ç°é‡‘ã€€ã€€ã€€ã€€ã€€ã€€<i>$myallmoney</i> $moneyname<br>~;
		$output .= qq~æ´»æœŸå­˜æ¬¾ã€€ã€€ã€€ã€€ã€€ã€€<i>$mysaves</i> $moneyname<br>ç´¯è®¡æ—¶é—´å’Œåˆ©æ¯ã€€ã€€ã€€<i>$mysavedays</i> å¤©å…± <i>$mysaveaccrual</i> $moneyname<br>~;
		$output .= qq~<font color=#ff99cc>å½“å‰è´·æ¬¾ã€€ã€€ã€€ã€€ã€€ã€€<i>$myloan</i> $moneyname</font><br><font color=#ff99cc>ç´¯è®¡æ—¶é—´å’Œåˆ©æ¯ã€€ã€€ã€€<i>$myloandays</i> å¤©å…± <i>$myloanaccrual</i> $moneyname</font><br>~ if ($myloan);
		$output .= qq~</td></tr></table><br></td></tr>~;
	}
	$output .= qq~<tr><td colspan=2 align=center><a href=setbank.cgi><font color=blue>è¿›å…¥é“¶è¡Œç®¡ç†ä¸­å¿ƒ</font></a></td></tr>~ if (($membercode eq "ad" && $bankadminallow ne "manager") || ($membercode eq "smo" && $bankadminallow eq "all") || ",$bankmanager," =~ /,$inmembername,/i);
	$output .= qq~<tr><td colspan=2><hr width=250></td></tr><tr><td colspan=2 align=center><font color=#7700ff>$banknameæ°å‡ºå®¢æˆ·<br><br></font></td></tr><tr><td bgcolor=$titlecolor align=center>å®¢ æˆ· å¸ å·</td><td bgcolor=$titlecolor align=center>å½“ å‰ å­˜ æ¬¾</td></tr>~;

	for ($i = 1; $i <= @maxusers; $i++)
	{
		$output .= qq~<tr><td bgcolor=$miscbackone>ã€€$i. <a href=profile.cgi?action=show&member=~ . uri_escape($maxusers[$i - 1]) . qq~ target=_blank>$maxusers[$i - 1]</a></td><td bgcolor=$miscbackone>&nbsp;<i>$maxsaves[$i - 1]</i></td></tr>~;
	}
	$output .= qq~<tr><td colspan=2 align=center><br><br></td></tr></table></td>~;

	if ($bankopen ne "on")
	{
		$output .= qq~
	<td bgcolor=$miscbackone align=center><font color=red size=4><b>é“¶è¡Œç›˜ç‚¹ä¸­ï¼Œæš‚æ—¶åœä¸šï¼Œè¯·ç¨å€™è®¿é—®ï¼</b></font></td>
</tr>~;
	}

	else
	{
		unless ($mystatus)
		{
			$output .= qq~
	<td bgcolor=$miscbackone align=center><font size=4>ä½ å½“å‰æ‹¥æœ‰ <i>$myallmoney</i> $moneynameç°é‡‘ï¼Œ<br>å¼€æˆ·è‡³å°‘éœ€è¦ <i>$bankmindeal</i> $moneynameç°é‡‘æ‰èƒ½å®Œæˆã€‚<br><br>ä½ éœ€è¦<a href=$thisprog?action=open><font color=#0000ff><b>å¼€æˆ·</b></font></a>åæ‰èƒ½ä½¿ç”¨æœ¬è¡Œçš„å„é¡¹ä¸šåŠ¡ã€‚</font></td>
</tr>~;
		}

		elsif ($mystatus == -1)
		{
			if ($membercode eq "banned" || $membercode eq "masked")
			{
				$output .= qq~
	<td bgcolor=$miscbackone align=center><font size=4>ç”±äºä½ è¢«ç¦æ­¢å‘è¨€ï¼Œæ‰€ä»¥ä½ çš„è´¦å·è¢«é“¶è¡Œè‡ªåŠ¨å†»ç»“ã€‚</font></td>
</tr>~;
			}
			else
			{
				$output .= qq~
	<td bgcolor=$miscbackone align=center><font size=4>ç”±äºä½ è¿åäº†æŸäº›è§„å®šè¿›è¡Œéæ³•é‡‘èæ´»åŠ¨ï¼Œ<br>ä½ çš„è´¦å·è¢«è¡Œé•¿æš‚æ—¶å†»ç»“ï¼Œè¯·å°½å¿«ä¸å…¶è”ç³»ã€‚</font></td>
</tr>~;
			}
		}

		else
		{
			$output .= qq~
	<td bgcolor=$miscbackone valign=top>ã€€<img src="$imagesurl/ebank/bank.gif" width=16><font color=#99ccff>æ´»æœŸå‚¨è“„</font><img src="$imagesurl/ebank/bank.gif" width=16>ã€€ï¼‘å·æŸœå°ã€€ æœ¬æŸœå°åŒæ—¶å…¼åŠé”€æˆ·è¯·ç‚¹<a href=# OnClick="PromptLogOff()"><font color=#cc0000><b>è¿™é‡Œ</b></font></a><hr><br>
	<form name=save action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="save">ã€€ æˆ‘è¦å­˜å…¥ç°é‡‘:ã€€<input type=text size=10 name=savemoney> $moneynameã€€ã€€<input name=submit type=submit value=å­˜ã€€å…¥ style="background:#99ccff">ã€€<input name=reset type=reset value=é‡ã€€å¡« style="background:#cccccc"></form>
	<form name=get action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="get"><input type=hidden name=getpass>ã€€ æˆ‘è¦å–å‡ºå­˜æ¬¾:ã€€<input type=text size=10 name=getmoney> $moneynameã€€ã€€<input name=submit type=submit value=å–ã€€å‡º style="background:#99ccff" OnClick="return PromptGetPass('get')">ã€€<input name=reset type=reset value=é‡ã€€å¡« style="background:#cccccc"></form>
	</td>
</tr>
<tr>
	<td bgcolor=$miscbacktwo valign=top>ã€€<img src="$imagesurl/ebank/bank.gif" width=16><font color=green>è½¬å¸æ±‡æ¬¾</font><img src="$imagesurl/ebank/bank.gif" width=16>ã€€ï¼’å·æŸœå°ã€€ æœ¬æŸœå°åŒæ—¶å…¼åŠé”€æˆ·è¯·ç‚¹<a href=# OnClick="PromptLogOff()"><font color=#cc0000><b>è¿™é‡Œ</b></font></a><hr><br>~;

			if ($rating < $banktransneed && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" )
			{
				$output .= qq~ã€€ è¡Œé•¿è®¾å®šäº†åªæœ‰å¨æœ›è¾¾åˆ° $banktransneed ä»¥ä¸Šçš„ä¼šå‘˜å’Œç‰ˆä¸»æ‰èƒ½ä½¿ç”¨è½¬å¸å’Œæ±‡æ¬¾åŠŸèƒ½ï¼<br><br>~;
			}
			else
			{#å¥½å‹åˆ—è¡¨å¤„ç†éƒ¨åˆ†
				&getmyfriendlist;
				my $friendlist1 = qq~<select name=friends OnChange="btransfriend();"><option>æˆ‘çš„å¥½å‹</option>~;
				my $friendlist2 = qq~<select name=friends OnChange="postfriend();"><option>æˆ‘çš„å¥½å‹</option>~;
				foreach (@myfriendlist)
				{
					$friendlist1 .= qq~<option value="$_">$_</option>~;
					$friendlist2 .= qq~<option value="$_">$_</option>~;
				}
				$friendlist1 .= qq~</select>~;
				$friendlist2 .= qq~</select>~;

				$output .= qq~
	<form name=btrans action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="btrans"><input type=hidden name=getpass>ã€€ æˆ‘è¦è½¬å¸:ã€€<input type=text size=10 name=btransmoney> $moneynameã€€ç»™ã€€<input type=text size=12 name=btransuser>ã€€$friendlist1<br>ã€€ è½¬è´¦é™„è¨€:ã€€<input type=text size=30 maxsize=50 name=btransmessage>ã€€ã€€<input name=submit type=submit value=è½¬ã€€å‡º style="background:green" OnClick="return PromptGetPass('btrans')">ã€€<input name=reset type=reset value=é‡ã€€å¡« style="background:#cccccc"></form>
	<form name=post action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="post"><input type=hidden name=getpass>ã€€ æˆ‘è¦æ±‡æ¬¾:ã€€<input type=text size=10 name=postmoney> $moneynameã€€ç»™ã€€<input type=text size=12 name=postuser>ã€€$friendlist2<br>ã€€ æ±‡æ¬¾é™„è¨€:ã€€<input type=text size=30 maxsize=50 name=postmessage>ã€€ã€€<input name=submit type=submit value=æ±‡ã€€å‡º style="background:green" OnClick="return PromptGetPass('post')">ã€€<input name=reset type=reset value=é‡ã€€å¡« style="background:#cccccc"></form>~;
			}

			$output .= qq~</td>
</tr>
<tr>~;
			if ($myloan)
			{
				$output .= qq~
	<td bgcolor=$miscbackone valign=top>ã€€<img src="$imagesurl/ebank/bank.gif" width=16><font color=#ff7777>ç¤¾åŒºä¿¡è´·</font><img src="$imagesurl/ebank/bank.gif" width=16>ã€€ï¼“å·æŸœå°<hr><br>
	ã€€ å¿è¿˜ä½ çš„è´·æ¬¾è¯·<a href=$thisprog?action=repay><font color=#ff99cc>ç‚¹å‡»è¿™é‡Œ</font></a>ã€‚<br><br>
	</td>
</tr>~;
			}
			else
			{
				$output .= qq~<td bgcolor=$miscbackone valign=top>ã€€<img src="$imagesurl/ebank/bank.gif" width=16><font color=red>ç¤¾åŒºä¿¡è´·</font><img src="$imagesurl/ebank/bank.gif" width=16>ã€€ï¼“å·æŸœå°<hr><br>~;

				if ($bankallowloan eq "yes")
				{
					if ($rating > 0)
					{
						$output .= qq~<form name=loan action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="loan">ã€€ æˆ‘è¦æŠµæŠ¼ã€€ <select size=1 name=loanrate>~;
						for ($i = 1; $i <= $rating; $i++)
						{
							$output .= qq~<option value=$i>$i</option>~;
						}
						$output .= qq~</select>ã€€ç‚¹å¨æœ›æ¥è´·æ¬¾:ã€€<input type=text size=10 name=loanmoney> $moneynameã€€ã€€<input type=text size=1 style="width: 1px; height: 1px"><input name=submit type=submit value=å†³å®šäº† style="background:#ff7777"><br>ã€€ ( æ¯ç‚¹å¨æœ›å…è®¸æœ€å¤šæŠµæŠ¼ $bankrateloan $moneyname )</form>~;
					}
					else
					{
						$output .= qq~ã€€ ä½ æ²¡æœ‰å¨æœ›ç‚¹æ¥æŠµæŠ¼ï¼Œæ— æ³•è´·æ¬¾ï¼<br><br>~;
					}
				}
				else
				{
					$output .= qq~ã€€ è¡Œé•¿å·²ç»åœç”¨äº†è´·æ¬¾æœåŠ¡ï¼<br><br>~;
				}
				$output .= qq~</td></tr>~;
			}

			$output .= qq~<tr><td bgcolor=$miscbacktwo valign=top>ã€€<img src="$imagesurl/ebank/bank.gif" width=16><font color=#000066>ä¸ªäººè´¦ç›®</font><img src="$imagesurl/ebank/bank.gif" width=16>ã€€ä»¥ä¸‹æ˜¯ä½ æœ€è¿‘çš„é“¶è¡Œäº¤æ˜“è®°å½•ã€‚<hr>~;
			$output .= qq~<table border=1 width=100% bordercolor=#cccccc><tr><td align=center width=30%>äº¤æ˜“æ—¶é—´</td><td align=center width=30%>äº‹ä»¶</td><td align=center width=20%>é‡‘é¢($moneyname)</td><td align=center width=20%>ä½™é¢($moneyname)</td></tr>~;
			if (-e $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi")
			{
				open(FILE, $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi");
				my @mylogs = <FILE>;
				close(FILE);
				foreach (@mylogs)
				{
					chomp;
					my ($banktime, $bankaction, $banknums, $banksavenum) = split(/\t/, $_);
					$banktime = &dateformat($banktime + $timezone * 3600 + $timedifferencevalue * 3600);
					$output .= qq~<tr><td align=center>$banktime</td><td align=center>$bankaction</td><td align=center>$banknums</td><td align=center>$banksavenum</td></tr>~;
				}
			}
			$output .= qq~</table></td></tr>~;
		}
	}

	$output .= qq~
</table></td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	$pagetitle = "$boardname - $banknameè¥ä¸šå¤§å…";

	return;
}

sub changepass #ä¿®æ”¹å–æ¬¾å¯†ç 
{
	my $getpass = $query->param('getpass');
	my $newpass = $query->param('newpass');
	&myerror("é“¶è¡Œé”™è¯¯&ä½ æ²¡åœ¨æœ¬é“¶è¡Œå¼€è¿‡æˆ·ï¼Œå“ªæ¥çš„å–æ¬¾å¯†ç ï¼Ÿ") unless ($mystatus);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ è¾“å…¥çš„æ—§çš„å–æ¬¾å¯†ç é”™è¯¯ï¼") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ è¾“å…¥çš„æ–°çš„å–æ¬¾å¯†ç ä¸ºç©ºï¼Ÿ") if ($newpass eq "");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ è¾“å…¥çš„æ–°çš„å–æ¬¾å¯†ç å«æœ‰ä¸åˆé€‚çš„éæ³•å­—ç¬¦ï¼") if ($newpass =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]/is);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ è¾“å…¥çš„æ–°çš„å–æ¬¾å¯†ç å¤ªé•¿ï¼") if (length($newpass) > 16);
	&updateuserinfo($cleanmembername, 0, 0, "nochange", 0, "nochange", 0, "nochange", 0, "no", $newpass);
	&printjump("è®¾å®šå–æ¬¾å¯†ç æˆåŠŸ");
	return;
}

sub open #å¼€æˆ·
{
	&myerror("é“¶è¡Œé”™è¯¯&é“¶è¡Œç›˜ç‚¹ï¼Œæš‚æ—¶åœä¸šï¼Œæ— æ³•å¼€æˆ·ï¼") unless ($bankopen eq "on");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ å·²ç»åœ¨æœ¬é“¶è¡Œå¼€è¿‡æˆ·äº†ï¼") if ($mystatus);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ åœ¨24å°æ—¶å†…çš„äº¤æ˜“æ¬¡æ•°å·²ç»è¶…è¿‡äº†å…è®¸çš„æœ€å¤§å€¼ $bankmaxdaydoï¼")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ çš„ç°é‡‘ä¸å¤Ÿå¼€æˆ·æœ€ä½è¦æ±‚ï¼") if ($myallmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\tåœ¨é“¶è¡Œå¼€æˆ·") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, -$bankmindeal, 1, $bankmindeal, $currenttime, 0, "", 0, "yes");
	&updateallsave(1, $bankmindeal);

	&logpriviate("å¼€æˆ·", $bankmindeal, $bankmindeal);
	&logaction($inmembername, "å¼€æˆ·æˆåŠŸï¼Œå­˜å…¥ $bankmindeal $moneynameã€‚");

	&order($cleanmembername, $bankmindeal);
	&printjump("å¼€æˆ·æˆåŠŸ");
	return;
}

sub logoff #é”€æˆ·
{
	my $getpass = $query->param('getpass');
	&myerror("é“¶è¡Œé”™è¯¯&é“¶è¡Œç›˜ç‚¹ï¼Œæš‚æ—¶åœä¸šï¼Œæ— æ³•é”€æˆ·ï¼") unless ($bankopen eq "on");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ æ²¡åœ¨æœ¬é“¶è¡Œå¼€è¿‡æˆ·ï¼Œæ€ä¹ˆé”€æˆ·ï¼Ÿ") unless ($mystatus);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ çš„å¸æˆ·è¢«æš‚æ—¶å†»ç»“ï¼Œè¯·ä¸è¡Œé•¿è”ç³»ï¼") if ($mystatus == -1);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ è¾“å…¥çš„å–æ¬¾å¯†ç é”™è¯¯ï¼") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ åœ¨24å°æ—¶å†…çš„äº¤æ˜“æ¬¡æ•°å·²ç»è¶…è¿‡äº†å…è®¸çš„æœ€å¤§å€¼ $bankmaxdaydoï¼")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ å¿…é¡»å…ˆå¿è¿˜åœ¨æœ¬é“¶è¡Œçš„è´·æ¬¾åæ‰èƒ½é”€æˆ·ï¼") if ($myloan);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\tåœ¨é“¶è¡Œé”€æˆ·") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, $mysaves + $mysaveaccrual, "", -$mysaves, "", 0, "", 0, "yes");
	&updateallsave(-1, -$mysaves);

	my $filetodel = $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi";
	unlink($filetodel);

	&logaction($inmembername, "é”€æˆ·æˆåŠŸï¼Œå–èµ°å­˜æ¬¾ $mysaves $moneynameï¼Œç»“ç®—åˆ©æ¯ $mysaveaccrual $moneynameã€‚");

	&order($cleanmembername, 0);
	&printjump("é”€æˆ·æˆåŠŸ");
	return;
}

sub get #å–æ¬¾
{
	my $getmoney = $query->param('getmoney');
	my $getpass = $query->param('getpass');
	&myerror("é“¶è¡Œé”™è¯¯&é“¶è¡Œç›˜ç‚¹ï¼Œæš‚æ—¶åœä¸šï¼Œæ— æ³•å–æ¬¾ï¼") unless ($bankopen eq "on");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ æ²¡åœ¨æœ¬é“¶è¡Œå¼€è¿‡æˆ·ï¼Œæ€ä¹ˆå–æ¬¾ï¼Ÿ") unless ($mystatus);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ çš„å¸æˆ·è¢«æš‚æ—¶å†»ç»“ï¼Œè¯·ä¸è¡Œé•¿è”ç³»ï¼") if ($mystatus == -1);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ è¾“å…¥çš„å–æ¬¾å¯†ç é”™è¯¯ï¼") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ åœ¨24å°æ—¶å†…çš„äº¤æ˜“æ¬¡æ•°å·²ç»è¶…è¿‡äº†å…è®¸çš„æœ€å¤§å€¼ $bankmaxdaydoï¼")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("é“¶è¡Œé”™è¯¯&å–æ¬¾æ•°é¢è¾“å…¥é”™è¯¯ï¼Œè¯·æ£€æŸ¥ï¼") if ($getmoney =~ /[^0-9]/ or $getmoney eq "");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ æ²¡æœ‰é‚£ä¹ˆå¤šå­˜æ¬¾å¯ä»¥å–å‡ºï¼Œå¦‚æœä¸é”€æˆ·ï¼Œä½ çš„æˆ·å¤´å¿…é¡»è‡³å°‘å­˜æœ‰ $bankmindeal $moneynameï¼") if ($getmoney > $mysaves + $mysaveaccrual - $bankmindeal);
	&myerror("é“¶è¡Œé”™è¯¯&å–æ¬¾æ•°é¢è¶…è¿‡æœ¬è¡Œæœ€å¤§å•ç¬”äº¤æ˜“é¢ $bankmaxdeal $moneyname") if ($getmoney > $bankmaxdeal);
	&myerror("é“¶è¡Œé”™è¯¯&å–æ¬¾æ•°é¢å°äºæœ¬è¡Œæœ€å°å•ç¬”äº¤æ˜“é¢ $bankmindeal $moneyname") if ($getmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\tåœ¨é“¶è¡Œå–æ¬¾") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, $getmoney, "nochange", $mysaveaccrual - $getmoney, $currenttime, 0, "nochange", 0, "yes");
	&updateallsave(0, $mysaveaccrual - $getmoney);

	&logpriviate("ç»“æ¯", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
	&logpriviate("å–å‡º", -$getmoney, $mysaves + $mysaveaccrual - $getmoney);
	&logaction($inmembername, "<font color=#99ccff>å–å‡ºå­˜æ¬¾ $getmoney $moneynameï¼ŒåŒæ—¶ç»“ç®—åˆ©æ¯ $mysaveaccrual $moneynameã€‚</font>");

	&order($cleanmembername, $mysaves + $mysaveaccrual - $getmoney);
	&printjump("å–æ¬¾æˆåŠŸ");
	return;
}

sub save #å­˜æ¬¾
{
	my $savemoney = $query->param('savemoney');
	&myerror("é“¶è¡Œé”™è¯¯&é“¶è¡Œç›˜ç‚¹ï¼Œæš‚æ—¶åœä¸šï¼Œæ— æ³•å­˜æ¬¾ï¼") unless ($bankopen eq "on");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ æ²¡åœ¨æœ¬é“¶è¡Œå¼€è¿‡æˆ·ï¼Œæ€ä¹ˆå­˜æ¬¾ï¼Ÿ") unless ($mystatus);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ çš„å¸æˆ·è¢«æš‚æ—¶å†»ç»“ï¼Œè¯·ä¸è¡Œé•¿è”ç³»ï¼") if ($mystatus == -1);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ åœ¨24å°æ—¶å†…çš„äº¤æ˜“æ¬¡æ•°å·²ç»è¶…è¿‡äº†å…è®¸çš„æœ€å¤§å€¼ $bankmaxdaydoï¼")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("é“¶è¡Œé”™è¯¯&å­˜æ¬¾æ•°é¢è¾“å…¥é”™è¯¯ï¼Œè¯·æ£€æŸ¥ï¼") if ($savemoney =~ /[^0-9]/ or $savemoney eq "");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ æ²¡æœ‰é‚£ä¹ˆå¤šç°é‡‘å¯ä»¥å­˜ï¼") if ($savemoney > $myallmoney);
	&myerror("é“¶è¡Œé”™è¯¯&å­˜æ¬¾æ•°é¢è¶…è¿‡æœ¬è¡Œæœ€å¤§å•ç¬”äº¤æ˜“é¢ $bankmaxdeal $moneyname") if ($savemoney > $bankmaxdeal);
	&myerror("é“¶è¡Œé”™è¯¯&å­˜æ¬¾æ•°é¢å°äºæœ¬è¡Œæœ€å°å•ç¬”äº¤æ˜“é¢ $bankmindeal $moneyname") if ($savemoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\tåœ¨é“¶è¡Œå­˜æ¬¾") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, -$savemoney, "nochange", $mysaveaccrual + $savemoney, $currenttime, 0, "nochange", 0, "yes");
	&updateallsave(0, $mysaveaccrual + $savemoney);

	&logpriviate("ç»“æ¯", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
	&logpriviate("å­˜å…¥", $savemoney, $mysaves + $mysaveaccrual + $savemoney);
	&logaction($inmembername, "<font color=#99ccff>å­˜å…¥å­˜æ¬¾ $savemoney $moneynameï¼ŒåŒæ—¶ç»“ç®—åˆ©æ¯ $mysaveaccrual $moneynameã€‚</font>");

	&order($cleanmembername, $mysaves + $mysaveaccrual + $savemoney);
	&printjump("å­˜æ¬¾æˆåŠŸ");
	return;
}

sub btrans #è½¬å¸
{
	my $btransuser = $query->param('btransuser');
	my $btransmoney = $query->param('btransmoney');
	my $btransmessage = $query->param('btransmessage');
	my $getpass = $query->param('getpass');
	$btransuser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
	&myerror("é“¶è¡Œé”™è¯¯&é“¶è¡Œç›˜ç‚¹ï¼Œæš‚æ—¶åœä¸šï¼Œæ— æ³•è½¬å¸ï¼") unless ($bankopen eq "on");
	&myerror("é“¶è¡Œé”™è¯¯&ä½ æ²¡åœ¨æœ¬é“¶è¡Œå¼€è¿‡æˆ·ï¼Œæ€ä¹ˆè½¬å¸ï¼Ÿ") unless ($mystatus);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ çš„å¸æˆ·è¢«æš‚æ—¶å†»ç»“ï¼Œè¯·ä¸è¡Œé•¿è”ç³»ï¼") if ($mystatus == -1);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ è¾“å…¥çš„å–æ¬¾å¯†ç é”™è¯¯ï¼") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ åœ¨24å°æ—¶å†…çš„äº¤æ˜“æ¬¡æ•°å·²ç»è¶…è¿‡äº†å…è®¸çš„æœ€å¤§å€¼ $bankmaxdaydoï¼")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("é“¶è¡Œé”™è¯¯&è½¬è´¦é™„è¨€å¤ªé•¿äº†ï¼") if (length($btransmessage) > 50);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ çš„ä¿¡ç”¨åº¦ï¼ˆå¨æœ›ï¼‰ä¸å¤Ÿé«˜ï¼Œæ— æ³•ä½¿ç”¨è½¬å¸ä¸šåŠ¡ï¼") if ($rating < $banktransneed && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo");
	&myerror("é“¶è¡Œé”™è¯¯&è½¬å¸æ•°é¢è¾“å…¥é”™è¯¯ï¼Œè¯·æ£€æŸ¥ï¼") if ($btransmoney =~ /[^0-9]/ or $btransmoney eq "");
	my $banktranscharge = int($banktransrate * $btransmoney + 0.5); #å››èˆäº”å…¥:)
	$banktranscharge = $bankmindeal if ($banktranscharge < $bankmindeal);
	&myerror("é“¶è¡Œé”™è¯¯&ä½ æ²¡æœ‰é‚£ä¹ˆå¤šå­˜æ¬¾ç”¨æ¥è½¬å¸å’Œæ”¯ä»˜è½¬å¸è´¹ç”¨ï¼Œå¦‚æœä¸é”€æˆ·ï¼Œä½ çš„æˆ·å¤´å¿…é¡»è‡³å°‘å­˜æœ‰ $bankmindeal $moneynameï¼") if ($btransmoney + $banktranscharge > $mysaves + $mysaveaccrual - $bankmindeal);
	&myerror("é“¶è¡Œé”™è¯¯&è½¬å¸æ•°é¢è¶…è¿‡æœ¬è¡Œæœ€å¤§å•ç¬”äº¤æ˜“é¢ $bankmaxdeal $moneyname") if ($btransmoney > $bankmaxdeal);
	&myerror("é“¶è¡Œé”™è¯¯&è½¬å¸æ•°é¢å°äºæœ¬è¡Œæœ€å°å•ç¬”äº¤æ˜“é¢ $bankmindeal $moneyname") if ($btransmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&rn;
}

sub btrans #æme¸ø $btransuser£¬½»ÄÉÊÖĞø·Ñ $banktranscharge $moneyname£¬Í¬Ê±½áËã×ª³ö·½½áËãÀûÏ¢ $mysaveaccrual $moneyname£¬×ªÈë·½½áËãÀûÏ¢ $tmysaveaccrual $moneyname¡£×ªÕË¸½ÑÔ£º$btransmessage</font>");
	&printjump("×ªÕÊ³É¹¦");
	return;
}

sub post
{
	my $postuser = $query->param('postuser');
	my $postmoney = $query->param('postmoney');
	my $postmessage = $query->param('postmessage');
	my $getpass = $query->param('getpass');
	$postuser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
	&myerror("ÒøĞĞ´íÎó&ÒøĞĞÅÌµã£¬ÔİÊ±Í£Òµ£¬ÎŞ·¨»ã¿î£¡") unless ($bankopen eq "on");
	&myerror("ÒøĞĞ´íÎó&ÄãÃ»ÔÚ±¾ÒøĞĞ¿ª¹ı»§£¬ÔõÃ´»ã¿î£¿") unless ($mystatus);
	&myerror("ÒøĞĞ´íÎó&ÄãµÄÕÊ»§±»ÔİÊ±¶³½á£¬ÇëÓëĞĞ³¤ÁªÏµ£¡") if ($mystatus == -1);
	&myerror("ÒøĞĞ´íÎó&ÄãÊäÈëµÄÈ¡¿îÃÜÂë´íÎó£¡") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("ÒøĞĞ´íÎó&ÄãÔÚ24Ğ¡Ê±ÄÚµÄ½»Ò×´ÎÊıÒÑ¾­³¬¹ıÁËÔÊĞíµÄ×î´óÖµ $bankmaxdaydo£¡")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("ÒøĞĞ´íÎó&»ã¿î¸½ÑÔÌ«³¤ÁË£¡") if (length($postmessage) > 50);
	&myerror("ÒøĞĞ´íÎó&ÄãµÄĞÅÓÃ¶È£¨ÍşÍû£©²»¹»¸ß£¬ÎŞ·¨Ê¹ÓÃ»ã¿îÒµÎñ£¡") if ($rating < $banktransneed && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo");
	&myerror("ÒøĞĞ´íÎó&»ã¿îÊı¶îÊäÈë´íÎó£¬Çë¼ì²é£¡") if ($postmoney =~ /[^0-9]/ or $postmoney eq "");
	my $bankpostcharge = int($bankpostrate * $postmoney + 0.5); #ËÄÉáÎåÈë:)
	$bankpostcharge = $bankmindeal if ($bankpostcharge < $bankmindeal);
	&myerror("ÒøĞĞ´íÎó&ÄãÃ»ÓĞÄÇÃ´¶à´æ¿îÓÃÀ´»ã¿îºÍÖ§¸¶»ã¿î·ÑÓÃ£¬Èç¹û²»Ïú»§£¬ÄãµÄ»§Í·±ØĞëÖÁÉÙ´æÓĞ $bankmindeal $moneyname£¡") if ($postmoney + $bankpostcharge > $mysaves + $mysaveaccrual - $bankmindeal);
	&myerror("ÒøĞĞ´íÎó&»ã¿îÊı¶î³¬¹ı±¾ĞĞ×î´óµ¥±Ê½»Ò×¶î $bankmaxdeal $moneyname") if ($postmoney > $bankmaxdeal);
	&myerror("ÒøĞĞ´íÎó&»ã¿îÊı¶îĞ¡ÓÚ±¾ĞĞ×îĞ¡µ¥±Ê½»Ò×¶î $bankmindeal $moneyname") if ($postmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\tÔÚÒøĞĞ»ã¿î") unless(-e "$filetoopens.lck");

	$postuser =~ s/ /\_/sg;
	$postuser =~ tr/A-Z/a-z/;
	&myerror("ÒøĞĞ´íÎó&×Ô¼º¸ø×Ô¼º»ã¸öÊ²Ã´¿î£¡") if ($postuser eq $cleanmembername);
	$postmessage = &unHTML($postmessage);

	&getmember($postuser);
	&myerror("ÒøĞĞ´íÎó&»ã¿î¶ÔÏóÓÃ»§²»´æÔÚ£¡") if ($userregistered eq "no");

	&updateuserinfo($cleanmembername, 0, 0, "nochange", $mysaveaccrual - $postmoney - $bankpostcharge, $currenttime, 0, "nochange", 0, "yes");
	&updateuserinfo($postuser, 0, $postmoney, "nochange", 0, "nochange", 0, "nochange", 0, "no");
	&updateallsave(0, $mysaveaccrual - $postmoney - $bankpostcharge);	

	&bankmessage($postuser, "»ã¿îµ¥", "¡¡¡¡$inmembername ´Ó±¾ĞĞ¸øÄã»ã¼ÄÁË $postmoney $moneynameÏÖ½ğ£¬ÏÖÔÚÒÑ¾­µ½Î»£¬Çë²éÊÕ£¡<br>¡¡¡¡»ã¿î¸½ÑÔ£º<font color=green>$postmessage</font>¡£");

	&logpriviate("½áÏ¢", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
	&logpriviate("»ã¿îÊÖĞø·Ñ", -$bankpostcharge, $mysaves + $mysaveaccrual - $bankpostcharge);
	&logpriviate("»ã³öµ½$postuser", -$postmoney, $mysaves + $mysaveaccrual - $bankpostcharge - $postmoney);
	&logaction($inmembername, "<font color=green>¸øÓÃ»§ $postuser »ã¼ÄÁË$postmoney $moneyname£¬½»ÄÉÊÖĞø·Ñ $bankpostcharge $moneyname£¬Í¬Ê±½áËãÀûÏ¢ $mysaveaccrual $moneyname¡£»ã¿î¸½ÑÔ£º$postmessage</font>");

	&order($cleanmembername, $mysaves + $mysaveaccrual - $bankpostcharge - $postmoney);
	&printjump("»ã¿î³É¹¦");
	return;
}

sub loan #´û¿î
{
	my $loanrate = $query->param('loanrate');
	my $loanmoney = $query->param('loanmoney');
	&myerror("ÒøĞĞ´íÎó&ÒøĞĞÅÌµã£¬ÔİÊ±Í£Òµ£¬ÎŞ·¨´û¿î£¡") unless ($bankopen eq "on");
	&myerror("ÒøĞĞ´íÎó&ÄãÃ»ÔÚ±¾ÒøĞĞ¿ª¹ı»§£¬ÔõÃ´´û¿î£¿") unless ($mystatus);
	&myerror("ÒøĞĞ´íÎó&ÄãµÄÕÊ»§±»ÔİÊ±¶³½á£¬ÇëÓëĞĞ³¤ÁªÏµ£¡") if ($mystatus == -1);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("ÒøĞĞ´íÎó&ÄãÔÚ24Ğ¡Ê±ÄÚµÄ½»Ò×´ÎÊıÒÑ¾­³¬¹ıÁËÔÊĞíµÄ×î´óÖµ $bankmaxdaydo£¡")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("ÒøĞĞ´íÎó&´û¿î·şÎñÒÑ¾­±»ĞĞ³¤Í£ÓÃ£¡") if ($bankallowloan ne "yes");
	&myerror("ÒøĞĞ´íÎó&Äãµ±Ç°»¹ÓĞ´û¿îÃ»ÓĞ»¹Çå£¬²»ÔÊĞíĞÂµÄ´û¿î£¡") if ($myloan);
	&myerror("ÒøĞĞ´íÎó&µÖÑºÍşÍûÊäÈë´íÎó£¡") if ($loanrate =~ /[^0-9]/ or $loanrate eq "");
	&myerror("ÒøĞĞ´íÎó&µÖÑºÍşÍûÊäÈë´íÎó£¡") if ($loanrate == 0);
	&myerror("ÒøĞĞ´íÎó&ÄãÃ»ÓĞÕâÃ´¶àÍşÍûµãÊıÓÃÀ´µÖÑº£¡") if ($loanrate > $rating);
	&myerror("ÒøĞĞ´íÎó&´û¿î½ğ¶îÊäÈë´íÎó£¡") if ($loanmoney =~ /[^0-9]/ or $loanmoney eq "");
	&myerror("ÒøĞĞ´íÎó&ÓÃÀ´µÖÑº´û¿îÖµµÄÍşÍûµãÊı²»¹»£¡") if ($loanmoney > $bankrateloan * $loanrate);
	&myerror("ÒøĞĞ´íÎó&´û¿î½ğ¶î³¬¹ı±¾ĞĞ×î´óµ¥±Ê½»Ò×¶î $bankmaxdeal $moneyname") if ($loanmoney > $bankmaxdeal);
	&myerror("ÒøĞĞ´íÎó&´û¿î½ğ¶îĞ¡ÓÚ±¾ĞĞ×îĞ¡µ¥±Ê½»Ò×¶î $bankmindeal $moneyname") if ($loanmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\tÔÚÒøĞĞ´û¿î") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, $loanmoney, "nochange", 0, "nochange", $loanmoney, $currenttime, $loanrate, "yes");
	my $filetomake = $lbdir . "ebankdata/allloan.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">>$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "$cleanmembername,$currenttime\n";
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");

	&bankmessage($cleanmembername, "´û¿îÍ¨Öª", "¡¡¡¡ÄãÔÚ±¾ĞĞµÖÑºÁË $loanrate µãÍşÍû´û¿î $loanmoney $moneyname£¬ÏÖÔÚ´û¿îÒÑ¾­·¢·Åµ½ÄãµÄÏÖ½ğ£¬ÇëÔÚ´Ó½ñÌì¿ªÊ¼µÄ $bankloanmaxdays ÌìÒÔÄÚ¼°Ê±¹é»¹´û¿î£¬·ñÔòÓâÆÚÏµÍ³½«×Ô¶¯Ç¿ÖÆÊÕ»Ø´û¿î²¢ÇÒ¿Û³ıÄãµÖÑºµÄÍşÍû¡£");

	&logpriviate("´û¿î", $loanmoney, $mysaves);
	&logaction($inmembername, "<font color=#ff7777>ÏòÒøĞĞµÖÑºÁË $loanrate µãÍşÍûÉêÇëÁË $loanmoney $moneyname´û¿î£¬ÒÑ·¢·ÅÖÁÆäÏÖ½ğ¡£</font>");
	&printjump("´û¿î³É¹¦");
	return;
}

sub repay
{
	&myerror("ÒøĞĞ´íÎó&ÒøĞĞÅÌµã£¬ÔİÊ±Í£Òµ£¬ÎŞ·¨³¥»¹´û¿î£¡") unless ($bankopen eq "on");
	&myerror("ÒøĞĞ´íÎó&ÄãÃ»ÔÚ±¾ÒøĞĞ¿ª¹ı»§£¬»¹Ê²Ã´´û¿î£¿") unless ($mystatus);
	&myerror("ÒøĞĞ´íÎó&ÄãµÄÕÊ»§±»ÔİÊ±¶³½á£¬ÇëÓëĞĞ³¤ÁªÏµ£¡") if ($mystatus == -1);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("ÒøĞĞ´íÎó&ÄãÔÚ24Ğ¡Ê±ÄÚµÄ½»Ò×´ÎÊıÒÑ¾­³¬¹ıÁËÔÊĞíµÄ×î´óÖµ $bankmaxdaydo£¡")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("ÒøĞĞ´íÎó&ÄãÃ»ÓĞ´û¹ı¿î,»¹É¶£¿") unless ($myloan);
	&myerror("ÒøĞĞ´íÎó&ÄãµÄÏÖ½ğ²»¹»³¥»¹´û¿î£¡") if ($myallmoney < $myloan + $myloanaccrual);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\tÔÚÒøĞĞ»¹´û") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, -($myloan + $myloanaccrual), "nochange", 0, "nochange", -$myloan, "", -$myloanrating, "no");

	my $filetoopen = $lbdir . "ebankdata/allloan.cgi";
	if (-e $filetoopen)
	{
		&winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my @filedata = <FILE>;
		close(FILE);
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@filedata)
		{
			chomp;
			print FILE $_ . "\n" unless ($_ =~ /^$cleanmembername,/i);
		}
		close(FILE);
		&winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	}

	&logpriviate("»¹´û", $myloan + $myloanaccrual, $mysaves);
	&logaction($inmembername, "<font color=#ff7777>ÏòÒøĞĞ³¥»¹ÁË $myloan $moneyname´û¿î£¬Ö§¸¶ÀûÏ¢ $myloanaccrual $moneyname¡£</font>");
	&printjump("»¹´û³É¹¦");
	return;	
}

#####ÒÔÏÂÎª¹«ÓÃº¯Êı¶Î

sub order #ÒøĞĞÅÅĞò³ÌĞò
{
	my ($adduser1, $addsave1, $adduser2, $addsave2) = @_;
	my %ordersaves;

	my $filetoopen = $lbdir . "ebankdata/order.cgi";
	my $filetoopens = &lockfilename($filetoopen);
	return if (-e $filetoopens . ".lck");
	&winlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	if (-e $filetoopen)
	{
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		@orderdata = <FILE>;
		close(FILE);
	}
	foreach (@orderdata)
	{
		chomp;
		my ($tempuser, $tempsave) = split(/\t/, $_);
		$ordersaves{$tempuser} = $tempsave if ($tempuser ne "");
	}
	$ordersaves{$adduser1} = $addsave1 if ($adduser1 ne "");
	$ordersaves{$adduser2} = $addsave2 if ($adduser2 ne "");
	my @orderusers = sort {$ordersaves{$a}<=>$ordersaves{$b}} keys(%ordersaves);
	open(FILE, ">$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	for ($i = 1; $i <= $bankmaxdisplay * 2; $i++)
	{
		$j = @orderusers - $i;
		last if ($j < 0);
		print FILE $orderusers[$j] . "\t" . $ordersaves{$orderusers[$j]} . "\n" if ($ordersaves{$orderusers[$j]});
	}
	close(FILE);
	&winunlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	return;
}

sub getbetween #È¡µÃÁ½¸öÊ±¼äÖ®¼äÏà²îµÄÌìÊı£¨µ÷ÓÃ²ÎÊı£º¿ªÊ¼Ê±¼ä£¬½áÊøÊ±¼ä£©
{
	my ($begintime, $endtime) = @_;
	my ($tmpsecond, $tmpminute, $tmphour, $tmpday, $tmpmonth, $tmpyear, $tmpwday, $tmpyday, $tmpisdst) = localtime($begintime + $timezone * 3600);
	$begintime -= ($tmphour * 3600 + $tmpminute * 60 + $tmpsecond);
	my $betweendays = int(($endtime - $begintime) / 86400);
	return $betweendays;
}

sub getmyfriendlist #È¡µÃÓÃ»§ºÃÓÑÁĞ±í
{
	my $filetoopen = $lbdir . "memfriend/" . $cleanmembername . ".cgi";
	if (-e $filetoopen)
	{
		open(FILE, $filetoopen);
		@myfriendlist = <FILE>;
		close(FILE);
	}

	chomp(@myfriendlist);
	foreach (@myfriendlist)
	{
		s/^£ª£££¡£¦£ª//sg;
	}
	return;
}

sub bankmessage #¸øÓÃ»§·¢ÒøĞĞ¶ÌÏûÏ¢£¨µ÷ÓÃ²ÎÊı£ºÊÕÈ¡ÈË¡¢Ö÷Ìâ¡¢ÄÚÈİ£©
{
	my ($receivemember, $topic, $content) = @_;
	my @filedata;
	my $filetomake = $lbdir . $msgdir . "/in/" . $receivemember . "_msg.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	if (-e $filetomake)
	{
		open(FILE, $filetomake);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		@filedata = <FILE>;
		close(FILE);
	}

	@filedata = ("£ª£££¡£¦£ª$bankname\tno\t$currenttime\t$topic\t$content<br><br>¡¡¡¡¸ĞĞ»Ê¹ÓÃ$banknameµÄÓÅÖÊ·şÎñ¡£<br><br>\n", @filedata);

	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach (@filedata)
	{
		chomp;
		print FILE "$_\n";
	}
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	return;
}

sub logaction #¼ÇÂ¼ÒøĞĞÈÕÖ¾£¨µ÷ÓÃ²ÎÊı£º²Ù×÷ÈËÔ±£¬ÈÕÖ¾ÄÚÈİ£©
{
	my ($actionmember, $actionretail) = @_;

	my $filetomake = $lbdir . "ebankdata/alllogs.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">>$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "$actionmember\t$currenttime\t$actionretail\n";
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	return;
}

sub logpriviate #¼ÇÈë¸öÈË´æÕÛ£¨µ÷ÓÃ²ÎÊı£º½»Ò×¶¯×÷£¬½ğ¶î£¬»§Í·»îÆÚ½áÓà£©
{
	my ($bankaction, $banknums, $banksavenum) = @_;

	my $filetomake = $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi";
	my @mylogs;
	&winlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	if (-e $filetomake)
	{
		open(FILE, $filetomake);

		flock(FILE, 1) if ($OS_USED eq "Unix");
		@mylogs = <FILE>;
		close(FILE);
		while (@mylogs >= $banklogpriviate)
		{
			pop(@mylogs) ;
		}
	}
	@mylogs = ("$currenttime\t$bankaction\t$banknums\t$banksavenum", @mylogs);

	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach (@mylogs)
	{
		chomp;
		print FILE $_ . "\n";
	}
	close(FILE);
	&winunlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	return;
}

sub dooutloan #´¦ÀíÓÃ»§µÄ¹ıÆÚ´û¿î£¨µ÷ÓÃ²ÎÊı£ºÓÃ»§Ãû£©
{
	my $loaner = shift;

	my $namenumber = &getnamenumber($loaner);
	&checkmemfile($loaner,$namenumber);
	my $filetoopen = "$lbdir$memdir/$namenumber/$loaner.cgi";
	if (-e $filetoopen)
	{
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $filedata = <FILE>;
		close(FILE);
		chomp($filedata);
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

		if ($mystatus && $myloan)
		{
			$mesloan = $myloan;
			$mesloantime = $myloantime;
			$mesloanrating = $myloanrating;
			$mymoney -= $myloan;
			$rating -= $myloanrating;
			$myloan = 0;
			$myloantime = "";
			$myloanrating = 0;
		}

		$rating = -5 if ($rating < -5);
		$rating = $maxweiwang if ($rating > $maxweiwang);
		$ebankdata = "$mystatus,$mysaves,$mysavetime,$myloan,$myloantime,$myloanrating,$mybankdotime,$bankgetpass,$bankadd2,$bankadd3,$bankadd4,$bankadd5";

		if (($membername ne "") && ($password ne ""))
		{
			if (open(FILE, ">$filetoopen"))
			{
				flock(FILE, 2) if ($OS_USED eq "Unix");
				$lastgone = time;
				print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
				close(FILE);
			}
		}
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
	}

	if ($mesloan)
	{
		$mesloantime = &shortdate($mesloantime);
		&logaction("<font color=red>ÒøĞĞ×Ô¶¯´¦Àí³ÌĞò</font>", "<font color=red>$loaner ÓÚ $mesloantime µÖÑº $mesloanrating µãÍşÍû½è´û $mesloan $moneynameÓâÆÚ£¬ÒÑ¿Û³ıµÖÑºÍşÍû£¬²¢ÇÒÇ¿ÖÆ×·»Ø´û¿î¡£</font>");
		&bankmessage($loaner, "´û¿îÓâÆÚ²»»¹Í¨Öª", "¡¡¡¡ÄãÓÚ $mesloantime ÔÚ±¾ĞĞµÖÑº $mesloanrating µãÍşÍû½è´ûµÄ $mesloan $moneyname¿îÏîÓâÆÚÎ´»¹£¬±¾ĞĞÒÑ°´ÕÕÂÛÌ³ÒøĞĞ·¨¿Û³ıÄãµÖÑºµÄÍşÍûÖµ¡£<br>¡¡¡¡Í¬Ê±ÄãµÄ²»Á¼´û¿îÒ²±»Ç¿ÖÆ×·»Ø£¬¶Ô´ËÊÂ¼ş£¬ÎÒÃÇÉî±íÒÅº¶£¡<br><br>");
	}
	return;
}

sub printjump #ÏÔÊ¾LB·ç¸ñÌø×ªÒ³Ãæ£¨µ÷ÓÃ²ÎÊı£ºÒ³ÃæÖ÷Ìâ£©
{
	my $content = shift;

	$output .= qq~
	<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=$navfontcolor><a href=leobbs.cgi>$boardname</a> ¡ú <a href=ebank.cgi>$bankname</a> ¡ú $content</td><td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellPadding=6 cellSpacing=1 border=0 width=100%>
	<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>¸ĞĞ»Ñ¡ÔñÎÒÃÇµÄÓÅÖÊ·şÎñ£¬Äã¸Õ²ÅÔÚÒøĞĞµÄ½»Ò×ÒÑ¾­ÉúĞ§£¡</b></font></td></tr>
	<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡£º
		<ul><li><a href=$thisprog>·µ»ØÒøĞĞÓªÒµ´óÌü</a>  $pagestoshow</ul>
	</td></tr>
</table></td></tr>
</table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	$pagetitle = "$boardname - ÔÚÒøĞĞ$content";
	return;
}

sub updateallsave #ÀûÓÃ±ä»¯Á¿À´¸üĞÂ×ÜÁ¿ĞÅÏ¢
{
	my ($callusers, $callsaves) = @_;

	my $filetoopen = $lbdir . "ebankdata/allsaves.cgi";
	my $allusers = 0;
	my $allsaves = 0;
	&winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	if (-e $filetoopen)
	{
		open(FILE, $lbdir . "ebankdata/allsaves.cgi");
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $allinfo = <FILE>;
		close(FILE);
		chomp($allinfo);
		($allusers, $allsaves) = split(/,/, $allinfo);
	}

	$allusers += $callusers;
	$allsaves += $callsaves;

	if (open(FILE, ">$filetoopen"))
	{
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$allusers,$allsaves";
		close(FILE);
	}
	&winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	return;
}

sub updateuserinfo #¸üĞÂÓÃ»§ĞÅÏ¢
{
	my ($nametocheck, $crating, $cmoney, $bankstats, $csaves, $savetime, $cloan, $loantime, $cloanrating, $allowcount, $newgetpass) = @_;
	#ÓÃ»§Ãû£¬ÍşÍû±ä»¯Á¿£¬½ğÇ®±ä»¯Á¿£¬¸üĞÂµÄÒøĞĞÕË»§×´Ì¬(²»±ä»¯ÇëÌî"nochange")£¬´æ¿î±ä»¯Á¿£¬¸üĞÂµÄ´æ¿îÊ±¼ä(²»±ä»¯ÇëÌî"nochange")£¬´û¿î±ä»¯Á¿£¬¸üĞÂµÄ´û¿îÊ±¼ä(²»±ä»¯ÇëÌî"nochange")£¬´û¿îµÖÑºÖµ±ä»¯Á¿£¬ÊÇ·ñ¼ÆÈëÒøĞĞ½»Ò×´ÎÊı£¨¼ÆÈëÎª"yes", ²»¼ÆÈëÎª"no"£©
	my $namenumber = &getnamenumber($nametocheck);
	&checkmemfile($nametocheck,$namenumber);

	my $filetoopen = "$lbdir$memdir/$namenumber/$nametocheck.cgi";
	if (-e $filetoopen)
	{
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, "+<$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		my $filedata = <FILE>;
		chomp($filedata);
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

		if ($allowcount eq "yes")
		{
			my @mybankdotimes = split(/\|/, $mybankdotime);
			@mybankdotimes = ($currenttime, @mybankdotimes);
			$mybankdotime = "";
			for (my $i = 0; $i < $bankmaxdaydo; $i++)
			{
				last if ($i == @mybankdotimes);
				$mybankdotime .= $mybankdotimes[$i] . "|";
			}
			chop($mybankdotime);
		}

		$rating += $crating;
		$mymoney += $cmoney;
		$mystatus = $bankstats if ($bankstats ne "nochange");
		$mysaves = 0 unless($mysaves);
		$mysaves += $csaves;
		$mysavetime = $savetime if ($savetime ne "nochange");
		$myloan = 0 unless($myloan);
		$myloan += $cloan;
		$myloantime = $loantime if ($loantime ne "nochange");
		$myloanrating = 0 unless($myloanrating);
		$myloanrating += $cloanrating;
		$bankgetpass = $newgetpass if ($newgetpass ne "");

		$ebankdata = "$mystatus,$mysaves,$mysavetime,$myloan,$myloantime,$myloanrating,$mybankdotime,$bankgetpass,$bankadd2,$bankadd3,$bankadd4,$bankadd5";

		if (($membername ne "") && ($password ne ""))
		{
			seek(FILE,0,0);
#			$lastgone = $currenttime;
			print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
			close(FILE);
			
		      if (open(FILE,">$lbdir$memdir/old/$nametocheck.cgi")) {
#			$lastgone = $currenttime;
			print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
			close(FILE);
		      }
		} else {
		    close(FILE);
		}
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
		unlink ("${lbdir}cache/myinfo/$nametocheck.pl");
		unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
	}
	return;
}

sub myerror
{
	my $errorinfo = shift;
	unlink($ebanklockfile);
	&error($errorinfo);
	return;
}
