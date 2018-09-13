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
$show .= qq~<card  title="$board_name-发表主题">~;
$lid = $query->param('lid');
&check($lid);
$in_forum = $query->param('f');
$in_topictitle = $query->param('title');
if ($in_member_name eq "" || $in_member_name eq "客人") {
    $in_member_name = "客人";
}
else {
    &getmember("$in_member_name");
}
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}
$inpost = $query->param('inpost');
$inpost = $uref->fromUTF8("UTF-8", $inpost);
$in_topictitle = $uref->fromUTF8("UTF-8", $in_topictitle);
$inpost = &cleaninput("$inpost");
$in_topictitle = &cleaninput("$in_topictitle");
$currenttime = time;
$postipaddress = &myip();
$inpost =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost =~ s/\[br\]/<br>/g;
$inpost =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost =~ s/USECHGFONTE/USECHGFONT\&\#069\;/sg;
$inpost =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
&moderator("$in_forum");
$myinmembmod = $inmembmod;
if ($allow_users ne '') {
    &errorout('进入论坛&你不允许进入该论坛！') if (",$allow_users," !~ /,$in_member_name,/i && $member_code ne 'ad');
}
if ($member_code ne 'ad' && $member_code ne 'smo' && $inmembmod ne 'yes') {
    &errorout("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0) {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        &errorout("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
        &errorout("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}
if ($startnewthreads eq "onlysub") {&errorout("发表&对不起，这里是纯子论坛区，不允许发言！");}

if (($floodcontrol eq "on") && ($member_code ne "ad") && ($member_code ne 'smo') && ($member_code ne 'amo') && ($member_code ne 'cmo') && ($member_code ne "mo") && ($inmembmod ne "yes")) {
    ($lastpost, $posturl, $posttopic) = split(/\%\%\%/, $lastpostdate);
    $lastpost = $lastpost + $floodcontrollimit;
    if ($lastpost > $currenttime) {
        my $lastpost1 = $lastpost - $currenttime;
        &errorout("发表新主题&灌水预防机制已经使用，您必须再等待 $lastpost1 秒钟才能再次发表！");
    }
}
if ($postopen eq "no") {&errorout("发表或回复主题&对不起，本论坛不允许发表或回复主题！");}
if (($userregistered eq "no") && (length($in_member_name) > 12)) {&errorout("发表新主题&您输入的用户名太长，请控制在6个汉字内！");}
if (($userregistered eq "no") && ($in_member_name =~ /^客人/)) {&errorout("发表新主题&请不要在用户名的开头中使用客人字样！");}
if ($in_member_name eq "客人") {&errorout("发表新主题&请不要在用户名的开头中使用客人字样！");}
if (($userregistered eq "no") && ($startnewthreads ne "all")) {&errorout("发表新主题&您没有注册！");}
# elsif ((($in_password ne $password)&&($userregistered ne "no"))||(($in_password ne "")&&($userregistered eq "no"))) { &errorout("发表新主题&您的密码错误！"); }
elsif (($member_code eq "banned") || ($member_code eq "masked")) {&errorout("添加回复&您被禁止发言或者发言被屏蔽，请联系管理员解决！");}
elsif ($in_topictitle eq "＊＃！＆＊") {&errorout("发表新主题&必须输入主题标题！");}
elsif (length($in_topictitle) > 92) {&errorout("发表新主题&主题标题过长！");}
else {
    $in_topictitle =~ s/\(无内容\)$//;
    if (($inpost eq "") && ($addme eq "")) {$in_topictitle .= " (无内容)";}
}
$in_topictitle =~ s/()+//isg;
my $tempintopictitle = $in_topictitle;
$tempintopictitle =~ s/ //g;
$tempintopictitle =~ s/\&nbsp\;//g;
$tempintopictitle =~ s/　//isg;
$tempintopictitle =~ s///isg;
$tempintopictitle =~ s/^＊＃！＆＊//;
if ($tempintopictitle eq "") {&errorout("发表新主题&主题标题有问题！");}

$tempaccess = "forumsallowed" . "$in_forum";
$test_entry = $query->cookie("$tempaccess");
if (($allowed_entry{$in_forum} eq "yes") || (($test_entry eq $forum_pass) && ($test_entry ne "")) || ($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {$allowed = "yes";}
if (($privateforum eq "yes") && ($allowed ne "yes")) {&errorout("发表&对不起，您不允许在此论坛发表！");}

if ($startnewthreads eq "no") {
    unless ($member_code eq "ad" || $member_code eq 'smo' || $inmembmod eq "yes") {&errorout("发表新主题&在此论坛中只能由坛主或者本版版主发表新主题！");}
}
elsif ($startnewthreads eq "cert") {
    unless ($member_code eq "ad" || $member_code eq 'smo' || $inmembmod eq "yes" || $member_code eq 'cmo' || $member_code eq 'mo' || $member_code eq 'amo' || $member_code =~ /^rz/) {&errorout("发表新主题&在此论坛中只能由坛主、版主和认证会员发表新主题！");}
}
elsif (($startnewthreads eq "follow") && ($action eq "addnew")) {
    unless ($member_code eq "ad" || $member_code eq 'smo' || $member_code eq 'cmo' || $member_code eq 'mo' || $member_code eq 'amo' || $inmembmod eq "yes") {&errorout("发表新主题&在此论坛中只能由坛主或者版主发表新主题！");}
}
elsif (($startnewthreads eq "all") && ($userregistered eq "no")) {$in_member_name = "$in_member_name(客)";}

if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $member_code ne "ad" && $member_code ne "smo" && $member_code ne "cmo" && $member_code ne "mo" && $member_code ne "amo" && $inmembmod ne "yes") {
    &errorout("发表新主题&对不起，你的删贴率超过了<b>$deletepercent</b>%，管理员不允许你发表新主题！请联系坛主解决！") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
}
$inpost =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;
$inpost = "<img src='$imagesurl/images/sj.gif' width='22' alt='由手机 WAP 发送' /> " . $inpost;
undef $newthreadnumber;
$filetoopen = "$lbdir" . "boarddata/lastnum$in_forum.cgi";
if (open(FILE, "$filetoopen")) {
    $newthreadnumber = <FILE>;
    close(FILE);
    chomp $newthreadnumber;
    $newthreadnumber++;
}

if ((!(-e "${lbdir}forum$in_forum/$newthreadnumber.pl")) && ($newthreadnumber =~ /^[0-9]+$/)) {
    if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE $newthreadnumber;
        close(FILE);
    }
}
else {
    opendir(DIR, "${lbdir}forum$in_forum");
    my @dirdata = readdir(DIR);
    closedir(DIR);
    @dirdata = grep (/.thd.cgi$/, @dirdata);
    @dirdata = sort {$b <=> $a} (@dirdata);
    $highest = $dirdata[0];
    $highest =~ s/.thd.cgi$//;
    $newthreadnumber = $highest + 1;
    if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE $newthreadnumber;
        close(FILE);
    }
}

my $oldthreadnumber = $newthreadnumber - 1;
if (open(FILE, "${lbdir}forum$in_forum/$oldthreadnumber.thd.cgi")) {
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my $threaddata = <FILE>;
    close(FILE);
    (my $amembername, my $atopictitle, my $no, my $no, my $no, my $no, my $apost, my $no) = split(/\t/, $threaddata);
    if (($amembername eq $in_member_name) && ((($apost eq $inpost) && ($apost ne "") && ($inpost ne "")) || ($atopictitle eq $in_topictitle))) {
        if (open(FILE, ">${lbdir}boarddata/lastnum$in_forum.cgi")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE $oldthreadnumber;
            close(FILE);
        }
        &errorout("发表新主题&请不要重复发帖子，已经存在与此帖子主题相同或者内容相同的而且是你发的帖子了！");
    }
}

my $temp = &dofilter("$in_topictitle\t$inpost");
($in_topictitle, $inpost) = split(/\t/, $temp);
$in_topictitle =~ s/(a|A)N(d|D)/$1&#78;$2/sg;
$in_topictitle =~ s/(a|A)n(d|D)/$1&#110;$2/sg;
$in_topictitle =~ s/(o|O)R/$1&#82;/sg;
$in_topictitle =~ s/(o|O)r/$1&#114;/sg;
$in_topictitle =~ s/\\/&#92;/isg;
$in_topictitle =~ s/E/\&\#69\;/g;
$in_topictitle =~ s/e/\&\#101\;/g;

$in_topictitletemp = $in_topictitle;
$in_topictitletemp =~ s/^＊＃！＆＊//;

if (open(FILE, ">${lbdir}forum$in_forum/$newthreadnumber.pl")) {
    print FILE "$newthreadnumber\t$in_topictitle\t\topen\t0\t0\t$in_member_name\t$currenttime\t\t$currenttime\t$inposticon\t$inposttemp\t$addme\t";
    close(FILE);
}

if (open(FILE, ">${lbdir}forum$in_forum/$newthreadnumber.thd.cgi")) {
    print FILE "$in_member_name\t$in_topictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t$inwater\t\n";
    close(FILE);
}
if ($privateforum ne "yes") {
    $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
    my $filetoopens = &lockfilename($filetomakeopen);
    if (!(-e "$filetoopens.lck")) {
        if (-e $filetomakeopen) {
            &winlock($filetomakeopen) if ($OS_USED eq "Nt");
            open(FILE, "$filetomakeopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            my @recentposts = <FILE>;
            close(FILE);
            my $checknumber = 0;
            $maxadpost = 3 if ($maxadpost < 3);
            if (($member_code ne "ad") && ($member_code ne "smo") && ($member_code ne "cmo") && ($member_code ne "mo") && ($member_code ne "amo") && ($member_code !~ /^rz/)) {
                foreach (@recentposts) {
                    (my $no, $no, my $temptopic, $no, $no, my $tempmembername) = split(/\t/, $_);
                    $temptopic =~ s/^＊＃！＆＊//;
                    $checknumber++ if (($in_topictitletemp eq $temptopic) && (lc($tempmembername) eq lc($in_member_name)));
                }

                if ($checknumber >= $maxadpost) {
                    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
                    unlink("${lbdir}forum$in_forum/$newthreadnumber.pl");
                    unlink("${lbdir}forum$in_forum/$newthreadnumber.thd.cgi");
                    unlink("${imagesdir}$usrdir/$in_forum/$in_forum\_${newthreadnumber}.$up_ext");

                    if (($in_member_name ne "") && ($userregistered ne "no") && ($password ne "")) {
                        $memberfiletitle = $in_member_name;
                        $memberfiletitle =~ s/ /\_/isg;
                        $memberfiletitle =~ tr/A-Z/a-z/;
                        my $namenumber = &getnamenumber($memberfiletitle);
                        &checkmemfile($memberfiletitle, $namenumber);
                        if (open(MEMFILE, ">${lbdir}$memdir/$namenumber/$memberfiletitle.cgi")) {
                            print MEMFILE "$in_member_name\t$password\t$membertitle\tmasked\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
                            close(MEMFILE);
                        }
                        unlink("${lbdir}cache/myinfo/$memberfiletitle.pl");
                        unlink("${lbdir}cache/meminfo/$memberfiletitle.pl");
                    }
                    $filetomake = "$lbdir" . "data/idbans.cgi";
                    open(FILE, ">>$filetomake");
                    print FILE "$in_member_name\t";
                    close(FILE);
                    &errorout("出错&由于你在多区发送广告，所以你已经被禁止发言！");
                }
            }

            $recentposts = @recentposts;
            $maxpostreport = 31;
            if ($recentposts < $maxpostreport) {$maxpostreport = $recentposts;}
            else {$maxpostreport--;}
            if ($maiweb_sl eq 'off') {
                if (open(FILE, ">$filetomakeopen")) {
                    flock(FILE, 2) if ($OS_USED eq "Unix");
                    print FILE "$in_forum\t$newthreadnumber\t$in_topictitletemp\t$currenttime\t$inposticon\t$in_member_name\t\n";
                    for ($i = 0; $i < $maxpostreport; $i++) {print FILE $recentposts[$i];}
                    close(FILE);
                }
                &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
            }
            else {
                $topictitle3 = $in_topictitletemp;
                $topictitle3 =~ s/~/\.\./g;
                $topictitle22 = &lbhz("$topictitle3", 30);
                $postdate = $currenttime;
                $postdate = &shortdate($postdate + $addtimes);
                if (open(FILE, ">$filetomakeopen")) {
                    open(PSF2, ">$lbdir/data/recentpost.pl");
                    print PSF2 "\$allnew=qq~";
                    flock(FILE, 2) if ($OS_USED eq "Unix");
                    print FILE "$in_forum\t$newthreadnumber\t$topictitle3\t$postdate\t\t$in_member_name\t$topictitle22\n";
                    print PSF2 "·<a href=topic.cgi?forum=$in_forum&topic=$newthreadnumber title='$topictitle3\n作者：$in_member_name\n时间：$postdate'>$topictitle22</a>";
                    for ($i = 0; $i < 9; $i++) {
                        chomp $recentposts[$i];
                        if ($recentposts[$i] ne '') {
                            my ($d1, $d2, $d3, $d4, $no, $d5, $d6) = split(/\t/, $recentposts[$i]);
                            next if ($d6 eq '');
                            print PSF2 "<br>·<a href=topic.cgi?forum=$d1&topic=$d2  title='$d3\n作者：$d5\n时间：$d4'>$d6</a>";
                            print FILE "$recentposts[$i]\n";
                        }
                    }
                    print PSF2 "~;\n1;";
                    close(PSF2);
                    close(FILE);
                }
                &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
            }
        }
        else {
            if ($maiweb_sl eq 'off') {
                if (open(FILE, ">$filetomakeopen")) {
                    print FILE "$in_forum\t$newthreadnumber\t$in_topictitletemp\t$currenttime\t$inposticon\t$in_member_name\t\n";
                    close(FILE);
                }
            }
            else {
                if (open(FILE, ">$filetomakeopen")) {
                    $topictitle3 = $in_topictitletemp;
                    $topictitle3 =~ s/~/\.\./g;
                    $topictitle22 = &lbhz("$topictitle3", 30);
                    $postdate = $currenttime;
                    $postdate = &shortdate($postdate + $addtimes);
                    print FILE "$in_forum\t$newthreadnumber\t$topictitle3\t$postdate\t$inposticon\t$in_member_name\t$topictitle22\n";
                    close(FILE);
                }
            }
        }
    }
    else {
        unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 30);
    }
}
my $nowtime = &shortdate($currenttime + $timezone * 3600);

my $filetoopens = "$lbdir/data/todaypost.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
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
            $nowtoday = $nowtime;
            $yestdaypost = $todaypostno;
            $todaypostno = 1;
            opendir(CATDIR, "${lbdir}cache");
            @dirdata = readdir(CATDIR);
            closedir(CATDIR);
            @dirdata = grep (/forumcache/, @dirdata);
            foreach (@dirdata) {unlink("${lbdir}cache/$_");}
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

$file = "$lbdir" . "boarddata/listno$in_forum.cgi";
&winlock($file) if ($OS_USED eq "Nt");
open(LIST, "$file");
flock(LIST, 2) if ($OS_USED eq "Unix");
sysread(LIST, $listall, (stat(LIST))[7]);
close(LIST);
$listall =~ s/\r//isg;

if (length($listall) > 500) {
    if (open(LIST, ">$file")) {
        flock(LIST, 2) if ($OS_USED eq "Unix");
        print LIST "$newthreadnumber\n$listall";
        close(LIST);
    }
    &winunlock($file) if ($OS_USED eq "Nt");
    if (open(LIST, ">>${lbdir}boarddata/listall$in_forum.cgi")) {
        print LIST "$newthreadnumber\t$in_topictitletemp\t$in_member_name\t$currenttime\t\n";
        close(LIST);
    }
}
else {
    &winunlock($file) if ($OS_USED eq "Nt");
    require "rebuildlist.pl";
    my $truenumber = rebuildLIST(-Forum => "$in_forum");
    ($tpost, $treply) = split(/\|/, $truenumber);
}

$cleanmembername = $in_member_name;
$cleanmembername =~ s/ /\_/isg;
$cleanmembername =~ tr/A-Z/a-z/;

$jifen = $numberofposts * 2 + $numberofposts - $postdel * 5 if ($jifen eq "");

if ($forumallowcount ne "no") {
    $numberofposts++;
    $mymoney += $forumpostmoney - $addmoney if ($forumpostmoney ne "");
    if ($forumpostjf ne "") {$jifen += $forumpostjf;}
    else {$jifen += $ttojf;}
}
$lastpostdate = "$currenttime\%\%\%topic.cgi?forum=$in_forum&topic=$newthreadnumber\%\%\%$in_topictitletemp" if ($privateforum ne "yes");
chomp $lastpostdate;

if (($userregistered ne "no") && ($password ne "")) {
    $filetomake = "$lbdir" . "$memdir/$cleanmembername.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    if ((open(FILE, ">$filetomake")) && ($in_member_name ne "")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$password\t$membertitle\t$member_code\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
    }
    &winunlock($filetomake) if ($OS_USED eq "Nt");
    unlink("${lbdir}cache/myinfo/$cleanmembername.pl");
    if (((-M "${lbdir}cache/meminfo/$cleanmembername.pl") * 86400 > 60 * 2) || (!(-e "${lbdir}cache/meminfo/$cleanmembername.pl"))) {
        require "getnameinfo.pl" if ($onloadinfopl ne 1);
        &getmemberinfo($cleanmembername);
    }
}

$filetoopen = "${lbdir}boarddata/foruminfo$in_forum.cgi";
my $filetoopens = &lockfilename($filetoopen);
if (!(-e "$filetoopens.lck")) {
    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(FILE, "+<$filetoopen");
    ($no, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/, <FILE>);

    $lastposter = $in_member_name;
    $lastposttime = $currenttime;
    if (($tpost ne "") && ($treply ne "")) {
        $threads = $tpost;
        $posts = $treply;
    }
    else {$threads++;}
    my ($todayforumpost, $todayforumposttime) = split(/\|/, $todayforumpost);
    if (($nowtime ne $todayforumposttime) || ($todayforumpost eq "")) {$todayforumpost = 1;}
    else {$todayforumpost++;}
    $todayforumpost = "$todayforumpost|$nowtime";
    $lastposttime = "$lastposttime\%\%\%$newthreadnumber\%\%\%$in_topictitletemp";
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

require "$lbdir" . "data/boardstats.cgi";
$filetomake = "$lbdir" . "data/boardstats.cgi";
my $filetoopens = &lockfilename($filetomake);
if (!(-e "$filetoopens.lck")) {
    $totalthreads++;
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

opendir(CATDIR, "${lbdir}cache");
my @dirdata = readdir(CATDIR);
closedir(CATDIR);
unlink("${lbdir}cache/plcache$in_forum\_0.pl");
$show .= qq~<p>新主题发表成功..<br/><a href="wap_forum.cgi?forum=$in_forum&amp;lid=$lid&amp;paGe=$pa">返回列表..</a></p><p><a href="wap_topic.cgi?f=$in_forum&amp;lid=$lid&amp;t=$newthreadnumber">返回帖子..</a></p>~;
&wapfoot;