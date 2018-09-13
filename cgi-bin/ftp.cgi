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

use warnings;
use strict;
use diagnostics;

use LBCGI;
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "data/mpic.cgi";
require "bbs.lib.pl";

opendir(DIRS, "$lbdir");
my @files = readdir(DIRS);
closedir(DIRS);
@files = grep (/^\w+?$/i, @files);
my @ftpdir = grep (/^ftpdata/i, @files);
$ftpdir = $ftpdir[0];

require "$ftpdir/conf.cgi";

$|++;
$thisprog = "ftp.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

&ipbanned;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") {$cookiepath = $mycookiepath;}
elsif ($COOKIE_USED eq 1) {$cookiepath = "";}
else {
    my $boardurltemp = $boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}

$in_member_name = $query->cookie("amembernamecookie") unless ($in_member_name);
$in_password = $query->cookie("apasswordcookie") unless ($in_password);
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t]//isg;
$cleanmembername = $in_member_name;
$cleanmembername =~ s/ /\_/sg;
$cleanmembername =~ tr/A-Z/a-z/;
$ftplockfile = "${lbdir}lock/$cleanmembername\_ftpiii.lck";
$currenttime = time;
$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

if ($in_member_name eq "" || $in_member_name eq "客人") { #检查用户身份
    &error("普通错误&访客不能查看FTP 联盟,请先登录！");
}
else {
    &getmember($in_member_name, 'no');
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    &error("普通错误&密码与用户名不相符，请重新登录！") if ($in_password ne $password);
    &error("权限错误&被屏蔽文章或禁言的用戶不允许访问 FTP 联盟！") if ($member_code eq "banned" || $member_code eq "masked");

    #避免恶意用户同时提交多个交易请求造成的负债购买等现象
    if (-e $ftplockfile) {
        &myerror("刷新错误&请不要刷新FTP联盟太快！") if ($currenttime < (stat($ftplockfile))[9] + 3);
    }
    open(LOCKCALFILE, ">$ftplockfile");
    close(LOCKCALFILE);

    $myallmoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
}

if (($member_code ne "ad") && ($plugstats eq "close")) {
    unlink($ftplockfile);
    &error("普通错误&FTP 联盟已经被管理员暂时关闭！");
}

$action = $query->param("action");
my %Mode = (
    "view"   => \&view, #查看某个FTP的登录资料
    "poll"   => \&poll, #给某个FTP打分
    "add"    => \&add,  #添加一个FTP登录资料
    "addok"  => \&addok,
    "edit"   => \&edit, #编辑一个FTP登录资料
    "editok" => \&editok,
    "info"   => \&info,   #查询FTP的购买记录
    "delete" => \&delete, #删除一个FTP登录资料
    "up"     => \&up,     #提升FTP在联盟中的位置
    "repair" => \&repair, #重建联盟索引
    "config" => \&config  #配置程序设置
);

if ($Mode{$action}) {
    $Mode{$action}->();
}
else {
    &list;
}

unlink($ftplockfile);
print header(-cookie => [ $onlineviewcookie ], -charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&output("$board_name - FTP 联盟", \$output);
exit;

sub list {
    my $onlineview = $query->cookie("onlineview");
    $onlineview = 0 if ($onlineview eq "");
    $onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
    $onlineviewcookie = cookie(-name => "onlineview", -value => "$onlineview", -path => "$cookiepath/", -expires => "+30d");
    my $onlinetitle = $onlineview == 1 ? "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>关闭详细列表</font></a>]" : "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>显示详细列表</font></a>]";

    #写入用户在线状态并获得在线列表
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    unless (-e "$filetoopens.lck") {
        $screenmode = $query->cookie("screenmode");
        $screenmode = 8 if ($screenmode eq "");
        &whosonline("$in_member_name\tFTP 联盟\tFTP 联盟\t查看 FTP 联盟列表");
        $membertongji =~ s/本分论坛/FTP 联盟/o;
        undef $memberoutput if ($onlineview != 1);
    }
    else {
        $memberoutput = "";
        $membertongji = " <b>由于服务器繁忙，所以 FTP 联盟的在线数据暂时不提供显示。</b>";
        $onlinetitle = "";
    }

    my $listtoupdate = "$lbdir$ftpdir/list.cgi";
    &winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(LIST, $listtoupdate);
    flock(LIST, 1) if ($OS_USED eq "Unix");
    my @ftpinfos = <LIST>;
    close(LIST);
    &winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

    #头部输出和在线统计
    &ftpheader;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT><table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr>
	<td bgcolor=$titlecolor width=92% $catbackpic><font color=$titlefontcolor>$membertongji　 $onlinetitle</td>
	<td bgcolor=$titlecolor width=8% align=center $catbackpic><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 width=40 height=12></a></td>
</tr>~;
    $output .= qq~\n<tr><td colspan=2 bgcolor=$forumcolorone $otherbackpic><table cellPadding=1 cellSpacing=0>$memberoutput</table><script language="JavaScript"> function O9(id) {if(id != "") window.open("profile.cgi?action=show&member=" + id);}</script></td></tr>~ if ($onlineview == 1 && $memberoutput);
    $output .= qq~
</table></td></tr></table><SCRIPT>valignend()</SCRIPT><p>
<script language="JavaScript">
function Closed()
{
	alert("这个 FTP 目前被暂时关闭了！");
	return false;
}
function LeastRate()
{
	alert("你的威望值好像不够这个 FTP 的查看要求！");
	return false;
}
function LeastMoney(myallmoney)
{
	alert("你的社区货币好像不够，只有 " + myallmoney + " $moneyname，买不起这个 FTP 的登录资料哦！\\n如果你在银行有存款的话赶紧去取钱，我们只收现金:)");
	return false;
}
function MaxUser()
{
	alert("查看这个 FTP 登录资料的人数已经达到了限定的最大数额！");
	return false;
}
function ViewNEW(money, myallmoney)
{
	if (confirm("这是你第一次查看这个 FTP，你现在有 " + myallmoney + " $moneyname社区货币。\\n购买登录资料需要花费你 " + money + " $moneyname社区货币，是否继续？"))
		return true;
	else
		return false;
}
function ViewOLD()
{
	if (confirm("你以前购买过这个 FTP 的资料，再次查看无需花钱:) 是否继续？"))
		return true;
	else
		return false;
}
function AdminView()
{
	if (confirm("你是这个 FTP 的管理人员，查看资料不受限制，是否继续？"))
		return true;
	else
		return false;	
}
</script>~;
    $output .= "\n<table width=$tablewidth align=center><tr><td>　　<a href=$thisprog?action=add><font color=$fonthighlight><b>出售新的 FTP 服务</b></font></a></td></tr></table>" if ($member_code eq "ad" || ",$saleusers," =~ /,$in_member_name,/i);
    $output .= qq~
	<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $titlefontcolor; font-weight: bold; background-color: $titlecolor" align=center><td $catbackpic>FTP 名称 (点击购买)</td><td $catbackpic>状态</td><td $catbackpic>类型</td><td $catbackpic>管理员</td><td $catbackpic>当前售价</td><td $catbackpic>威望要求</td><td $catbackpic>购买限制</td><td $catbackpic>得分</td></tr>~;

    foreach (@ftpinfos) {
        undef @ftpviews;
        undef $adminoption;
        chomp;
        my ($ftpid, $ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $_);
        my $viewfile = "$lbdir$ftpdir/view$ftpid.cgi";
        if (-e $viewfile) {
            open(VIEW, $viewfile);
            @ftpviews = <VIEW>;
            close(VIEW);
        }
        my @view = grep (/^$cleanmembername\t/, @ftpviews);
        my $viewnum = @ftpviews;
        $ftpmoney -= $ftpreduce * int(($currenttime - $ftptime) / 86400);
        $ftpmoney = 1 if ($ftpmoney < 1);

        if ($ftpstatus eq "close") {
            $prompt = "Closed()";
        }
        elsif (lc($in_member_name) eq lc($ftpadmin) || $member_code eq "ad") {
            $prompt = "AdminView()";
        }
        elsif ($rating < $ftprate) {
            $prompt = "LeastRate()";
        }
        elsif (@view >= 1) {
            $prompt = "ViewOLD()";
        }
        elsif ($viewnum >= $ftpmaxuser && $ftpmaxuser ne "") {
            $prompt = "MaxUser()";
        }
        elsif ($myallmoney < $ftpmoney) {
            $prompt = "LeastMoney($myallmoney)";
        }
        else {
            $prompt = "ViewNEW($ftpmoney, $myallmoney)";
        }

        if (lc($in_member_name) eq lc($ftpadmin) || $member_code eq "ad") {
            $adminoption = qq~<a href=$thisprog?action=edit&id=$ftpid><font color=$titlecolor>编</font></a> <font color=$titlecolor>|</font> <a href=$thisprog?action=delete&id=$ftpid OnClick="return confirm('这将彻底删除你的 FTP 服务资料，如果只是一时中断使用，建议你只将其暂时关闭。是否继续？');"><font color=$titlecolor>删</font></a> <font color=$titlecolor>|</font> <a href=$thisprog?action=info&id=$ftpid><font color=$titlecolor>记录</font></a>~;
        }
        $adminoption .= qq~ <font color=$titlecolor>|</font> <a href=$thisprog?action=up&id=$ftpid OnClick="return confirm('这将把这个 FTP 提升到联盟的最顶端位置，是否继续？');"><font color=$titlecolor>提</font></a>~ if ($member_code eq "ad");

        $ftpintro =~ s/<br>/\n/isg;
        $ftpname = "<font color=$fonthighlight><b>$ftpname</b></font>" if ($ftptype ne "priviate");
        $ftpname = qq~<a href=$thisprog?action=view&id=$ftpid OnClick="return $prompt;" title="$ftpintro">$ftpname</a>~;
        $ftpstatus = $ftpstatus eq "close" ? "关闭" : "开放";
        $ftptype = $ftptype eq "priviate" ? "个人" : "公共";
        my $encodeftpadmin = uri_escape($ftpadmin);
        $ftpadmin = "<a href=profile.cgi?action=show&member=$encodeftpadmin target=_blank>$ftpadmin</a>";
        $ftpmaxuser = $ftpmaxuser eq "" ? qq~<span title="当前购买人数: $viewnum\n最多允许购买人数: 不限">$viewnum / MAX</span>~ : qq~<span title="当前购买人数: $viewnum\n最多允许购买人数: $ftpmaxuser">$viewnum / $ftpmaxuser</span>~;
        $pollscore = $polluser > 0 ? sprintf("%4.2f", $pollscore / $polluser) : "无";
        $output .= "\n<tr bgColor=$forumcolortwo align=center><td>$ftpname<div align=right>$adminoption</div></td><td>$ftpstatus</td><td>$ftptype</td><td>$ftpadmin</td><td><i>$ftpmoney</i> $moneyname</td><td>$ftprate</td><td>$ftpmaxuser</td><td>$pollscore</td></tr>";
    }

    $output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><table cellPadding=0 cellSpacing=0 width=$tablewidth><tr><td align=right width=100% style="line-height: 150%">&copy; <b>程序设计: <a href=http://www.94cool.net target=_blank><font color=5599ff>94Cool</font><font color=ff9955>.net</font></a></b> <a href=mailto:Jim_White\@etang.com>BigJim</a> </td></tr></table>~;

    if ($member_code eq "ad") {
        #坛主可以看到管理选项
        $plugopenorclose = qq~<select name="plugstats"><option value="open">正常开放</option><option value="close">暂时关闭</option></select>~;
        $plugopenorclose =~ s/value=\"$plugstats\"/value=\"$plugstats\" selected/;
        $output .= qq~<p>
<script language="JavaScript">
function AddSALE()
{
	if (name = prompt("请输入要添加的允许出售 FTP 服务的 ID：", ""))
	{
		if (CONFIG.saleusers.innerText) CONFIG.saleusers.innerText += "," + name;
		else CONFIG.saleusers.innerText = name;
	}
}
function DeleteSALE()
{
	if (name = prompt("请输入要去除的允许出售 FTP 服务的 ID：", ""))
	{
		CONFIG.saleusers.innerText = eval("CONFIG.saleusers.innerText.replace(/," + name + "/ig" + ",'')");
		CONFIG.saleusers.innerText = eval("CONFIG.saleusers.innerText.replace(/" + name + ",/ig" + ",'')");
		CONFIG.saleusers.innerText = eval("CONFIG.saleusers.innerText.replace(/" + name + "/ig" + ",'')");
	}
}
function ShowConfig()
{
	if (configtable.style.display == "none")
	{
		configtable.style.display = "";
		showtext.innerHTML = "隐藏 FTP 联盟设置";
	}
	else
	{
		configtable.style.display = "none";
		showtext.innerHTML = "显示 FTP 联盟设置";
	}
}
</script>
<SCRIPT>valigntop()</SCRIPT>
<table cellSpacing=0 cellPadding=0 width=$tablewidth bgColor=$tablebordercolor align=center><tr><td><table cellSpacing=1 cellPadding=6 width=100%>
<tr><td bgColor=$titlecolor $catbackpic><font color=$titlefontcolor>　<b>管理选项</b>　　<input type=checkbox OnClick="ShowConfig()"> <span id=showtext>显示 FTP 联盟设置</span></font>　　　　<a href=$thisprog?action=repair OnClick="return confirm('当联盟页面信息丢失的时候，可以使用此功能恢复，是否继续？')"><font color=$fonthighlight><b>修复联盟索引</b></font></a></td></tr>
<tr><td bgColor=$forumcolorone align=center><table id=configtable cellSpacing=15 style="display:none"><form name=CONFIG action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="config"><tr><td align=center><textarea name=saleusers rows=3 cols=40 readonly=true>$saleusers</textarea><br>除坛主以外的允许出售人员　<input type=button value="添 加" OnClick="AddSALE()">　<input type=button value="删 除" OnClick="DeleteSALE()"></td><td><br>　　FTP 联盟插件状态: $plugopenorclose<br>　　个人 FTP 管理员提成: <input name=percent type=text size=3 value="$percent"> %<br><br>　　　　<input type=submit name=submit value="保　存">　<input type=reset value="重　来"></td><form></tr></table></td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
    return;
}

sub view {
    my $ftpid = $query->param("id");
    &myerror("普通错误&老大，别乱黑我的程序呀！") unless ($ftpid =~ /^[0-9]+$/);
    my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
    &myerror("普通错误&你要查看的 FTP 并不存在！") unless (-e $infofile);

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t查看 FTP 服务登录资料") unless (-e "$filetoopens.lck");

    open(INFO, $infofile);
    flock(INFO, 1) if ($OS_USED eq "Unix");
    my $ftpinfo = <INFO>;
    close(INFO);
    chomp($ftpinfo);
    my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, $ftpaddress, $ftpport, $ftpuser, $ftppass, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);

    &myerror("查看错误&这个 FTP 已经暂时关闭！") if ($ftpstatus eq "close");
    &myerror("查看错误&你的威望不够查看这个 FTP 的最低要求！") if ($rating < $ftprate && lc($in_member_name) ne lc($ftpadmin) && $member_code ne "ad");

    my $viewfile = "$lbdir$ftpdir/view$ftpid.cgi";
    if (-e $viewfile) {
        open(VIEW, $viewfile);
        flock(VIEW, 1) if ($OS_USED eq "Unix");
        @ftpviews = <VIEW>;
        close(VIEW);
    }
    my @view = grep (/^$cleanmembername\t/, @ftpviews);
    if (@view < 1 && lc($in_member_name) ne lc($ftpadmin) && $member_code ne "ad") {
        &myerror("查看错误&查看这个 FTP 登录资料的人数已经达到了限定的最大数额！") if (@ftpviews >= $ftpmaxuser && $ftpmaxuser ne "");
        $ftpmoney -= $ftpreduce * int(($currenttime - $ftptime) / 86400);
        $ftpmoney = 1 if ($ftpmoney < 1);
        &myerror("查看错误&你的论坛货币现金不够支付查看这个 FTP 服务登录资料所需要的花费！") if ($myallmoney < $ftpmoney);

        #更新用户金钱和查看记录
        use testinfo qw(ipwhere);
        my $fromwhere = &ipwhere($trueipaddress);
        &updateusermoney($in_member_name, -$ftpmoney);
        &winlock($viewfile) if ($OS_USED eq "Nt");
        open(VIEW, ">>$viewfile");
        flock(VIEW, 2) if ($OS_USED eq "Unix");
        print VIEW "$cleanmembername\t$trueipaddress\t$currenttime\t$fromwhere\n";
        close(VIEW);
        &winunlock($viewfile) if ($OS_USED eq "Nt");
        &updateusermoney($ftpadmin, $ftpmoney * $percent / 100) if ($ftptype eq "priviate");
    }

    if ($ftpuser =~ /\*$/) {
        #使用Serv-U的独立账户方式
        eval("use Digest::MD5 qw(md5_hex);");
        if ($@ eq "") {
            #MD5模块工作正常
            $ftpuser =~ s/\*$//o;
            $ftpuser .= $cleanmembername;
            $ftppass = md5_hex("$ftppass$ftpuser");
        }
    }
    $pollscore = $polluser > 0 ? sprintf("%4.2f", $pollscore / $polluser) . " 分" : "无";

    #输出页面
    &ftpheader;
    $output .= qq~
	<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $fonthighlight; font-weight: bold; background-color: $titlecolor" align=center><td colSpan=2>$ftpname 的具体登录资料</td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" width=20% align=center>服务地址:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$board_name</font>$ftpaddress<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>服务端口:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$board_name</font>$ftpport<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>登陆用户:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$board_name</font>$ftpuser<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>登陆密码:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$board_name</font>$ftppass<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>相关说明:　</td><td bgColor=$miscbacktwo><form action=$thisprog method=POST><input name=action type=hidden value="poll"><input name=id type=hidden value="$ftpid"><table width=100%><tr><td width=12></td><td>$ftpintro</td><td align=right>当前评价: $pollscore<br><br><select name=score><option value=1>1</option><option value=2>2</option><option value=3>3</option><option value=4>4</option><option value=5>5</option><option value=6 selected>6</option><option value=7>7</option><option value=8>8</option><option value=9>9</option><option value=10>10</option></select> <input type=submit value="评分"></td></tr></table></td></tr></form>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    return;
}

sub poll {
    my $ftpid = $query->param("id");
    &myerror("普通错误&老大，别乱黑我的程序呀！") unless ($ftpid =~ /^[0-9]+$/);
    my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
    &myerror("普通错误&你要评分的 FTP 并不存在！") unless (-e $infofile);
    my $score = $query->param("score");
    &myerror("普通错误&老大，别乱黑我的程序呀！") unless ($score =~ /^[0-9]+$/ && $score > 0 && $score <= 10);

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t对 FTP 服务评分") unless (-e "$filetoopens.lck");

    #更新用户评分操作时间
    my $pollfile = "$lbdir$ftpdir/poll$ftpid.cgi";
    &winlock($pollfile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    if (-e $pollfile) {
        open(POLL, $pollfile);
        flock(POLL, 1) if ($OS_USED eq "Unix");
        @pollusers = <POLL>;
        close(POLL);
    }
    foreach (@pollusers) {
        chomp;
        my ($pollname, $lasttime) = split(/\t/, $_);
        $polltime{$pollname} = $lasttime;
    }
    if ($currenttime - $polltime{$cleanmembername} < 86400) {
        &winunlock($pollfile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        &myerror("评分错误&你在最近24小时内已经给这个服务器打过分了！");
    }
    $polltime{$cleanmembername} = $currenttime;
    open(POLL, ">$pollfile");
    flock(POLL, 2) if ($OS_USED eq "Unix");
    while (($pollname, $lasttime) = each(%polltime)) {
        print POLL "$pollname\t$lasttime\n";
    }
    close(POLL);
    &winunlock($pollfile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

    #更新服务器评分
    &winlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(INFO, $infofile);
    flock(INFO, 1) if ($OS_USED eq "Unix");
    my $ftpinfo = <INFO>;
    close(INFO);
    chomp($ftpinfo);
    my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, $ftpaddress, $ftpport, $ftpuser, $ftppass, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);
    $polluser++;
    $pollscore += $score;
    open(INFO, ">$infofile");
    flock(INFO, 2) if ($OS_USED eq "Unix");
    print INFO "$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftpaddress\t$ftpport\t$ftpuser\t$ftppass\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore";
    close(INFO);
    &winunlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

    #更新索引文件
    my $listtoupdate = "$lbdir$ftpdir/list.cgi";
    $filetoopens = &lockfilename($listtoupdate);
    unless (-e "$filetoopens.lck") {
        #服务器忙则放弃更新索引
        &winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        open(LIST, $listtoupdate);
        flock(LIST, 1) if ($OS_USED eq "Unix");
        my @ftpinfos = <LIST>;
        close(LIST);
        open(LIST, ">$listtoupdate");
        flock(LIST, 2) if ($OS_USED eq "Unix");
        foreach (@ftpinfos) {
            chomp;
            my ($id, undef) = split(/\t/, $_);
            print LIST $id == $ftpid ? "$ftpid\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n" : "$_\n";
        }
        close(LIST);
        &winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    }

    #输出跳转返回页面
    &ftpheader;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>对 FTP 服务评分成功！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！<ul><li><a href=$thisprog>返回 FTP 联盟页面</a><li><a href=$thisprog?action=view&id=$ftpid>返回 FTP 登录资料</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
    return;
}

sub add {
    &myerror("权限错误&你没有权利出售 FTP 服务！") unless ($member_code eq "ad" || ",$saleusers," =~ /,$in_member_name,/i);

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t出售 FTP") unless (-e "$filetoopens.lck");

    &ftpheader;
    my $statusoption = qq~<input name=ftpstatus type=radio value="open" checked> 正常开放　　<input name=ftpstatus type=radio value="close"> 暂时关闭~;
    my $typeoption = qq~<select name=ftptype><option value="public">论坛公共</option><option value="priviate">个人服务</option></select>~;
    my $rateoption = "";
    for (0 .. $maxweiwang) {
        $rateoption .= qq~<option value="$_">$_</option>~;
    }
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="addok">
<tr><td bgcolor=$miscbackone align=center><table width=80%>
<tr><td><b>FTP 状态(*): 　　</b>$statusoption</td></tr>
<tr><td><b>FTP 名称(*): 　　</b><input name=ftpname type=text size=60></td></tr>
<tr><td><b>FTP 类型(*): 　　</b>$typeoption　　<i>选择个人服务类型，则您个人可以得到该 FTP 收益的 $percent% 作为酬劳。</i></td></tr>
<tr><td><b>FTP 地址(*): 　　</b><input name=ftpaddress type=text size=24></td></tr>
<tr><td><b>FTP 端口(*): 　　</b><input name=ftpport type=text size=8 value="21" OnFocus="this.select()"></td></tr>
<tr><td><b>登录用户名称(*): </b><input name=ftpuser type=text size=36></td></tr>
<tr><td><b>登录密码(*): 　　</b><input name=ftppass type=text size=36></td></tr>
<tr><td>　　<i>注意：如果你要使用 Serv-U 的独立帐户功能，请将登录用户名填成用户名前缀 +“*”的形式，比如“leobbs_*”，这样用户“BigJim“所获得的用户名就是“leobbs_bigjim”，登录密码填 Serv-U 插件里设定的密码生成使用的Key。Serv-U 没有安装插件切勿如此使用！Serv-U 插件的下载地址为 <a href=http://www.94cool.net/download/Serv-U.rar>http://www.94cool.net/download/Serv-U.rar</a>。</i></td></tr>
<tr><td><b>查看需要威望(*): </b><select name=ftprate>$rateoption</select></td></tr>
<tr><td><b>初始售价(*): 　　</b><input name=ftpmoney type=text size=18></td></tr>
<tr><td><b>每24小时降价:　　</b><input name=ftpreduce type=text size=15>　　<i>不需要请留空。</i></td></tr>
<tr><td><b>最大出售人数:　　</b><input name=ftpmaxuser type=text size=8>　　<i>达到限制以后，FTP 会自动停止出售，如果不想限制请留空。</i></td></tr>
<tr><td><b>FTP 其它简介:　　</b><textarea name=ftpintro rows=5 cols=60></textarea></td></tr>
<tr><td align=center><br><input type=submit name=submit value="出　　售"></td></tr>
</table></td></tr></form>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    return;
}

sub addok {
    &myerror("权限错误&你没有权利出售 FTP 服务！") unless ($member_code eq "ad" || ",$saleusers," =~ /,$in_member_name,/i);

    for ("ftpstatus", "ftpname", "ftptype", "ftpaddress", "ftpport", "ftpuser", "ftppass", "ftprate", "ftpmoney", "ftpreduce", "ftpmaxuser", "ftpintro") {
        ${$_} = &cleaninput($query->param($_));
    }
    #输入检查
    $ftpstatus = "open" unless ($ftpstatus eq "close");
    &myerror("输入错误&你没有输入 FTP 的名称！") if ($ftpname eq "");
    $ftptype = "public" unless ($ftptype eq "priviate");
    &myerror("输入错误&你没有输入 FTP 的地址！") if ($ftpaddress eq "");
    $ftpport = 21 unless ($ftpport =~ /^[0-9]+$/);
    &myerror("输入错误&你没有输入 FTP 的用户名！") if ($ftpuser eq "");
    &myerror("输入错误&你没有输入 FTP 的密码！") if ($ftppass eq "");
    $ftprate = 0 unless ($ftprate =~ /^[0-9]+$/);
    $ftpmoney = 1 unless ($ftpmoney =~ /^[0-9]+$/);
    $ftpreduce = "" unless ($ftpreduce =~ /^[0-9]+$/);
    $ftpmaxuser = "" unless ($ftpmaxuser =~ /^[0-9]+$/);

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t出售 FTP") unless (-e "$filetoopens.lck");

    #取得新FTP的ID
    my $numfiletoupdate = "$lbdir$ftpdir/lastnum.cgi";
    if (open(NUMFILE, $numfiletoupdate)) {
        $lastnumber = <NUMFILE>;
        close(NUMFILE);
        chomp($lastnumber);
    }
    do
    {
        $lastnumber++;
    } while (-e "$lbdir$ftpdir/info$lastnumber.cgi");
    open(NUMFILE, ">$numfiletoupdate");
    flock(NUMFILE, 2) if ($OS_USED eq "Unix");
    print NUMFILE $lastnumber;
    close(NUMFILE);

    #写入新数据文件
    open(INFO, ">$lbdir$ftpdir/info$lastnumber.cgi");
    print INFO "$ftpstatus\t$ftpname\t$ftptype\t$in_member_name\t$currenttime\t$ftpaddress\t$ftpport\t$ftpuser\t$ftppass\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t0\t0";
    close(INFO);

    #更新索引文件
    my $listtoupdate = "$lbdir$ftpdir/list.cgi";
    &winlock($listtoupdate) if ($OS_USED eq "Nt");
    open(LIST, ">>$listtoupdate");
    flock(LIST, 2) if ($OS_USED eq "Unix");
    print LIST "$lastnumber\t$ftpstatus\t$ftpname\t$ftptype\t$in_member_name\t$currenttime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t0\t0\t0\n";
    close(LIST);
    &winunlock($listtoupdate) if ($OS_USED eq "Nt");

    #输出跳转返回页面
    &ftpheader;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>出售你的 FTP 成功！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！<ul><li><a href=$thisprog>返回 FTP 联盟页面</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
    return;
}

sub edit {
    my $ftpid = $query->param("id");
    &myerror("普通错误&老大，别乱黑我的程序呀！") unless ($ftpid =~ /^[0-9]+$/);
    my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
    &myerror("普通错误&你要编辑的 FTP 并不存在！") unless (-e $infofile);

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t编辑 FTP 资料") unless (-e "$filetoopens.lck");

    #读入旧的资料
    open(INFO, $infofile);
    flock(INFO, 1) if ($OS_USED eq "Unix");
    my $ftpinfo = <INFO>;
    close(INFO);
    chomp($ftpinfo);
    my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, undef, $ftpaddress, $ftpport, $ftpuser, $ftppass, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, undef) = split(/\t/, $ftpinfo);
    &myerror("权限错误&你没有权利编辑这个 FTP！") unless ($member_code eq "ad" || lc($in_member_name) eq lc($ftpadmin));

    &ftpheader;
    my $statusoption = qq~<input name=ftpstatus type=radio value="open"> 正常开放　　<input name=ftpstatus type=radio value="close"> 暂时关闭~;
    $statusoption =~ s/value=\"$ftpstatus\"/value=\"$ftpstatus\" checked/o;
    my $typeoption = qq~<select name=ftptype><option value="public">论坛公共</option><option value="priviate">个人服务</option></select>~;
    $typeoption =~ s/value=\"$ftptype\"/value=\"$ftptype\" selected/o;
    my $rateoption = "";
    for (0 .. $maxweiwang) {
        $rateoption .= qq~<option value="$_">$_</option>~;
    }
    $rateoption =~ s/value=\"$ftprate\"/value=\"$ftprate\" selected/o;
    $ftpintro =~ s/<br>/\n/isg;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="editok"><input type=hidden name=id value="$ftpid">
<tr><td bgcolor=$miscbackone align=center><table width=80%>
<tr><td><b>FTP 状态(*): 　　</b>$statusoption</td></tr>
<tr><td><b>FTP 名称(*): 　　</b><input name=ftpname type=text size=60 value="$ftpname"></td></tr>
<tr><td><b>FTP 类型(*): 　　</b>$typeoption　　<i>选择个人服务类型，则您个人可以得到该 FTP 收益的 $percent% 作为酬劳。</i></td></tr>
<tr><td><b>FTP 地址(*): 　　</b><input name=ftpaddress type=text size=24 value="$ftpaddress"></td></tr>
<tr><td><b>FTP 端口(*): 　　</b><input name=ftpport type=text size=8 value="$ftpport" OnFocus="this.select()" value="$ftpport"></td></tr>
<tr><td><b>登录用户名称(*): </b><input name=ftpuser type=text size=36 value="$ftpuser"></td></tr>
<tr><td><b>登录密码(*): 　　</b><input name=ftppass type=text size=36 value="$ftppass"></td></tr>
<tr><td>　　<i>注意：如果你要使用 Serv-U 的独立帐户功能，请将登录用户名填成用户名前缀 +“*”的形式，比如“dlmovie_*”，这样用户“BigJim“所获得的用户名就是“dlmovie_bigjim”，登录密码填 Serv-U 插件里设定的密码生成使用的Key。Serv-U 没有安装插件切勿如此使用！Serv-U 插件的下载地址为 <a href=http://www.94cool.net/download/Serv-U.rar>http://www.94cool.net/download/Serv-U.rar</a>。</i></td></tr>
<tr><td><b>查看需要威望(*): </b><select name=ftprate>$rateoption</select></td></tr>
<tr><td><b>初始售价(*): 　　</b><input name=ftpmoney type=text size=18 value="$ftpmoney"></td></tr>
<tr><td><b>每24小时降价:　　</b><input name=ftpreduce type=text size=15 value="$ftpreduce">　　<i>不需要请留空。</i></td></tr>
<tr><td><b>最大出售人数:　　</b><input name=ftpmaxuser type=text size=8 value="$ftpmaxuser">　　<i>达到限制以后，FTP 会自动停止出售，如果不想限制请留空。</i></td></tr>
<tr><td><b>FTP 其它简介:　　</b><textarea name=ftpintro rows=5 cols=60>$ftpintro</textarea></td></tr>
<tr><td><b>清除所有查看纪录:</b>　　<input name=ftpclear type=checkbox value="yes"> <i>选择此项以后，FTP 的查看人员名单会被清空，所有人均需重新花费论坛货币购买新的登录资料。</i></td></tr>
<tr><td align=center><br><input type=submit name=submit value="更　　新"></td></tr>
</table></td></tr></form>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    return;
}

sub editok {
    my $ftpid = $query->param("id");
    &myerror("普通错误&老大，别乱黑我的程序呀！") unless ($ftpid =~ /^[0-9]+$/);
    my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
    &myerror("普通错误&你要编辑的 FTP 并不存在！") unless (-e $infofile);

    for ("ftpstatus", "ftpname", "ftptype", "ftpaddress", "ftpport", "ftpuser", "ftppass", "ftprate", "ftpmoney", "ftpreduce", "ftpmaxuser", "ftpintro", "ftpclear") {
        ${$_} = &cleaninput($query->param($_));
    }
    #输入检查
    $ftpstatus = "open" unless ($ftpstatus eq "close");
    &myerror("输入错误&你没有输入 FTP 的名称！") if ($ftpname eq "");
    $ftptype = "public" unless ($ftptype eq "priviate");
    &myerror("输入错误&你没有输入 FTP 的地址！") if ($ftpaddress eq "");
    $ftpport = 21 unless ($ftpport =~ /^[0-9]+$/);
    &myerror("输入错误&你没有输入 FTP 的用户名！") if ($ftpuser eq "");
    &myerror("输入错误&你没有输入 FTP 的密码！") if ($ftppass eq "");
    $ftprate = 0 unless ($ftprate =~ /^[0-9]+$/);
    $ftpmoney = 1 unless ($ftpmoney =~ /^[0-9]+$/);
    $ftpreduce = "" unless ($ftpreduce =~ /^[0-9]+$/);
    $ftpmaxuser = "" unless ($ftpmaxuser =~ /^[0-9]+$/);

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t编辑 FTP 资料") unless (-e "$filetoopens.lck");

    &winlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(INFO, $infofile);
    flock(INFO, 1) if ($OS_USED eq "Unix");
    my $ftpinfo = <INFO>;
    close(INFO);
    chomp($ftpinfo);
    my (undef, undef, undef, $ftpadmin, $ftptime, undef, undef, undef, undef, undef, undef, undef, undef, undef, $polluser, $pollscore) = split(/\t/, $ftpinfo);
    unless ($member_code eq "ad" || lc($in_member_name) eq lc($ftpadmin)) {
        &winunlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        &myerror("权限错误&你没有权利编辑这个 FTP！");
    }

    #清空查看记录
    if ($ftpclear eq "yes") {
        unlink("$lbdir$ftpdir/view$ftpid.cgi");
        $ftptime = $currenttime;
    }

    #更新数据文件
    open(INFO, ">$infofile");
    flock(INFO, 2) if ($OS_USED eq "Unix");
    print INFO "$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftpaddress\t$ftpport\t$ftpuser\t$ftppass\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore";
    close(INFO);
    &winunlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

    #更新索引文件
    my $listtoupdate = "$lbdir$ftpdir/list.cgi";
    &winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(LIST, $listtoupdate);
    flock(LIST, 1) if ($OS_USED eq "Unix");
    my @ftpinfos = <LIST>;
    close(LIST);
    open(LIST, ">$listtoupdate");
    flock(LIST, 2) if ($OS_USED eq "Unix");
    foreach (@ftpinfos) {
        chomp;
        my ($id, undef) = split(/\t/, $_);
        print LIST $id == $ftpid ? "$ftpid\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n" : "$_\n";
    }
    close(LIST);
    &winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

    #输出跳转返回页面
    &ftpheader;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>编辑你的 FTP 资料成功！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！<ul><li><a href=$thisprog>返回 FTP 联盟页面</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
    return;
}

sub info {
    use testinfo qw(ipwhere);

    my $ftpid = $query->param("id");
    &myerror("普通错误&老大，别乱黑我的程序呀！") unless ($ftpid =~ /^[0-9]+$/);
    my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
    &myerror("普通错误&你要查询的 FTP 并不存在！") unless (-e $infofile);

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t查询 FTP 购买记录") unless (-e "$filetoopens.lck");

    #判断用户权限
    if ($member_code ne "ad") {
        open(INFO, $infofile);
        flock(INFO, 1) if ($OS_USED eq "Unix");
        my $ftpinfo = <INFO>;
        close(INFO);
        chomp($ftpinfo);
        my (undef, undef, undef, $ftpadmin, undef) = split(/\t/, $ftpinfo);
        &myerror("权限错误&你没有权利查询这个 FTP 的购买记录！") unless (lc($in_member_name) eq lc($ftpadmin));
    }

    #读取查看记录
    my $viewfile = "$lbdir$ftpdir/view$ftpid.cgi";
    if (-e $viewfile) {
        open(VIEW, $viewfile);
        flock(VIEW, 1) if ($OS_USED eq "Unix");
        @ftpusers = <VIEW>;
        close(VIEW);
    }

    #按指定IP条件搜索
    my $key = $query->param("key");
    $key = "" unless ($key =~ /^[0-9\.]+$/);
    $key =~ s/^\.//sg;
    $key =~ s/\.$//sg;
    if ($key ne "") {
        @ips = split(/\./, $key);
        if (@ips < 4) {
            @ftpusers = grep (/\t$key\./, @ftpusers);
        }
        else {
            @ftpusers = grep (/\t$key/, @ftpusers);
        }
    }
    $allitems = @ftpusers;
    &splitpage("action=info&id=$ftpid&key=$key"); #分页

    #输出页面
    &ftpheader;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $titlefontcolor; font-weight: bold; background-color: $titlecolor" align=center><td $catbackpic>查看者</td><td $catbackpic>来自IP</td><td $catbackpic>来源鉴定</td><td $catbackpic>购买时间</td></tr>~;
    my $timeadd = ($timezone + $timedifferencevalue) * 3600;
    for ($i = $startnum; $i >= $endnum; $i--) {
        my $userinfo = $ftpusers[$i];
        chomp($userinfo);
        my ($username, $userip, $usertime, $userwhere) = split(/\t/, $userinfo);
        my $encodename = uri_escape($username);
        $userwhere = &ipwhere($userip) if ($userwhere eq "");
        my $usertime = &dateformatshort($usertime);
        $output .= qq~\n<tr align=center bgColor=$forumcolorone><td><a href=profile.cgi?action=show&member=$encodename target=_blank>$username</a></td><td>$userip</td><td>$userwhere</td><td>$usertime</td></tr>~;
    }
    $output .= qq~
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth align=center>
<form action=$thisprog><input name=action type=hidden value="info"><input name=id type=hidden value="$ftpid"><tr><td>$pages</td>
<td align=right>按照查看者IP搜索(支持按A、B、C类地址搜索) <input name=key type=text size=16> <input type=submit value="搜 索"></td></tr>
</table></form>~;
    return;
}

sub delete {
    my $ftpid = $query->param("id");
    &myerror("普通错误&老大，别乱黑我的程序呀！") unless ($ftpid =~ /^[0-9]+$/);
    my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
    &myerror("普通错误&你要删除的 FTP 并不存在！") unless (-e $infofile);

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t删除 FTP 资料") unless (-e "$filetoopens.lck");

    #判断用户权限
    if ($member_code ne "ad") {
        open(INFO, $infofile);
        flock(INFO, 1) if ($OS_USED eq "Unix");
        my $ftpinfo = <INFO>;
        close(INFO);
        chomp($ftpinfo);
        my (undef, undef, undef, $ftpadmin, undef) = split(/\t/, $ftpinfo);
        &myerror("权限错误&你没有权利删除这个 FTP！") unless (lc($in_member_name) eq lc($ftpadmin));
    }

    #删除数据文件
    unlink("$lbdir$ftpdir/info$ftpid.cgi");
    unlink("$lbdir$ftpdir/view$ftpid.cgi");
    unlink("$lbdir$ftpdir/poll$ftpid.cgi");

    #更新索引文件
    my $listtoupdate = "$lbdir$ftpdir/list.cgi";
    &winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(LIST, $listtoupdate);
    flock(LIST, 1) if ($OS_USED eq "Unix");
    my @ftpinfos = <LIST>;
    close(LIST);
    open(LIST, ">$listtoupdate");
    flock(LIST, 2) if ($OS_USED eq "Unix");
    foreach (@ftpinfos) {
        chomp;
        my ($id, undef) = split(/\t/, $_);
        print LIST "$_\n" unless ($id == $ftpid);
    }
    close(LIST);
    &winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

    #输出跳转返回页面
    &ftpheader;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>删除 FTP 资料成功！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！<ul><li><a href=$thisprog>返回 FTP 联盟页面</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
    return;
}

sub up {
    &myerror("权限错误&你无权提升 FTP 位置！") unless ($member_code eq "ad");
    my $ftpid = $query->param("id");
    &myerror("普通错误&老大，别乱黑我的程序呀！") unless ($ftpid =~ /^[0-9]+$/);
    my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
    &myerror("普通错误&你要提升的 FTP 并不存在！") unless (-e $infofile);

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t提升 FTP 位置") unless (-e "$filetoopens.lck");

    #读入旧的资料
    open(INFO, $infofile);
    flock(INFO, 1) if ($OS_USED eq "Unix");
    my $ftpinfo = <INFO>;
    close(INFO);
    chomp($ftpinfo);
    my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, undef, undef, undef, undef, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);

    #更新索引文件
    my $listtoupdate = "$lbdir$ftpdir/list.cgi";
    &winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(LIST, $listtoupdate);
    flock(LIST, 1) if ($OS_USED eq "Unix");
    my @ftpinfos = <LIST>;
    close(LIST);
    open(LIST, ">$listtoupdate");
    flock(LIST, 2) if ($OS_USED eq "Unix");
    print LIST "$ftpid\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n";
    foreach (@ftpinfos) {
        chomp;
        my ($id, undef) = split(/\t/, $_);
        print LIST "$_\n" unless ($id == $ftpid);
    }
    close(LIST);
    &winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

    #输出跳转返回页面
    &ftpheader;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>提升 FTP 位置成功！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！<ul><li><a href=$thisprog>返回 FTP 联盟页面</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
    return;
}

sub repair {
    &myerror("权限错误&你无权进行 FTP 联盟管理！") unless ($member_code eq "ad");

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t修复 FTP 联盟") unless (-e "$filetoopens.lck");

    #获取所有数据文件ID并排序
    opendir(DIR, "$lbdir$ftpdir");
    my @infofiles = readdir(DIR);
    closedir(DIR);
    @infofiles = grep (/^info[0-9]+\.cgi$/i, @infofiles);
    foreach (@infofiles) {
        s/^info//is;
        s/\.cgi$//is;
    }
    @infofiles = sort numerically @infofiles;

    #重新从数据文件中读入
    my $listtoupdate = "$lbdir$ftpdir/list.cgi";
    &winlock($listtoupdate) if ($OS_USED eq "Nt");
    open(LIST, ">$listtoupdate");
    flock(LIST, 2) if ($OS_USED eq "Unix");
    foreach (@infofiles) {
        open(INFO, "$lbdir$ftpdir/info$_.cgi");
        flock(INFO, 1) if ($OS_USED eq "Unix");
        my $ftpinfo = <INFO>;
        close(INFO);
        chomp($ftpinfo);
        my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, undef, undef, undef, undef, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);
        print LIST "$_\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n";
    }
    close(LIST);
    &winunlock($listtoupdate) if ($OS_USED eq "Nt");

    #输出跳转返回页面
    &ftpheader;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>重建 FTP 联盟索引完成！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！<ul><li><a href=$thisprog>返回 FTP 联盟页面</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
    return;
}

sub config {
    &myerror("权限错误&你无权进行 FTP 联盟管理！") unless ($member_code eq "ad");

    #写入用户在线状态
    my $filetoopens = "${lbdir}data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    &whosonline("$in_member_name\tFTP 联盟\tnone\t设定 FTP 联盟") unless (-e "$filetoopens.lck");

    my $newsaleusers = $query->param("saleusers");
    my $newpercent = $query->param("percent");
    my $newplugstats = $query->param("plugstats");
    $newpercent = 10 if ($newpercent eq "");
    $newplugstats = "open" if ($newplugstats eq "");
    if (($newpercent ne "") || ($newsaleusers ne "") || ($newplugstats ne "")) {
        my $configtomake = "$lbdir$ftpdir/conf.cgi";
        &winlock($configtomake) if ($OS_USED eq "Nt");
        open(CONFIG, ">$configtomake");
        flock(CONFIG, 2) if ($OS_USED eq "Unix");
        print CONFIG qq~\$plugstats = "$newplugstats";\n\$saleusers = "$newsaleusers";\n\$percent = $newpercent;\n1;~;
        close(CONFIG);
        &winunlock($configtomake) if ($OS_USED eq "Nt");
    }

    #输出跳转返回页面
    &ftpheader;
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>修改 FTP 联盟设置完成！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！<ul><li><a href=$thisprog>返回 FTP 联盟页面</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
    return;
}

sub ftpheader {
    #输出头部导航栏
    my $boardgraphic = $boardlogo =~ /\.swf$/i ? qq~<param name=play value=true><param name=loop value=true><param name=quality value=high><embed src=$imagesurl/myimages/$boardlogo quality=high width=$fgwidth height=$fgheight pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash"></embed>~ : "<img src=$imagesurl/myimages/$boardlogo border=0>";

    my $jump;
    if ($action eq "view") {
        $jump = qq~查看 FTP 服务登录资料~;
    }
    elsif ($action eq "poll") {
        $jump = qq~对 FTP 服务评分~;
    }
    elsif ($action eq "add") {
        $jump = qq~出售你的 FTP~;
    }
    elsif ($action eq "addok") {
        $jump = qq~出售你的 FTP 成功~;
    }
    elsif ($action eq "edit") {
        $jump = qq~编辑你的 FTP 资料~;
    }
    elsif ($action eq "editok") {
        $jump = qq~编辑你的 FTP 资料成功~;
    }
    elsif ($action eq "info") {
        $jump = qq~查看 FTP 购买记录~;
    }
    elsif ($action eq "delete") {
        $jump = qq~删除 FTP 资料成功~;
    }
    elsif ($action eq "up") {
        $jump = qq~提升 FTP 位置成功~;
    }
    elsif ($action eq "repair") {
        $jump = qq~重建 FTP 联盟索引完成~;
    }
    elsif ($action eq "config") {
        $jump = qq~修改 FTP 联盟设置完成~;
    }
    else {
        $jump = qq~查看 FTP 联盟~;
    }

    &title;
    $output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以查看本站 FTP 联盟的列表及详细信息</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$board_name</a> → <a href=$thisprog>FTP 联盟</a> → $jump<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
~;
    return;
}

sub updateusermoney {
    #更新用户金钱
    my ($nametochange, $cmoney) = @_;
    $nametochange =~ s/ /\_/sg;
    $nametochange =~ tr/A-Z/a-z/;
    my $namenumber = &getnamenumber($nametochange);
    &checkmemfile($nametochange, $namenumber);
    my $memfiletoupdate = "$lbdir$memdir/$namenumber/$nametochange.cgi";
    $memfiletoupdate = &stripMETA($memfiletoupdate);
    if (-e $memfiletoupdate) {
        &winlock($memfiletoupdate) if ($OS_USED eq "Nt");
        open(FILE, $memfiletoupdate);
        flock(FILE, 1) if ($OS_USED eq "Unix");
        my $filedata = <FILE>;
        close(FILE);
        chomp($filedata);
        my ($membername, $password, $membertitle, $member_code, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $soccerdata, $useradd5) = split(/\t/, $filedata);
        $mymoney += int($cmoney);
        if ($membername ne "" && $password ne "") {
            open(FILE, ">$memfiletoupdate");
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "$membername\t$password\t$membertitle\t$member_code\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$soccerdata\t$useradd5";
            close(FILE);
        }
        &winunlock($memfiletoupdate) if ($OS_USED eq "Nt");
    }
    return;
}

sub splitpage {
    #获得分页
    my $addstring = shift;
    my $instart = $query->param("start");
    $instart = 0 if ($instart !~ /^[0-9]+$/);

    my $temppages = $allitems / 20;
    my $numberofpages = int($temppages);
    $numberofpages++ if ($numberofpages != $temppages);

    if ($numberofpages > 1) {
        $startnum = $allitems - $instart - 1;
        $endnum = $startnum - 19;
        $endnum = 0 if ($endnum < 0);

        my $currentpage = int($instart / 20) + 1;
        my $endstart = ($numberofpages - 1) * 20;
        my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?start=0&$addstring title="首 页" ><font face=webdings>9</font></a>~;
        my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?start=$endstart&$addstring title="尾 页" ><font face=webdings>:</font></a>~;

        my $uppage = $currentpage - 1;
        my $nextpage = $currentpage + 1;
        my $upstart = $instart - 20;
        my $nextstart = $instart + 20;
        my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?start=$upstart&$addstring title="第$uppage页"><font face=webdings>7</font></a>~;
        my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?start=$nextstart&$addstring title="第$nextpage页"><font face=webdings>8</font></a>~;

        my $tempstep = $currentpage / 7;
        my $currentstep = int($tempstep);
        $currentstep++ if ($currentstep != $tempstep);
        my $upsteppage = ($currentstep - 1) * 7;
        my $nextsteppage = $currentstep * 7 + 1;
        my $upstepstart = ($upsteppage - 1) * 20;
        my $nextstepstart = ($nextsteppage - 1) * 20;
        my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?start=$upstepstart&$addstring class=hb title="第$upsteppage页">←</a> ~;
        my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?start=$nextstepstart&$addstring class=hb title="第$nextsteppage页">→</a> ~;

        $pages = "";
        my $currentstart = $upstepstart + 20;
        for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++) {
            last if ($i > $numberofpages);
            $pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=$thisprog?start=$currentstart&$addstring class=hb>$i</a> ~;
            $currentstart += 20;
        }
        $pages = "<font color=$menufontcolor><b>共 <font color=$fonthighlight>$numberofpages</font> 页</b> $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font><br>";
    }
    else {
        $startnum = $allitems - 1;
        $endnum = 0;
        $pages = "<font color=$menufontcolor>只有一页</font><br>";
    }
    return;
}

sub myerror {
    my $errorinfo = shift;
    unlink($ftplockfile);
    &error($errorinfo);
    return;
}