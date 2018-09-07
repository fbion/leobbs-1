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
require "cleanolddata.pl";
$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$thisprog = "loginout.cgi";
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

$inforum  = $query -> param('forum');
&error("打开文件&老大，别乱黑我的程序呀！") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

for ('inmembername','inpassword','action','CookieDate','onlineview','viewMode','nodispavatar',
'nodispsign','nodispphoto','freshtime','hidden','selectstyle','tanchumsg') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
}
$hidden = 0 if ($canhidden eq "no");
$CookieDate = "+1d" if ($CookieDate eq "");

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "客人") {
    $inmembername = "客人";
    $userregistered = "no";
}
else {
    &error("用户登陆&对不起，您输入的用户名有问题，请不要在用户名中包含\@\#\$\%\^\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]这类字符！") if ($inmembername =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/);
    &getmember("$inmembername","no");
    &error("用户登录&对不起,用户名和密码输入错误！") if (($inpassword ne $password)&&($action ne "logout"));
    $inmembername = $membername;
}
$memberfilename = $inmembername;
$memberfilename =~ s/ /\_/g;
$memberfilename =~ tr/A-Z/a-z/;
&getoneforum("$inforum");
#&moderator("$inforum");
#&title;
&mischeader("登录/退出");

$output .= qq~<p><SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
~;

if ($action eq "login") {
    &cleanolddata;
    if (($userregistered ne "no") && ($inpassword eq $password)) {
	&whosonline("$inmembername\t论坛登录\tnone\t登录论坛\t");
	if ($inforum eq "") { $refrashurl = "leobbs.cgi"; } else { $refrashurl = "forums.cgi?forum=$inforum"; }
	$output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>感谢你登录 $inmembername</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
具体情况：<ul><li><a href="$refrashurl">进入论坛</a>
<meta http-equiv="refresh" content="3; url=$refrashurl">
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

	if ($boarddispsign eq "no") { $nodispsign="yes"; } else { $nodispsign="no" if !($nodispsign); } 
        	
	$namecookie        = cookie(-name => "amembernamecookie", -value => "$inmembername", -path => "$cookiepath/", -expires => "$CookieDate");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "$inpassword",   -path => "$cookiepath/", -expires => "$CookieDate");
	$onlineviewcookie  = cookie(-name => "onlineview",        -value => "$onlineview",   -path => "$cookiepath/", -expires => "$CookieDate");
	$viewcookie        = cookie(-name => "viewMode",          -value => "$viewMode",     -path => "$cookiepath/", -expires => "$CookieDate");
	$freshtimecookie   = cookie(-name => "freshtime",         -value => "$freshtime",    -path => "$cookiepath/", -expires => "$CookieDate");
	$selectstylecookie = cookie(-name => "selectstyle",       -value => "$selectstyle",  -path => "$cookiepath/", -expires => "$CookieDate");
	$tanchumsgcookie   = cookie(-name => "tanchumsg",         -value => "$tanchumsg",    -path => "$cookiepath/", -expires => "$CookieDate");
	$nodisp            = cookie(-name => "nodisp",            -value => "$nodispavatar|$nodispsign|$nodispphoto", -path => "$cookiepath/", -expires => "$CookieDate");


  	print header(-cookie=>[$onlineviewcookie,$threadcookie,$viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie, $namecookie,$passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

    }
    else {

	print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

	$output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>登录错误</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>登录错误的可能原因：
<ul><li>密码错误<li>用户名错误<li>您不是<a href=register.cgi?forum=$inforum>注册</a>用户</ul></tr></td></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    }
}
elsif ($action eq "logout") {
   &cleanolddata1;
   if ($inmembername ne "" && $inmembername ne "客人") {
    $filetoopen = "$lbdir" . "data/onlinedata.cgi";
    my $filetoopens = &lockfilename($filetoopen);
    if (!(-e "$filetoopens.lck")) {
	&winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(FILE,"$filetoopen");
	flock(FILE, 1) if ($OS_USED eq "Unix");
	sysread(FILE, my $onlinedata,(stat(FILE))[7]);
	close(FILE);
	$onlinedata =~ s/\r//isg;

	if (length($onlinedata) >= 80) {
	    my $inmembername1 = $inmembername;
   	    $inmembername1 =~ s/\|/\\\|/isg;
   	    $onlinedata =~ s/(.*)(^|\n)$inmembername1\t(.*?)(\n|$)(.*)/$1$2$5/i;
	    ($savedcometime, $savedtime, undef) = split(/\t/, $3);
	    open(ONLINEFILE,">$filetoopen");
            flock(ONLINEFILE, 2) if ($OS_USED eq "Unix");
            print ONLINEFILE "$onlinedata";
	    close(ONLINEFILE);
	}
	else { unlink("$filetoopen"); }
	&winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	require "douplogintime.pl";
        &uplogintime("$inmembername","")
    }
    else {
    	unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
    }
   }
    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>您现在已经退出论坛</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
具体选项：<ul><li><a href="leobbs.cgi">返回论坛</a><li><a href=javascript:close();>关闭您的浏览器</a></ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        $trashcookie       = cookie(-name => "templastvisit",     -value => "", -path => "$cookiepath/");
        $onlineviewcookie  = cookie(-name => "onlineview",        -value => "", -path => "$cookiepath/");
        $viewcookie        = cookie(-name => "viewMode",          -value => "", -path => "$cookiepath/");
        $nodisp            = cookie(-name => "nodisp",            -value => "", -path => "$cookiepath/");
        $freshtimecookie   = cookie(-name => "freshtime",         -value => "", -path => "$cookiepath/");
        $selectstylecookie = cookie(-name => "$selectstyle",      -value => "", -path => "$cookiepath/");
        $tanchumsgcookie   = cookie(-name => "$tanchumsg",        -value => "", -path => "$cookiepath/");
       	$banfreshcookie    = cookie(-name => "banfresh"         , -value => "", -path => "$cookiepath/");
	$treeviewcookie    = cookie(-name => "treeview"         , -value => "", -path => "$cookiepath/");
	$tecookie	   = cookie(-name => "catlog"           , -value => "", -path => "$cookiepath/");


        print header(-cookie=>[$banfreshcookie, $treeviewcookie, $tecookie, $namecookie, $passcookie, $trashcookie,$onlineviewcookie,$viewcookie, $nodisp, $freshtimecookie, $selectstylecookie, $tanchumsgcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

}
else {
    if ($query->cookie("selectstyle")) { $inselectstyle = $query->cookie("selectstyle"); }
    $inselectstyle   = $skinselected if ($inselectstyle eq "");
    if ($query->cookie("viewMode") ne "")  { $checked ="checked"; $checked1 =""; } else { $checked1 ="checked"; $checked =""; }
    if ($query->cookie("tanchumsg") eq "") { $tcchecked ="checked"; $tcchecked1 =""; } else { $tcchecked1 ="checked"; $tcchecked =""; }
    if (($query->cookie("onlineview") == 1)||($query->cookie("onlineview") eq "")) { $online ="checked"; $online1 =""; } else { $online1 ="checked"; $online =""; }
    $nodisp = $query->cookie("nodisp");
    ($nodispavatar, $nodispsign, $nodispphoto)  = split(/\|/,$nodisp);
    if ($nodispavatar eq "yes"){ $checked2 ="checked" ; }

    if ($boarddispsign eq "no") { $checked3 ="checked disabled"; }
    elsif ($boarddispsign eq "noselect" && $nodispsign eq "")    { $checked3 ="checked"; }
    elsif ($boarddispsign eq "noselect" && $nodispsign eq "yes") { $checked3 ="checked"; }
    elsif ($boarddispsign eq "noselect" && $nodispsign eq "no")  { $checked3 ="" ;       }
    elsif ($boarddispsign eq "yes" && $nodispsign eq "")         { $checked3 ="";        }
    elsif ($boarddispsign eq "yes" && $nodispsign eq "yes")      { $checked3 ="checked"; }	
    elsif ($boarddispsign eq "yes" && $nodispsign eq "no")       { $checked3 ="";        }	

    if ($nodispphoto eq "yes") { $checked4 ="checked"; }


    print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
    if ($inmembername ne "客人") {
      my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
      $filetoopens = &lockfilename($filetoopens);
      if (!(-e "$filetoopens.lck")) {
	&whosonline("$inmembername\t论坛登录\tnone\t登录论坛\t");
      }
    }
    opendir (DIR, "${lbdir}data/skin");
    @skindata = readdir(DIR);
    closedir (DIR);
    my $myskin="";
    @skindata = grep(/\.cgi$/,@skindata);
    $topiccount = @skindata;
    @skindata=sort @skindata;
    for (my $i=0;$i<$topiccount;$i++){
        $skindata[$i]=~s /\.cgi//isg;
        $myskin.=qq~<option value="$skindata[$i]">[ $skindata[$i] ]</option>~;
    }
    if ($canhidden ne "no") {
        $userhidden = qq~<tr><td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>论坛隐身</b><BR>请选择你的登录显示方式，可以适当保密你的隐私。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="hidden" value="0" checked id=1> <label for=1>正常登录，显示在在线会员列表中</label><br>
                <input type="radio" name="hidden" value="1" id=2> <label for=2>隐身登录，不要把我显示在在线列表中</label><br>
                </font>
                </td></tr>
    ~;
    }
    else { $userhidden = ""; }
$helpurl = &helpnewfiles("快速登录");
$helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

    $output .= qq~
    <tr>
    <td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
    <form action="$thisprog" name="login" method="post" onSubmit="submitonce(this)">
    <input type=hidden name="action" value="login">
    <input type=hidden name="forum" value="$inforum">
    <font face="$font" color=$fontcolormisc><b>请输入您的用户名、密码登录</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="inmembername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="inpassword"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
    <tr>
    <td bgcolor=$miscbacktwo colspan=2 valign=middle><font face="$font" color=$fontcolormisc><b>论坛登录选项</b></font></td></tr>
    $userhidden
    <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>Cookie 选项</b><BR> 请选择你的 Cookie 保存时间，下次访问可以方便输入。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="CookieDate" value="0" checked id=3> <label for=3>不保存，关闭浏览器就失效</label> <font color=$fonthighlight>(在网吧等公共场所建议选择这个)</font><br>
                <input type="radio" name="CookieDate" value="+1d" id=4> <label for=4>保 存 一 天</label><br>
                <input type="radio" name="CookieDate" value="+30d" id=5> <label for=5>保 存 一 月</label><br>
                <input type="radio" name="CookieDate" value="+20y" id=6> <label for=6>永 久 保 存</label> <font color=$fonthighlight>(在家里或使用自己的电脑时才可选择这个)</font><br>
                </font>
                </td></tr>
</table></td></tr></table>
~; 
if ($advlogin == 1) { 
$advloginout = "true"; 
$advmode = qq~<td width=50%><INPUT id=advcheck name=advshow type=checkbox value=1 onclick=showadv() checked><span id="advance">关闭高级登录选项</a></span> </td><td width=50%><input type=submit value="登 录" name=submit></td>~;} 
else { 
$advloginout = "none"; 
$advmode = qq~<td width=50%><INPUT id=advcheck name=advshow type=checkbox value=1 onclick=showadv()><span id="advance">显示高级登录选项</a></span> </td><td width=50%><input type=submit value="登 录" name=submit></td>~;} 
$output .=qq~ 
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center id=adv style="DISPLAY: $advloginout">
 <tr><td>
    <table cellpadding=4 cellspacing=1 width=100%>

<tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>在线列表</b> 请选择你的在线名单显示方式，可以加快论坛显示。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="onlineview" value="1" $online id=9> <label for=9>显示详细名单</label><br>
                <input type="radio" name="onlineview" value="0" $online1 id=10> <label for=10>关闭详细名单</label><br>
                </font>
                </td></tr>
      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>查看贴子</b> 请选择你喜好的查看贴子方式，可以方便阅读。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" name="viewMode" value="" $checked1 id=11> <label for=11>在原窗口中浏览</label><br>
                <input type="radio" name="viewMode" value="_blank" $checked id=12> <label for=12>在新窗口中浏览</label><br>
                </font>
                </td></tr>

      <tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>查看贴子内容</b> 请选择查看贴子内容时候是否显示用户头像、签名和贴图。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="checkbox" name="nodispavatar" value="yes" $checked2 id=13> <label for=13>不显示用户头像</label><br>
                <input type="checkbox" name="nodispsign"   value="yes" $checked3 id=14> <label for=14>不显示用户签名</label><br>
                <input type="checkbox" name="nodispphoto"  value="yes" $checked4 id=15> <label for=15>不显示用户贴图</label><br>
                </font>
                </td></tr>
		   <tr>
~;
if ($showskin ne "off") {$output.=qq~
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>风格设定</b> 请选择你的论坛风格。</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
		  <select name="selectstyle">
        <option value="">默认风格</option>
	$myskin
        </select>
        </font>
        </td></tr>
~;}
$output.=qq~
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>有短消息是否弹出？</b> <BR>（如果管理员设置了不弹出则此选择无效）</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
                <input type="radio" class=1 name="tanchumsg" value="" $tcchecked id=16> <label for=16>弹出短消息窗口</label><br>
                <input type="radio" class=1 name="tanchumsg" value="no" $tcchecked1 id=17> <label for=17>不弹出短消息窗口</label><br>
                </font></td></tr>

<tr>
    <td bgcolor=$miscbackone valign=top width=30%><font face="$font" color=$fontcolormisc><b>页面自动刷新时间</b> <BR>请输入分论坛首页自动刷新的时间（不输入则按照分论坛的默认设置进行刷新或者不刷新）</font></td>
    <td bgcolor=$miscbackone valign=middle><font class='misc'>
每隔 <input type=text name="freshtime" value="$freshtime" maxlength="2" size="2"> 分钟自动刷新一次

</tr>
</table></td></tr>
<SCRIPT>valignend()</SCRIPT>
<script>
function showadv(){
if (document.login.advshow.checked == true) {
		adv.style.display = "";
		advance.innerText="关闭高级登录选项"
	}else{
		adv.style.display = "none";
		advance.innerText="显示高级登录选项"
	}
}		
function submitonce(theform){
if (document.all||document.getElementById){
for (i=0;i<theform.length;i++){
var tempobj=theform.elements[i]
if(tempobj.type.toLowerCase()=="submit"||tempobj.type.toLowerCase()=="reset")
tempobj.disabled=true
}}}
</script>
</tr></table><img src="" width=0 height=4><BR>
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
<tr>
$advmode</form></tr></table></td></tr></table><BR><BR>

~;
}

$inselectstyle =~ s/\(/\\(/isg;
$inselectstyle =~ s/\)/\\)/isg;
$output =~ s/option value=\"$inselectstyle\"/option value=\"$inselectstyle\" selected/;
&output("$boardname - 登录/退出",\$output);
exit;
