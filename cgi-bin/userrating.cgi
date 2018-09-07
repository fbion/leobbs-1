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
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "recooper.pl";

$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$thisprog = "userrating.cgi";
$query = new LBCGI;
$inforum = $query->param("oldforum");
$intopic = $query->param("oldtopic");
$inpostno = $query->param("oldpostno");
&error("普通错误&老大，别乱黑我的程序呀！") if ($inforum !~ /^[0-9]+$/ || $intopic !~ /^[0-9]+$/ || $inpostno !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inmembername = $query->param ("inmembername");
$inpassword = $query->param ("password");
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inmembername = $query->cookie("amembernamecookie") if ($inmembername eq "");
$inpassword = $query->cookie("apasswordcookie") if ($inpassword eq "");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "客人")
{
	&error("用户投票&没有该注册用户或者您在投票前没有登录！");
}
else
{
	&getmember($inmembername,"no");
	&error("用户投票&没有该注册用户！") if ($userregistered eq "no");
	&error("用户投票&错误的管理员密码！") if ($inpassword ne $password);
}

$editmembername = $query->param("membername");
$editmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

$action = $query->param("action");

&error("论坛投票&主题不存在！") unless (-e "${lbdir}forum$inforum/$intopic.pl");

$action = "login" if ($action ne "logmein" && $action ne "process");
&getoneforum($inforum);

&title;

$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以对用户进行投票，减少或增加他们的威望或积分，甚至可以禁止他们发言！</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> → <a href="forums.cgi?forum=$inforum">$forumname</a> → 给用户投票<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>~;

if ($action eq "login")
{
	$output .= qq~
<form action=$thisprog method=POST>
<input type=hidden name=action value="logmein">
<input type=hidden name=oldforum value="$inforum">
<input type=hidden name=oldtopic value="$intopic">
<input type=hidden name=oldpostno value="$inpostno">
<input type=hidden name=membername value="$editmembername">
<tr><td bgcolor=$titlecolor $catbackpic colSpan=2 align=center><font color=$fontcolormisc><b>请首先登录然后对 $editmembername 进行投票(仅对坛主和版主开放)</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colSpan=2 align=center><input type=submit name=submit value="登录投票"></td></form></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

elsif ($action eq "logmein")
{
        $inmembmod = "no" if ($membercode eq "amo");
        $mymembercode = $membercode;
	&error("用户投票&仅仅本版管理员才能在本版投票") unless ($membercode eq "ad" || $membercode eq "smo" || $inmembmod eq "yes");
	&error("用户投票&不能对自己投票") if ($inmembername eq $editmembername);
	&getmember($editmembername);
	&error("用户投票&没有该注册用户") if ($userregistered eq "no");
	&error("用户投票&坛主不能被投票") if ($membercode eq "ad");
	&error("用户投票&只有坛主才能给版主们投票！") if (($membercode eq "smo" || $membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && $mymembercode ne "ad");

	my $threadtomake = "${lbdir}forum$inforum/$intopic.thd.cgi";
	$inpostno--;
	if (-e $threadtomake)
	{
		open(FILE, $threadtomake);
		my @threads = <FILE>;
		close(FILE);
		if ($inpostno < @threads && $inpostno >= 0)
		{
			(my $membername, $topictitle, my $postipaddresstemp, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/, $threads[$inpostno]);
			&error("用户投票&此帖子并不是$editmembername发表！") if (lc($membername) ne  lc($editmembername));
		} else { &error("用户投票&对应的帖子不存在！!"); }
	}
	else { &error("用户投票&对应的帖子不存在！"); }
	$inpostno++;
	
	$rating = 0 if ($rating eq "");
	if ($jifen eq "") {
		require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
		$jifen = $numberofposts * $ttojf + $numberofreplys * $rtojf - $postdel * $deltojf;
  }
	$rating = -6 if ($rating < -6);
	$rating = $maxweiwang if ($rating > $maxweiwang);

	if ($rating == $maxweiwang) {$pwout = qq~<input type=radio name=pw value="warn" >警告用户(威望减 1)~;}
	elsif ($rating == -5) {$pwout = qq~<input type=radio name=pw value="praise" >赞扬用户(威望加 1)　　<input type=radio name=pw value="warn">禁止用户发言(威望减为 -6)　　<input type=radio name=pw value="worstm">屏蔽此用户贴子(威望减为 -6)~;}
	elsif ($rating == -6) {$pwout = qq~<input type=radio name=pw value="praise" >恢复用户(威望恢复成 -5)~;}
	else {$pwout = qq~<input type=radio name=pw value="praise" >赞扬用户(威望加 1)　　<input type=radio name=pw value="warn">警告用户(威望减 1)　　<input type=radio name=pw value="reset">清零(威望为 0)　　<input type=radio name=pw value="worst">禁止发言(威望减为 -6)　　<input type=radio name=pw value="worstm">屏蔽此用户贴子(威望减为 -6)~;}
                $max1jf = 50 if ($max1jf eq "");

	$output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>$editmembername 目前的威望是: $rating，拥有的积分为: $jifen</b></font></td></tr>
<tr><td bgcolor=$miscbackone align=center>
<form action=$thisprog method=POST>
<input type=hidden name=action value=process>
<input type=hidden name=membername value="$editmembername">
<input type=hidden name=oldforum value="$inforum">
<input type=hidden name=oldtopic value="$intopic">
<input type=hidden name=oldpostno value="$inpostno">
<b>* 积 分 处 理 *</b><BR>
<input type=radio name=pw value="jfzj" checked> 奖励/惩罚论坛积分 <input type=text name=numschange size=3 maxsize=3> 分 (必须控制在 -$max1jf 到 $max1jf 之间)<BR><BR>
<b>* 威 望 处 理 *</b><BR>
$pwout
<BR><BR><BR>
</td></tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>投票原因:<br><textarea size=20 name=reason cols=40 rows=5></textarea></td></tr>
<tr><td bgcolor=$miscbackone align=center>使用论坛短消息通知用户: <input type=radio name=msgnotify value="yes" checked>是　　<input type=radio name=msgnotify value="no">否</td>~;
	$output .= qq~<tr><td bgcolor=$miscbackone align=center>使用邮件通知用户: <input type=radio name=notify value="yes">是　　<input type=radio name=notify value="no" checked>否</td>~ if ($emailfunctions eq "on");
	$output .= qq~
<tr><td bgcolor=$miscbacktwo align=center><input type=submit value="确认" name=submit></td></form></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

elsif ($action eq "process")
{
        $inmembmod = "no" if ($membercode eq "amo");
        $mymembercode = $membercode;
	&error("用户投票&仅仅本版管理员才能在本版投票") unless ($membercode eq "ad" || $membercode eq "smo" || $inmembmod eq "yes");
	&error("用户投票&不能对自己投票") if ($inmembername eq $editmembername);
	&getmember($editmembername);
	&error("用户投票&没有该注册用户") if ($userregistered eq "no");
	&error("用户投票&坛主不能被投票") if ($membercode eq "ad");
	&error("用户投票&只有坛主才能给版主们投票！") if (($membercode eq "smo" || $membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && $mymembercode ne "ad");
	my $thistime = time;

	my $pw = $query->param("pw");
	my $reason = $query->param("reason");
	my $notify = $query->param("notify");
	my $msgnotify = $query->param("msgnotify");
	&error("用户投票&投票必须说明理由！") if ($reason eq "");
	$reason = &cleaninput($reason);
	$reason =~ s/\|//isg;

	my $oldrating = $rating;
	if ($pw eq "praise")
	{
		$pwmail = $pwmailing = "增加威望";
		$rating++;
		$ratingname = "威望由 $oldrating 增加至 $rating";
	}
	elsif ($pw eq "warn")
	{
		$pwmail = $pwmailing = "减少威望";
		$rating--;
		$ratingname = "威望由 $oldrating 减少至 $rating";
	}
	elsif ($pw eq "reset")
	{
		$pwmail = "调整威望为 0";
		$pwmailing = "调整威望";
		$rating = 0;
		$ratingname = "威望由 $oldrating 调整至 $rating";
	}
	elsif ($pw eq "worst" || $pw eq "worstm")
	{
		$pwmail = "减低威望到最低";
		$pwmailing = "减低威望";
		$rating = -6;
		$ratingname = "威望由 $oldrating 减少至 $rating";
	}
        elsif ($pw eq 'jfzj') {
		$numschange = $query->param("numschange");
                $max1jf = 50 if ($max1jf eq "");
		&error("用户投票&奖惩货币或者积分数量输入错误！") unless ($numschange =~ /^[0-9\-]+$/);
		&error("用户投票&一次奖惩积分数量不得超过 $max1jf 分！！") if (abs($numschange) > $max1jf);
		$oldrating = "积分 $jifen";
		$jiangcheng = $numschange >= 0 ?  "奖励" : "惩罚";
		$pwmail = "$jiangcheng积分 $numschange分";
		$pwmailing = "$jiangcheng积分";
		$jifen += $numschange;
		$numschange = abs($numschange);
		$ratingname = "$jiangcheng积分 $numschange";
	}

	$rating = 0 if ($rating eq "");
	$rating = -6 if ($rating < -6);
	$rating = $maxweiwang if ($rating > $maxweiwang);
	$newmembercode = $rating == -6 ? "banned" : ($membercode eq "banned" || $membercode eq "masked") ? "me" : $membercode;
	$newmembercode = "masked" if ($pw eq "worstm");


	my $threadtomake = "${lbdir}forum$inforum/$intopic.thd.cgi";
	$inpostno--;
	if (-e $threadtomake)
	{
		&winlock($threadtomake) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		open(FILE, $threadtomake);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my @threads = <FILE>;
		close(FILE);
		if ($inpostno < @threads && $inpostno >= 0)
		{
			(my $membername, $topictitle, my $postipaddresstemp, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/, $threads[$inpostno]);
			&error("用户投票&此帖子并不是$editmembername发表！") if (lc($membername) ne  lc($editmembername));
			$post = "[ADMINOPE=$inmembername|$editmembername|$ratingname|$reason|$thistime]$post";
			$threads[$inpostno] = "$membername\t$topictitle\t$postipaddresstemp\t$showemoticons\t$showsignature\t$postdate\t$post\t$posticon";
			open(FILE, ">$threadtomake");
			flock(FILE, 2) if ($OS_USED eq "Unix");
			foreach (@threads)
			{
				chomp;
				next if ($_ eq "");
				print FILE "$_\n";
			}
			close(FILE);
		} else { &winunlock($threadtomake) if ($OS_USED eq "Nt" || $OS_USED eq "Unix"); &error("用户投票&对应的帖子不存在!！"); }
		&winunlock($threadtomake) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	}
	else { &error("用户投票&对应的帖子不存在！"); }

	my $memfilename = $editmembername;
	$memfilename =~ s/ /\_/sg;
	$memfilename =~ tr/A-Z/a-z/;
	my $namenumber = &getnamenumber($memfilename);
	&checkmemfile($memfilename,$namenumber);
	if ($membername ne "" && $password ne "")
	{
		my $filetomake = "$lbdir$memdir/$namenumber/$memfilename.cgi";
		$filetomake = &stripMETA($filetomake);
		&winlock($filetomake) if ($OS_USED eq "Nt");
		if (open(FILE0, "+<$filetomake"))
		{
	    		seek(FILE0,0,0);
			flock(FILE0, 2) if ($OS_USED eq "Unix");
			print FILE0 "$membername\t$password\t$membertitle\t$newmembercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5";
			close(FILE0);
		}
		&winunlock($filetomake) if ($OS_USED eq "Nt");
		my $filetomake = "$lbdir$memdir/old/$memfilename.cgi";
		$filetomake = &stripMETA($filetomake);
		if (open(FILE0, ">$filetomake"))
		{
			print FILE0 "$membername\t$password\t$membertitle\t$newmembercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5";
			close(FILE0);
		}
	}
        unlink ("${lbdir}cache/meminfo/$memfilename.pl");
	unlink ("${lbdir}cache/myinfo/$memfilename.pl");

	if ($rating == -6)
	{
		my $filetoopen = "${lbdir}data/banemaillist.cgi";
		open(FILE, ">>$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$emailaddress\t";
		close(FILE);
		$filetoopen = "${lbdir}data/baniplist.cgi";
		open(FILE, ">>$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$ipaddress\t";
		close(FILE);
	}
	else
	{
		my $filetoopen = "${lbdir}data/banemaillist.cgi";
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		$emaildata = <FILE>;
		close(FILE);
		chomp($emaildata);
		@emaildata = split(/\t/, $emaildata);
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@emaildata)
		{
			next if ($_ eq "");
			print FILE "$_\t" if ($emailaddress ne $_);
		}
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");

		$filetoopen = "${lbdir}data/baniplist.cgi";
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		$ipdata = <FILE>;
		close(FILE);
		chomp($ipdata);
		@ipdata = split(/\t/, $ipdata);
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@ipdata)
		{
			next if ($_ eq "");
			print FILE "$_\t" if ($ipaddress ne $_);
		}
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
	}

	$trueipaddress = $ENV{"HTTP_CLIENT_IP"};
	$trueipaddress = $ENV{"HTTP_X_FORWARDED_FOR"} if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	$trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	
	$filetomake = "${lbdir}data/userratinglog.cgi";
	open(FILE0, ">>$filetomake");
	print FILE0 "$editmembername\t$inmembername\t$ratingname\t$thistime\t$inforum\t$intopic\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t$reason\t\n";
	close(FILE0);
	
	&addadminlog("对用户 $editmembername 操作： $ratingname，理由：$reason", $intopic);

	if ($notify eq "yes" && $emailfunctions eq "on") {
		eval("use MAILPROG qw(sendmail);");
		my $membertitleout = $newmembercode eq "banned" ? "被禁止" : "普通会员";
		my $subject = "你已经被 $inmembername $pwmail !";
		my $message = "<br>$homename<br>";
		$message .= "<a href=$boardurl/leobbs.cgi target=_blank>$boardurl/leobbs.cgi</a><br>";
		$message .= "<a href=$boardurl/topic.cgi?forum=$inforum&topic=$intopic target=_blank>$boardurl/topic.cgi?forum=$inforum&topic=$intopic</a><br><br><br>";
		$message .= "你已经被 $inmembername $pwmail !<br><br><br>";
		$message .= "内容：$ratingname<br>";
		$message .= "你现在的状态是: $membertitleout<br>";
		$message .= "你被 $pwmailing 的原因是:<br>";
		$message .= "$reason<br><br>";
		$message .= "假如你认为有错, 请发信给<br>";
		$message .= "坛主: $adminemail_in 解释原因！<br>";
		&sendmail($adminemail_out, $adminemail_out, $emailaddress, $subject, $message);
	}
	if ($msgnotify eq "yes") {
	    $topictitle =~ s/^＊＃！＆＊//;
	    &shortmessage($inmembername, $editmembername, "你已经被$pwmail!", "　　你已经被 $inmembername $pwmailing! 　内容：$ratingname。<br>　　相关的主题是: \[url=topic.cgi?forum=$inforum&topic=$intopic\]按此进入\[\/url\]，操作原因是: $reason。");
	}
	$output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>$editmembername 已经成功被$pwmail</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>具体情况:<br><ul>
<li><a href=topic.cgi?forum=$inforum&topic=$intopic>返回当前主题 </a>$pages
<li><a href=forums.cgi?forum=$inforum>返回当前论坛</a>
<li><a href=leobbs.cgi>返回论坛首页</a>
</ul></td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&output("$boardname - 用户投票",\$output);
exit;

sub shortmessage #给用户发短消息（调用参数：发送人、收取人、主题、内容）
{
	my ($sendername, $receivemember, $topic, $content) = @_;
	$currenttime = time;
	my $filetomake = "$lbdir$msgdir/in/$receivemember\_msg.cgi";
	$filetomake = &stripMETA($filetomake);
	&winlock($filetomake) if ($OS_USED eq "Nt");
	if (open(FILE, $filetomake))
	{
		flock(FILE, 1) if ($OS_USED eq "Unix");
		@filedata = <FILE>;
		close(FILE);
	}
	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "＊＃！＆＊$sendername\tno\t$currenttime\t$topic\t$content\n";
	foreach (@filedata)
	{
		chomp;
		print FILE "$_\n";
	}
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	undef @filedata;
	return;
}
