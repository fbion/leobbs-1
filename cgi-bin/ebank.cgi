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

use strict;
use warnings;
use diagnostics;

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
if ($COOKIE_USED eq 2 && $mycookiepath ne "") {$cookiepath = $mycookiepath;}
elsif ($COOKIE_USED eq 1) {$cookiepath = "";}
else {
    $boardurltemp = $boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}

$inmembername = $query->cookie("amembernamecookie") if (!$inmembername);
$inpassword = $query->cookie("apasswordcookie") if (!$inpassword);
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle = $query->cookie("selectstyle");
$inselectstyle = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~ m/\//) || ($inselectstyle =~ m/\\/) || ($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

if ($inmembername eq "" || $inmembername eq "客人") #必须登录才能访问银行
{
    &error("普通错误&你现在的身份是访客，必须登陆以后才能访问银行！");
}
else {
    &getmember($inmembername);
    if ($inpassword ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}

$cleanmembername = $inmembername;
$cleanmembername =~ s/ /\_/sg;
$cleanmembername =~ tr/A-Z/a-z/;
$currenttime = time;

#避免恶意用户同时提交多个交易请求造成的负债存款等现象
$ebanklockfile = $lbdir . "lock/" . $cleanmembername . "_ebank.lck";
if (-e $ebanklockfile) {
    &myerror("银行错误&请不要同时在银行进行多笔交易！") if ($currenttime < (stat($ebanklockfile))[9] + 3);
}
open(LOCKCALFILE, ">$ebanklockfile");
print LOCKCALFILE "1;";
close(LOCKCALFILE);
#END防刷

#用户金钱
$myallmoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

#依次为账户状态（空值：未开户，1；正常，-1：账户冻结），存款，存款时间，贷款、贷款时间，贷款抵押积分值，最近数次交易时间，预留了五个变量以便以后开发新功能比如定期存款、用户是否保密自己的存款
($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
unless ($mystatus eq "1" || $mystatus eq "-1" || $ebankdata eq "") {
    ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = "";
}
if ($mystatus) {
    $mysavedays = &getbetween($mysavetime, $currenttime);
    $mysaveaccrual = int($mysaves * $banksaverate * $mysavedays);
    if ($myloan) {
        $myloandays = &getbetween($myloantime, $currenttime) + 1;
        if ($myloandays > $bankloanmaxdays) {
            #如果贷款过期
            &dooutloan($cleanmembername);
            $myallmoney -= $myloan;
            $rating -= $myloanrating;
            $myloan = 0;
        }
        else {
            $myloanaccrual = int($myloan * $bankloanrate * $myloandays);
        }
    }
}

#自动冻结发言被屏蔽用户、禁言用户（监狱中的犯人剥夺金融权利？:D）
$mystatus = -1 if (($membercode eq "banned" || $membercode eq "masked") && $mystatus == 1);

#检查过期贷款
if (-e $lbdir . "ebankdata/allloan.cgi") {
    &winlock($lbdir . "ebankdata/allloan.cgi") if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    open(FILE, $lbdir . "ebankdata/allloan.cgi");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @allloan = <FILE>;
    close(FILE);
    foreach (@allloan) {
        chomp;
        ($loaner, $loantime) = split(/,/, $_);
        if (&getbetween($loantime, $currenttime) >= $bankloanmaxdays) {
            shift(@allloan);
            push(@outloan, $loaner);
        }
        else {
            last;
        }
    }
    if (@outloan) {
        open(FILE, ">" . $lbdir . "ebankdata/allloan.cgi");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach (@allloan) {
            chomp;
            print FILE $_ . "\n" if ($_);
        }
        close(FILE);
    }
    &winunlock($lbdir . "ebankdata/allloan.cgi") if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    foreach (@outloan) {
        &dooutloan($_);
    }
}
#End过期贷款

&title;
$action = $query->param('action');
my %Mode = (
    'changepass' => \&changepass, #修改取款密码
    'open'       => \&open,       #开户
    'logoff'     => \&logoff,     #销户
    'get'        => \&get,        #取款
    'save'       => \&save,       #存款
    'btrans'     => \&btrans,     #转帐
    'post'       => \&post,       #汇款
    'loan'       => \&loan,       #贷款
    'repay'      => \&repay       #偿还
);

if ($Mode{$action}) {
    $Mode{$action}->();
}
else {
    &display; #营业厅
}

unlink($ebanklockfile); #解除锁定

print header(-cookie => [ $onlineviewcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

&output($pagetitle, \$output);
exit;

sub display #营业厅
{
    my $onlineview = $query->cookie("onlineview");
    $onlineview = 0 if ($onlineview eq "");
    $onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
    $onlineviewcookie = cookie(-name => "onlineview", -value => "$onlineview", -path => "$cookiepath/", -expires => "+30d");
    my $onlinetitle = $onlineview == 1 ? "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>关闭详细列表</font></a>]" : "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>显示详细列表</font></a>]";

    #取得总存款信息
    my $allusers = 0;
    my $allsaves = 0;
    if (-e $lbdir . "ebankdata/allsaves.cgi") {
        open(FILE, $lbdir . "ebankdata/allsaves.cgi");
        my $allinfo = <FILE>;
        close(FILE);
        chomp($allinfo);
        ($allusers, $allsaves) = split(/,/, $allinfo);
    }

    #取得排名信息
    my @maxusers;
    my @maxsaves;
    if (-e $lbdir . "ebankdata/order.cgi") {
        open(FILE, $lbdir . "ebankdata/order.cgi");
        my @orders = <FILE>;
        close(FILE);
        for ($i = 0; $i < @orders && $i < $bankmaxdisplay; $i++) {
            chomp($orders[$i]);
            ($maxusers[$i], $maxsaves[$i]) = split(/\t/, $orders[$i]);
        }
    }

    my $banksave100rate = $banksaverate * 100;
    my $bankloan100rate = $bankloanrate * 100;
    my $banktrans100rate = $banktransrate * 100;
    my $bankpost100rate = $bankpostrate * 100;

    my $helpurl = &helpfiles("银行");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></span>~;

    my $freshtime = $query->cookie("freshtime");
    if ($freshtime ne "") {
        my $autofreshtime = $freshtime * 60 - 1;
        $autofreshtime = 60 if ($autofreshtime < 60);
        my $refreshnow = qq~<meta http-equiv="refresh" content="$autofreshtime;">~;
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    unless (-e "$filetoopens.lck") {
        $screenmode = $query->cookie("screenmode");
        $screenmode = 8 if ($screenmode eq "");
        &whosonline("$inmembername\t$bankname\t$bankname\t银行营业大厅");
        $membertongji =~ s/本分论坛/$bankname/o;
        undef $memberoutput if ($onlineview != 1);
    }
    else {
        $memberoutput = "";
        $membertongji = " <b>由于服务器繁忙，所以银行营业大厅的在线数据暂时不提供显示。</b>";
        $onlinetitle = "";
    }

    $output .= qq~$refreshnow
	<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=$navfontcolor><a href=leobbs.cgi>$boardname</a> → $bankname</td><td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center><font face=$font color=$fontcolormisc><b>欢迎光临$bankname营业大厅</b></font></td></tr>
<tr>
	<td bgcolor=$forumcolorone width=92%><font color=$titlefontcolor>$membertongji　 $onlinetitle</td>
	<td bgcolor=$forumcolorone width=8% align=center><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 width=40 height=12></a></td>
</tr>~;
    $output .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><table cellPadding=1 cellSpacing=0 border=0>$memberoutput</table><script language="JavaScript"> function O9(id) {if(id != "") window.open("profile.cgi?action=show&member=" + id);}</script></td></tr>~ if ($onlineview == 1 && $memberoutput);
    my $waitress = int(&myrand(10)) + 1;
    $waitress = "$imagesurl/ebank/mm$waitress.gif";
    if ($bankgetpass ne "") {
        $promptpassword = qq~prompt("请输入你的取款密码:", "")~;
        $promptchange = "修改个人取款密码";
    }
    else {
        $promptpassword = '1';
        $promptchange = "创建个人取款密码";
    }
    $output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><br>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 border=0 width=100%>
<tr><td bgcolor=$forumcolortwo valign=middle colspan=2 align=center $catbackpic><font face=$font color=$fontcolormisc>
<script language="JavaScript" src="$imagesurl/ebank/fader.js"></script>
<script language="JavaScript" type="text/javascript">
prefix="";
arNews = ["$bankmessage", "", "<b><font color=#99ccff>单笔交易额： 最低 <i>$bankmindeal</i> $moneyname，最高 <i>$bankmaxdeal</i> $moneyname　24小时最大交易次数： $bankmaxdaydo</font></b>", "", "<b><font color=#885200>当前存款日利率： <i>$banksave100rate</i>%　当前贷款日利率： <i>$bankloan100rate</i>%　贷款偿还期限： <i>$bankloanmaxdays</i> 天以内</font></b>", "", "<b><font color=green>转账手续费率： <i>$banktrans100rate</i>%　汇款手续费率： <i>$bankpost100rate</i>%　(最低 <i>$bankmindeal</i> $moneyname)</font></b>", ""];
</script>
<span id="elFader" style="position:relative;visibility:hidden; height:16" ></span></font>
</td></tr>
<tr>
	<td bgcolor=$miscbacktwo width=260 rowspan=4 valign=top>
		<table><tr><td><font face=$font color=$fontcolormisc><br>　现任行长： <font color=#990000>$bankmanager</font><br><br>　客户数量： $allusers<br><br>　存款总额：<br>　 <font color=#000099><i>$allsaves</i></font> $moneyname<br></td><td width=40% align=center><img src=$waitress width=90 height=90 alt="这是正在给您服务的当班营业员MM:)" OnClick="DoKiss()"></td></tr>
		<tr><td colspan=2><br>　当前时间： <span id=showtime></span></td></tr>
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
	if (confirm('这将把你所有的存款和累计利息加到你的现金上，\\n如果你在本行有贷款，必须先还贷以后才能销户。\\n是否真的要销户？'))
		if (mypass = $promptpassword)
			location.href = "$thisprog?action=logoff&getpass=" + mypass;
}
function PromptChangePass()
{
	if (mypass = $promptpassword)
		if (newpass = prompt("请输入新的取款密码:", ""))
			if (newpass2 = prompt("请再次输入新的取款密码:", ""))
				if (newpass != newpass2) alert("两次输入的新密码不一致！");
				else location.href = "$thisprog?action=changepass&getpass=" + mypass + "&newpass=" + newpass;
}
--></script>~;

    if ($mystatus) {
        $output .= qq~<tr><td align=center colspan=2><br><table border=1 cellPadding=10 cellSpacing=3><tr><td style="line-height: 140%"><font color=#000066>个人财务状况</font>　　　　<a href=# OnClick="PromptChangePass()"><font color=blue>$promptchange</font></a><br>~;
        if ($mystatus == 1) {
            $output .= qq~<font color=green>账户状态　　　　　　正常使用</font><br>~;
        }
        else {
            $output .= qq~<font color=red>账户状态　　　　　　暂时冻结</font><br>~;
        }
        $output .= qq~当前现金　　　　　　<i>$myallmoney</i> $moneyname<br>~;
        $output .= qq~活期存款　　　　　　<i>$mysaves</i> $moneyname<br>累计时间和利息　　　<i>$mysavedays</i> 天共 <i>$mysaveaccrual</i> $moneyname<br>~;
        $output .= qq~<font color=#ff99cc>当前贷款　　　　　　<i>$myloan</i> $moneyname</font><br><font color=#ff99cc>累计时间和利息　　　<i>$myloandays</i> 天共 <i>$myloanaccrual</i> $moneyname</font><br>~ if ($myloan);
        $output .= qq~</td></tr></table><br></td></tr>~;
    }
    $output .= qq~<tr><td colspan=2 align=center><a href=setbank.cgi><font color=blue>进入银行管理中心</font></a></td></tr>~ if (($membercode eq "ad" && $bankadminallow ne "manager") || ($membercode eq "smo" && $bankadminallow eq "all") || ",$bankmanager," =~ /,$inmembername,/i);
    $output .= qq~<tr><td colspan=2><hr width=250></td></tr><tr><td colspan=2 align=center><font color=#7700ff>$bankname杰出客户<br><br></font></td></tr><tr><td bgcolor=$titlecolor align=center>客 户 帐 号</td><td bgcolor=$titlecolor align=center>当 前 存 款</td></tr>~;

    for ($i = 1; $i <= @maxusers; $i++) {
        $output .= qq~<tr><td bgcolor=$miscbackone>　$i. <a href=profile.cgi?action=show&member=~ . uri_escape($maxusers[$i - 1]) . qq~ target=_blank>$maxusers[$i - 1]</a></td><td bgcolor=$miscbackone>&nbsp;<i>$maxsaves[$i - 1]</i></td></tr>~;
    }
    $output .= qq~<tr><td colspan=2 align=center><br><br></td></tr></table></td>~;

    if ($bankopen ne "on") {
        $output .= qq~
	<td bgcolor=$miscbackone align=center><font color=red size=4><b>银行盘点中，暂时停业，请稍候访问！</b></font></td>
</tr>~;
    }
    else {
        unless ($mystatus) {
            $output .= qq~
	<td bgcolor=$miscbackone align=center><font size=4>你当前拥有 <i>$myallmoney</i> $moneyname现金，<br>开户至少需要 <i>$bankmindeal</i> $moneyname现金才能完成。<br><br>你需要<a href=$thisprog?action=open><font color=#0000ff><b>开户</b></font></a>后才能使用本行的各项业务。</font></td>
</tr>~;
        }
        elsif ($mystatus == -1) {
            if ($membercode eq "banned" || $membercode eq "masked") {
                $output .= qq~
	<td bgcolor=$miscbackone align=center><font size=4>由于你被禁止发言，所以你的账号被银行自动冻结。</font></td>
</tr>~;
            }
            else {
                $output .= qq~
	<td bgcolor=$miscbackone align=center><font size=4>由于你违反了某些规定进行非法金融活动，<br>你的账号被行长暂时冻结，请尽快与其联系。</font></td>
</tr>~;
            }
        }
        else {
            $output .= qq~
	<td bgcolor=$miscbackone valign=top>　<img src="$imagesurl/ebank/bank.gif" width=16><font color=#99ccff>活期储蓄</font><img src="$imagesurl/ebank/bank.gif" width=16>　１号柜台　 本柜台同时兼办销户请点<a href=# OnClick="PromptLogOff()"><font color=#cc0000><b>这里</b></font></a><hr><br>
	<form name=save action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="save">　 我要存入现金:　<input type=text size=10 name=savemoney> $moneyname　　<input name=submit type=submit value=存　入 style="background:#99ccff">　<input name=reset type=reset value=重　填 style="background:#cccccc"></form>
	<form name=get action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="get"><input type=hidden name=getpass>　 我要取出存款:　<input type=text size=10 name=getmoney> $moneyname　　<input name=submit type=submit value=取　出 style="background:#99ccff" OnClick="return PromptGetPass('get')">　<input name=reset type=reset value=重　填 style="background:#cccccc"></form>
	</td>
</tr>
<tr>
	<td bgcolor=$miscbacktwo valign=top>　<img src="$imagesurl/ebank/bank.gif" width=16><font color=green>转帐汇款</font><img src="$imagesurl/ebank/bank.gif" width=16>　２号柜台　 本柜台同时兼办销户请点<a href=# OnClick="PromptLogOff()"><font color=#cc0000><b>这里</b></font></a><hr><br>~;

            if ($rating < $banktransneed && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo") {
                $output .= qq~　 行长设定了只有威望达到 $banktransneed 以上的会员和版主才能使用转帐和汇款功能！<br><br>~;
            }
            else {
                #好友列表处理部分
                &getmyfriendlist;
                my $friendlist1 = qq~<select name=friends OnChange="btransfriend();"><option>我的好友</option>~;
                my $friendlist2 = qq~<select name=friends OnChange="postfriend();"><option>我的好友</option>~;
                foreach (@myfriendlist) {
                    $friendlist1 .= qq~<option value="$_">$_</option>~;
                    $friendlist2 .= qq~<option value="$_">$_</option>~;
                }
                $friendlist1 .= qq~</select>~;
                $friendlist2 .= qq~</select>~;

                $output .= qq~
	<form name=btrans action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="btrans"><input type=hidden name=getpass>　 我要转帐:　<input type=text size=10 name=btransmoney> $moneyname　给　<input type=text size=12 name=btransuser>　$friendlist1<br>　 转账附言:　<input type=text size=30 maxsize=50 name=btransmessage>　　<input name=submit type=submit value=转　出 style="background:green" OnClick="return PromptGetPass('btrans')">　<input name=reset type=reset value=重　填 style="background:#cccccc"></form>
	<form name=post action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="post"><input type=hidden name=getpass>　 我要汇款:　<input type=text size=10 name=postmoney> $moneyname　给　<input type=text size=12 name=postuser>　$friendlist2<br>　 汇款附言:　<input type=text size=30 maxsize=50 name=postmessage>　　<input name=submit type=submit value=汇　出 style="background:green" OnClick="return PromptGetPass('post')">　<input name=reset type=reset value=重　填 style="background:#cccccc"></form>~;
            }

            $output .= qq~</td>
</tr>
<tr>~;
            if ($myloan) {
                $output .= qq~
	<td bgcolor=$miscbackone valign=top>　<img src="$imagesurl/ebank/bank.gif" width=16><font color=#ff7777>社区信贷</font><img src="$imagesurl/ebank/bank.gif" width=16>　３号柜台<hr><br>
	　 偿还你的贷款请<a href=$thisprog?action=repay><font color=#ff99cc>点击这里</font></a>。<br><br>
	</td>
</tr>~;
            }
            else {
                $output .= qq~<td bgcolor=$miscbackone valign=top>　<img src="$imagesurl/ebank/bank.gif" width=16><font color=red>社区信贷</font><img src="$imagesurl/ebank/bank.gif" width=16>　３号柜台<hr><br>~;

                if ($bankallowloan eq "yes") {
                    if ($rating > 0) {
                        $output .= qq~<form name=loan action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="loan">　 我要抵押　 <select size=1 name=loanrate>~;
                        for ($i = 1; $i <= $rating; $i++) {
                            $output .= qq~<option value=$i>$i</option>~;
                        }
                        $output .= qq~</select>　点威望来贷款:　<input type=text size=10 name=loanmoney> $moneyname　　<input type=text size=1 style="width: 1px; height: 1px"><input name=submit type=submit value=决定了 style="background:#ff7777"><br>　 ( 每点威望允许最多抵押 $bankrateloan $moneyname )</form>~;
                    }
                    else {
                        $output .= qq~　 你没有威望点来抵押，无法贷款！<br><br>~;
                    }
                }
                else {
                    $output .= qq~　 行长已经停用了贷款服务！<br><br>~;
                }
                $output .= qq~</td></tr>~;
            }

            $output .= qq~<tr><td bgcolor=$miscbacktwo valign=top>　<img src="$imagesurl/ebank/bank.gif" width=16><font color=#000066>个人账目</font><img src="$imagesurl/ebank/bank.gif" width=16>　以下是你最近的银行交易记录。<hr>~;
            $output .= qq~<table border=1 width=100% bordercolor=#cccccc><tr><td align=center width=30%>交易时间</td><td align=center width=30%>事件</td><td align=center width=20%>金额($moneyname)</td><td align=center width=20%>余额($moneyname)</td></tr>~;
            if (-e $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi") {
                open(FILE, $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi");
                my @mylogs = <FILE>;
                close(FILE);
                foreach (@mylogs) {
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
    $pagetitle = "$boardname - $bankname营业大厅";

    return;
}

sub changepass #修改取款密码
{
    my $getpass = $query->param('getpass');
    my $newpass = $query->param('newpass');
    &myerror("银行错误&你没在本银行开过户，哪来的取款密码？") unless ($mystatus);
    &myerror("银行错误&你输入的旧的取款密码错误！") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
    &myerror("银行错误&你输入的新的取款密码为空？") if ($newpass eq "");
    &myerror("银行错误&你输入的新的取款密码含有不合适的非法字符！") if ($newpass =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]/is);
    &myerror("银行错误&你输入的新的取款密码太长！") if (length($newpass) > 16);
    &updateuserinfo($cleanmembername, 0, 0, "nochange", 0, "nochange", 0, "nochange", 0, "no", $newpass);
    &printjump("设定取款密码成功");
    return;
}

sub open #开户
{
    &myerror("银行错误&银行盘点，暂时停业，无法开户！") unless ($bankopen eq "on");
    &myerror("银行错误&你已经在本银行开过户了！") if ($mystatus);
    @mybankdotimes = split(/\|/, $mybankdotime);
    &myerror("银行错误&你在24小时内的交易次数已经超过了允许的最大值 $bankmaxdaydo！") if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
    &myerror("银行错误&你的现金不够开户最低要求！") if ($myallmoney < $bankmindeal);

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$inmembername\t$bankname\tnone\t在银行开户") unless (-e "$filetoopens.lck");

    &updateuserinfo($cleanmembername, 0, -$bankmindeal, 1, $bankmindeal, $currenttime, 0, "", 0, "yes");
    &updateallsave(1, $bankmindeal);

    &logpriviate("开户", $bankmindeal, $bankmindeal);
    &logaction($inmembername, "开户成功，存入 $bankmindeal $moneyname。");

    &order($cleanmembername, $bankmindeal);
    &printjump("开户成功");
    return;
}

sub logoff #销户
{
    my $getpass = $query->param('getpass');
    &myerror("银行错误&银行盘点，暂时停业，无法销户！") unless ($bankopen eq "on");
    &myerror("银行错误&你没在本银行开过户，怎么销户？") unless ($mystatus);
    &myerror("银行错误&你的帐户被暂时冻结，请与行长联系！") if ($mystatus == -1);
    &myerror("银行错误&你输入的取款密码错误！") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
    @mybankdotimes = split(/\|/, $mybankdotime);
    &myerror("银行错误&你在24小时内的交易次数已经超过了允许的最大值 $bankmaxdaydo！") if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
    &myerror("银行错误&你必须先偿还在本银行的贷款后才能销户！") if ($myloan);

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$inmembername\t$bankname\tnone\t在银行销户") unless (-e "$filetoopens.lck");

    &updateuserinfo($cleanmembername, 0, $mysaves + $mysaveaccrual, "", -$mysaves, "", 0, "", 0, "yes");
    &updateallsave(-1, -$mysaves);

    my $filetodel = $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi";
    unlink($filetodel);

    &logaction($inmembername, "销户成功，取走存款 $mysaves $moneyname，结算利息 $mysaveaccrual $moneyname。");

    &order($cleanmembername, 0);
    &printjump("销户成功");
    return;
}

sub get #取款
{
    my $getmoney = $query->param('getmoney');
    my $getpass = $query->param('getpass');
    &myerror("银行错误&银行盘点，暂时停业，无法取款！") unless ($bankopen eq "on");
    &myerror("银行错误&你没在本银行开过户，怎么取款？") unless ($mystatus);
    &myerror("银行错误&你的帐户被暂时冻结，请与行长联系！") if ($mystatus == -1);
    &myerror("银行错误&你输入的取款密码错误！") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
    @mybankdotimes = split(/\|/, $mybankdotime);
    &myerror("银行错误&你在24小时内的交易次数已经超过了允许的最大值 $bankmaxdaydo！") if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
    &myerror("银行错误&取款数额输入错误，请检查！") if ($getmoney =~ /[^0-9]/ or $getmoney eq "");
    &myerror("银行错误&你没有那么多存款可以取出，如果不销户，你的户头必须至少存有 $bankmindeal $moneyname！") if ($getmoney > $mysaves + $mysaveaccrual - $bankmindeal);
    &myerror("银行错误&取款数额超过本行最大单笔交易额 $bankmaxdeal $moneyname") if ($getmoney > $bankmaxdeal);
    &myerror("银行错误&取款数额小于本行最小单笔交易额 $bankmindeal $moneyname") if ($getmoney < $bankmindeal);

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$inmembername\t$bankname\tnone\t在银行取款") unless (-e "$filetoopens.lck");

    &updateuserinfo($cleanmembername, 0, $getmoney, "nochange", $mysaveaccrual - $getmoney, $currenttime, 0, "nochange", 0, "yes");
    &updateallsave(0, $mysaveaccrual - $getmoney);

    &logpriviate("结息", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
    &logpriviate("取出", -$getmoney, $mysaves + $mysaveaccrual - $getmoney);
    &logaction($inmembername, "<font color=#99ccff>取出存款 $getmoney $moneyname，同时结算利息 $mysaveaccrual $moneyname。</font>");

    &order($cleanmembername, $mysaves + $mysaveaccrual - $getmoney);
    &printjump("取款成功");
    return;
}

sub save #存款
{
    my $savemoney = $query->param('savemoney');
    &myerror("银行错误&银行盘点，暂时停业，无法存款！") unless ($bankopen eq "on");
    &myerror("银行错误&你没在本银行开过户，怎么存款？") unless ($mystatus);
    &myerror("银行错误&你的帐户被暂时冻结，请与行长联系！") if ($mystatus == -1);
    @mybankdotimes = split(/\|/, $mybankdotime);
    &myerror("银行错误&你在24小时内的交易次数已经超过了允许的最大值 $bankmaxdaydo！") if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
    &myerror("银行错误&存款数额输入错误，请检查！") if ($savemoney =~ /[^0-9]/ or $savemoney eq "");
    &myerror("银行错误&你没有那么多现金可以存！") if ($savemoney > $myallmoney);
    &myerror("银行错误&存款数额超过本行最大单笔交易额 $bankmaxdeal $moneyname") if ($savemoney > $bankmaxdeal);
    &myerror("银行错误&存款数额小于本行最小单笔交易额 $bankmindeal $moneyname") if ($savemoney < $bankmindeal);

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$inmembername\t$bankname\tnone\t在银行存款") unless (-e "$filetoopens.lck");

    &updateuserinfo($cleanmembername, 0, -$savemoney, "nochange", $mysaveaccrual + $savemoney, $currenttime, 0, "nochange", 0, "yes");
    &updateallsave(0, $mysaveaccrual + $savemoney);

    &logpriviate("结息", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
    &logpriviate("存入", $savemoney, $mysaves + $mysaveaccrual + $savemoney);
    &logaction($inmembername, "<font color=#99ccff>存入存款 $savemoney $moneyname，同时结算利息 $mysaveaccrual $moneyname。</font>");

    &order($cleanmembername, $mysaves + $mysaveaccrual + $savemoney);
    &printjump("存款成功");
    return;
}

sub btrans #转帐
{
    my $btransuser = $query->param('btransuser');
    my $btransmoney = $query->param('btransmoney');
    my $btransmessage = $query->param('btransmessage');
    my $getpass = $query->param('getpass');
    $btransuser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    &myerror("银行错误&银行盘点，暂时停业，无法转帐！") unless ($bankopen eq "on");
    &myerror("银行错误&你没在本银行开过户，怎么转帐？") unless ($mystatus);
    &myerror("银行错误&你的帐户被暂时冻结，请与行长联系！") if ($mystatus == -1);
    &myerror("银行错误&你输入的取款密码错误！") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
    @mybankdotimes = split(/\|/, $mybankdotime);
    &myerror("银行错误&你在24小时内的交易次数已经超过了允许的最大值 $bankmaxdaydo！") if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
    &myerror("银行错误&转账附言太长了！") if (length($btransmessage) > 50);
    &myerror("银行错误&你的信用度（威望）不够高，无法使用转帐业务！") if ($rating < $banktransneed && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo");
    &myerror("银行错误&转帐数额输入错误，请检查！") if ($btransmoney =~ /[^0-9]/ or $btransmoney eq "");
    my $banktranscharge = int($banktransrate * $btransmoney + 0.5); #四舍五入:)
    $banktranscharge = $bankmindeal if ($banktranscharge < $bankmindeal);
    &myerror("银行错误&你没有那么多存款用来转帐和支付转帐费用，如果不销户，你的户头必须至少存有 $bankmindeal $moneyname！") if ($btransmoney + $banktranscharge > $mysaves + $mysaveaccrual - $bankmindeal);
    &myerror("银行错误&转帐数额超过本行最大单笔交易额 $bankmaxdeal $moneyname") if ($btransmoney > $bankmaxdeal);
    &myerror("银行错误&转帐数额小于本行最小单笔交易额 $bankmindeal $moneyname") if ($btransmoney < $bankmindeal);

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$inmembername\t$bankname\tnone\t在银行转账") unless (-e "$filetoopens.lck");

    $btransuser =~ s/ /\_/sg;
    $btransuser =~ tr/A-Z/a-z/;
    &myerror("银行错误&自己给自己转什么帐！") if ($btransuser eq $cleanmembername);
    $btransmessage = &unHTML($btransmessage);

    &getmember($btransuser);
    &myerror("银行错误&转帐对象用户不存在！") if ($userregistered eq "no");
    my ($tmystatus, $tmysaves, $tmysavetime, $tmyloan, $tmyloantime, $tmyloanrating, $tbankadd1, $tbankadd2, $tbankadd3, $tbankadd4, $tbankadd5) = split(/,/, $ebankdata);
    &myerror("银行错误&转帐对象用户并没有在本行开户！你可以考虑使用汇款业务。") if ($tmystatus eq "");
    &myerror("银行错误&对方账户已经被冻结，无法给他汇款！") if ($tmystatus == -1 || $membercode eq "banned" || $membercode eq "masked");
    my $tmysavedays = &getbetween($tmysavetime, $currenttime);
    my $tmysaveaccrual = int($tmysaves * $banksaverate * $tmysavedays);

    &updateuserinfo($cleanmembername, 0, 0, "nochange", $mysaveaccrual - $btransmoney - $banktranscharge, $currenttime, 0, "nochange", 0, "yes");
    &updateuserinfo($btransuser, 0, 0, "nochange", $tmysaveaccrual + $btransmoney, $currenttime, 0, "nochange", 0, "no");
    &updateallsave(0, $mysaveaccrual + $tmysaveaccrual - $banktranscharge);

    &bankmessage($btransuser, "转帐通知", "　　$inmembername 向你在本行的帐户里转入了 $btransmoney $moneyname存款，现在已经到帐，请查收！<br>　　转账附言：<font color=green>$btransmessage</font>。");

    &logpriviate("结息", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
    &logpriviate("转帐手续费", -$banktranscharge, $mysaves + $mysaveaccrual - $banktranscharge);
    &logpriviate("转出到$btransuser", -$btransmoney, $mysaves + $mysaveaccrual - $banktranscharge - $btransmoney);
    &order($cleanmembername, $mysaves + $mysaveaccrual - $banktranscharge - $btransmoney, $btransuser, $tmysaves + $tmysaveaccrual + $btransmoney);

    $cleanmembername = $btransuser;
    &logpriviate("结息", $tmysaveaccrual, $tmysaves + $tmysaveaccrual) if ($tmysaveaccrual != 0);
    &logpriviate("从$inmembername转入", $btransmoney, $tmysaves + $tmysaveaccrual + $btransmoney);

    &logaction($inmembername, "<font color=green>转出存款 $btransmoney $moneyname给 $btransuser，交纳手续费 $banktranscharge $moneyname，同时结算转出方结算利息 $mysaveaccrual $moneyname，转入方结算利息 $tmysaveaccrual $moneyname。转账附言：$btransmessage</font>");
    &printjump("转帐成功");
    return;
}

sub post {
    my $postuser = $query->param('postuser');
    my $postmoney = $query->param('postmoney');
    my $postmessage = $query->param('postmessage');
    my $getpass = $query->param('getpass');
    $postuser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    &myerror("银行错误&银行盘点，暂时停业，无法汇款！") unless ($bankopen eq "on");
    &myerror("银行错误&你没在本银行开过户，怎么汇款？") unless ($mystatus);
    &myerror("银行错误&你的帐户被暂时冻结，请与行长联系！") if ($mystatus == -1);
    &myerror("银行错误&你输入的取款密码错误！") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
    @mybankdotimes = split(/\|/, $mybankdotime);
    &myerror("银行错误&你在24小时内的交易次数已经超过了允许的最大值 $bankmaxdaydo！") if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
    &myerror("银行错误&汇款附言太长了！") if (length($postmessage) > 50);
    &myerror("银行错误&你的信用度（威望）不够高，无法使用汇款业务！") if ($rating < $banktransneed && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo");
    &myerror("银行错误&汇款数额输入错误，请检查！") if ($postmoney =~ /[^0-9]/ or $postmoney eq "");
    my $bankpostcharge = int($bankpostrate * $postmoney + 0.5); #四舍五入:)
    $bankpostcharge = $bankmindeal if ($bankpostcharge < $bankmindeal);
    &myerror("银行错误&你没有那么多存款用来汇款和支付汇款费用，如果不销户，你的户头必须至少存有 $bankmindeal $moneyname！") if ($postmoney + $bankpostcharge > $mysaves + $mysaveaccrual - $bankmindeal);
    &myerror("银行错误&汇款数额超过本行最大单笔交易额 $bankmaxdeal $moneyname") if ($postmoney > $bankmaxdeal);
    &myerror("银行错误&汇款数额小于本行最小单笔交易额 $bankmindeal $moneyname") if ($postmoney < $bankmindeal);

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$inmembername\t$bankname\tnone\t在银行汇款") unless (-e "$filetoopens.lck");

    $postuser =~ s/ /\_/sg;
    $postuser =~ tr/A-Z/a-z/;
    &myerror("银行错误&自己给自己汇个什么款！") if ($postuser eq $cleanmembername);
    $postmessage = &unHTML($postmessage);

    &getmember($postuser);
    &myerror("银行错误&汇款对象用户不存在！") if ($userregistered eq "no");

    &updateuserinfo($cleanmembername, 0, 0, "nochange", $mysaveaccrual - $postmoney - $bankpostcharge, $currenttime, 0, "nochange", 0, "yes");
    &updateuserinfo($postuser, 0, $postmoney, "nochange", 0, "nochange", 0, "nochange", 0, "no");
    &updateallsave(0, $mysaveaccrual - $postmoney - $bankpostcharge);

    &bankmessage($postuser, "汇款单", "　　$inmembername 从本行给你汇寄了 $postmoney $moneyname现金，现在已经到位，请查收！<br>　　汇款附言：<font color=green>$postmessage</font>。");

    &logpriviate("结息", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
    &logpriviate("汇款手续费", -$bankpostcharge, $mysaves + $mysaveaccrual - $bankpostcharge);
    &logpriviate("汇出到$postuser", -$postmoney, $mysaves + $mysaveaccrual - $bankpostcharge - $postmoney);
    &logaction($inmembername, "<font color=green>给用户 $postuser 汇寄了$postmoney $moneyname，交纳手续费 $bankpostcharge $moneyname，同时结算利息 $mysaveaccrual $moneyname。汇款附言：$postmessage</font>");

    &order($cleanmembername, $mysaves + $mysaveaccrual - $bankpostcharge - $postmoney);
    &printjump("汇款成功");
    return;
}

sub loan #贷款
{
    my $loanrate = $query->param('loanrate');
    my $loanmoney = $query->param('loanmoney');
    &myerror("银行错误&银行盘点，暂时停业，无法贷款！") unless ($bankopen eq "on");
    &myerror("银行错误&你没在本银行开过户，怎么贷款？") unless ($mystatus);
    &myerror("银行错误&你的帐户被暂时冻结，请与行长联系！") if ($mystatus == -1);
    @mybankdotimes = split(/\|/, $mybankdotime);
    &myerror("银行错误&你在24小时内的交易次数已经超过了允许的最大值 $bankmaxdaydo！") if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
    &myerror("银行错误&贷款服务已经被行长停用！") if ($bankallowloan ne "yes");
    &myerror("银行错误&你当前还有贷款没有还清，不允许新的贷款！") if ($myloan);
    &myerror("银行错误&抵押威望输入错误！") if ($loanrate =~ /[^0-9]/ or $loanrate eq "");
    &myerror("银行错误&抵押威望输入错误！") if ($loanrate == 0);
    &myerror("银行错误&你没有这么多威望点数用来抵押！") if ($loanrate > $rating);
    &myerror("银行错误&贷款金额输入错误！") if ($loanmoney =~ /[^0-9]/ or $loanmoney eq "");
    &myerror("银行错误&用来抵押贷款值的威望点数不够！") if ($loanmoney > $bankrateloan * $loanrate);
    &myerror("银行错误&贷款金额超过本行最大单笔交易额 $bankmaxdeal $moneyname") if ($loanmoney > $bankmaxdeal);
    &myerror("银行错误&贷款金额小于本行最小单笔交易额 $bankmindeal $moneyname") if ($loanmoney < $bankmindeal);

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$inmembername\t$bankname\tnone\t在银行贷款") unless (-e "$filetoopens.lck");

    &updateuserinfo($cleanmembername, 0, $loanmoney, "nochange", 0, "nochange", $loanmoney, $currenttime, $loanrate, "yes");
    my $filetomake = $lbdir . "ebankdata/allloan.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    open(FILE, ">>$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "$cleanmembername,$currenttime\n";
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");

    &bankmessage($cleanmembername, "贷款通知", "　　你在本行抵押了 $loanrate 点威望贷款 $loanmoney $moneyname，现在贷款已经发放到你的现金，请在从今天开始的 $bankloanmaxdays 天以内及时归还贷款，否则逾期系统将自动强制收回贷款并且扣除你抵押的威望。");

    &logpriviate("贷款", $loanmoney, $mysaves);
    &logaction($inmembername, "<font color=#ff7777>向银行抵押了 $loanrate 点威望申请了 $loanmoney $moneyname贷款，已发放至其现金。</font>");
    &printjump("贷款成功");
    return;
}

sub repay {
    &myerror("银行错误&银行盘点，暂时停业，无法偿还贷款！") unless ($bankopen eq "on");
    &myerror("银行错误&你没在本银行开过户，还什么贷款？") unless ($mystatus);
    &myerror("银行错误&你的帐户被暂时冻结，请与行长联系！") if ($mystatus == -1);
    @mybankdotimes = split(/\|/, $mybankdotime);
    &myerror("银行错误&你在24小时内的交易次数已经超过了允许的最大值 $bankmaxdaydo！") if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
    &myerror("银行错误&你没有贷过款,还啥？") unless ($myloan);
    &myerror("银行错误&你的现金不够偿还贷款！") if ($myallmoney < $myloan + $myloanaccrual);

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$inmembername\t$bankname\tnone\t在银行还贷") unless (-e "$filetoopens.lck");

    &updateuserinfo($cleanmembername, 0, -($myloan + $myloanaccrual), "nochange", 0, "nochange", -$myloan, "", -$myloanrating, "no");

    my $filetoopen = $lbdir . "ebankdata/allloan.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
        open(FILE, $filetoopen);
        flock(FILE, 1) if ($OS_USED eq "Unix");
        my @filedata = <FILE>;
        close(FILE);
        open(FILE, ">$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach (@filedata) {
            chomp;
            print FILE $_ . "\n" unless ($_ =~ /^$cleanmembername,/i);
        }
        close(FILE);
        &winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    }

    &logpriviate("还贷", $myloan + $myloanaccrual, $mysaves);
    &logaction($inmembername, "<font color=#ff7777>向银行偿还了 $myloan $moneyname贷款，支付利息 $myloanaccrual $moneyname。</font>");
    &printjump("还贷成功");
    return;
}

#####以下为公用函数段

sub order #银行排序程序
{
    my ($adduser1, $addsave1, $adduser2, $addsave2) = @_;
    my %ordersaves;

    my $filetoopen = $lbdir . "ebankdata/order.cgi";
    my $filetoopens = &lockfilename($filetoopen);
    return if (-e $filetoopens . ".lck");
    &winlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    if (-e $filetoopen) {
        open(FILE, $filetoopen);
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @orderdata = <FILE>;
        close(FILE);
    }
    foreach (@orderdata) {
        chomp;
        my ($tempuser, $tempsave) = split(/\t/, $_);
        $ordersaves{$tempuser} = $tempsave if ($tempuser ne "");
    }
    $ordersaves{$adduser1} = $addsave1 if ($adduser1 ne "");
    $ordersaves{$adduser2} = $addsave2 if ($adduser2 ne "");
    my @orderusers = sort {$ordersaves{$a} <=> $ordersaves{$b}} keys(%ordersaves);
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    for ($i = 1; $i <= $bankmaxdisplay * 2; $i++) {
        $j = @orderusers - $i;
        last if ($j < 0);
        print FILE $orderusers[$j] . "\t" . $ordersaves{$orderusers[$j]} . "\n" if ($ordersaves{$orderusers[$j]});
    }
    close(FILE);
    &winunlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    return;
}

sub getbetween #取得两个时间之间相差的天数（调用参数：开始时间，结束时间）
{
    my ($begintime, $endtime) = @_;
    my ($tmpsecond, $tmpminute, $tmphour, $tmpday, $tmpmonth, $tmpyear, $tmpwday, $tmpyday, $tmpisdst) = localtime($begintime + $timezone * 3600);
    $begintime -= ($tmphour * 3600 + $tmpminute * 60 + $tmpsecond);
    my $betweendays = int(($endtime - $begintime) / 86400);
    return $betweendays;
}

sub getmyfriendlist #取得用户好友列表
{
    my $filetoopen = $lbdir . "memfriend/" . $cleanmembername . ".cgi";
    if (-e $filetoopen) {
        open(FILE, $filetoopen);
        @myfriendlist = <FILE>;
        close(FILE);
    }

    chomp(@myfriendlist);
    foreach (@myfriendlist) {
        s/^＊＃！＆＊//sg;
    }
    return;
}

sub bankmessage #给用户发银行短消息（调用参数：收取人、主题、内容）
{
    my ($receivemember, $topic, $content) = @_;
    my @filedata;
    my $filetomake = $lbdir . $msgdir . "/in/" . $receivemember . "_msg.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    if (-e $filetomake) {
        open(FILE, $filetomake);
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @filedata = <FILE>;
        close(FILE);
    }

    @filedata = ("＊＃！＆＊$bankname\tno\t$currenttime\t$topic\t$content<br><br>　　感谢使用$bankname的优质服务。<br><br>\n", @filedata);

    open(FILE, ">$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    foreach (@filedata) {
        chomp;
        print FILE "$_\n";
    }
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");
    return;
}

sub logaction #记录银行日志（调用参数：操作人员，日志内容）
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

sub logpriviate #记入个人存折（调用参数：交易动作，金额，户头活期结余）
{
    my ($bankaction, $banknums, $banksavenum) = @_;

    my $filetomake = $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi";
    my @mylogs;
    &winlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    if (-e $filetomake) {
        open(FILE, $filetomake);

        flock(FILE, 1) if ($OS_USED eq "Unix");
        @mylogs = <FILE>;
        close(FILE);
        while (@mylogs >= $banklogpriviate) {
            pop(@mylogs);
        }
    }
    @mylogs = ("$currenttime\t$bankaction\t$banknums\t$banksavenum", @mylogs);

    open(FILE, ">$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    foreach (@mylogs) {
        chomp;
        print FILE $_ . "\n";
    }
    close(FILE);
    &winunlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    return;
}

sub dooutloan #处理用户的过期贷款（调用参数：用户名）
{
    my $loaner = shift;

    my $namenumber = &getnamenumber($loaner);
    &checkmemfile($loaner, $namenumber);
    my $filetoopen = "$lbdir$memdir/$namenumber/$loaner.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, $filetoopen);
        flock(FILE, 1) if ($OS_USED eq "Unix");
        my $filedata = <FILE>;
        close(FILE);
        chomp($filedata);
        my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
        my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

        if ($mystatus && $myloan) {
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

        if (($membername ne "") && ($password ne "")) {
            if (open(FILE, ">$filetoopen")) {
                flock(FILE, 2) if ($OS_USED eq "Unix");
                $lastgone = time;
                print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
                close(FILE);
            }
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }

    if ($mesloan) {
        $mesloantime = &shortdate($mesloantime);
        &logaction("<font color=red>银行自动处理程序</font>", "<font color=red>$loaner 于 $mesloantime 抵押 $mesloanrating 点威望借贷 $mesloan $moneyname逾期，已扣除抵押威望，并且强制追回贷款。</font>");
        &bankmessage($loaner, "贷款逾期不还通知", "　　你于 $mesloantime 在本行抵押 $mesloanrating 点威望借贷的 $mesloan $moneyname款项逾期未还，本行已按照论坛银行法扣除你抵押的威望值。<br>　　同时你的不良贷款也被强制追回，对此事件，我们深表遗憾！<br><br>");
    }
    return;
}

sub printjump #显示LB风格跳转页面（调用参数：页面主题）
{
    my $content = shift;

    $output .= qq~
	<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=$navfontcolor><a href=leobbs.cgi>$boardname</a> → <a href=ebank.cgi>$bankname</a> → $content</td><td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellPadding=6 cellSpacing=1 border=0 width=100%>
	<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>感谢选择我们的优质服务，你刚才在银行的交易已经生效！</b></font></td></tr>
	<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！：
		<ul><li><a href=$thisprog>返回银行营业大厅</a>  $pagestoshow</ul>
	</td></tr>
</table></td></tr>
</table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
    $pagetitle = "$boardname - 在银行$content";
    return;
}

sub updateallsave #利用变化量来更新总量信息
{
    my ($callusers, $callsaves) = @_;

    my $filetoopen = $lbdir . "ebankdata/allsaves.cgi";
    my $allusers = 0;
    my $allsaves = 0;
    &winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    if (-e $filetoopen) {
        open(FILE, $lbdir . "ebankdata/allsaves.cgi");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        my $allinfo = <FILE>;
        close(FILE);
        chomp($allinfo);
        ($allusers, $allsaves) = split(/,/, $allinfo);
    }

    $allusers += $callusers;
    $allsaves += $callsaves;

    if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$allusers,$allsaves";
        close(FILE);
    }
    &winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    return;
}

sub updateuserinfo #更新用户信息
{
    my ($nametocheck, $crating, $cmoney, $bankstats, $csaves, $savetime, $cloan, $loantime, $cloanrating, $allowcount, $newgetpass) = @_;
    #用户名，威望变化量，金钱变化量，更新的银行账户状态(不变化请填"nochange")，存款变化量，更新的存款时间(不变化请填"nochange")，贷款变化量，更新的贷款时间(不变化请填"nochange")，贷款抵押值变化量，是否计入银行交易次数（计入为"yes", 不计入为"no"）
    my $namenumber = &getnamenumber($nametocheck);
    &checkmemfile($nametocheck, $namenumber);

    my $filetoopen = "$lbdir$memdir/$namenumber/$nametocheck.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "+<$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        my $filedata = <FILE>;
        chomp($filedata);
        my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
        my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

        if ($allowcount eq "yes") {
            my @mybankdotimes = split(/\|/, $mybankdotime);
            @mybankdotimes = ($currenttime, @mybankdotimes);
            $mybankdotime = "";
            for (my $i = 0; $i < $bankmaxdaydo; $i++) {
                last if ($i == @mybankdotimes);
                $mybankdotime .= $mybankdotimes[$i] . "|";
            }
            chop($mybankdotime);
        }

        $rating += $crating;
        $mymoney += $cmoney;
        $mystatus = $bankstats if ($bankstats ne "nochange");
        $mysaves = 0 unless ($mysaves);
        $mysaves += $csaves;
        $mysavetime = $savetime if ($savetime ne "nochange");
        $myloan = 0 unless ($myloan);
        $myloan += $cloan;
        $myloantime = $loantime if ($loantime ne "nochange");
        $myloanrating = 0 unless ($myloanrating);
        $myloanrating += $cloanrating;
        $bankgetpass = $newgetpass if ($newgetpass ne "");

        $ebankdata = "$mystatus,$mysaves,$mysavetime,$myloan,$myloantime,$myloanrating,$mybankdotime,$bankgetpass,$bankadd2,$bankadd3,$bankadd4,$bankadd5";

        if (($membername ne "") && ($password ne "")) {
            seek(FILE, 0, 0);
            #			$lastgone = $currenttime;
            print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
            close(FILE);

            if (open(FILE, ">$lbdir$memdir/old/$nametocheck.cgi")) {
                #			$lastgone = $currenttime;
                print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
                close(FILE);
            }
        }
        else {
            close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        unlink("${lbdir}cache/myinfo/$nametocheck.pl");
        unlink("${lbdir}cache/meminfo/$nametocheck.pl");
    }
    return;
}

sub myerror {
    my $errorinfo = shift;
    unlink($ebanklockfile);
    &error($errorinfo);
    return;
}