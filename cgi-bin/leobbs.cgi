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
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

eval{ require "data/boardinfo.cgi"; };
if ($@) {
    require "data/boardinfobak.cgi";
    open(FILE,"data/boardinfobak.cgi");
    my @ddd = <FILE>;
    close(FILE);
    open(FILE,">data/boardinfo.cgi");
    foreach (@ddd) {
    	chomp $_;
        print FILE "$_\n";
    }
    close(FILE);
}
require "data/styles.cgi";
require "data/mpic.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "leobbs.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

require "imagead.cgi" if (($useimagead eq "1")||($useimagead1 eq "1"));
$query = new LBCGI;
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}
&ipbanned; #封杀一些 ip
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }

$action = $query->param('action');
$catlog = $query->cookie('catlog');
$catlog1 = $query->param('catlog');

$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($action eq "delcookieall") { require "dodelallcookies.pl"; }

if ($inmembername eq "") { $inmembername = "客人"; }
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
    eval('use VISITFORUM qw(getlastvisit);');
    &getlastvisit;
}

$union      = $query->cookie("union");
$union      = 1 if ($union eq "");
$screenmode = $query->cookie("screenmode");
$screenmode = 8 if ($screenmode eq "");

my $onlineview1 = $query->cookie("onlineview");
$onlineview = $onlineview1 if ($onlineview1 ne "");
$onlineview = 0 if ($onlineview eq "");
$onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
$timeadd  = $timedifferencevalue*3600 + $timezone*3600;
$currenttime = time;
$nowtime = &shortdate($currenttime + $timeadd);
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }
if ($catsbackpicinfo ne "")  { $catsbackpicinfo = "background=$imagesurl/images/$skin/$catsbackpicinfo"; }

if (((-e "${lbdir}cache/forumcache-$skin.pl")&&((-M "${lbdir}cache/forumcache-$skin.pl") *86400 < 220))||(-e "${lbdir}cache/forumcache-$skin.pl.lock")) {
    unlink("${lbdir}cache/forumcache-$skin.pl.lock") if ((-M "${lbdir}cache/forumcache-$skin.pl.lock") *86400 > 15);
    if (-e "${lbdir}cache/forumcache-$skin.pl.lock") {
    	select(undef, undef, undef, 0.2);
	select(undef, undef, undef, 0.2) if (-e "${lbdir}cache/forumcache-$skin.pl.lock");
	select(undef, undef, undef, 0.2) if (-e "${lbdir}cache/forumcache-$skin.pl.lock");
	select(undef, undef, undef, 0.3) if (-e "${lbdir}cache/forumcache-$skin.pl.lock");
	unlink("${lbdir}cache/forumcache-$skin.pl.lock");
	&error("普通错误&服务器忙，请稍后再试！！") if (-e "${lbdir}cache/forumcache-$skin.pl.lock");
    }
    if (-e "${lbdir}cache/forumcache-$skin.pl") {
        eval{ require "${lbdir}cache/forumcache-$skin.pl"; };
        if ($@) { unlink ("${lbdir}cache/forumcache-$skin.pl"); require "doforumcache.pl"; }
        $forumcached = "yes";
    } else { require "doforumcache.pl"; }
}
else { require "doforumcache.pl"; }

if ($action eq "union")    { if ($union == 1) { $union=0; } else { $union=1; } }
if ($action eq "resetall") { require "resetall.pl"; }

if ($action eq "expand")   { $catlog="-"; }
elsif ($action eq "depand")   { $catlog="--"; }
else {
    foreach (split(/-/,$catlog)) {
        next if ($_ eq "");
        $catshow{$_}=1;
    }
    if ($catlog1) {
        if ($catshow{$catlog1}) { delete $catshow{$catlog1}; }
                       else { $catshow{$catlog1}=1; }
    }
    if ($catlog ne "--" || $catlog1 ne "") {
        $catlog = "";
        foreach (keys %catshow) {$catlog.="-$_" if ($_ ne "");}
    }
}


if ($onlineview==1) { $onlinetitle="<a href=$thisprog?action=onlineview><font color=$fontcolormisc>关闭详细列表</font></a>"; } else { $onlinetitle="<a href=$thisprog?action=onlineview><font color=$fontcolormisc>显示详细列表</font></a>";}
               
$onlineviewcookie = cookie(-name => "onlineview", -value => "$onlineview", -path => "$cookiepath/" , -expires => "+30d");
$catlogcookie     = cookie(-name => "catlog"    , -value => "$catlog"    , -path => "$cookiepath/" , -expires => "+30d");
$unioncookie      = cookie(-name => "union"     , -value => "$union"     , -path => "$cookiepath/" , -expires => "+30d");

&title;

print header(-cookie  =>[$onlineviewcookie, $cookie, $tempcookie ,$unioncookie,$catlogcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

if ($action eq "expand" || $action eq "depand" || $catlog1 ne "") {
    print qq ~<script>location.href="leobbs.cgi";</script>~;
    exit;
}

if ($useadfoot ne 0) {
    $adfoot   = &HTML("$adfoot");
    $adfoot   =~ s/\$imagesurl/$imagesurl/isg;
    $adfoot   =~ s/\[br\]/\n/isg;
}
else { $adfoot =""; }

$insidead  = "" if ($useimagead  ne "1");
$insidead1 = "" if ($useimagead1 ne "1");

$output .= qq~$insidead$insidead1~;
$output .= qq~<BGSOUND SRC=$imagesurl/midi/$midiaddr2 LOOP=-1>~ if ($midiaddr2 ne "");

if ($usefake eq "yes") {
$output .= qq~<script language="javascript">
function O3(id) {window.open("forums-"+id+"-0.htm");}
function O9(id) {if(id!="")window.open("profile-"+id+".htm");}
~;
} else {
$output .= qq~<script language="javascript">
function O3(id) {window.open("forums.cgi?forum="+id);}
function O9(id) {if(id!="")window.open("profile.cgi?action=show&member="+id);}
~;
}
$output .= qq~
var expDays = 30;var exp = new Date();exp.setTime(exp.getTime() + (expDays*24*60*60*1000));
if (screen.width <= 800 ){SetCookie('screenmode','5',exp,"$cookiepath/");}
if ((screen.width >800 )&&(screen.width<=1024)){SetCookie('screenmode','8',exp,"$cookiepath/");}
if (screen.width >1024 ){SetCookie('screenmode','10',exp,"$cookiepath/");}
function SetCookie (name, value) { var argv = SetCookie.arguments;var argc = SetCookie.arguments.length;var expires = (argc > 2) ? argv[2] : null;var path = (argc > 3) ? argv[3] : null;var domain = (argc > 4) ? argv[4] : null;var secure = (argc > 5) ? argv[5] : false; document.cookie = name + "=" + escape (value) + ((expires == null) ? "" : ("; expires=" + expires.toGMTString())) + ((path == null) ? "" : ("; path=" + path)) + ((domain == null) ? "" : ("; domain=" + domain)) + ((secure == true) ? "; secure" : ""); } 
</script>
<br>
~;
&whosonline("$inmembername\t论坛首页\tboth\t查看论坛信息");
undef $memberoutput if ($onlineview != 1);

if ($announcements eq 'yes') {
    if (-e "${lbdir}data/announce.pl") {
        require "${lbdir}data/announce.pl";
        $announcedisp =~ s/\$forumfontcolor/$forumfontcolor/isg;
	$announcedisp =~ s/\$fonthighlight/$fonthighlight/isg;
    } else {
        $announcedisp=qq~&nbsp;<a href=announcements.cgi target=_blank title=当前没有公告><b>当前没有公告</b></a>~;
	$announcetemp1 = qq~<img src=$imagesurl/images/announce.gif border=0 alt=总论坛暂时无公告！ width=18>~;
    }
}

if ($adlinks ne "") {
    require "doadlinks.pl";
}

$rsshtml = qq~<td align=center width=80><a href="rss.cgi?/leo.xml" target="_blank"><img src="$imagesurl/images/xml.gif" height=15 border="0" align="absmiddle" alt="RSS 订阅全部论坛"></a>&nbsp;<a href="wap.cgi" target="_blank"><img src="$imagesurl/images/wap.gif" height=15 border="0" align="absmiddle" alt="通过手机访问论坛，地址：$boardurl/wap.cgi"></a></td>~;
if ($regaccess eq "on") {
$rsshtml = "";
}

if ($rssinfo eq "no") {
$rsshtml = "";
}

$output .= qq~$adlinks
<table cellpadding=1 cellspacing=0 width=$tablewidth align=center>
<tr><td align=center width=2></td>
<td align=center width=34>$announcetemp1</td><td width=* align=left><font color=$forumfontcolor>$announcedisp</td><td width=140>&nbsp;</td>
$rsshtml
<td width=64 align=right><a href=team.cgi target=_blank><img src=$imagesurl/images/$skin/team.gif border=0 alt=显示管理团队 align=absmiddle></a></td>
<td width=64 align=right><a href=memberlist.cgi?a=4 target=_blank><img src=$imagesurl/images/$skin/userlist.gif border=0 alt=显示用户列表 align=absmiddle></a></td>
<td width=64 align=right><a href=memberlist.cgi?a=1 target=_blank><img src=$imagesurl/images/$skin/top.gif border=0 alt=显示发帖量排名 align=absmiddle></a></td>
</tr></table>
<style>
TABLE {BORDER-TOP: 0px; BORDER-LEFT: 0px; BORDER-BOTTOM: 1px; }
TD    {BORDER-RIGHT: 0px; BORDER-TOP: 0px; color: $fontcolormisc; }
</style>
~;
if ($dispinfos ne "no") {
$output .= qq~
<img src=$imagesurl/images/none.gif height=2><br>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=6 cellspacing=0 width=$tablewidth height=28 align=center bordercolor=$tablebordercolor border=1>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellpadding=6 cellspacing=1 width=100%>
~;

if ($inmembername eq "客人") {
    require "fastlogin.pl";
}
else {
  $memberfilename = $inmembername;
  $memberfilename =~ s/ /\_/g;
  $memberfilename =~ tr/A-Z/a-z/;
  if ((-e "${lbdir}cache/myinfo/$memberfilename.pl")&&(((-M "${lbdir}cache/myinfo/$memberfilename.pl") *86400 < 1800)||($docache eq "yes"))) {
    eval{ require "${lbdir}cache/myinfo/$memberfilename.pl";};
    if ($@) { unlink ("${lbdir}cache/myinfo/$memberfilename.pl"); require "domyinfo.pl"; }
  } else { require "domyinfo.pl"; }
  $output =~ s/totalmessageshtc/$totalmessages/isg;
}

$todaypostlist =~ s/totleonlineall/$totleonlineall/isg;

$output .= qq~$todaypostlist
</td></tr></form></table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR>~;

}

if (($displink eq "yes")&&($links ne "")&&($displinkaddr eq "2")) {
    require "dodisplink.pl";
}

$output .= qq~<img src=$imagesurl/images/none.gif height=5><br>
<SCRIPT LANGUAGE="JavaScript">
function surfto(list) { var myindex1 = list.selectedIndex; var newwindow = list.options[myindex1].value; if (newwindow != "") { var msgwindow = window.open("profile.cgi?action=show&member="+newwindow,"",""); }}
</SCRIPT>
~;

&getonlineno() if ($dispboardonline ne "no");
$childno = 100;
$biaozhi = 1;
require "${lbdir}data/category_display.cgi" if (-e "${lbdir}data/category_display.cgi");
foreach (@rearrangedforums) {
    chomp $_;
    ($categoryplace,my $a, $category, $forumname, $forumdescription, $privateforum, $startnewthreads, $lastposter, $lastposttime1, $threads, $posts, $hiddenforum, $forumid, $team, $miscad4, $todayforumpost) = split(/\t/,$_);
    next unless (($hiddenforum eq "no")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode =~/^rz/));
    $categoryplace  = sprintf("%01d",$categoryplace);
#    $forumdescription  = &HTML("$forumdescription");
    $threads+=$threadadds[$forumid] if($threadadds[$forumid] ne "");
    $posts+=$postadds[$forumid] if($postadds[$forumid] ne "");
    $lastposttime1=$lastposttime[$forumid] if($lastposttime[$forumid] ne "" && $lastposter[$forumid] ne "");
    $lastposter=$lastposter[$forumid] if($lastposttime[$forumid] ne "" && $lastposter[$forumid] ne "");
    if ($categoryplace ne $lastcategoryplace) {
	if ($is_in_other_mode != 0) {
	    $is_in_other_mode = 0;
	    if ($now_display_count > 0) {
	    	$output .= qq~<td width="25%" bgcolor=$forumcolorone>&nbsp;</td>~ x (4-$now_display_count);
	    	$is_in_other_mode = 0;
	    	$now_display_count = 0;
	    }
	    $output .= qq~</table>~;
	}
	$catshow{$categoryplace}=1 if ($catlog eq "--");
	if ($biaozhi ne 1) {
	    $output .= qq~<SCRIPT>valignend()</SCRIPT><BR>~;
	}
	$biaozhi = 0;
	$output .= qq~
	<SCRIPT>valigntop()</SCRIPT>
	<table cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table><table cellpadding=2 cellspacing=0 width=$tablewidth height=27 align=center bordercolor=$tablebordercolor border=1>~;
        if (!$catshow{$categoryplace}) {
      	    $output .= qq~<tr><td bgcolor=$catback $catsbackpicinfo height=27><table width=100% cellpadding=0 cellspacing=0><tr><td width=6></td><td><a href=$thisprog?catlog=$categoryplace title=收缩此分类><img src=$imagesurl/images/cat1.gif border=0 width=9></a> <a href=category.cgi?category=$categoryplace><font color=$catfontcolor><b>$category</a></td><td align=right width=150>$cmodoutput[$categoryplace]</td><td width=5></td></tr></table></td></tr></table>~;
      	}
      	else {
$output .= qq~<tr><td bgcolor=$catback $catsbackpicinfo height=27><table width=100% cellpadding=0 cellspacing=0><tr><td width=6></td><td><a href=$thisprog?catlog=$categoryplace title=展开此分类><img src=$imagesurl/images/cat.gif border=0 width=9></a> <a href=category.cgi?category=$categoryplace><font color=$catfontcolor><b>$category</a></td><td align=right width=150>$cmodoutput[$categoryplace]</td><td width=5></td></tr></table></td></tr></table>~;
      	}
    }
    if (!$catshow{$categoryplace}) {
    	if ($category_display_type{$categoryplace} ne "basic") {
	    if (($dispchildforumnum ne "no")&&($#forums >= 0)) {
	       $childno++;
	       $realchindforumnums = grep(/^[0-9]+\tchildforum\-$forumid\t(.*)\t/, @forums);
      	       $childforumnums = @childforumnums = ($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode =~/^rz/) ? grep(/^[0-9]+\tchildforum\-$forumid\t(.*)\t/, @forums) : grep(/^[0-9]+\tchildforum\-$forumid\tno\t/, @forums);
	       if ($childforumnums > 0) {
        	   if ($privateforum ne 'yes' || $membercode =~ /^(ad|smo)$/) {
		        $childforumnums = ($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode =~/^rz/) ? qq~  <span title="有 $childforumnums 个下属子论坛" style=cursor:hand onMouseover="showmenu(event,linkset[$childno])" onMouseout="delayhidemenu()">[$childforumnums]</span>~ : qq~  <span title="有 $realchindforumnums 个下属子论坛,其中 $childforumnums 个正常子论坛" style=cursor:hand onMouseover="showmenu(event,linkset[$childno])" onMouseout="delayhidemenu()">[$childforumnums]</span>~;
		        ($childforumnumshtml = join ("\n", @childforumnums)) =~ s/(^|\n)(.*?)\t.*?\t(.*)\t(.*?)\t/<div class=menuitems> <a href=forums.cgi?forum=$2><font color=$menufontcolor>$4<\/font><\/a> <\/div>/g;
			$childforumnumshtml = qq~<script>linkset[$childno]='$childforumnumshtml'</script>~;
	           } else {
	               $childforumnums = qq~  <span title="有 $childforumnums 个下属子论坛">[$childforumnums]</span>~;
        	       $childforumnumshtml = '';
	           }
	       } else {
        	   $childforumnums = '';
	           $childforumnumshtml = '';
	       }
	    }
    	    $forumnameadd = "$boardname - $forumname";
	    $forumnameadd =~ s/\&\#039\;/\\\'/g;
	    $titleinfos{"$forumname\n"} =~ s/\|/\n/isg;
	    my $forumbookmark = qq~<span style=CURSOR:hand onClick="window.external.AddFavorite('$boardurl/forums.cgi?forum=$forumid', '$forumnameadd')"><IMG SRC=$imagesurl/images/fav_add.gif width=16 ALT="将 $forumname 添加到收藏夹"></span>~;
    	    $forumname = qq~<a href=forums.cgi?forum=$forumid$titleinfos{"$forumname\n"}><font color=$fontcolormisc2>$forumname</a>$childforumnums$childforumnumshtml~;
	    $forumlastvisit = $lastvisitinfo{$forumid};
    	    $folderpicture = qq(　);

    	    ($lastposttime,$threadnumber,$topictitle,$cforumid)=split(/\%\%\%/,$lastposttime1);
    	    $cforumid=$forumid if($cforumid eq "");
	    my ($todayforumpost, $todayforumposttime) = split(/\|/,$todayforumpost);
	    $todayforumpost = 0 if (($nowtime ne $todayforumposttime)||($todayforumpost eq ""));
	    $todayforumpost+=$todayforumpostadds[$forumid] if($todayforumpostadds[$forumid] ne "");
	    
    	    if (($lastposttime > $forumlastvisit)&&($inmembername ne "客人")&&($action ne "resetall")) {
		if ($privateforum eq "yes") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		      elsif ($startnewthreads eq "follow") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		      elsif ($startnewthreads eq "yes")    { $folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		      elsif ($startnewthreads eq "all")    { $folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		      elsif ($startnewthreads eq "cert")   { $folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
        	$posts   = qq~<font color=$fonthighlight><b>$posts</b></font>~;
		$threads = qq~<font color=$fonthighlight><b>$threads</b></font>~;
		$todayforumpost = qq~<font color=$fonthighlight><b>$todayforumpost</b></font>~;
	    }
    	    else {
        	if ($privateforum eq "yes") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		      elsif ($startnewthreads eq "follow") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		      elsif ($startnewthreads eq "yes")    { $folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		      elsif ($startnewthreads eq "all")    { $folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		      elsif ($startnewthreads eq "cert")   { $folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
        	$posts   = qq~<font color=$forumfontcolor>$posts</b></font>~;
		$threads = qq~<font color=$forumfontcolor>$threads</b></font>~;
		$todayforumpost = qq~<font color=$fonthighlight>$todayforumpost</b></font>~;
	    }
	    if ($startnewthreads eq "no") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$jh_pic style=cursor:hand onClick=javascript:O3($forumid)>~; }

	    if ($lastposttime) {
    	        $lastposttime  = &longdateandtime("$lastposttime");
                $forumlastpost = qq~<BR>&nbsp;$lastposttime<BR>~;
       	    }
       	    else { $forumlastpost = qq~<BR>&nbsp;没有帖子，或由于服务器<BR>&nbsp;繁忙，数据暂时未知 ...~; $lastposter  = ""; }

	    $topictitle = "" unless (($privateforum ne "yes")||($membercode eq "ad")||($membercode eq "smo"));

	    if ($hiddenforum eq "yes") { $hiddeninfo = "　<I>(隐含)</I>"; } else { $hiddeninfo = ""; }

	if ($forumnamedisp eq 1 && $startnewthreads ne "onlysub") { $forumnamelink = qq~<table width=100% cellpadding=2 cellspacing=0><tr><td width=93%>$forumname$hiddeninfo</td><td width=12><a href=post.cgi?action=new&forum=$forumid><img src="$imagesurl/images/$skin/fpost2.gif" alt="在此分论坛发表新主题" width=12 border=0></a></td><td width=12><a href=poll.cgi?action=new&forum=$forumid><img src="$imagesurl/images/$skin/fpost1.gif" alt="在此分论坛发表新投票" width=12 border=0></a></td><td width=12><a href=jinghua.cgi?action=list&forum=$forumid><img src="$imagesurl/images/$skin/fpost3.gif" alt="查看此分论坛的精华帖子" width=12 border=0></a></td></tr><tr><td colspan=4 width=100%><img src=$imagesurl/images/forumme.gif width=9> <font color=$forumfontcolor>$forumdescription</td></tr></table></td></tr></table>~; }
	                                                     else { $forumnamelink = "$forumname$hiddeninfo<font color=$forumfontcolor><br><img src=$imagesurl/images/forumme.gif width=9> $forumdescription</td></tr></table>"; }

	$output .= qq~<table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center bordercolor=$tablebordercolor border=1><tr><td bgcolor=$forumcolorone align=center width=26>$folderpicture</td><td bgcolor=$forumcolortwo valign=top width=*>
<table width=100% cellpadding=1><tr><td width=1%>$team</td><td width=12></td><td width=*>$forumnamelink</td><td bgcolor=$forumcolorone align=center width=90><font color=$forumfontcolor>$modout[$forumid]</td>
<td bgcolor=$forumcolortwo width=97><table width=100% cellpadding=0 cellspacing=0><tr><td align=left><font color=$fontcolormisc2>&nbsp;今日：<BR>&nbsp;主题：<BR>&nbsp;回复：</td><td align=right>$todayforumpost&nbsp;<BR>$threads&nbsp;<BR>$posts&nbsp;</td></tr></table></td>
<td bgcolor=$forumcolorone width=168><font color=$lastpostfontcolor>$topictitle$lastposter$forumlastpost</td><td bgcolor=$forumcolortwo align=center width=26>$forumbookmark</td></tr></table>
~;
    	} else {
	  if (($dispchildforumnum ne "no")&&($#forums >= 0)) {
	    $childno++;
	    $realchindforumnums = grep(/^[0-9]+\tchildforum\-$forumid\t(.*)\t/, @forums);
      	    $childforumnums = @childforumnums = ($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode =~/^rz/) ? grep(/^[0-9]+\tchildforum\-$forumid\t(.*)\t/, @forums) : grep(/^[0-9]+\tchildforum\-$forumid\tno\t/, @forums);
	    if ($childforumnums > 0) {
		if ($privateforum ne 'yes' || $membercode =~ /^(ad|smo)$/) {
		    $childforumnums = ($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode =~/^rz/) ? qq~  <span title="有 $childforumnums 个下属子论坛" style=cursor:hand onMouseover="showmenu(event,linkset[$childno])" onMouseout="delayhidemenu()">[$childforumnums]</span>~ : qq~  <span title="有 $realchindforumnums 个下属子论坛,其中 $childforumnums 个正常子论坛" style=cursor:hand onMouseover="showmenu(event,linkset[$childno])" onMouseout="delayhidemenu()">[$childforumnums]</span>~;
		    ($childforumnumshtml = join ("\n", @childforumnums)) =~ s/(^|\n)(.*?)\t.*?\t(.*)\t(.*?)\t/<div class=menuitems> <a href=forums.cgi?forum=$2><font color=$menufontcolor>$4<\/font><\/a> <\/div>/g;
		    $childforumnumshtml = qq~<script>linkset[$childno]='$childforumnumshtml'</script>~;
		} else {
		    $childforumnums = qq~  <span title="有 $childforumnums 个下属子论坛">[$childforumnums]</span>~;
		    $childforumnumshtml = '';
          	}
      	    } else {
                $childforumnums = '';
          	$childforumnumshtml = '';
      	    }
	  }
	  $forumlastvisit = $lastvisitinfo{$forumid};
   	  $titleinfos{"$forumname\n"} =~ s/\|/\n/isg;
 	  $forumdescription =~ s/<.+?>//isg;
       	  $forumname = qq~<a href=forums.cgi?forum=$forumid$titleinfos{"$forumname\n"} title="$forumdescription"><font color=$fontcolormisc2>$forumname</a>$childforumnums$childforumnumshtml~;

          $folderpicture = qq(　);

          ($lastposttime,$threadnumber,$topictitle,$cforumid)=split(/\%\%\%/,$lastposttime1);
          $cforumid=$forumid if($cforumid eq "");
   	  my ($todayforumpost, $todayforumposttime) = split(/\|/,$todayforumpost);
   	  $todayforumpost = 0 if (($nowtime ne $todayforumposttime)||($todayforumpost eq ""));
   	  $todayforumpost+=$todayforumpostadds[$forumid] if($todayforumpostadds[$forumid] ne "");

       	  if (($lastposttime > $forumlastvisit)&&($inmembername ne "客人")&&($action ne "resetall")) {
	  if ($privateforum eq "yes")          { $folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
     	  elsif ($startnewthreads eq "follow") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
     	  elsif ($startnewthreads eq "yes")    { $folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
     	  elsif ($startnewthreads eq "all")    { $folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
     	  elsif ($startnewthreads eq "cert")   { $folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_havenew style=cursor:hand onClick=javascript:O3($forumid)>~; }
       
          $posts   = qq~<font color=$fonthighlight><b>$posts</b></font>~;
	  $threads = qq~<font color=$fonthighlight><b>$threads</b></font>~;
	  $todayforumpost = qq~<font color=$fonthighlight><b>$todayforumpost</b></font>~;
   	  }
          else {
		if ($privateforum eq "yes") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		elsif ($startnewthreads eq "follow") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		elsif ($startnewthreads eq "yes")    { $folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		elsif ($startnewthreads eq "all")    { $folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		elsif ($startnewthreads eq "cert")   { $folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_nonew style=cursor:hand onClick=javascript:O3($forumid)>~; }
		$posts   = qq~<font color=$forumfontcolor>$posts</b></font>~;
		$threads = qq~<font color=$forumfontcolor>$threads</b></font>~;
		$todayforumpost = qq~<font color=$fonthighlight>$todayforumpost</b></font>~;
	  }
	  if ($startnewthreads eq "no") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$jh_pic style=cursor:hand onClick=javascript:O3($forumid)>~; }
	  $hiddeninfo = ($hiddenforum eq "yes")?"　<I>(隐含)</I>":"";
	  $output .= qq~<table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center bordercolor=$tablebordercolor border=1>~ if($is_in_other_mode == 0);
	  $output .=qq~<tr>~ if($now_display_count == 0);
	  $output .=qq~<td width="25%" bgcolor=$forumcolortwo>
<table width="100%" cellspacing="0" cellpadding="1">
<tr><td colspan="3" valign="middle">$folderpicture $forumname$hiddeninfo</td></tr>
<tr><td width="30%" align="left">主: $threads</td><td width="30%" align="left">回: $posts</td><td width="30%" align="left">今: $todayforumpost</td></tr>
</table></td>
~;

	  if ($now_display_count == 3) {
		$now_display_count = -1;
		$output .=qq~</tr>~;
	  }
	  $now_display_count++;
   	  $is_in_other_mode = 1;
	}#
    }
    $lastcategoryplace = $categoryplace;
}
if ($is_in_other_mode != 0) {
    $is_in_other_mode = 0;
    if ($now_display_count > 0) {
	$output .= qq~<td width="25%" bgcolor=$forumcolorone>&nbsp;</td>~ x (4-$now_display_count);
	$is_in_other_mode = 0;
	$now_display_count = 0;
    }
    $output .= qq~</table>~;
}
$output .= qq~<SCRIPT>valignend()</SCRIPT><br>~;

if (-e "${lbdir}data/unionoutput.pl") {
    $output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellpadding=4 cellspacing=1 width=100%>~;
    require "${lbdir}data/unionoutput.pl";
    $output .= qq~</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<img src=$imagesurl/images/none.gif height=5><br>~;
}

$output .= $birthdayoutput if ($dispborn ne "no");

$onlinemaxtime = &dateformatshort($onlinemaxtime + $timeadd);

if (($createyear>0)&&($createmon>0)&&($createday>0)) { $createday = "自 <font color=$fontcolormisc2>$createyear年$createmon月$createday日</font> 创建以来，";} else { $createday =""; }

$output .= qq~
</table></td></tr></table><img src=$imagesurl/images/none.gif height=5><br>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=7 $catbackpic><font color=$titlefontcolor>
<B>-=> 论坛在线统计 （同时在线峰值：$onlinemax 人，发生时刻：$onlinemaxtime）</B>　 [$onlinetitle]</td></tr>
<tr><td bgcolor=$forumcolorone align=center width=26><img src=$imagesurl/images/$skin/online.gif alt=$membergone></td>
<td bgcolor=$forumcolortwo colspan=6 width=*><font color=$titlefontcolor>
&nbsp;<font color=$forumfontcolor>$membertongji $createday论坛总共被访问 <b>$count1</b> 次，共被点击 <b>$count2</b> 次。<BR></font>
~;
if ($onlineview == 1) {
    my $defrzmpic1 = " 　<img src=$imagesurl/images/$defrzonline1 width=12> $defrz1" if ($defrz1 ne "" && $defrzonline1 ne "");
    my $defrzmpic2 = " 　<img src=$imagesurl/images/$defrzonline2 width=12> $defrz2" if ($defrz2 ne "" && $defrzonline2 ne "");
    my $defrzmpic3 = " 　<img src=$imagesurl/images/$defrzonline3 width=12> $defrz3" if ($defrz3 ne "" && $defrzonline3 ne "");
    my $defrzmpic4 = " 　<img src=$imagesurl/images/$defrzonline4 width=12> $defrz4" if ($defrz4 ne "" && $defrzonline4 ne "");
    my $defrzmpic5 = " 　<img src=$imagesurl/images/$defrzonline5 width=12> $defrz5" if ($defrz5 ne "" && $defrzonline5 ne "");
    $output .= qq~&nbsp;<font color=$forumfontcolor>在线图例：　<img src=$imagesurl/images/$onlineadmin width=12> 论坛坛主 　<img src=$imagesurl/images/$onlinesmod width=12> 论坛总版主 　<img src=$imagesurl/images/$onlinecmod width=12> 分类区版主 　<img src=$imagesurl/images/$onlinemod width=12> 论坛版主 　<img src=$imagesurl/images/$onlineamod width=12> 论坛副版主$defrzmpic1$defrzmpic2$defrzmpic3$defrzmpic4$defrzmpic5 　<img src=$imagesurl/images/$onlinerz width=12> 认证会员 　<img src=$imagesurl/images/$onlinemember width=12> 普通会员 　<img src=$imagesurl/images/$onlineguest width=12> 客人或隐身会员<br><hr size=1 width=99%><table cellpadding=1 cellspacing=0><tr>$memberoutput</tr></table>~;
}

if ($dispview eq "yes" || $membercode eq "ad" || $membercode eq 'smo') { require "dodispviewleobbs.pl"; }

$output .= qq~</td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

if (($displink eq "yes")&&($links ne "")&&($displinkaddr eq "1")) {
    require "dodisplink.pl";
}

$timenow  = $currenttime + $timeadd;
$timenow  = &longdateandtime("$timenow");

$output .= qq~
<img src=$imagesurl/images/none.gif height=5><br>
<table cellspacing=0 cellpadding=0 width=$tablewidth align=center>
<tr><td>　$timenow ($basetimes)</td>
<td align=right noWrap>[ <a href=leobbs.cgi?action=delcookieall>删除论坛 cookie</a> ] :: [ <a href=leobbs.cgi?action=resetall>标记所有为已读</a> ] :: [ <a href=$thisprog?action=expand>展开所有分类</a> ] :: [ <a href=$thisprog?action=depand>收缩所有分类</a> ]&nbsp;</td>enow");

$output .= qq~
<img src=$imagesurl/images/none.gif height=5><br>
<table cellspacing=0 cellpadding=0 width=$tablewidth align=center>
<tr><td>