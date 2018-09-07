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

#  $ENV{'TMP'}="$LBPATH/lock"; #如果你不能上传图片，请去掉前面的#
#  $ENV{'TEMP'}="$LBPATH/lock";#如果你不能上传图片，请去掉前面的#

use LBCGI;
$LBCGI::POST_MAX=1000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/membertitles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "profile.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

&ipbanned; #封杀一些 ip

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$addme=$query->param('addme');

if ($arrowavaupload ne "on") { undef $addme; }

$action        = $query -> param('action');
$inmember      = $query -> param('member');
$inmember      =~ s/\///g;
$inmember      =~ s/\.\.//g;
$inmembername  = $query -> param("membername");
$inpassword    = $query -> param("password");
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$oldpassword   = $query -> param("oldpassword");
$action        = &cleaninput("$action");
$inmember      = &cleaninput("$inmember");
$inmembername  = &cleaninput("$inmembername");
$inpassword    = &cleaninput("$inpassword");
$oldpassword   = &cleaninput("$oldpassword");
$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if (($inmembername eq "")&&($action ne "lostpass")&&($action ne "lostpassword")&&($action ne "sendpassword")){
    $inmembername = "客人";
    $userregistered = "no";
    if ($dispprofile eq "no") {
        print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("查看会员资料&客人无权查看会员资料！")
    }
} else {
    &getmember("$inmembername","no");
    &error("普通错误&用户 $inmembername 在本论坛中不存在！") if (($userregistered eq "no")&&($action ne "lostpass")&&($action ne "lostpassword"));
    &error("普通错误&论坛密码与用户名不相符，请重新登录！") if ($inpassword ne $password && $action eq "show");
}
if ($arrawsignpic eq "on")      { $signpicstates = "允许";}      else {$signpicstates = "禁止";}
if ($arrawsignflash eq "on")    { $signflashstates = "允许";}    else {$signflashstates = "禁止";}
if ($arrawsignfontsize eq "on") { $signfontsizestates = "允许";} else {$signfontsizestates = "禁止";}
if ($arrawsignsound eq "on")    { $signsoundstates = "允许";}    else {$signsoundstates = "禁止";}

&mischeader("用户资料");

$output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
~;

my %Mode = (
'show'                 =>    \&showprofile,
'shows'                =>    \&showprofile,
'lostpassword'         =>    \&lostpasswordform,
'lostpass'             =>    \&lostpasswordform,
'sendpassword'         =>    \&sendpassword,
'modify'               =>    \&modify,
'process'              =>    \&savemodify,
);

if($Mode{$action}) {
    $Mode{$action}->();
} else {
    &error("查看资料&请勿非正常访问本程序！");
}

print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output($boardname,\$output);
exit;

sub lostpasswordform {
    require "dolostpasswordform.pl";
}

sub sendpassword {
    require "dosendpassword.pl";
}

sub savemodify {
    require "dosavemodify.pl";
}

sub modify {
    require "domodify.pl";
}

sub showprofile {
    $inmember =~ s/\_/ /isg;
    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t个人资料\tboth\t查看<b>$inmember</b>的个人资料\t");
    }
    &getmember("$inmember","no");
    if ("$userregistered" eq "no") { &error("查看资料&没有此用户名！"); }
    
    if ($jifen >= $mpostmarkmax) { $mtitle =  $mtitlemax;  $membergraphic = $mgraphicmax; }
    elsif ($jifen >= $mpostmark19) { $mtitle =  $mtitle19;  $membergraphic = $mgraphic19; }
    elsif ($jifen >= $mpostmark18) { $mtitle =  $mtitle18;  $membergraphic = $mgraphic18; }
    elsif ($jifen >= $mpostmark17) { $mtitle =  $mtitle17;  $membergraphic = $mgraphic17; }
    elsif ($jifen >= $mpostmark16) { $mtitle =  $mtitle16;  $membergraphic = $mgraphic16; }
    elsif ($jifen >= $mpostmark15) { $mtitle =  $mtitle15;  $membergraphic = $mgraphic15; }
    elsif ($jifen >= $mpostmark14) { $mtitle =  $mtitle14;  $membergraphic = $mgraphic14; }
    elsif ($jifen >= $mpostmark13) { $mtitle =  $mtitle13;  $membergraphic = $mgraphic13; }
    elsif ($jifen >= $mpostmark12) { $mtitle =  $mtitle12;  $membergraphic = $mgraphic12; }
    elsif ($jifen >= $mpostmark11) { $mtitle =  $mtitle11;  $membergraphic = $mgraphic11; }
    elsif ($jifen >= $mpostmark10) { $mtitle =  $mtitle10;  $membergraphic = $mgraphic10; }
    elsif ($jifen >= $mpostmark9)  { $mtitle =  $mtitle9;   $membergraphic = $mgraphic9; }
    elsif ($jifen >= $mpostmark8)  { $mtitle =  $mtitle8;   $membergraphic = $mgraphic8; }
    elsif ($jifen >= $mpostmark7)  { $mtitle =  $mtitle7;   $membergraphic = $mgraphic7; }
    elsif ($jifen >= $mpostmark6)  { $mtitle =  $mtitle6;   $membergraphic = $mgraphic6; }
    elsif ($jifen >= $mpostmark5)  { $mtitle =  $mtitle5;   $membergraphic = $mgraphic5; }
    elsif ($jifen >= $mpostmark4)  { $mtitle =  $mtitle4;   $membergraphic = $mgraphic4; }
    elsif ($jifen >= $mpostmark3)  { $mtitle =  $mtitle3;   $membergraphic = $mgraphic3; }
    elsif ($jifen >= $mpostmark2)  { $mtitle =  $mtitle2;   $membergraphic = $mgraphic2; }
    elsif ($jifen >= $mpostmark1)  { $mtitle =  $mtitle1;   $membergraphic = $mgraphic1; }
    else { $mtitle = $mtitle0; $mgraphic0 ="none.gif" if ($mgraphic0 eq ""); $membergraphic = $mgraphic0; }  #显示默认等级

    $emailaddress = &encodeemail($emailaddress);
    if ($showemail eq "no") { $emailaddress = "保密"; }
	elsif ($showemail eq "popo") { $emailaddress = qq~<img src=$imagesurl/images/popo.gif border=0 width=16 align=absmiddle> <a href=mailto:$emailaddress>$emailaddress</a>~; }
	elsif ($showemail eq "msn")  { $emailaddress = qq~<img src=$imagesurl/images/msn.gif border=0 width=16 align=absmiddle> <a href="mailto:$emailaddress">$emailaddress</a>~; }
	else { $emailaddress = qq~<a href="mailto:$emailaddress">$emailaddress</a>~; }

    if (($oicqnumber) && ($oicqnumber =~ /[0-9]/)) { $qqlogo = qq~<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$oicqnumber target=_blank><img src=$imagesurl/images/oicq.gif alt="查看 OICQ:$oicqnumber 的资料" atta="<img src=http://qqshow-user.tencent.com/$oicqnumber/10/00/>" border=0 width=16 height=16></a>~;} else { $oicqnumber = "没有"; $qqlogo ="";}
    if ($icqnumber eq "") { $icqnumber = "没有"; $icqlogo = ""; } else { $icqlogo = qq~<a href=misc.cgi?action=icq&UIN=$icqnumber target=_blank><img src=$imagesurl/images/icq.gif alt="给 ICQ:$icqnumber 发个消息" border=0 width=16 height=16></a>~; }
    if ((($membercode eq "ad")&&($membertitle eq "Member"))||(($membercode eq "ad")&&($membertitle eq "member")))   { $membertitle = "论坛坛主"; }
    if ((($membercode eq "mo")&&($membertitle eq "Member"))||(($membercode eq "mo")&&($membertitle eq "member")))   { $membertitle = "论坛版主";}
    if ((($membercode eq "cmo")&&($membertitle eq "Member"))||(($membercode eq "cmo")&&($membertitle eq "member")))  { $membertitle = "分类区版主";}
    if ((($membercode eq "smo")&&($membertitle eq "Member"))||(($membercode eq "smo")&&($membertitle eq "member"))) { $membertitle = "总版主";}
    if ((($membercode eq "amo")&&($membertitle eq "Member"))||(($membercode eq "amo")&&($membertitle eq "member"))) { $membertitle = "论坛副版主";}

    $mtitle = $motitle  if (($membercode eq "mo")&&($motitle ne ""));
    $mtitle = $adtitle  if (($membercode eq "ad")&&($adtitle ne ""));
    $mtitle = $cmotitle if (($membercode eq "cmo")&&($cmotitle ne ""));
    $mtitle = $smotitle if (($membercode eq "smo")&&($smotitle ne ""));
    $mtitle = $amotitle if (($membercode eq "amo")&&($amotitle ne ""));

    if ($membercode eq "banned") { $membertitle = "禁止发言"; }
    if ($membertitle eq "member" || $membertitle eq "Member" || $membertitle eq "") { $membertitle = "没有"; }
    if (($homepage eq "http://") || ($homepage eq "")) { $homepage = "没有"; } else { $homepage = qq~<a href="$homepage" target=_blank>$homepage</a>~; }

    $lastgone   = $joineddate if($lastgone eq "");
    $joineddate = &longdate($joineddate + ($timedifferencevalue*3600) + ($timezone*3600));
    $lastgone   = &dateformat($lastgone + ($timedifferencevalue*3600) + ($timezone*3600));

    ($postdate, $posturl, $posttopic) = split(/\%%%/,$lastpostdate);
    $posttopic =~ s/^＊＃！＆＊//;

    if ($postdate ne "没有发表过") {
        $postdate = &longdate($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
        $lastpostdetails = qq~<a href="$posturl">$posttopic</a> ($postdate)~;
    } else {
	$lastpostdetails = "没有发表过";
    }
    
    if ($avatars eq "on") {
	if (($personalavatar)&&($personalwidth)&&($personalheight)) { #自定义头像存在
	    $personalavatar =~ s/\$imagesurl/${imagesurl}/o;
	    if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	        $personalavatar=uri_escape($personalavatar);
		$useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
	    } else {
	        $personalavatar=uri_escape($personalavatar);
		$useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>);
	    }
	}
        elsif (($useravatar ne "noavatar") && ($useravatar)) {
            $useravatar=uri_escape($useravatar);
	    $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$useravatar.gif" border=0 $defaultwidth $defaultheight>);
        }
        else {$useravatar="没有"; }
    }
    
    $xnuseravatar = "没有";
    if ($userface ne '') {
        my ($currequip,$x,$loadface)=split(/\|/,$userface);
        $xnuseravatar = qq~<SCRIPT>Face_Info("$currequip","$imagesurl");</SCRIPT>~;
    }

    $interests = "没有" if ($interests eq "");
    $location  = "没有" if ($location eq "");

    if ($signaturehtml) {$signature = $signaturehtml ;} 
        elsif ($signatureorigin)  { if ($idmbcodestate eq 'on') { require "dosignlbcode.pl"; $signature = &signlbcode($signatureorigin); } $signature =~ s/\n/\<BR\>/isg;} 
	else {$signature = "没有";}

    if ($sex eq "f") {
	$sex = "美女 <img src=$imagesurl/images/fem.gif width=20 alt=美女 align=absmiddle>";
    }
    elsif ($sex eq "m") {
	$sex = "帅哥 <img src=$imagesurl/images/mal.gif width=20 alt=帅哥 align=absmiddle>";
    }
    else { $sex = "保密"; }

    $numberofreplys = 0 if ($numberofreplys eq "");
    $postdel   = 0 if ($postdel eq "");
    $jhmp    = "无门无派" if ($jhmp eq "");
    if ($rating !~ /^[0-9\-]+$/) {$rating = 0;}
    if ($rating eq "") {$rating =0;}
    $mymoney   = 0 if ($mymoney eq "");
    $education = "未输入" if ($education eq "");
    $marry     = "未输入" if ($marry eq "");
    $work      = "未输入" if ($work eq "");
    $born      = "未输入" if (($born eq "")||($born eq "//"));
    $userflag  = "blank" if ($userflag eq "");

$blank="未输入";
$China="中国";
$Angola="安哥拉";
$Antigua="安提瓜";
$Argentina="阿根廷";
$Armenia="亚美尼亚";
$Australia="澳大利亚";
$Austria="奥地利";
$Bahamas="巴哈马";
$Bahrain="巴林";
$Bangladesh="孟加拉";
$Barbados="巴巴多斯";
$Belgium="比利时";
$Bermuda="百慕大";
$Bolivia="玻利维亚";
$Brazil="巴西";
$Brunei="文莱";
$Canada="加拿大";
$Chile="智利";
$Colombia="哥伦比亚";
$Croatia="克罗地亚";
$Cuba="古巴";
$Cyprus="塞浦路斯";
$Czech_Republic="捷克";
$Denmark="丹麦";
$Dominican_Republic="多米尼加";
$Ecuador="厄瓜多尔";
$Egypt="埃及";
$Estonia="爱沙尼亚";
$Finland="芬兰";
$France="法国";
$Germany="德国";
$Great_Britain="英国";
$Greece="希腊";
$Guatemala="危地马拉";
$Honduras="洪都拉斯";
$Hungary="匈牙利";
$Iceland="冰岛";
$India="印度";
$Indonesia="印度尼西亚";
$Iran="伊朗";
$Iraq="伊拉克";
$Ireland="爱尔兰";
$Israel="以色列";
$Italy="意大利";
$Jamaica="牙买加";
$Japan="日本";
$Jordan="约旦";
$Kazakstan="哈萨克";
$Kenya="肯尼亚";
$Kuwait="科威特";
$Latvia="拉脱维亚";
$Lebanon="黎巴嫩";
$Lithuania="立陶宛";
$Malaysia="马来西亚";
$Malawi="马拉维";
$Malta="马耳他";
$Mauritius="毛里求斯";
$Morocco="摩洛哥";
$Mozambique="莫桑比克";
$Netherlands="荷兰";
$New_Zealand="新西兰";
$Nicaragua="尼加拉瓜";
$Nigeria="尼日利亚";
$Norway="挪威";
$Pakistan="巴基斯坦";
$Panama="巴拿马";
$Paraguay="巴拉圭";
$Peru="秘鲁";
$Poland="波兰";
$Portugal="葡萄牙";
$Romania="罗马尼亚";
$Russia="俄罗斯";
$Saudi_Arabia="沙特阿拉伯";
$Singapore="新加坡";
$Slovakia="斯洛伐克";
$Slovenia="斯洛文尼亚";
$Solomon_Islands="所罗门";
$Somalia="索马里";
$South_Africa="南非";
$South_Korea="韩国";
$Spain="西班牙";
$Sri_Lanka="印度";
$Surinam="苏里南";
$Sweden="瑞典";
$Switzerland="瑞士";
$Thailand="泰国";
$Trinidad_Tobago="多巴哥";
$Turkey="土耳其";
$Ukraine="乌克兰";
$United_Arab_Emirates="阿拉伯联合酋长国";
$United_States="美国";
$Uruguay="乌拉圭";
$Venezuela="委内瑞拉";
$Yugoslavia="南斯拉夫";
$Zambia="赞比亚";
$Zimbabwe="津巴布韦";
$blank="未输入";

    $usersx    = "blank" if ($usersx eq "");
    if ($usersx eq "sx1")     {$showsx = "子鼠 <IMG src=$imagesurl/sx/sx1s.gif  alt=子鼠 align=absmiddle>";}
    elsif ($usersx eq "sx2")  {$showsx = "丑牛 <IMG src=$imagesurl/sx/sx2s.gif  alt=丑牛 align=absmiddle>";}
    elsif ($usersx eq "sx3")  {$showsx = "寅虎 <IMG src=$imagesurl/sx/sx3s.gif  alt=寅虎 align=absmiddle>";}
    elsif ($usersx eq "sx4")  {$showsx = "卯兔 <IMG src=$imagesurl/sx/sx4s.gif  alt=卯兔 align=absmiddle>";}
    elsif ($usersx eq "sx5")  {$showsx = "辰龙 <IMG src=$imagesurl/sx/sx5s.gif  alt=辰龙 align=absmiddle>";}
    elsif ($usersx eq "sx6")  {$showsx = "巳蛇 <IMG src=$imagesurl/sx/sx6s.gif  alt=巳蛇 align=absmiddle>";}
    elsif ($usersx eq "sx7")  {$showsx = "午马 <IMG src=$imagesurl/sx/sx7s.gif  alt=午马 align=absmiddle>";}
    elsif ($usersx eq "sx8")  {$showsx = "未羊 <IMG src=$imagesurl/sx/sx8s.gif  alt=未羊 align=absmiddle>";}
    elsif ($usersx eq "sx9")  {$showsx = "申猴 <IMG src=$imagesurl/sx/sx9s.gif  alt=申猴 align=absmiddle>";}
    elsif ($usersx eq "sx10") {$showsx = "酉鸡 <IMG src=$imagesurl/sx/sx10s.gif alt=酉鸡 align=absmiddle>";}
    elsif ($usersx eq "sx11") {$showsx = "戌狗 <IMG src=$imagesurl/sx/sx11s.gif alt=戌狗 align=absmiddle>";}
    elsif ($usersx eq "sx12") {$showsx = "亥猪 <IMG src=$imagesurl/sx/sx12s.gif alt=亥猪 align=absmiddle>";}
    else {$showsx = "未输入";}

    $userxz    = "blank" if ($userxz eq "");
    if ($userxz eq "z1")     {$showxz = "白羊 <IMG height=15 src=$imagesurl/star/z1.gif  width=15 alt=白羊座 align=absmiddle>";}
    elsif ($userxz eq "z2")  {$showxz = "金牛 <IMG height=15 src=$imagesurl/star/z2.gif  width=15 alt=金牛座 align=absmiddle>";}
    elsif ($userxz eq "z3")  {$showxz = "双子 <IMG height=15 src=$imagesurl/star/z3.gif  width=15 alt=双子座 align=absmiddle>";}
    elsif ($userxz eq "z4")  {$showxz = "巨蟹 <IMG height=15 src=$imagesurl/star/z4.gif  width=15 alt=巨蟹座 align=absmiddle>";}
    elsif ($userxz eq "z5")  {$showxz = "狮子 <IMG height=15 src=$imagesurl/star/z5.gif  width=15 alt=狮子座 align=absmiddle>";}
    elsif ($userxz eq "z6")  {$showxz = "处女 <IMG height=15 src=$imagesurl/star/z6.gif  width=15 alt=处女座 align=absmiddle>";}
    elsif ($userxz eq "z7")  {$showxz = "天秤 <IMG height=15 src=$imagesurl/star/z7.gif  width=15 alt=天秤座 align=absmiddle>";}
    elsif ($userxz eq "z8")  {$showxz = "天蝎 <IMG height=15 src=$imagesurl/star/z8.gif  width=15 alt=天蝎座 align=absmiddle>";}
    elsif ($userxz eq "z9")  {$showxz = "射手 <IMG height=15 src=$imagesurl/star/z9.gif  width=15 alt=射手座 align=absmiddle>";}
    elsif ($userxz eq "z10") {$showxz = "魔羯 <IMG height=15 src=$imagesurl/star/z10.gif width=15 alt=魔羯座 align=absmiddle>";}
    elsif ($userxz eq "z11") {$showxz = "水瓶 <IMG height=15 src=$imagesurl/star/z11.gif width=15 alt=水瓶座 align=absmiddle>";}
    elsif ($userxz eq "z12") {$showxz = "双鱼 <IMG height=15 src=$imagesurl/star/z12.gif width=15 alt=双鱼座 align=absmiddle>";}
    else {$showxz = "未输入";}

    $mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
    $moneyname ="雷傲元" if ($moneyname eq "");

    my $onlinetimehour = int($onlinetime/3600);
    my $onlinetimemin  = int(($onlinetime%3600)/60);
    my $onlinetimesec  = int(($onlinetime%3600)%60);
    $onlinetimehour = "0$onlinetimehour" if ($onlinetimehour <10);
    $onlinetimemin  = "0$onlinetimemin"  if ($onlinetimemin <10);
    $onlinetimesec  = "0$onlinetimesec"  if ($onlinetimesec <10);
    
    
    if (-e "${lbdir}soccer.cgi")
    {
    	my ($mywin, $mydraw, $mylose, $myplay, $myget) = split(/:/, $soccerdata);
    	$mywin = 0 if ($mywin eq "");
    	$mydraw = 0 if ($mydraw eq "");
    	$mylose = 0 if ($mylose eq "");
    	$myplay = 0 if ($myplay eq "");
    	$myget = 0  if ($myget eq "");
    	my $soccerwinrate = 0;
	$soccerwinrate = sprintf("%.2f", $mywin * 100 / ($mywin + $mydraw + $mylose)) if (($mywin + $mydraw + $mylose) > 0);
	$soccerinfo = qq~  <tr>
    <td valign=middle colSpan=5><font color=$fontcolormisc>博彩战绩： 胜: <b><i>$mywin</i></b>　　平: <b><i>$mydraw</i></b>　　负: <b><i>$mylose</i></b>　　胜率: <b><i>$soccerwinrate</i></b>%　　　　历史投注: <b><i>$myplay</i></b> $moneyname　　历史收益: <b><i>$myget</i></b> $moneyname</font></td>
  </tr>~ if (($mywin + $mydraw + $mylose) > 0);
     }

    my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
    if ($mystatus) {
	$mysaves .= " $moneyname";
	if ($myloan) {
	    $myloan .= " $moneyname";
	} else {
	    $myloan = "没贷款";
	}
    } else {
	$mysaves = "没开户";
	$myloan = "没贷款";
    }
    
    $inmember = uri_escape($inmember);
    
    $jhcount = 0 if ($jhcount <0);

    $onlinetimehour = int($onlinetime/3600);
    $onlinetimemin  = int(($onlinetime%3600)/60);
    $onlinetimesec  = int(($onlinetime%3600)%60);
    $onlinetimehour = "0$onlinetimehour" if ($onlinetimehour <10);
    $onlinetimemin  = "0$onlinetimemin"  if ($onlinetimemin <10);
    $onlinetimesec  = "0$onlinetimesec"  if ($onlinetimesec <10);
    if ($onlinetimehour >= 1000) { my $onlinetime1 = $onlinetimehour; $onlinetime = int($onlinetime1/24); $onlinetime1 = $onlinetime1 - $onlinetime * 24; $onlinetime = "$onlinetime天$onlinetime1时$onlinetimemin分$onlinetimesec秒"; }
                                         else { $onlinetime = "$onlinetimehour 时 $onlinetimemin 分 $onlinetimesec 秒"; }

    if (-e "${lbdir}pet.cgi") {

  eval{ require "${lbdir}petdata/config.pl"; } if ($pet_open eq "");
  if ($pet_open eq 'open') {
    if(-e"${lbdir}petdata/pet/$membername.cgi") {
	open(file,"${lbdir}petdata/pet/$membername.cgi");
	my $file=<file>;
	close(file);

	my $pet_zt;
	my $pet_style;
	my ($pet_name,$pet_jb,$x,$pet_sx,$pet_born,$pet_win,$pet_lose,$pet_gjl,$pet_fyl,$pet_exp,$pet_hp,$pet_sp,$x,$x,$x,$x,$x,$x,$x,$x,$pet_die,$x,$x,$pet_xz_time)=split(/\t/,$file);
	$pet_xz_time or $pet_xz_time = $pet_born;
	$pet_born=int((time-$pet_born)/86400)+1;
	if(time - $pet_xz_time > 86400*3) {$pet_xz_time="身上痒痒的，快给我洗澡吧";} else {$pet_xz_time='很舒服，不用洗澡了';}
	if ($pet_sp<0) {$pet_zt.='(我好久没吃东西了)';} elsif ($pet_sp<500) {$pet_zt.='(我快饿死了)';} elsif ($pet_sp<1000) {$pet_zt.='(我好饿啊)';} elsif ($pet_sp<2000) {$pet_zt.='(我好想吃东西)';} else {$pet_zt.='(我好饱哦)';}

	my $pet_exp1 = int(sqrt($pet_exp)/6);
	$pet_exp1 = 110 if ($pet_exp1 > 110);
	$pet_exp1 = qq~<img src=$imagesurl/images/jy_left.gif width=2 height=8><img src=$imagesurl/images/jy_0.gif width=$pet_exp1 height=8 alt="经验: $pet_exp"><img src=$imagesurl/images/jy_right.gif width=4 height=8>~;

	my $pet_hp1 = int(sqrt($pet_hp));
	$pet_hp1 = 110 if ($pet_hp1 > 110);
	$pet_hp1 = qq~<img src=$imagesurl/images/vi_left.gif width=2 height=8><img src=$imagesurl/images/vi_0.gif width=$pet_hp1 height=8 alt="体力: $pet_hp"><img src=$imagesurl/images/vi_right.gif width=4 height=8>~;

	my $pet_sp1 = int(sqrt($pet_sp)/6);
	$pet_sp1 = 110 if ($pet_sp1 > 110);
	$pet_sp1 = qq~<img src=$imagesurl/images/jy_left.gif width=2 height=8><img src=$imagesurl/images/jy_0.gif width=$pet_sp1 height=8 alt="食物: $pet_sp"><img src=$imagesurl/images/jy_right.gif width=4 height=8>~;

	$pet_jb1=$pet_jb;
	$pet_jb=int($pet_jb/10);

	if($pet_die eq 'die'){$pet_name.='(已经死亡)'; $pet_zt=''; $pet_xz_time='已经死亡...'; $pet_style = qq~ style="filter:xray"~; }
	my $tempmembername = uri_escape($inmembername);
	$petinfo=qq~<tr><td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc><b>宠物资料：</b></font></td><td bgcolor=$miscbacktwo valign=middle><table border="1" width="320" style="border-collapse: collapse" bordercolor="$tablebordercolor" cellPadding=2 cellSpacing=0><tr><td colspan="2" height="23" bgcolor="$miscbacktwo">&nbsp;<img src=$imagesurl/pet_maiweb/cw.gif> 昵称： <a href=pet.cgi?action=myspet&petname=$tempmembername target=_blank><b>$pet_name</b></a> $pet_zt　　年龄： $pet_born 天</td></tr><tr><td width="110" align=center $pet_style><img src=$imagesurl/pet_maiweb/pet/$pet_sx/$pet_sx$pet_jb.gif border=0></td><td width="*">&nbsp;胜利 $pet_win 次 / 失败 $pet_lose 次<br>&nbsp;攻击力 $pet_gjl 点 / 防御力 $pet_fyl 点<br>&nbsp;经验： $pet_exp1<br>&nbsp;体力： $pet_hp1<br>&nbsp;食物： $pet_sp1<BR>&nbsp;状态： $pet_xz_time</td></tr></table></td></tr>~;
    } else { $petinfo='';}
} else { $petinfo='';}

}  else { $petinfo='';}

    $output .= qq~

	    <tr>
	    <td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center><font color=$fontcolormisc>"<b><font color=$fonthighlight>$membername</b></font>" 的个人资料</td></tr>
  <tr>
    <td bgcolor=$miscbackone valign=middle width=150 align=center>$xnuseravatar</td>
    <td bgcolor=$miscbackone valign=middle>
<table width="100%" border="0" cellspacing="0" cellpadding="4">
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>用户名：</font></td>
    <td valign=middle><font color=$fontcolormisc>$membername</font></td>
    <td valign=middle><font color=$fontcolormisc>性别：</font></td>
    <td valign=middle><font color=$fontcolormisc>$sex</font></td>
    <td valign=middle><font color=$fontcolormisc>注册时间：</font></td>
    <td valign=middle><font color=$fontcolormisc>$joineddate</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>出生年月：</font></td>
    <td valign=middle><font color=$fontcolormisc>$born</font></td>
    <td valign=middle><font color=$fontcolormisc>生肖：</font></td>
    <td valign=middle><font color=$fontcolormisc>$showsx</font></td>
    <td valign=middle><font color=$fontcolormisc>星座：</font></td>
    <td valign=middle><font color=$fontcolormisc>$showxz</font></td>
  </tr>
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>婚姻状况：</font></td>
    <td valign=middle><font color=$fontcolormisc>$marry</font></td>
    <td valign=middle><font color=$fontcolormisc>学历：</font></td>
    <td valign=middle><font color=$fontcolormisc>$education</font></td>
    <td valign=middle><font color=$fontcolormisc>职业：</font></td>
    <td valign=middle><font color=$fontcolormisc>$work</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>威望：</font></td>
    <td valign=middle><font color=$fontcolormisc>$rating</font></td>
    <td valign=middle><font color=$fontcolormisc>积分：</font></td>
    <td valign=middle><font color=$fontcolormisc>$jifen</font></td>
    <td valign=middle><font color=$fontcolormisc>精华帖;</font></td>
    <td valign=middle><font color=$fontcolormisc>$jhcount 篇</font></td>
  </tr>
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>当前级别：</font></td>
    <td valign=middle><font color=$fontcolormisc><a href="lookinfo.cgi?action=style" target="_blank">$mtitle</a></font></td>
    <td valign=middle><font color=$fontcolormisc>当前头衔：</font></td>
    <td valign=middle><font color=$fontcolormisc>$membertitle</font></td>
    <td valign=middle><font color=$fontcolormisc>江湖门派：</font></td>
    <td valign=middle><font color=$fontcolormisc>$jhmp</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>总共发表：</font></td>
    <td valign=middle><font color=$fontcolormisc>$numberofposts 篇</font></td>
    <td valign=middle><font color=$fontcolormisc>总共回复：</font></td>
    <td valign=middle><font color=$fontcolormisc>$numberofreplys 篇</font></td>
    <td valign=middle><font color=$fontcolormisc>被删除：</font></td>
    <td valign=middle><font color=$fontcolormisc>$postdel 篇</font></td>
  </tr>
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>邮件地址：</font></td>
    <td valign=middle><font color=$fontcolormisc>$emailaddress</font></td>
    <td valign=middle><font color=$fontcolormisc>QQ 号码：</font></td>
    <td valign=middle><font color=$fontcolormisc>$qqlogo $oicqnumber</font></td>
    <td valign=middle><font color=$fontcolormisc>ICQ 号码：</font></td>
    <td valign=middle><font color=$fontcolormisc>$icqlogo $icqnumber</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>国家：</font></td>
    <td valign=middle><font color=$fontcolormisc>$$userflag <img src=$imagesurl/flags/$userflag.gif alt="$$userflag" width=21 height=14></font></td>
    <td valign=middle><font color=$fontcolormisc>来自：</font></td>
    <td valign=middle><font color=$fontcolormisc>$location</font></td>
    <td valign=middle><font color=$fontcolormisc>主页地址：</font></td>
    <td valign=middle><font color=$fontcolormisc>$homepage</font></td>
  </tr>
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>现金：</font></td>
    <td valign=middle><font color=$fontcolormisc>$mymoney $moneyname</font></td>
    <td valign=middle><font color=$fontcolormisc>存款：</font></td>
    <td valign=middle><font color=$fontcolormisc>$mysaves</font></td>
    <td valign=middle><font color=$fontcolormisc>贷款：</font></td>
    <td valign=middle><font color=$fontcolormisc>$myloan</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>在线时间：</font></td>
    <td valign=middle><font color=$fontcolormisc>$onlinetime</font></td>
    <td valign=middle><font color=$fontcolormisc>访问次数：</font></td>
    <td valign=middle><font color=$fontcolormisc>$visitno 次</font></td>
    <td valign=middle><font color=$fontcolormisc>最后访问：</font></td>
    <td valign=middle><font color=$fontcolormisc>$lastgone</font></td>
  </tr>
$soccerinfo
  <tr bgcolor=$miscbacktwo align=center>
    <td valign=middle colspan=2><span onClick="openScript('friendlist.cgi?action=adduser&adduser=$inmember', 420, 320)" style="cursor: hand">把$membername加为我的好友</span></td>
    <td valign=middle colspan=2><span onClick="openScript('messanger.cgi?action=new&touser=$inmember&actionto=msg', 600, 400)" style="cursor: hand">发送一个短消息给$membername</span></td>
    <td valign=middle colspan=2><a href=search.cgi?action=startsearch&TYPE_OF_SEARCH=username_search&NAME_SEARCH=topictitle_search&FORUMS_TO_SEARCH=all&SEARCH_STRING=$inmember target=_blank>查找$membername发表的所有帖子</a></td>
  </tr>
</table>
</td>
  </tr>
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc><b>最后发表：</b></font></td>
	    <td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc>$lastpostdetails</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>自我简介：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$interests</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc><b>签名：</b></font></td>
	    <td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc>$signature</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>个性图片：</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><br>$useravatar</td></tr>
		$petinfo
	    </table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR>
	    ~;
}
