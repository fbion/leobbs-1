#!/usr/bin/perl
#########################
# 手机论坛WAP版
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
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
$query = new LBCGI;
$LBCGI::POST_MAX = 2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "bbs.lib.pl";
require "wap.pl";
require "data/styles.cgi";
$|++;
&waptitle;
$show .= qq~<card  title="$boardname">~;
$lid = $query->param('lid');
&check($lid);
$in_forum = $query->param('f');
$in_topic = $query->param('t');
if ($inmembername eq "" || $inmembername eq "客人") {
    $inmembername = "客人";
}
else {
    &getmember("$inmembername", "no");
}
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}
$inpost = $query->param('inpost');
$inpost = $uref->fromUTF8("UTF-8", $inpost);
$inpost = &cleaninput("$inpost");
$currenttime = time;
$postipaddress = &myip();
$inpost =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost =~ s/USECHGFONTE/USECHGFONT\&\#069\;/sg;
$inpost =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost =~ s/\[br\]/<br>/g;
$inpost =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
&moderator("$in_forum");
$myinmembmod = $inmembmod;
if ($allowusers ne '') {
    &errorout('进入论坛&你不允许进入该论坛！') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &errorout("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0) {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        &errorout("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
        &errorout("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}
if ($startnewthreads eq "onlysub") {&errorout("发表&对不起，这里是纯子论坛区，不允许发言！");}
if ($postopen eq "no") {&errorout("发表或回复主题&对不起，本论坛不允许发表或回复主题！");}
if (($userregistered eq "no") && ($inmembername =~ /^客人/)) {&errorout("发表新回复&请不要在用户名的开头中使用客人字样！");}

if ($inmembername eq "客人") {&errorout("发表新回复&请不要在用户名的开头中使用客人字样！");}

if (($userregistered eq "no") && ($startnewthreads ne "all")) {&errorout("发表新回复&您没有注册！");}
# elsif ((($inpassword ne $password)&&($userregistered ne "no"))||(($inpassword ne "")&&($userregistered eq "no"))) { &errorout("发表新回复&您的密码错误！"); }
elsif (($membercode eq "banned") || ($membercode eq "masked")) {&errorout("发表&已被禁止发言或者发言被屏蔽，请联系管理员解决！");}
elsif ($inpost eq "") {&errorout("发表新回复&必须输入内容！");}
else {
    if ($startnewthreads eq "no") {
        unless ($membercode eq "ad" || $membercode eq 'smo' || $inmembmod eq "yes") {&errorout("发表新回复&在此论坛中只能由坛主或者本版版主发表新回复！");}
    }
    elsif ($startnewthreads eq "cert") {
        unless ($membercode eq "ad" || $membercode eq 'smo' || $inmembmod eq "yes" || $membercode eq 'cmo' || $membercode eq 'amo' || $membercode eq 'mo' || $membercode =~ /^rz/) {&errorout("发表新回复&在此论坛中只能由坛主、版主和认证会员发表新回复！");}
    }
    $tempaccess = "forumsallowed" . "$in_forum";
    $testentry = $query->cookie("$tempaccess");

    if ((($testentry eq $forumpass) && ($testentry ne "")) || ($allowedentry{$in_forum} eq "yes") || ($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes")) {$allowed = "yes";}
    if (($privateforum eq "yes") && ($allowed ne "yes")) {&errorout("发表&对不起，您不允许在此论坛发表！");}
    if (($startnewthreads eq "all") && ($userregistered eq "no")) {$inmembername = "$inmembername(客)";}
}
$inpost =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;
$filetoopen = "$lbdir" . "forum$in_forum/$in_topic.thd.cgi";
if (-e $filetoopen) {
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    sysread(FILE, $allmessages, (stat(FILE))[7]);
    close(FILE);
    $allmessages =~ s/\r//isg;
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    @allmessages = split(/\n/, $allmessages);
}
else {
    unlink("$lbdir" . "forum$in_forum/$in_topic.pl");
    &errorout("回复&这个主题不存在！可能已经被删除！");
}

my $file = "$lbdir" . "forum$in_forum/$in_topic.pl";
&winlock($file) if ($OS_USED eq "Nt");
open(ENT, $file);
flock(ENT, 2) if ($OS_USED eq "Unix");
$in = <ENT>;
close(ENT);
&winunlock($file) if ($OS_USED eq "Nt");
($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, my $no, $addmetype) = split(/\t/, $in);
if (($threadstate eq "closed") || ($threadstate eq "pollclosed")) {&errorout("发表回复&对不起，这个主题已经被锁定！");}
$numberofitems = $threadposts + 1;
if (($rdays ne '') && ($membercode ne "ad") && ($membercode ne "smo")) {&errorout("发表回复&超过 $rdays 天的帖子不允许再回复！") if ($currenttime - $lastpostdate > $rdays * 86400);}

$inpost = &dofilter("$inpost");
$inpost = "<img src='$imagesurl/images/sj.gif' width='22' alt='由手机 WAP 发送' />" . $inpost;
&winlock($filetoopen) if ($OS_USED eq "Nt");
if (open(FILE, ">>$filetoopen")) {
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "$inmembername\t$topictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t\n";
    close(FILE);
}
&winunlock($filetoopen) if ($OS_USED eq "Nt");

$threadposts = @allmessages;
$threadviews = $threadposts if ($threadviews < $threadposts);
#	$threadviews = 9999 if ($threadviews > 10000);

my $topictitletemp = $topictitle;
$topictitletemp =~ s/^＊＃！＆＊//;
&winlock($file) if ($OS_USED eq "Nt");
if (open(FILE, ">$file")) {
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "$in_topic\t＊＃！＆＊$topictitletemp\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$inmembername\t$currenttime\t$posticon\t$inposttemp\t$addmetype\t";
    close(FILE);
}
&winunlock($file) if ($OS_USED eq "Nt");

$file = "$lbdir" . "boarddata/listno$in_forum.cgi";
&winlock($file) if ($OS_USED eq "Nt");
open(LIST, "$file");
flock(LIST, 2) if ($OS_USED eq "Unix");
sysread(LIST, $listall, (stat(LIST))[7]);
close(LIST);
$listall =~ s/\r//isg;
$listall =~ s/(.*)(^|\n)$in_topic\n(.*)/$1$2$3/;

if (length($listall) > 500) {
    if (open(LIST, ">$file")) {
        flock(LIST, 2) if ($OS_USED eq "Unix");
        print LIST "$in_topic\n$listall";
        close(LIST);
    }
    &winunlock($file) if ($OS_USED eq "Nt");
}
else {
    &winunlock($file) if ($OS_USED eq "Nt");
    require "rebuildlist.pl";
    my $truenumber = rebuildLIST(-Forum => "$in_forum");
    ($tpost, $treply) = split(/\|/, $truenumber);
}

$cleanmembername = $inmembername;
$cleanmembername =~ s/ /\_/isg;
$cleanmembername =~ tr/A-Z/a-z/;

$maxpersontopic = 25;
if ($maxpersontopic && $userregistered ne "no") {
    $cleanstart = $startedby;
    $cleanstart =~ s/ /\_/isg;
    $cleanstart =~ tr/A-Z/a-z/;
    #   &addmytopic("reply", $cleanmembername, $in_forum, $in_topic, $topictitletemp, $currenttime, $posticon);
    #  &addmytopic("post", $cleanstart, $in_forum, $in_topic, $topictitletemp, $currenttime, $posticon) if ($cleanmembername ne $cleanstart);
}

$jifen = $numberofposts * 2 + $numberofposts - $postdel * 5 if ($jifen eq "");

if ($forumallowcount ne "no") {
    $numberofreplys++;
    $mymoney += $forumreplymoney - $replymoney if ($forumreplymoney ne "");
    if ($forumreplyjf ne "") {$jifen += $forumreplyjf;}
    else {$jifen += $rtojf;}
}
$lastpostdate = "$currenttime\%\%\%topic.cgi?forum=$in_forum&topic=$in_topic\%\%\%$topictitletemp" if ($privateforum ne "yes");
chomp $lastpostdate;

if (($userregistered ne "no") && ($password ne "")) {
    my $namenumber = &getnamenumber($cleanmembername);
    &checkmemfile($cleanmembername, $namenumber);
    $filetomake = "$lbdir" . "$memdir/$namenumber/$cleanmembername.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    if ((open(FILE, ">$filetomake")) && ($inmembername ne "")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
    }
    &winunlock($filetomake) if ($OS_USED eq "Nt");
    unlink("${lbdir}cache/myinfo/$cleanmembername.pl");
    if (((-M "${lbdir}cache/meminfo/$cleanmembername.pl") * 86400 > 60 * 2) || (!(-e "${lbdir}cache/meminfo/$cleanmembername.pl"))) {
        require "getnameinfo.pl" if ($onloadinfopl ne 1);
        &getmemberinfo($cleanmembername);
    }
}

my $nowtime = &shortdate($currenttime + $timezone * 3600);

my $filetoopens = "$lbdir/data/todaypost.cgi";
$filetoopens = &lockfilename($filetoopens);

if (($usetodaypostreply ne "no") && (!(-e "$filetoopens.lck"))) {
    &winlock("$lbdir/data/todaypost.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    if (-e "$lbdir/data/todaypost.cgi") {
        open(FILE, "+<$lbdir/data/todaypost.cgi");
        $todaypost = <FILE>;
        chomp $todaypost;
        my ($nowtoday, $todaypostno, $maxday, $maxdaypost, $yestdaypost) = split(/\t/, $todaypost);
        if ($nowtoday eq $nowtime) {
            $todaypostno++;
            if ($todaypostno > $maxdaypost) {
                $maxday = $nowtime;
                $maxdaypost = $todaypostno;
            }
        }
        else {
            opendir(CATDIR, "${lbdir}cache");
            @dirdata = readdir(CATDIR);
            closedir(CATDIR);
            @dirdata = grep (/forumcache/, @dirdata);
            foreach (@dirdata) {unlink("${lbdir}cache/$_");}
            $nowtoday = $nowtime;
            $yestdaypost = $todaypostno;
            $todaypostno = 1;
        }
        seek(FILE, 0, 0);
        print FILE "$nowtoday\t$todaypostno\t$maxday\t$maxdaypost\t$yestdaypost\t";
        close(FILE);
    }
    else {
        open(FILE, ">$lbdir/data/todaypost.cgi");
        print FILE "$nowtime\t1\t$nowtime\t1\t0\t";
        close(FILE);
    }
    &winunlock("$lbdir/data/todaypost.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
}
$filetoopen = "${lbdir}boarddata/foruminfo$in_forum.cgi";
my $filetoopens = &lockfilename($filetoopen);
if (!(-e "$filetoopens.lck")) {
    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(FILE, "+<$filetoopen");
    ($no, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/, <FILE>);
    $lastposter = $inmembername;
    $lastposttime = $currenttime;
    if (($tpost ne "") && ($treply ne "")) {
        $threads = $tpost;
        $posts = $treply;
    }
    else {$posts++;}
    if ($usetodayforumreply eq "yes") {
        ($todayforumpost, $todayforumposttime) = split(/\|/, $todayforumpost);
        if (($nowtime ne $todayforumposttime) || ($todayforumpost eq "")) {$todayforumpost = 1;}
        else {$todayforumpost++;}
        $todayforumpost = "$todayforumpost|$nowtime";
    }
    $lastposttime = "$lastposttime\%\%\%$in_topic\%\%\%$topictitletemp";

    seek(FILE, 0, 0);
    print FILE "$lastposttime\t$threads\t$posts\t$todayforumpost\t$lastposter\t\n";
    close(FILE);

    $posts = 0 if ($posts eq "");
    $threads = 0 if ($threads eq "");
    open(FILE, ">${lbdir}boarddata/forumposts$in_forum.pl");
    print FILE "\$threads = $threads;\n\$posts = $posts;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
    close(FILE);

    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
}
else {
    unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 30);
}
if ($privateforum ne "yes") {
    $topictitletemp =~ s/^＊＃！＆＊//;
    $topictitletemp =~ s/~/\.\./g;
    my $topictitletemp2 = &lbhz("$topictitletemp", 30);
    open(PSF, "$lbdir/data/recentreply.cgi");
    my @hasPSF = <PSF>;
    close(PSF);
    open(PSF, ">$lbdir/data/recentreply.cgi");
    open(PSF2, ">$lbdir/data/recentreply.pl");
    $postdate = &shortdate($currenttime + $addtimes);
    print PSF2 "\$alljh=qq~";
    print PSF "$topictitletemp\t$inmembername\t$in_forum\t$in_topic\t$postdate\t$topictitletemp2\n";
    print PSF2 "・<a href=topic.cgi?forum=$in_forum&topic=$in_topic title='$topictitletemp\n作者：$inmembername\n时间：$postdate'>$topictitletemp2</a>";
    for ($j = 0; $j <= 8; $j++) {
        chomp $hasPSF[$j];
        if ($hasPSF[$j] ne '') {
            my ($d1, $d2, $d3, $d4, $d5, $d6) = split(/\t/, $hasPSF[$j]);
            print PSF2 "<br>・<a href=topic.cgi?forum=$d3&topic=$d4 title='$d1\n作者：$d2\n时间：$d5'>$d6</a>";
            print PSF "$hasPSF[$j]\n";
        }
    }
    print PSF2 "~;\n1;";
    close(PSF2);
    close(PSF);
}
require "$lbdir" . "data/boardstats.cgi";

$filetomake = "$lbdir" . "data/boardstats.cgi";
my $filetoopens = &lockfilename($filetomake);
if (!(-e "$filetoopens.lck")) {
    $totalposts++;
    &winlock($filetomake) if ($OS_USED eq "Nt");
    if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close(FILE);
    }
    &winunlock($filetomake) if ($OS_USED eq "Nt");
}
else {
    unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 30);
}
my $all_1 = ($threadposts + 1) / $topicpre;
if ($all_1 > int($all_1)) {$all_1 = int($all_1) + 1;}

unlink("${lbdir}cache/plcache$in_forum\_0.pl");

$show .= qq~<p>回复成功！<br/><br/><a href="wap_forum.cgi?forum=$in_forum&amp;lid=$lid&amp;paGe=$pa">返回列表..</a></p><p><a href="wap_topic.cgi?f=$in_forum&amp;lid=$lid&amp;t=$in_topic&amp;paGe=$all_1">返回帖子..</a></p>~;
&wapfoot;