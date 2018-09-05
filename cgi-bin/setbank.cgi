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
require "data/ebankinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";

$|++;
$thisprog = "setbank.cgi";
$query = new LBCGI;
#&ipbanned;

$action = $query->param('action');
if ($action eq "login")
{
	$inmembername = $query->param("membername");
	$inpassword = $query->param("password");
	$inpasswordtemp = $inpassword;
	if ($inpassword ne "") {
	    eval {$inpassword = md5_hex($inpassword);};
	    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
	    unless ($@) {$inpassword = "lEO$inpassword";}
	}
	&checkverify;
	my $tempmembername = uri_escape($inmembername);
	print "Set-Cookie: adminname=$tempmembername\n";
	print "Set-Cookie: adminpass=$inpassword\n";
}
else
{
	$inmembername = $query->cookie("adminname");
	$inpassword = $query->cookie("adminpass");
}
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
&getmember($inmembername,"no");
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

if (($membercode eq "ad" || ($membercode eq "smo" && $bankadminallow eq "all") || ",$bankmanager," =~ /,$inmembername,/i) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername)))
{
	my %Mode = (
		'setinfo' => \&setinfo,     #è®¾å®šé“¶è¡Œå„é¡¹ä¸šåŠ¡æŒ‡æ ‡
		'setok' => \&setok,         #ä¿å­˜è®¾å®š
		'editmem' => \&editmem,     #ç¼–è¾‘ä¸€ä¸ªç”¨æˆ·çš„å­˜è´·æ¬¾
		'editok' => \&editok,       #ä¿å­˜ç¼–è¾‘å€¼
		'empty' => \&empty,         #æ¸…ç©ºé“¶è¡Œäº¤æ˜“æ—¥å¿—
		'deletelog' => \&deletelog, #åˆ é™¤æŒ‡å®šæ—¥å¿—
		'repair' => \&repair,       #ä¿®å¤é“¶è¡Œæ˜¾ç¤ºæ€»é‡
		'viewloan' => \&viewloan,   #æŸ¥çœ‹è´·æ¬¾æ¸…å•
		'bonus' => \&bonus,         #ç»™ä¼šå‘˜å‘çº¢åŒ…
		'bonusok' => \&bonusok
		);

	if ($Mode{$action})
	{
		$Mode{$action} -> ();
	}
	else
	{
		&showlog;
	}
	print $output;
}
 
else
{
	my $ipaddress = $ENV{'REMOTE_ADDR'};
	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
	$trueipaddress = $ENV{'HTTP_CLIENT_IP'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
	&logaction($inmembername, "<b>ä» $ipaddress ä»¥å¯†ç  $inpasswordtemp ç™»å½•è¡Œé•¿åŠå…¬å®¤å¤±è´¥ã€‚</b>") if ($inmembername && $inpassword);	
	&ebankadminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;

sub viewloan
{
	open(FILE, $lbdir . "ebankdata/allloan.cgi");
	my @loaninfo = <FILE>;
	close(FILE);
	
	$output = qq~<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=4><font color=#ffffff><b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / é“¶è¡Œè¡Œé•¿åŠå…¬å®¤</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=4>ã€€<a href=$thisprog>è¿” å›</a>  >> æŸ¥çœ‹è´·æ¬¾æ¸…å•ï¼š</td>
</tr>
<tr>
	<td bgcolor=#eeeeee align=center width=20%>è´·æ¬¾äºº</td>
	<td bgcolor=#eeeeee align=center width=40%>è´·æ¬¾æ—¥æœŸ</td>
	<td bgcolor=#eeeeee align=center width=20%>è´·æ¬¾æ•°é¢</td>
	<td bgcolor=#eeeeee align=center width=20%>æŠµæŠ¼å¨æœ›</td>
</tr>~;

	foreach (@loaninfo)
	{
		chomp;
		my ($loaner, $loantime) = split(/,/, $_);
		my $namenumber = &getnamenumber($loaner);
		&checkmemfile($loaner,$namenumber);
		my $loanfile = "$lbdir$memdir/$namenumber/$loaner.cgi";
		if (-e $loanfile)
		{
			open(FILE, $loanfile);
			my $filedata = <FILE>;
			close(FILE);
		
			my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
			my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
			$loantime = &shortdate($loantime);
		
			$output .= qq~<tr>
	<td bgcolor=#ffffff align=center><a href=profile.cgi?action=show&member=~ . uri_escape($loaner) . qq~ target=_blank>$membername</a></td>
	<td bgcolor=#ffffff align=center>$loantime</td>
	<td bgcolor=#ffffff align=center>$myloan</td>
	<td bgcolor=#ffffff align=center>$myloanrating</td>
</tr>~;
		}
	}
	$output .= "</table>";	

	return;	
}

sub bonusok
{
	my $step = $query->param('step');
	$step = 1 if ($step eq "");
	my $bonusmem = $query->param('bonusmem');

	for ("bonustarget", "bonusday", "bonuspost", "bonusnum", "bonusreason")
	{
		${$_} = &cleaninput($query->param($_));
	}
	&seterror("çº¢åŒ…å¯¹è±¡é™„åŠ è¦æ±‚è¾“å…¥æœ‰è¯¯ï¼") if ($bonusday =~ /[^0-9]/ || $bonuspost =~ /[^0-9]/);
	&seterror("æ²¡æœ‰è¾“å…¥çº¢åŒ…çš„æ•°é¢æˆ–è€…è¾“å…¥æœ‰è¯¯ï¼") if ($bonusnum !~ /^[0-9]+$/);
	&seterror("å¿…é¡»è¾“å…¥å‘çº¢åŒ…çš„ç†ç”±ï¼") if ($bonusreason eq "");

	opendir(DIR, "$lbdir$memdir/old");
	my @memberfiles = readdir(DIR);
	close(DIR);
	@memberfiles = grep(/\.cgi$/i, @memberfiles);

	my $currenttime = time;
	for ($i = ($step - 1) * 200; $i < $step * 200 && $i < @memberfiles; $i++)
	{
		&winunlock($lastfile) if (($OS_USED eq "Unix" || $OS_USED eq "Nt") && $lastfile ne "");
		($nametocheck,$no) = split (/\./,$memberfiles[$i]);
		my $namenumber = &getnamenumber($nametocheck);
		&checkmemfile($nametocheck,$namenumber);
		$lastfile = $lbdir . $memdir . "/$namenumber/" . $memberfiles[$i];
		&winlock($lastfile) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");
		open(FILE, $lastfile);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $filedata = <FILE>;
		close(FILE);
		
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
		my ($numberofposts, $numberofreplys) = split(/\|/, $numberofposts);

		next if ($membercode eq "banned" || $membercode eq "masked");
		next if ($bonustarget ne "all" && $mystatus != 1);
		next if ($bonusday ne "" && $currenttime - $joineddate < $bonusday * 86400);
		next if ($bonuspost ne "" && $numberofposts + $numberofreplys < $bonuspost);

		$mymoney += $bonusnum;
		open(FILE, ">$lastfile");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
		close(FILE);
		&winunlock($lastfile) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");
		$bonusmem++;
	        unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
		unlink ("${lbdir}cache/myinfo/$nametocheck.pl");

		$lastfile = $memberfiles[$i];
		$lastfile =~ s/\.cgi$//isg;
		&bankmessage($lastfile, "<font color=red>çº¢åŒ…é€šçŸ¥</font>", "ã€€ã€€$inmembername ä»¥$bonusreasonçš„ç†ç”±ï¼Œç»™æ‚¨å‘äº† $bonusnum $moneynameçš„çº¢åŒ…ï¼Œè¯·æŸ¥æ”¶æ‚¨çš„ç°é‡‘ã€‚");
		$lastfile = "";
	}
	&winunlock($lastfile) if (($OS_USED eq "Unix" || $OS_USED eq "Nt") && $lastfile ne "");

	if ($i < @memberfiles - 1)
	{
		#ç»§ç»­ä¸‹ä¸€æ­¥
		$step++;
		$output = qq~<form name=MAINFORM action=$thisprog?step=$step method=POST>
<input type=hidden name=action value=bonusok>
<input type=hidden name=step value=$step>
<input type=hidden name=bonustarget value="$bonustarget">
<input type=hidden name=bonusmem value="$bonusmem">
<input type=hidden name=bonusday value="$bonusday">
<input type=hidden name=bonuspost value="$bonuspost">
<input type=hidden name=bonusnum value="$bonusnum">
<input type=hidden name=bonusreason value="$bonusreason">
</form>
<script language="JavaScript">
setTimeout("MAINFORM.submit()", 1000);
</script>
ã€€å¦‚æœä½ çš„æµè§ˆå™¨æ²¡æœ‰è‡ªåŠ¨å‰è¿›ï¼Œè¯·<a href="javascript: MAINFORM.submit()">ç‚¹å‡»ç»§ç»­</a>~;
	}
	else
	{
		$bonustarget = $bonustarget eq "all" ? "æ‰€æœ‰æ³¨å†Œä¼šå‘˜" : "æ‰€æœ‰é“¶è¡Œå®¢æˆ·";
		$bonusday = "æ³¨å†Œ $bonusday å¤©ä»¥ä¸Š" if ($bonusday ne "");
		$bonuspost = "å‘å¸– $bonuspost ç¯‡ä»¥ä¸Š" if ($bonuspost ne "");
		$bonusday = $bonusday ne "" && $bonuspost ne "" ? "$bonusdayä¸”$bonuspostçš„" : $bonusday ne "" || $bonuspost ne "" ? "$bonusday$bonuspostçš„" : "";
		&logaction($inmembername, "<font color=red>ä»¥$bonusreasonçš„ç†ç”±ç»™$bonusday$bonustargetå‘äº†æ€»å…± $bonusmem ä¸ª $bonusnum $moneyname çš„çº¢åŒ…ã€‚");
		$output = qq~
<table width=100% cellpadding=6 cellspacing=0>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / é›·å‚²é“¶è¡Œè¡Œé•¿åŠå…¬å®¤</b></td></tr>
<tr><td align=center><br><b><font color=red>ç»™$bonusday$bonustargetçš„çº¢åŒ…å‘æ”¾å®Œæˆï¼Œæ€»å…±å‘å‡ºçº¢åŒ… $bonusmem ä¸ª!</font></b></td></tr>
</table>~;
	}
	return;
}

sub repair
{
	my $step = $query->param('step');
	$step = 1 unless ($step);

	my %ordersaves;
	if ($step == 1)
	{
		&setbankonoff("off");
		unlink($lbdir . "ebankdata/allsaves.cgi");
		unlink($lbdir . "ebankdata/allloan.cgi");
		unlink($lbdir . "ebankdata/order.cgi");
		unlink(&lockfilename($lbdir . "ebankdata/order.cgi") . ".lck");
	}
	else
	{
		#è¯»å–å·²æœ‰æ’åºç»“æœ
		open(FILE, $lbdir . "ebankdata/order.cgi");
		my @orderdata = <FILE>;
		close(FILE);
		foreach (@orderdata)
		{
			chomp;
			my ($tempuser, $tempsave) = split(/\t/, $_);
			$ordersaves{$tempuser} = $tempsave if ($tempuser ne "");
		}
	}
	opendir(DIR, "${lbdir}ebankdata/log");
	my @memberfiles = readdir(DIR);
	close(DIR);
	@memberfiles = grep(/\.cgi$/i, @memberfiles);

	my $stepusers = 0;
	my $stepsaves = 0;
	for ($i = ($step - 1) * 200; $i < $step * 200 && $i < @memberfiles; $i++)
	{
		($nametocheck,$no) = split(/\./,$memberfiles[$i]);
		my $namenumber = &getnamenumber($nametocheck);
		&checkmemfile($nametocheck,$namenumber);
		my $filetoopen = $lbdir . $memdir . "/$namenumber/" . $memberfiles[$i];
		open(FILE, $filetoopen);
		my $filedata = <FILE>;
		close(FILE);
		
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
		
		if ($mystatus)
		{
			$membername =~ s/ /\_/sg;
			$membername =~ tr/A-Z/a-z/;
			$stepusers++;
			$stepsaves += $mysaves;
			$ordersaves{$membername} = $mysaves;
			if ($myloan)
			{
				my $filetomake = $lbdir . "ebankdata/allloan.cgi";
				&winlock($filetomake) if ($OS_USED eq "Nt");
				open(FILE, ">>$filetomake");
				flock(FILE, 2) if ($OS_USED eq "Unix");
				print FILE "$membername,$myloantime\n";
				close(FILE);
				&winunlock($filetomake) if ($OS_USED eq "Nt");
			}
		}
	}
	&updateallsave($stepusers, $stepsaves);
	#å°†æœ¬æ¬¡æ’åºå’Œå·²æœ‰æ’åºç»“æœç»¼åˆ
	my @orderusers = sort {$ordersaves{$a}<=>$ordersaves{$b}} keys(%ordersaves);
	open(FILE, ">" . $lbdir . "ebankdata/order.cgi");
	for ($k = 1; $k <= $bankmaxdisplay * 2; $k++)
	{
		$j = @orderusers - $k;
		last if ($j < 0);
		print FILE $orderusers[$j] . "\t" . $ordersaves{$orderusers[$j]} . "\n" if ($ordersaves{$orderusers[$j]});
	}
	close(FILE);

	if ($i < @memberfiles - 1)
	{
		#ç»§ç»­ä¸‹ä¸€æ­¥
		$step++;
		$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog?action=repair&step=$step"><br>ã€€å¦‚æœä½ çš„æµè§ˆå™¨æ²¡æœ‰è‡ªåŠ¨å‰è¿›ï¼Œè¯·<a href=$thisprog>ç‚¹å‡»ç»§ç»­</a>~;
	}
	else
	{
		#è´·æ¬¾è®°å½•å¿…é¡»æ’åºå­˜æ”¾
		my $filetomake = $lbdir . "ebankdata/allloan.cgi";
		open(FILE, $filetomake);
		my @loaninfo = <FILE>;
		close(FILE);
		my %loantimes;
		foreach (@loaninfo)
		{
			chomp;
			my ($loaner, $loantime) = split(/,/, $_);
			$loantimes{$loaner} = $loantime if ($loaner ne "");
		}
		
		my @loaners = sort {$loantimes{$a}<=>$loantimes{$b}} keys(%loantimes);
		
		&winlock($filetomake) if ($OS_USED eq "Nt");
		open(FILE, ">$filetomake");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@loaners)
		{
			print FILE $_ . "," . $loantimes{$_} . "\n";
		}
		close(FILE);
		&winunlock($filetomake) if ($OS_USED eq "Nt");

		&setbankonoff("on");
		$output = qq~
<table width=100% cellpadding=6 cellspacing=0>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / é›·å‚²é“¶è¡Œè¡Œé•¿åŠå…¬å®¤</b></td></tr>
<tr><td align=center><br><b>æ€»é‡æ˜¾ç¤ºä¿®å¤å®Œæˆ!</b></td></tr>
</table>~;
	}

	return;
}

sub showlog
{
	my $page = $query->param('page');
	$page = 1 unless ($page);
	my $type = $query->param('type');
	$type = "name" unless($type eq "key" || $type eq "time");
	my $key = $query->param('key');

	open(FILE, $lbdir . "ebankdata/alllogs.cgi");
	my @ebanklogs = <FILE>;
	close(FILE);

	if ($key ne "")
	{#é€‰å‡ºæŒ‡å®šçºªå½•
		if ($type eq "name")
		{
			$key =~ s/ /\_/sg;
			@ebanklogs = grep(/^$key\t.+\t.+$/i, @ebanklogs);
		}
		elsif ($type eq "time")
		{
			my ($begin, $end);
			for ($begin = 0; $begin < @ebanklogs; $begin++)
			{
				my ($temp1, $temptime, $temp2) = split(/\t/, $ebanklogs[$begin]);
				$temptime = &shortdate($temptime + $timezone * 3600 + $timedifferencevalue * 3600);
				last if ($key eq $temptime);
			}
			for ($end = @ebanklogs - 1; $end >= $begin - 1; $end--)
			{
				my ($temp1, $temptime, $temp2) = split(/\t/, $ebanklogs[$end]);
				$temptime = &shortdate($temptime + $timezone * 3600 + $timedifferencevalue * 3600);
				last if ($key eq $temptime);
			}
			if ($begin > $end)
			{
				undef(@ebanklogs);
			}
			else
			{
				@ebanklogs = @ebanklogs[$begin..$end];
			}
		}
		else
		{
			@ebanklogs = grep(/^.+\t.+\t.*$key.*$/i, @ebanklogs);
		}
	}

	my $allpages = int(@ebanklogs / 25) + 1;
	$page = 1 if ($page < 1);
	$page = $allpages if ($page > $allpages);
	my $showpage = "";
	if ($allpages > 1)
	{
		$showpage .= qq~è®°å½•å…± <b>$allpages</b> é¡µ ~;
		$i = $page - 1;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();" title="ä¸Šä¸€é¡µ"><<</span> ~ if ($i > 0);
		$showpage .= "[ ";
		$i = $page - 3;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">â†</span> ~ if ($i > 0);
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i > 0);
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i > 0);
		$i++;
		$showpage .= qq~<font color=#990000>$i</font> ~;
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i <= $allpages);
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i <= $allpages);
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">â†’</span> ~ if ($i <= $allpages);
		$showpage .= "] ";
		$i = $page + 1;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();" title="ä¸‹ä¸€é¡µ">>></span> ~ if ($i <= $allpages);
		$showpage .= "ã€€ç›´æ¥è·³è½¬åˆ°ç¬¬ <input type=text name=page size=2 value=$page style='text-align: right' OnMouseOver='this.focus();' OnFocus='this.select();'> é¡µ <input type=submit value='Go'>";
	}
	else
	{
		$showpage = "è®°å½•åªæœ‰ <b>1</b> é¡µ";
	}

	$output = qq~
<script language="JavaScript">
function goempty()
{
	if (clearday = prompt("è¯·è¾“å…¥è¦æ¸…ç©ºå¤šå°‘å¤©ä»¥å‰çš„æ—¥å¿—ï¼š", "30"))
		location.href = "$thisprog?action=empty&day=" + clearday;
}
</script>
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=4><font color=#ffffff><b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / é›·å‚²é“¶è¡Œè¡Œé•¿åŠå…¬å®¤</b></td>
</tr>
<form name=EDIT action=$thisprog method=POST>
<input type=hidden name=action value="editmem">
<tr>
	<td bgcolor=#cccccc width=20%>ã€€<a href=$thisprog?action=setinfo>è®¾å®šé“¶è¡Œä¸šåŠ¡</a></td>
	<td bgcolor=#cccccc width=20%><a href=$thisprog?action=repair OnClick="return confirm('è¿™å°†æš‚æ—¶è‡ªåŠ¨å…³é—­é“¶è¡Œï¼Œæ“ä½œå®Œæˆä¼šè‡ªåŠ¨é‡æ–°å¼€æ”¾ã€‚\\nä¸€èˆ¬æ— éœ€è¿›è¡Œæ­¤æ“ä½œï¼Œæ˜¯å¦ç»§ç»­ï¼Ÿ');">é‡æ–°è®¡ç®—ç»Ÿè®¡å’Œæ’å</a></td>
	<td bgcolor=#cccccc width=20%><a href=$thisprog?action=bonus><font color=red>ç»™æ‰€æœ‰å®¢æˆ·å‘çº¢åŒ…</font></a></td>
	<td bgcolor=#cccccc width=45% align=right>å¿«é€Ÿç¼–è¾‘ä¼šå‘˜å¸æˆ·ï¼š <input type=text size=10 name=memid value=ç”¨æˆ·å OnMouseOver="this.focus();" OnFocus="this.select();">ã€€<input type=submit value=ç¼–è¾‘></td>
</tr>
</form>
<form name=MAINFORM action=$thisprog method=POST>
<tr>
	<td align=left bgcolor=#ffffff>ã€€<a href=$thisprog?action=viewloan><font color=#ff7700>è´·æ¬¾æ¸…å•</font></a></td> 
	<td align=center colspan=3 bgcolor=#ffffff>$showpage</td>
</tr>
<tr>
	<td bgcolor=#eeeeee>ã€€<b>æŸ¥æ‰¾æ—¥å¿—</b></td>
	<td bgcolor=#eeeeee><select name=type><option value="name">æœç´¢æŒ‡å®šä¼šå‘˜</option><option value="time">æœç´¢ç‰¹å®šæ—¥æœŸ</option><option value="key">æœç´¢æ“ä½œå†…å®¹</option></select></td>
	<td bgcolor=#eeeeee align=right colspan=2><input name=key value="$key" type=text size=20 OnMouseOver="this.focus();" OnFocus="this.select();">ã€€<input type=submit value=æŸ¥æ‰¾>ã€€ã€€<a href="javascript:goempty()">æ¸…ç©ºè¿‡æœŸäº¤æ˜“è®°å½•</a>ã€€</td>	
</tr>
</form>
<form name=DELETE action=$thisprog method=POST>
<input type=hidden name=action value=deletelog>
<tr>
	<td bgcolor=#ffffff>ã€€<b>è¥ä¸šçŠ¶å†µ</b></td>~;
	if ($key ne "")
	{
		$output .= qq~<td bgcolor=#ffffff colspan=3><table width=98%><td><i><font color=#0000ee>æŒ‰æ—¥æœŸæœç´¢ï¼Œè¾“å…¥æ—¥æœŸçš„æ ¼å¼å¿…é¡»æ˜¯ 2002/09/29 è¿™æ ·çš„å½¢å¼ï¼</font></i></td><td align=right><a href="$thisprog">è¿”å›å…¨éƒ¨æ—¥å¿—æ˜¾ç¤º</a></td></table></td>~;
	}
	else
	{
		$output .= qq~<script language="JavaScript">
function CheckAll() {for (var i = 0; i < DELETE.dellogid.length; i++) {DELETE.dellogid[i].checked = true;}}
function FanAll() {for (var i = 0; i < DELETE.dellogid.length; i++) {DELETE.dellogid[i].checked = !DELETE.dellogid[i].checked;}}
</script>
<td bgcolor=#ffffff colspan=3><table width=98%><td><i><font color=#0000ee>æŒ‰æ—¥æœŸæœç´¢ï¼Œè¾“å…¥æ—¥æœŸçš„æ ¼å¼å¿…é¡»æ˜¯ 2002/09/29 è¿™æ ·çš„å½¢å¼ï¼</font></i></td><td align=right><input type=button OnClick="CheckAll();" value="å…¨é€‰"> <input type=button OnClick="FanAll();" value="åé€‰">ã€€<a href="JavaScript:DELETE.submit();" OnClick="return confirm('è¿™å°†åˆ é™¤ä½ é€‰å®šçš„äº¤æ˜“æ—¥å¿—ï¼Œæ˜¯å¦ç»§ç»­ï¼Ÿ');">åˆ é™¤é€‰å®šçš„çºªå½•</a></td></table></td>~;
	}
	$output .= qq~</tr>~;

	my $lognum = @ebanklogs - ($page - 1) * 25;
	my ($logcustomer, $logtime, $logevent);
	for ($i = $lognum - 1; $i >= $lognum - 25 && $i >= 0; $i--)
	{
		chomp($ebanklogs[$i]);
		($logcustomer, $logtime, $logevent) = split(/\t/, $ebanklogs[$i]);
		$logtime = &dateformatshort($logtime + $timezone * 3600 + $timedifferencevalue * 3600);
		$logcustomer = qq~<a href=profile.cgi?action=show&member=~ . uri_escape($logcustomer) . qq~ target=_blank>$logcustomer</a>~ unless ($logcustomer =~ /é“¶è¡Œè‡ªåŠ¨å¤„ç†ç¨‹åº/);
		$output .= qq~<tr>
	<td bgcolor=#ffffff>ã€€$logcustomer</td>
	<td bgcolor=#ffffff>$logtime</td>~;
		if ($key ne "")
		{
			$output .= qq~<td bgcolor=#ffffff colspan=2>$logevent</td>~;
		}
		else
		{
			my $j = $i + 1;
			$output .= qq~<td bgcolor=#ffffff colspan=2><table width=98%><td>$logevent</td><td align=right><input type=checkbox name=dellogid value=$j></td></table></td>~;
		}
		$output .= qq~</tr>~;
	}

	$output .= qq~</form>	
<form action=$thisprog method=POST>
<input type=hidden name=action value="search">
<tr>
	<td bgcolor=#eeeeee>ã€€<b>æŸ¥æ‰¾æ—¥å¿—</b></td>
	<td bgcolor=#eeeeee><select name=type><option value="name">æœç´¢æŒ‡å®šä¼šå‘˜</option><option value="time">æœç´¢ç‰¹å®šæ—¥æœŸ</option><option value="key">æœç´¢æ“ä½œå†…å®¹</option></select></td>
	<td bgcolor=#eeeeee align=right colspan=2><input name=key value="$key" type=text size=20 OnMouseOver="this.focus();" OnFocus="this.select();">ã€€<input type=submit value=æŸ¥æ‰¾>ã€€ã€€<a href="javascript:goempty()">æ¸…ç©ºè¿‡æœŸäº¤æ˜“è®°å½•</a>ã€€</td>	
</tr>
<tr>
	<td align=left bgcolor=#ffffff>ã€€<a href=$thisprog?action=viewloan><font color=#ff7700>è´·æ¬¾æ¸…å•</font></a></td> 
	<td align=center colspan=3 bgcolor=#ffffff>$showpage</td>
</tr>
</form>
</table>~;

	$output =~ s/<option value="$type">/<option value="$type" selected>/g;
	return;
}

sub bonus
{
	$output = qq~<form action=$thisprog method=POST><input type=hidden name=action value="bonusok">
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / é“¶è¡Œè¡Œé•¿åŠå…¬å®¤</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=2>ã€€<a href=$thisprog>è¿” å›</a>  >> <font color=red>ç»™å®¢æˆ·å‘çº¢åŒ…ï¼š</font></td>
</tr>
<tr>
	<td bgcolor=#ffffff width=35%>ã€€çº¢åŒ…å¯¹è±¡ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=radio name=bonustarget value="user" checked>ã€€æ‰€æœ‰é“¶è¡Œå®¢æˆ·(é™¤è´¦å·è¢«å†»ç»“)ã€€<input type=radio name=bonustarget value="all">ã€€æ‰€æœ‰æ³¨å†Œä¼šå‘˜(é™¤ç¦è¨€å’Œå±è”½)</td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€å¯¹è±¡é™„åŠ è¦æ±‚ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€æ³¨å†Œ <input type=text size=3 name=bonusday> å¤©ä»¥ä¸Š å¹¶ä¸”å‘è´´ <input type=text size=4 name=bonuspost> ä»¥ä¸Šã€€(ä¸éœ€è¦çš„è¯·ç•™ç©º)</td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€çº¢åŒ…æ•°é¢ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=12 name=bonusnum> $moneyname</td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€çº¢åŒ…ç†ç”±ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=50 name=bonusreason></td>
</tr>
<tr>
	<td bgcolor=#ffffff align=center><input type=submit value=å‘ã€€å‡º></td>
	<td bgcolor=#ffffff align=center><input type=reset value=é‡ã€€æ¥></td>
</tr>
</table></form>~;
	return;	
}

sub deletelog
{
	my @dellogid = $query->param('dellogid');
	
	my $delnum = 0;
	my $currenttime = time;
	my $filetoopen = $lbdir . "ebankdata/alllogs.cgi";
	&winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	flock(FILE, 1) if ($OS_USED eq "Unix");
	open(FILE, $filetoopen);
	my @ebanklogs = <FILE>;
	close(FILE);	
	foreach (@dellogid)
	{
		if ($_ > 0 && $_ <= @ebanklogs)
		{
			$ebanklogs[$_ - 1] = "";
			$delnum++;
		}
	}
	unless ($delnum)
	{
		&winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
		&seterror("è¯·é€‰æ‹©è¦åˆ é™¤çš„é“¶è¡Œè®°å½•ä»¥åå†æ“ä½œï¼");
	}
	open(FILE, ">$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach (@ebanklogs)
	{
		chomp;
		print FILE $_ . "\n" if ($_);
	}
	print FILE "$inmembername\t$currenttime\t<b>åˆ é™¤äº† $delnum æ¡é“¶è¡Œäº¤æ˜“æ—¥å¿—ã€‚</b>\n";
	close(FILE);
	&winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	
	$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>ã€€æˆåŠŸåœ°åˆ é™¤äº† $delnum æ¡é“¶è¡Œäº¤æ˜“æ—¥å¿—ã€‚<br>ã€€å¦‚æœä½ çš„æµè§ˆå™¨æ²¡æœ‰è‡ªåŠ¨è¿”å›ï¼Œè¯·<a href=$thisprog>ç‚¹å‡»è¿™é‡Œ</a>~;
	return;	
}

sub setinfo
{
	my $banksave100rate = $banksaverate * 100;
	my $bankloan100rate = $bankloanrate * 100;
	my $banktrans100rate = $banktransrate * 100;
	my $bankpost100rate = $bankpostrate * 100;

	$output = qq~<form action=$thisprog method=POST><input type=hidden name=action value="setok">
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / é“¶è¡Œè¡Œé•¿åŠå…¬å®¤</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=2>ã€€<a href=$thisprog>è¿” å›</a>  >> è®¾å®šé“¶è¡Œä¸šåŠ¡å‚æ•°ï¼š</td>
</tr>
<tr>
	<td bgcolor=#ffffff width=35%>ã€€é“¶è¡ŒçŠ¶æ€ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=radio name=bankopen value="on">ã€€æ­£å¸¸å¼€æ”¾ã€€<input type=radio name=bankopen value="off">ã€€æš‚æ—¶å…³é—­</td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€é“¶è¡Œåç§°ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=20 name=bankname value="$bankname"></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€è¡Œé•¿åç§°ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=20 name=bankmanager value="$bankmanager">ã€€ç”¨è‹±æ–‡é€—å·é—´éš”å¤šä½è¡Œé•¿</td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€é“¶è¡Œæ¬¢è¿æç¤ºï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=60 name=bankmessage value="$bankmessage"></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€å­˜æ¬¾æ—¥åˆ©ç‡ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=4 name=banksaverate value="$banksave100rate"> %ã€€<i>é»˜è®¤ä¸º 0.88%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€è½¬å¸æ±‡æ¬¾åŠŸèƒ½æœ€ä½éœ€è¦å¨æœ›å€¼ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=6 name=banktransneed value="$banktransneed"></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€è½¬å¸æ‰‹ç»­è´¹ç‡ï¼š</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=6 name=banktransrate value="$banktrans100rate"> %ã€€<i>é»˜è®¤ä¸º 10%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€æ±‡æ¬¾æ‰‹ç»­è´¹ç‡ï¼š</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=6 name=bankpostrate value="$bankpost100rate"> %ã€€<i>é»˜è®¤ä¸º 20%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€æ˜¯å¦å¼€æ”¾è´·æ¬¾åŠŸèƒ½ï¼š</td>
	<td bgcolor=#ffffff>ã€€<input type=radio name=bankallowloan value="yes">ã€€å¼€æ”¾ã€€ã€€ã€€<input type=radio name=bankallowloan value="no">ã€€å…³é—­</td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€è´·æ¬¾æœ€é•¿å¿è¿˜æœŸé™ï¼š</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=2 name=bankloanmaxdays value="$bankloanmaxdays"> å¤©ã€€<i>é»˜è®¤ä¸º 7</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€è´·æ¬¾æ—¥åˆ©ç‡ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=4 name=bankloanrate value="$bankloan100rate"> %ã€€<i>é»˜è®¤ä¸º 1.88%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€æ¯ç‚¹å¨æœ›æœ€é«˜æŠµæŠ¼è´·æ¬¾æ•°é¢ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=6 name=bankrateloan value="$bankrateloan"> $moneyname</td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€å•ç¬”äº¤æ˜“æœ€é«˜é™é¢ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type size=10 name=bankmaxdeal value="$bankmaxdeal"> $moneynameã€€<i>é»˜è®¤ä¸º 500000</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€å•ç¬”äº¤æ˜“æœ€ä½é™é¢ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type size=10 name=bankmindeal value="$bankmindeal"> $moneynameã€€<i>é»˜è®¤ä¸º 10</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€é¦–é¡µæ˜¾ç¤ºçš„ç”¨æˆ·æ’åæ•°ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type size=4 name=bankmaxdisplay value="$bankmaxdisplay">ã€€<i>é»˜è®¤ä¸º 10 ï¼Œä¸èƒ½è¶…è¿‡ 20</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€24å°æ—¶å†…æœ€å¤§äº¤æ˜“æ¬¡æ•°ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type size=4 name=bankmaxdaydo value="$bankmaxdaydo">ã€€<i>é»˜è®¤ä¸º 5 ï¼Œä¸èƒ½è¶…è¿‡ 10ï¼Œå¯¹å›ä¸»æ— æ•ˆ</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€ä¸ªäººå­˜æŠ˜æœ€å¤šè®°å½•æ¡æ•°ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type size=4 name=banklogpriviate value="$banklogpriviate">ã€€<i>é»˜è®¤ä¸º 6 ï¼Œä¸èƒ½è¶…è¿‡ 20</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€å…è®¸ç®¡ç†é“¶è¡Œä¼šå‘˜ï¼š</td>
	<td bgcolor=#ffffff>ã€€<select name=bankadminallow><option value="allad">æ‰€æœ‰å›ä¸»ã€è¡Œé•¿</option><option value="all">æ‰€æœ‰æ€»ç‰ˆä¸»å’Œå›ä¸»ã€è¡Œé•¿</option></select></td>
</tr>
<tr>
	<td bgcolor=#ffffff align=center><input type=submit value=æã€€äº¤></td>
	<td bgcolor=#ffffff align=center><input type=reset value=é‡ã€€ç½®></td>
</tr>
</table></form>~;

	$output =~ s/<input type=radio name=bankopen value="$bankopen">/<input type=radio name=bankopen value="$bankopen" checked>/g;
	$output =~ s/<input type=radio name=bankrateuse value="$bankrateuse">/<input type=radio name=bankrateuse value="$bankrateuse" checked>/g;
	$output =~ s/<input type=radio name=bankallowloan value="$bankallowloan">/<input type=radio name=bankallowloan value="$bankallowloan" checked>/g;
	$output =~ s/<option value="$bankadminallow">/<option value="$bankadminallow" selected>/g;

	return;
}

sub editmem
{
	my $memid = $query->param('memid');
	&seterror("æ²¡æœ‰è¾“å…¥ç¼–è¾‘çš„å¸æˆ·åï¼") if ($memid eq "");
	&seterror("å¸æˆ·åå«æœ‰éæ³•å­—ç¬¦ï¼") if (($memid =~ m/\//) || ($memid =~ m/\\/) || ($memid =~ m/\.\./));
	&getmember($memid, "no");
	&seterror("ç”¨æˆ· $memid ä¸å­˜åœ¨ï¼") if ($userregistered eq "no");
	($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
	&seterror("ç”¨æˆ· $memid æ²¡æœ‰åœ¨æœ¬è¡Œå¼€æˆ·ï¼") unless ($mystatus);

	my $loanoutput;
	if ($myloan)
	{
		$loanoutput = qq~ç”¨æˆ·ä»æœ¬è¡Œè´·æ¬¾ $myloan $moneynameã€€ã€€<input type=checkbox name=clearloan value="yes">ã€€æ¸…é™¤ç”¨æˆ·çš„è´·æ¬¾è®°å½•ï¼Ÿ~;
	}
	else
	{
		$loanoutput = qq~ç”¨æˆ·åœ¨æœ¬è¡Œæ²¡æœ‰è´·æ¬¾~;
	}

	$output = qq~<form action=$thisprog method=POST><input type=hidden name=action value="editok"><input type=hidden name=memid value="$memid">
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / é›·å‚²é“¶è¡Œè¡Œé•¿åŠå…¬å®¤</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=2>ã€€<a href=$thisprog>è¿” å›</a>  >> ç¼–è¾‘ $memid çš„å­˜è´·æ¬¾èµ„æ–™ï¼š</td>
</tr>
<tr>
	<td bgcolor=#ffffff width=40%>ã€€ç”¨æˆ·å­˜æ¬¾æ•°é¢ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=text size=15 name=newsavenums value="$mysaves"> $moneyname</td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€ç”¨æˆ·è´·æ¬¾æ•°é¢ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€$loanoutput</td>
</tr>
<tr>
	<td bgcolor=#ffffff>ã€€ä¿®æ”¹å–æ¬¾å¯†ç ï¼šã€€</td>
	<td bgcolor=#ffffff>ã€€<input type=isplay = $query->param('bankmaxdisplay');
	my $newbankmaxdaydo = $query->param('bankmaxdaydo');
	my $newbanklogpriviate = $query->param('banklogpriviate');
	my $newbankadminallow = $query->param('bankadminallow');

	$newbankopen = "on" if ($newbankopen ne "off");
	&seterror("»¹Ã»ÓĞÊäÈëĞĞ³¤´óÃû£¡") if ($newbankmanager eq "");
	$newbankmanager = &unHTML($newbankmanager);
	&seterror("»¹Ã»ÓĞÊäÈëÒøĞĞÃû³Æ£¡") if ($newbankname eq "");
	$newbankname = &unHTML($newbankname);
	$newbankmessage = &unHTML($newbankmessage);
	&seterror("´æ¿îÈÕÀûÂÊÊäÈë´íÎó£¡") if ($newbanksaverate =~ /[^0-9\.]/ or $newbanksaverate eq "");
	&seterror("´æ¿îÈÕÀûÂÊÌ«¸ß£¡") if ($newbanksaverate > 10);
	$newbanksaverate /= 100;
	&seterror("×ªÕÊ»ã¿î¹¦ÄÜ×îµÍĞèÒªÍşÍûÖµÊäÈë´íÎó£¡") if ($newbanktransneed =~ /[^0-9]/ or $newbanktransneed eq "");
	&seterror("×ªÕÊ»ãÂÊÊäÈë´íÎó£¡") if ($newbanktransrate =~ /[^0-9\.]/ or $newbanktransrate eq "");
	$newbanktransrate /= 100;
	&seterror("»ã¿î»ãÂÊÊäÈë´íÎó£¡") if ($newbankpostrate =~ /[^0-9\.]/ or $newbankpostrate eq "");
	$newbankpostrate /= 100;
	$newbankallowloan = "yes" if ($newbankallowloan ne "no");
	&seterror("´û¿î×î³¤³¥»¹ÆÚÏŞÊäÈë´íÎó£¡") if ($newbankloanmaxdays =~ /[^0-9]/ or $newbankloanmaxdays eq "");
	&seterror("´û¿îÈÕÀûÂÊÊäÈë´íÎó£¡") if ($newbankloanrate =~ /[^0-9\.]/ or $newbankloanrate eq "");
	$newbankloanrate /= 100;
	&seterror("´û¿îÀûÂÊ±ØĞë¸ßÓÚ´æ¿îÀûÂÊ£¡") if ($newbankloanrate <= $newbanksaverate);
	&seterror("Ã¿µãÍşÍû×î¸ßµÖÑº´û¿îÊı¶îÊäÈë´íÎó£¡") if ($newbankrateloan =~ /[^0-9]/ or $newbankrateloan eq "");
	&seterror("µ¥±Ê½»Ò××î¸ßÏŞ¶îÊäÈë´íÎó£¡") if ($newbankmaxdeal =~ /[^0-9]/ or $newbankmaxdeal eq "");
	&seterror("µ¥±Ê½»Ò××îµÍÏŞ¶îÊäÈë´íÎó£¡") if ($newbankmindeal =~ /[^0-9]/ or $newbankmindeal eq "");
	&seterror("µ¥±Ê½»Ò××î¸ßÏŞ¶îÓ¦¸Ã´óÓÚµ¥±Ê½»Ò××îµÍÏŞ¶î£¡") if ($newbankmaxdeal <= $newbankmindeal);
	&seterror("Ê×Ò³ÏÔÊ¾µÄÓÃ»§ÅÅÃûÊıÊäÈë´íÎó£¡") if ($newbankmaxdisplay =~ /[^0-9]/ or $newbankmaxdisplay eq "");
	&seterror("Ê×Ò³ÏÔÊ¾µÄÓÃ»§ÅÅÃûÊı¹ı¶à£¡") if ($newbankmaxdisplay > 20);
	&seterror("24Ğ¡Ê±ÄÚ×î´ó½»Ò×´ÎÊıÊäÈë´íÎó£¡") if ($newbankmaxdaydo =~ /[^0-9]/ or $newbankmaxdaydo eq "");
	&seterror("24Ğ¡Ê±ÄÚ×î´ó½»Ò×´ÎÊı¹ı¶à£¡") if ($newbankmaxdaydo > 10);
	&seterror("¸öÈË´æÕÛ×î¸ß¼ÇÂ¼ÌõÊıÊäÈë´íÎó£¡") if ($newbanklogpriviate =~ /[^0-9]/ or $newbanklogpriviate eq "");
	&seterror("¸öÈË´æÕÛ×î¸ß¼ÇÂ¼ÌõÊı¹ı¶à£¡") if ($newbanklogpriviate > 20);
	$newbankadminallow = "allad" unless ($newbankadminallow eq "all" or $newbankadminallow eq "manager");

	my $filetomake = $lbdir . "data/ebankinfo.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE qq~\# EbankMX For LB Plus is Powered By 94Cool.Net BigJim
\$bankopen = "$newbankopen";
\$bankname = "$newbankname";
\$bankmanager = "$newbankmanager";
\$bankmessage = "$newbankmessage";
\$banksaverate = $newbanksaverate;
\$banktransneed = $newbanktransneed;
\$banktransrate = $newbanktransrate;
\$bankpostrate = $newbankpostrate;
\$bankallowloan = "$newbankallowloan";
\$bankloanmaxdays = $newbankloanmaxdays;
\$bankloanrate = $newbankloanrate;
\$bankrateloan = $newbankrateloan;
\$bankmaxdeal = $newbankmaxdeal;
\$bankmindeal = $newbankmindeal;
\$bankmaxdisplay = $newbankmaxdisplay;
\$bankmaxdaydo = $newbankmaxdaydo;
\$banklogpriviate = $newbanklogpriviate;
\$bankadminallow = "$newbankadminallow";
1;~;
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");

	$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>¡¡Èç¹ûÄãµÄä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çë<a href=$thisprog>µã»÷ÕâÀï</a>~;
	return;
}

sub editok
{
	my $memid = $query->param('memid');
	&seterror("Ã»ÓĞÊäÈë±à¼­µÄÕÊ»§Ãû£¡") if ($memid eq "");
	&seterror("ÕÊ»§Ãûº¬ÓĞ·Ç·¨×Ö·û£¡") if (($memid =~ m/\//) || ($memid =~ m/\\/) || ($memid =~ m/\.\./));
	$memid =~ s/ /\_/sg;
	$memid =~ tr/A-Z/a-z/;

	my $newsavenums = $query->param('newsavenums');
	my $clearloan = $query->param('clearloan');
	my $accountstats = $query->param('accountstats');
	my $getpass = $query->param('getpass');
	$getpass =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

	$memid = &stripMETA($memid);
	my $namenumber = &getnamenumber($memid);
	&checkmemfile($memid,$namenumber);
	my $filetoopen = "$lbdir$memdir/$namenumber/$memid.cgi";
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

		if ($mystatus)
		{
			if ($mysaves != $newsavenums)
			{			
				&logaction($inmembername, "±à¼­ÓÃ»§ $membername µÄ´æ¿î´Ó $mysaves $moneynameµ½ $newsavenums $moneyname¡£");
				&updateallsave(0, $newsavenums - $mysaves);
				$mysaves = $newsavenums;
				&order($memid, $newsavenums);
			}

			if ($myloan && $clearloan eq "yes")
			{		
				&logaction($inmembername, "Çå³ıÁËÓÃ»§ $membername $myloan $moneynameµÄ´û¿î¼ÇÂ¼¡£");
				$myloan = 0;
				$myloantime = "";
				$myloanrating = 0;
			}

			if ($getpass ne "")
			{
				$bankgetpass = $getpass;
				&logaction($inmembername, "<b>ĞŞ¸ÄÁËÓÃ»§ $membername µÄÈ¡¿îÃÜÂë¡£</b>");
			}

			if ($accountstats eq "on" && $mystatus == -1)
			{
				&bankmessage($memid, "½â¶³Í¨Öª", "ÄãÔÚ$banknameµÄÕË»§ÒÑ¾­±»$inmembername½â¶³¡£");
				&logaction($inmembername, "<font color=green>½â³ıÁË¶ÔÓÃ»§ $membername ÕÊ»§µÄ¶³½á¡£</font>");
				$mystatus = 1;
			}
			elsif ($accountstats eq "off" && $mystatus == 1)
			{
				&bankmessage($memid, "¶³½áÍ¨Öª", "ÄãÔÚ$banknameµÄÕË»§ÒÑ¾­±»$inmembername¶³½á£¬ÈçÓĞÒÉÎÊÇëÓëÆäÁªÏµ¡£");
				&logaction($inmembername, "<font color=red>ÔİÊ±¶³½áÁËÓÃ»§ $membername µÄÕÊ»§¡£</font>");
				$mystatus = -1;
			}

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
		else
		{
			&winunlock($filetoopen) if ($OS_USED eq "Nt");
			&seterror("ÓÃ»§ $memid Ã»ÓĞÔÚ±¾ĞĞ¿ª»§£¡");
		}
	}
	else
	{
		&seterror("ÓÃ»§ $memid ²»´æÔÚ£¡");
	}

	$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>¡¡Èç¹ûÄãµÄä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çë<a href=$thisprog>µã»÷ÕâÀï</a>~;
	return;
}

sub empty
{
	my $clearday = $query->param("day");
	$clearday = 30 if ($clearday !~ /^[0-9]+$/);
	my $currenttime = time;
	my $cleartime = $currenttime - $clearday * 86400;
	my $filetomake = $lbdir . "ebankdata/alllogs.cgi";
	&winlock($filetomake) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");
	open(FILE, $filetomake);
	flock(FILE, 1)  if ($OS_USED eq "Unix");
	my @alllogs = <FILE>;
	close(FILE);
	my $deletenum = 0;
	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach (@alllogs)
	{
		chomp;
		my (undef, $logtime, undef) = split(/\t/, $_);
		if ($logtime < $cleartime)
		{
			$deletenum++;
		}
		else
		{
			print FILE "$_\n";
		}
	}
	print FILE "$inmembername\t$currenttime\t<b>ÅúÁ¿É¾³ıÁËÒøĞĞ $clearday ÌìÒÔÇ°µÄ¹ıÆÚ½»Ò×ÈÕÖ¾¹² $deletenum Ìõ¡£</b>\n";
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");

	$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>¡¡Èç¹ûÄãµÄä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çë<a href=$thisprog>µã»÷ÕâÀï</a>~;
	return;
}

sub seterror
{
	my $message = $_[0];
	my $output = qq~
<table width=100% cellpadding=6 cellspacing=0>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>»¶Ó­À´µ½ÂÛÌ³¹ÜÀíÖĞĞÄ / ÒøĞĞ¹ÜÀí·¢Éú´íÎó</b></font></td></tr>
<tr><td bgcolor=#eeeeee><font color=#990000><b>¡¡³ö´íÀ­£º</b>$message</font></td></tr>
<tr><td bgcolor=#ffffff>¡¡¡¡<a href="javascript:history.go(-1);">·µ»ØÉÏÒ»Ò³</a></td></tr>
</table>
</td></tr></table></body></html>~;
	print $output;	
	exit;
}

sub bankmessage #¸øÓÃ»§·¢ÒøĞĞ¶ÌÏûÏ¢£¨µ÷ÓÃ²ÎÊı£ºÊÕÈ¡ÈË¡¢Ö÷Ìâ¡¢ÄÚÈİ£©
{
	my ($receivemember, $topic, $content) = @_;

	my @filedata;
	my $filetomake = $lbdir . $msgdir . "/in/" . $receivemember . "_msg.cgi";
	$filetomake = &stripMETA($filetomake);
	my $currenttime = time;
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

sub logaction #¼ÇÂ¼ÒøĞĞÈÕÖ¾£¨µ÷ÓÃ²ÎÊı£º²Ù×÷ÈËÔ±£¬ÈÕÖ¾ÄÚÈİ£©
{
	my ($actionmember, $actionretail) = @_;
	my $currenttime = time;

	my $filetomake = $lbdir . "ebankdata/alllogs.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">>$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "$actionmember\t$currenttime\t$actionretail\n";
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");

	return;
}

sub ebankadminlogin
{
if ($useverify eq 'yes')
{
   if ($verifyusegd ne 'no')
   {
       eval ('use GD;');
       if ($@)
       {
           $verifyusegd = 'no';
       }
   }
   if ($verifyusegd eq 'no')
   {
       $houzhui = 'bmp';
   } else {
       $houzhui = 'png';
   }
   require 'verifynum.cgi';
}

	print qq~
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>»¶Ó­À´µ½ÒøĞĞĞĞ³¤°ì¹«ÊÒ</b></font></td>
</tr>
<form action=$thisprog method=POST>
<input type=hidden name=action value="login">
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
~;
print qq~
<tr>
	<td bgcolor=#ffffff valign=middle width=40% align=right><font color=#555555>ÇëÊäÈëÓÒ±ßÍ¼Æ¬µÄÊı×Ö</font></td>
	<td bgcolor=#ffffff valign=middle><input type=hidden name=sessionid value="$sessionid"><input type=text name=verifynum size=4 maxlength=4>¡¡¡¡<img src=$imagesurl/verifynum/$sessionid.$houzhui border=0 align=absmiddle></td>
</tr>
~ if ($useverify eq "yes");

print qq~
<tr>
	<td bgcolor=#ffffff valign=middle colspan=2 align=center><input type=submit value="µÇ Â½"></td>
</tr>
</form>
<tr>
	<td bgcolor=#ffffff valign=middle align=left colspan=2><font face=$font color=#555555>
		<blockquote><b>Çë×¢Òâ</b><p><b>Ö»ÓĞÒøĞĞĞĞ³¤²ÅÄÜ½øÈëĞĞ³¤°ì¹«ÊÒ¡£<br>Î´¾­¹ıÊÚÈ¨µÄ³¢ÊÔµÇÂ¼ĞĞÎª½«»á±»¼ÇÂ¼ÔÚÒøĞĞÈÕÖ¾£¡</b><p>ÔÚ½øÈëĞĞ³¤°ì¹«ÊÒÇ°£¬ÇëÈ·¶¨ÄãµÄä¯ÀÀÆ÷´ò¿ªÁË Cookie Ñ¡Ïî¡£<br> Cookie Ö»»á´æÔÚÓÚµ±Ç°µÄä¯ÀÀÆ÷½ø³ÌÖĞ¡£ÎªÁË°²È«Æğ¼û£¬µ±Äã¹Ø±ÕÁËä¯ÀÀÆ÷ºó£¬Cookie »áÊ§Ğ§²¢±»×Ô¶¯É¾³ı¡£</blockquote>
	</td>
</tr>
~;
	return;
}

sub order #ÒøĞĞÅÅĞò³ÌĞò
{
	my ($adduser, $addsave) = @_;
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
	$ordersaves{$adduser} = $addsave if ($adduser ne "");
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

sub setbankonoff
{
	my $status = shift;

        my $filetomake = $lbdir . "data/ebankinfo.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, $filetomake);
	flock(FILE, 1) if ($OS_USED eq "Unix");
	my @tempinfo = <FILE>;
	close(FILE);
	open(FILE,">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach $tempconfig (@tempinfo)
	{
		chomp($tempconfig);
		$tempconfig = "\$bankopen = \"$status\";" if ($tempconfig =~ /\$bankopen/);
		print FILE $tempconfig . "\n";
	}
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
}

sub checkverify {
	my $verifynum = $query->param('verifynum');
	my $sessionid = $query->param('sessionid');
	$sessionid =~ s/[^0-9a-f]//isg;
	if (length($sessionid) != 32 && $useverify eq "yes")
	{
		$inpassword = "";
		return;
	}
        mkdir ("${lbdir}verifynum", 0777) unless (-e "${lbdir}verifynum");
        mkdir ("${lbdir}verifynum/login", 0777) if (!(-e "${lbdir}verifynum/login"));

	###»ñÈ¡ÕæÊµµÄ IP µØÖ·
	my $ipaddress = $ENV{'REMOTE_ADDR'};
	my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
	$trueipaddress = $ENV{'HTTP_CLIENT_IP'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);

	###»ñÈ¡µ±Ç°½ø³ÌµÄÑéÖ¤ÂëºÍÑéÖ¤Âë²úÉúÊ±¼ä¡¢ÓÃ»§ÃÜÂë
	my $filetoopen = "${lbdir}verifynum/$sessionid.cgi";
	open(FILE, $filetoopen);
	my $content = <FILE>;
	close(FILE);
	unlink($filetoopen);
	chomp($content);
	my ($trueverifynum, $verifytime, $savedipaddress) = split(/\t/, $content);
	my $currenttime = time;

	if (($verifynum ne $trueverifynum || $currenttime > $verifytime + 300 || $ipaddress ne $savedipaddress)&&($useverify eq "yes"))
	{#ÑéÖ¤ÂëÓĞĞ§Ê±¼ä½öÎª5·ÖÖÓ
		$inpassword = "";
	}
	else
	{
		unlink("${lbdir}verifynum/$sessionid.cgi");
		unlink("${imagesdir}verifynum/$sessionid.cgi");
		my $memberfilename = $inmembername;
		$memberfilename =~ s/ /_/g;
		$memberfilename =~ tr/A-Z/a-z/;
		$memberfilename = "${lbdir}verifynum/login/$memberfilename.cgi";

		open(FILE, ">$memberfilename");
		print FILE "$currenttime";
		close(FILE);
	}
	return;
}