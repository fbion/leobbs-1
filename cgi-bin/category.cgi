#!/usr/bin/perl
#####################################################
# LeoBBSx 适用的分类页功能 (测试版)
# 编写：Anthony
# 网址：http://www.youtough.com/bbs/leobbs.cgi
# 最後修改日期：2004/05/13a
# 注：所有删去版权号及违规修改版权号之人士切勿使用！
#     另外如封包到你的外挂版本内，请通知我。
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

use diagnostics;
use LBCGI;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require 'data/boardinfo.cgi';
require 'data/styles.cgi';
require 'data/mpic.cgi';
require 'bbs.lib.pl';

$|++;
$thisprog = 'category.cgi';
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq 'yes');

$query = new LBCGI;

if ($COOKIE_USED eq 1) {
    $cookiepath = '';
}
else {
    $boardurltemp = $boardurl;
    $boardurltemp =~ s/^http:\/\/(.*?)(\/.*?$|$)/$1/;
    $cookiepath = $boardurltemp;
}
&ipbanned; #封杀一些 IP
$inselectstyle = $query->cookie('selectstyle');
&error('普通错误&老大，别乱攻击我的程式呀！') if ($inselectstyle =~ m/\/|\\|\.\./);
if ($inselectstyle ne '' && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {
    require "${lbdir}data/skin/${inselectstyle}.cgi";
}

$inmembername = $query->cookie('amembernamecookie');
$inpassword = $query->cookie('apasswordcookie');
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq '') {
    $inmembername = '客人';
}
else {
    &getmember($inmembername, 'no');
    if ($inpassword ne $password) {
        $namecookie = cookie(-name => 'amembernamecookie', -value => '', -path => $cookiepath . '/');
        $passcookie = cookie(-name => 'apasswordcookie', -value => '', -path => $cookiepath . '/');
        print header(-cookie => [ $namecookie, $passcookie ], -expires => $EXP_MODE, -cache => $CACHE_MODES);
        &error('普通错误&密码与会员名称不相符，请重新登入！');
    }
    &error('普通错误&此会员根本不存在！') if ($userregistered eq 'no');
    eval ('use VISITFORUM qw (getlastvisit);');
    &getlastvisit;
}

$inselectstyle = $query->cookie("selectstyle");
$inselectstyle = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~ m/\//) || ($inselectstyle =~ m/\\/) || ($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$timeadd = $timedifferencevalue * 3600 + $timezone * 3600;
$currenttime = time;
$nowtime = &shortdate($currenttime + $timeadd);
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}
if ($catsbackpicinfo ne "") {$catsbackpicinfo = "background=$imagesurl/images/$skin/$catsbackpicinfo";}

if (((-e "${lbdir}cache/forumcache-$skin.pl") && ((-M "${lbdir}cache/forumcache-$skin.pl") * 86400 < 180)) || (-e "${lbdir}cache/forumcache-$skin.pl.lock")) {
    unlink("${lbdir}cache/forumcache-$skin.pl.lock") if ((-M "${lbdir}cache/forumcache-$skin.pl.lock") * 86400 > 15);
    if (-e "${lbdir}cache/forumcache-$skin.pl.lock") {
        select(undef, undef, undef, 0.2);
        select(undef, undef, undef, 0.2) if (-e "${lbdir}cache/forumcache-$skin.pl.lock");
        select(undef, undef, undef, 0.2) if (-e "${lbdir}cache/forumcache-$skin.pl.lock");
        select(undef, undef, undef, 0.3) if (-e "${lbdir}cache/forumcache-$skin.pl.lock");
        unlink("${lbdir}cache/forumcache.pl.lock");
        &error("普通错误&服务器忙，请稍后再试！！") if (-e "${lbdir}cache/forumcache.pl.lock");
    }
    if (-e "${lbdir}cache/forumcache-$skin.pl") {
        eval {require "${lbdir}cache/forumcache-$skin.pl";};
        if ($@) {
            unlink("${lbdir}cache/forumcache-$skin.pl");
            require "doforumcache.pl";
        }
        $forumcached = "yes";
    }
    else {require "doforumcache.pl";}
}
else {require "doforumcache.pl";}

#&title;

print header(-cookie => [ $onlineviewcookie, $cookie, $tempcookie, $unioncookie, $catlogcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

$incategory = $query->param('category');
&error('普通错误&输入有误') if ($incategory !~ /^[0-9]+$/);
$incategory = sprintf('%09d', $incategory);

if ($membercode !~ /^(ad|(s|c|)mo)$/) {
    &error('普通错误&资料不存在') if ((@rearrangedforums = grep (/^$incategory\t(.*?\t){10}no\t/, @rearrangedforums)) < 1);
}
else {
    &error('普通错误&资料不存在') if ((@rearrangedforums = grep (/^$incategory\t/, @rearrangedforums)) < 1);
}

my $categoryname = $rearrangedforums[0];
$categoryname =~ s/^(.*?\t){2}(.*?)\t.*?$/$2/;
&whosonline("$inmembername\t$categoryname\t$categoryname\t查看分类论坛上的分区");
&mischeader("<a href=$thisprog?category=" . int($incategory) . ">$categoryname</a> → 查看分类论坛上的分区");
$output .= qq~<style>
TABLE {BORDER-TOP: 0px; BORDER-LEFT: 0px; BORDER-BOTTOM: 1px; }
TD    {BORDER-RIGHT: 0px; BORDER-TOP: 0px; color: #333333; }
</style>
~;

$output .= qq~<p><SCRIPT>valigntop()</SCRIPT><table cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table><table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center bordercolor=$tablebordercolor border=1>~;
$output .= qq~<tr><td bgcolor=$catback $catsbackpicinfo height=24><table width=100% cellpadding=0 cellspacing=0><tr><td><img src=$imagesurl/images/cat1.gif border=0 width=9> <font color=$catfontcolor><b>$categoryname</td><td align=right width=150>$cmodoutput[$incategory]</td></tr></table></td></tr></table>~;

chomp @rearrangedforums;
foreach (@rearrangedforums) {
    ($categoryplace, my $a, $category, $forumname, $forumdescription, $privateforum, $startnewthreads, $lastposter, $lastposttime1, $threads, $posts, $hiddenforum, $forumid, $team, $miscad4, $todayforumpost) = split(/\t/, $_);
    $categoryplace = sprintf('%01d', $categoryplace);
    $threads += $threadadds[$forumid] if ($threadadds[$forumid] ne '');
    $posts += $postadds[$forumid] if ($postadds[$forumid] ne '');
    $lastposttime1 = $lastposttime[$forumid] if ($lastposttime[$forumid] ne '' && $lastposter[$forumid] ne '');
    $lastposter = $lastposter[$forumid] if ($lastposttime[$forumid] ne '' && $lastposter[$forumid] ne '');

    if (($dispchildforumnum ne "no") && ($#forums >= 0)) #&&($privateforum ne 'yes'))
    {
        $childforumnums = grep (/^[0-9]+\tchildforum\-$forumid\t/, @forums);
        $countcforum = $childforumnums;
        $childforumnums = $childforumnums > 0 ? qq~  <span title="有 $childforumnums 个附属子论坛">[$childforumnums]</span>~ : "";
    }
    $forumnameadd = "$boardname - $forumname";
    $forumnameadd =~ s/\&\#039\;/\\\'/g;
    $titleinfos{"$forumname\n"} =~ s/\|/\n/isg;
    my $forumbookmark = qq~<span style=CURSOR:hand onClick="window.external.AddFavorite('$boardurl/forums.cgi?forum=$forumid', '$forumnameadd')"><img src=$imagesurl/images/fav_add.gif width=15 alt="将 $forumname 加到我的最爱"></span>~;
    $forumname = qq~<a href=forums.cgi?forum=$forumid$titleinfos{"$forumname\n"}><font color=$fontcolormisc2>$forumname</a>$childforumnums~;
    $forumlastvisit = $lastvisitinfo{$forumid};
    $folderpicture = qq(  );
    ($lastposttime, $threadnumber, $topictitle, $cforumid) = split(/\%\%\%/, $lastposttime1);
    $cforumid = $forumid if ($cforumid eq '');
    my ($todayforumpost, $todayforumposttime) = split(/\|/, $todayforumpost);
    $todayforumpost = 0 if (($nowtime ne $todayforumposttime) || ($todayforumpost eq ''));
    $todayforumpost += $todayforumpostadds[$forumid] if ($todayforumpostadds[$forumid] ne '');

    if (($lastposttime > $forumlastvisit) && ($inmembername ne "客人") && ($action ne "resetall")) {
        if ($privateforum eq "yes") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_havenew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        elsif ($startnewthreads eq "follow") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_havenew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        elsif ($startnewthreads eq "yes") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_havenew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        elsif ($startnewthreads eq "all") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_havenew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        elsif ($startnewthreads eq "cert") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_havenew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        $posts = qq~<font color=$fonthighlight><b>$posts</b></font>~;
        $threads = qq~<font color=$fonthighlight><b>$threads</b></font>~;
        $todayforumpost = qq~<font color=$fonthighlight><b>$todayforumpost</b></font>~;
    }
    else {
        if ($privateforum eq "yes") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_nonew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        elsif ($startnewthreads eq "follow") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_nonew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        elsif ($startnewthreads eq "yes") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_nonew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        elsif ($startnewthreads eq "all") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_nonew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        elsif ($startnewthreads eq "cert") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_nonew style=cursor:hand onClick=javascript:O3($forumid)>~;}
        $posts = qq~<font color=$forumfontcolor>$posts</b></font>~;
        $threads = qq~<font color=$forumfontcolor>$threads</b></font>~;
        $todayforumpost = qq~<font color=$fonthighlight>$todayforumpost</b></font>~;
    }
    if ($startnewthreads eq "no") {$folderpicture = qq~<img src=$imagesurl/images/$skin/$jh_pic style=cursor:hand onClick=javascript:O3($forumid)>~;}

    if ($lastposttime) {
        $lastposttime = &longdateandtime($lastposttime);
        $forumlastpost = qq~<br>&nbsp;$lastposttime<br>~;
    }
    else {
        $forumlastpost = qq~<BR>&nbsp;没有帖子，或由于服务器<BR>&nbsp;繁忙，数据暂时未知 ...~;
        $lastposter = '';
    }
    $topictitle = '' unless (($privateforum ne 'yes') || ($membercode =~ /^(ad|smo)$/));
    if ($hiddenforum eq 'yes') {
        $hiddeninfo = '  <i>(隐藏)</i>';
    }
    else {
        $hiddeninfo = '';
    }
    if ($forumnamedisp eq 1 && $startnewthreads ne 'onlysub') {
        $forumnamelink = qq~<table width=100% cellpadding=2 cellspacing=0><tr><td width=93%>$forumname$hiddeninfo</td><td width=12><a href=post.cgi?action=new&forum=$forumid><img src="$imagesurl/images/$skin/fpost2.gif" alt="在此分论坛发表新主题" width=12 border=0></a></td><td width=12><a href=poll.cgi?action=new&forum=$forumid><img src="$imagesurl/images/$skin/fpost1.gif" alt="在此分论坛发表新投票" width=12 border=0></a></td><td width=12><a href=jinghua.cgi?action=list&forum=$forumid><img src="$imagesurl/images/$skin/fpost3.gif" alt="查看此分论坛的精华文章" width=12 border=0></a></td></tr><tr><td colspan=4 width=100%><img src=$imagesurl/images/forumme.gif width=9> <font color=$forumfontcolor>$forumdescription</td></tr></table></td></tr></table>~;
    }
    else {
        $forumnamelink = "$forumname$hiddeninfo<font color=$forumfontcolor><br><img src=$imagesurl/images/forumme.gif width=9> $forumdescription</td></tr></table>";
    }
    $output .= qq~<table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center bordercolor=$tablebordercolor border=1><tr><td bgcolor=$forumcolorone align=center width=26>$folderpicture</td><td bgcolor=$forumcolortwo valign=top width=*>
<table width=100% cellpadding=1><tr><td width=1%>$team</td><td width=12></td><td width=*>$forumnamelink</td><td bgcolor=$forumcolorone align=center width=90><font color=$forumfontcolor>$modout[$forumid]</td>
<td bgcolor=$forumcolortwo width=97><table width=100% cellpadding=0 cellspacing=0><tr><td align=left><font color=$fontcolormisc2>&nbsp;今日：<br>&nbsp;主题：<br>&nbsp;回复：</td><td align=right>$todayforumpost&nbsp;<br>$threads&nbsp;<br>$posts&nbsp;</td></tr></table></td>
<td bgcolor=$forumcolorone width=168><font color=$lastpostfontcolor>$topictitle$lastposter$forumlastpost</td><td bgcolor=$forumcolortwo align=center width=26>$forumbookmark</td></tr></table>
~;

    #######cforum
    if ($childforumnums ne '') {
        &moderator($forumid);
        chomp @childforum;
        foreach (@childforum[0 .. $countcforum - 1]) {
            ($cforumname, $cforumdescription, $cprivateforum, $cstartnewthreads, $clastposter, $clastposttime1, $cthreads, $cposts, $chiddenforum, $cforumid, $modout, $cteam, $cmiscad4, $ctodayforumpost, $cmiscad5) = split(/\t/, $_);
            next unless (($chiddenforum eq "no") || ($membercode =~ /^(ad|(s|c)mo)$/));
            $cforumnameadd = $cforumname;
            $cforumnameadd1 = $cforumnameadd;
            $cforumnameadd1 =~ s/\'/\\'/g;
            $titleinfos{"$cforumname\n"} =~ s/\|/\n/isg;
            $cforumname = qq~<a href=forums.cgi?forum=$cforumid$titleinfos{"$cforumname\n"}><font color=$fontcolormisc2>$cforumname</a>~;
            my $forumlastvisit = $lastvisitinfo{$cforumid};
            $folderpicture = qq(  );
            ($clastposttime, $threadnumber, $topictitle) = split(/\%\%\%/, $clastposttime1);
            my ($ctodayforumpost, $ctodayforumposttime) = split(/\|/, $ctodayforumpost);
            $ctodayforumpost = 0 if (($nowtime ne $ctodayforumposttime) || ($ctodayforumpost eq ''));
            ##############
            if (($clastposttime > $forumlastvisit) && ($inmembername ne '客人')) {
                $cposts = qq~<font color=$fonthighlight><b>$cposts</b>~;
                $cthreads = qq~<font color=$fonthighlight><b>$cthreads</b>~;
            }
            else {
                $cposts = qq~<font color=$forumfontcolor>$cposts</b>~;
                $cthreads = qq~<font color=$forumfontcolor>$cthreads</b>~;
            }
            $ctodayforumpost = qq~<font color=$fonthighlight><b>$ctodayforumpost</b>~;
            ##############
            if ($clastposttime) {
                $clastposttime = &longdateandtime($clastposttime);
                $forumlastpost = qq~<br>&nbsp;$clastposttime<br>~;
            }
            else {
                $forumlastpost = qq~<BR>&nbsp;没有帖子，或由于服务器<BR>&nbsp;繁忙，数据暂时未知 ...~;
                $clastposter = '';
            }
            $topictitle = '' unless ((($cprivateforum ne 'yes') || ($membercode =~ /^(ad|smo)$/)) && ($topictitle));
            $forumbookmark = qq~<span style=CURSOR: hand onClick="window.external.AddFavorite('$boardurl/forums.cgi?forum=$cforumid', '$boardname - $cforumnameadd1')"><img src=$imagesurl/images/fav_add.gif border=0 width=16 alt="将$cforumnameadd加到我的最爱"></span>~;
            if ($chiddenforum eq 'yes') {
                $hiddeninfo = '  <i>(隐藏)</i>';
            }
            else {
                $hiddeninfo = '';
            }
            if ($forumnamedisp eq 1) {
                $cforumnamelink = qq~<table width=100% cellpadding=2 cellspacing=0><tr><td width=93%>$cforumname$hiddeninfo</td><td width=12><a href=post.cgi?action=new&forum=$cforumid><img src=$imagesurl/images/$skin/fpost2.gif alt=在此分论坛发表新主题 width=12 border=0></a></td><td width=12><a href=poll.cgi?action=new&forum=$cforumid><img src=$imagesurl/images/$skin/fpost1.gif alt=在此分论坛发表新投票 width=12 border=0></a></td><td width=12><a href=jinghua.cgi?action=list&forum=$cforumid><img src=$imagesurl/images/$skin/fpost3.gif alt=查看此分论坛的精华文章 width=12 border=0></a></td></tr><tr><td colspan=4 width=100%><img src=$imagesurl/images/forumme.gif width=9> <font color=$forumfontcolor>$cforumdescription</td></tr></table></td></tr></table>~;
            }
            else {
                $cforumnamelink = "$cforumname$hiddeninfo<font color=$forumfontcolor><br><img src=$imagesurl/images/forumme.gif width=9> $cforumdescription</td></tr></table>";
            }
            $output .= qq~<table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center bordercolor=$tablebordercolor border=1><tr><td bgcolor=$forumcolortwo valign=top width=*>
<table width=100% cellpadding=1><tr><td width=1%>$cteam</td><td width=12></td><td width=*>$cforumnamelink</td><td bgcolor=$forumcolorone align=center width=90><font color=$forumfontcolor>$modout</td>
<td bgcolor=$forumcolortwo align=left width=97><table width=100% cellpadding=0 cellspacing=0><tr><td align=left><font color=$fontcolormisc2>&nbsp;今日：<br>&nbsp;主题：<br>&nbsp;回复：</td><td align=right>$ctodayforumpost&nbsp;<br>$cthreads&nbsp;<br>$cposts&nbsp;</td></tr></table></td>
<td bgcolor=$forumcolorone width=168><font color=$lastpostfontcolor>$topictitle$clastposter$forumlastpost</td><td bgcolor=$forumcolortwo align=center width=26>$forumbookmark</td></tr></table>
~;
        }
        #########cforum
    }
    $lastcategoryplace = $categoryplace;
}
$output .= qq~</td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR>~;

&output($boardname, \$output);
exit;
