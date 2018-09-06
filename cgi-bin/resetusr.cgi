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
require "admin.lib.pl";

$|++;
$thisprog = "resetusr.cgi";

$query = new LBCGI;
#&ipbanned;

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&getmember($inmembername,"no");

$prestep = $query->param('prestep');
$prestep = 300 if ($prestep <= 0 );
&getadmincheck;
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
if ($membercode eq "ad" && $inpassword eq $password && lc($inmembername) eq lc($membername))
{
	my $action = $query->param('action');
	if ($action eq "process")
	{
		my @resettype = $query->param('resettype');
		@resettype = map(&cleaninput($_), @resettype);
		my $step = $query->param('step');
		$step =~ s/[^\d]//sg;
		$step ||= 1;

		opendir(DIR, "$lbdir$memdir/old");
		my @memberfiles = readdir(DIR);
		close(DIR);
		@memberfiles = grep(/\.cgi$/i, @memberfiles);

		my $begin = ($step - 1) * $prestep;
		my $end = $step * $prestep - 1;
		$end = $#memberfiles if ($end > $#memberfiles);

		for ($begin .. $end)
		{
			($nametocheck,$no) = split(/\./,$memberfiles[$_]);
			my $namenumber = &getnamenumber($nametocheck);
			&checkmemfile($nametocheck,$namenumber);
		        unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
			unlink ("${lbdir}cache/myinfo/$nametocheck.pl");

			my $filetoopen = "$lbdir$memdir/$namenumber/$memberfiles[$_]";

			open(FILE, $filetoopen);
			my $filedata = <FILE>;
			close(FILE);
			chomp($filedata);

			my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
			($numberofposts, my $numberofreplys) = split(/\|/, $numberofposts);

			foreach my $resetname (@resettype)
			{
				if ($resetname eq "membertitle") { $datainfo = "Member"; } else { $datainfo = ""; }
				eval("\$$resetname = '$datainfo';");
			}

			if ($membername ne "" && $password ne "")
			{
				if (open(FILE, ">$filetoopen"))
				{
					print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5";
					close(FILE);
				}
			}
		}

		if ($end < $#memberfiles)
		{
			$step1=$step*$prestep;
			$step++;

			foreach (@resettype)
			{
				$typedisplay .= qq~<input type=hidden name=resettype value="$_">~;
			}
			print qq~<form name=MAINFORM action=$thisprog method=POST>
<input type=hidden name=action value="process">
<input type=hidden name=step value=$step>
<input type=hidden name=prestep value=$prestep>
$typedisplay
</form>
<script language="JavaScript">
setTimeout("MAINFORM.submit()", 2000);
</script>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>欢迎来到论坛管理中心 / 用户数据重置</b></td></tr>
<tr><td align=center><br>已经重置了$step1个用户，现在开始下面$prestep个用户的数据重置<BR>如果你的浏览器没有自动前进，请<a href="javascript: MAINFORM.submit()">点击继续</a>。</td></tr>~;
		}

		else
		{
    opendir (DIRS, "${lbdir}cache/meminfo");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/meminfo/$_");
    }
			print qq~
<tr><td bgcolor=#2159C9><font color=#ffffff><b>欢迎来到论坛管理中心 / 用户数据重置</b></td></tr>
<tr><td align=center><br><b>用户数据重置完成!</b></td></tr>~;
		}
	}

	else
	{
		print qq~<form action=$thisprog method=POST onSubmit="return confirm('你确认真的要重置所有用户的数据？')">
<input type=hidden name=action value="process">
<input type=hidden name=step value=1>
<tr><td bgColor=#2159C9 colSpan=4><font color=#ffffff><b>欢迎来到论坛管理中心 / 用户数据重置</b></td></tr>
<tr><td bgColor=#ffffff colSpan=4><b>请选择要重置的用户数据</b></td></tr>
<tr bgColor=#ffffff><td><input type=checkbox name=resettype value="numberofposts"> 发帖数量</td><td><input type=checkbox name=resettype value="numberofreplys"> 回帖数量</td><td><input type=checkbox name=resettype value="postdel"> 被删帖数量</td><td><input type=checkbox name=resettype value="rating"> 威望</td></tr>
<tr bgColor=#ffffff><td><input type=checkbox name=resettype value="mymoney"> 额外金钱</td><td><input type=checkbox name=resettype value="ebankdata"> 银行数据</td><td><input type=checkbox name=resettype value="jifen"> 额外积分</td><td><input type=checkbox name=resettype value="onlinetime"> 在线时间</td></tr>
<tr bgColor=#ffffff><td><input type=checkbox name=resettype value="userface"> 虚拟形象</td><td><input type=checkbox name=resettype value="membertitle"> 用户头衔</td><td><input type=checkbox name=resettype value="jhmp"> 江湖门派</td><td><input type=checkbox name=resettype value="signature"> 用户签名</td></tr>
<tr bgColor=#ffffff><td colSpan=4> 其他用户数据字段名 <input type=text size=12 name=resettype> <i>高级选项，比如填写 signature 将清空所有用户签名，非熟悉的请留空，不要随便填写！</i></td></tr>
<tr bgColor=#ffffff><td colSpan=4> 其他用户数据字段名 <input type=text size=12 name=resettype> <i>高级选项，非熟悉的用户请留空，不要随便填写！</i></td></tr>
<tr bgColor=#ffffff><td colSpan=4> 其他用户数据字段名 <input type=text size=12 name=resettype> <i>高级选项，非熟悉的用户请留空，不要随便填写！</i></td></tr>
<tr bgColor=#ffffff><td colSpan=4> 每次重置的用户数 <input type=text size=4 maxlength=4 name=prestep value=300> 默认：300，如果出现白屏等现象，请适当减少这个数值．</td></tr>
<tr><td bgColor=#ffffff colSpan=4 align=center><input type=submit value="重　置"></td></tr></form>~;
	}
}

else
{
	&adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;