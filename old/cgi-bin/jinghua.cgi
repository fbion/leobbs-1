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
use File::Copy;
$loadcopymo = 1;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "code.cgi";
require "bbs.lib.pl";
require "rebuildlist.pl";
require "recooper.pl";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$|++;
$thisprog = "jinghua.cgi";
$query = new LBCGI;
&ipbanned; #封杀一些 ip

$inshow = $query->param('show');
for ('forum', 'topic', 'membername', 'password', 'action', 'checked', 'movetoid') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$in_forum = $forum;
$in_topic = $topic;
$in_member_name = $membername;
$in_password = $password;
if ($in_password ne "") {
    eval {$in_password = md5_hex($in_password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
    unless ($@) {$in_password = "lEO$in_password";}
}

@intopic = split(/ /, $in_topic);
$in_topic =~ s/ //g;
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic) && ($in_topic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
require "sendmanageinfo.pl" if ($sendmanageinfo eq "yes");

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

if (($in_forum) && ($in_forum !~ /^[0-9]+$/)) {&error("普通错误&请不要修改生成的 URL！");}
if (($in_topic) && ($in_topic !~ /^[0-9]+$/)) {&error("普通错误&请不要修改生成的 URL！");}
if (!$in_member_name) {$in_member_name = $query->cookie("amembernamecookie");}
if (!$in_password) {$in_password = $query->cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($in_member_name eq "") {
    $in_member_name = "客人";
}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    if ($in_password ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
&getoneforum("$in_forum");
#&moderator("$in_forum");
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}
&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz !~ /,$member_code,/);
if ($allow_users ne '') {
    &error('进入论坛&你不允许进入该论坛！') if (",$allow_users," !~ /,$in_member_name,/i && $member_code ne 'ad');
}
if ($member_code ne 'ad' && $member_code ne 'smo' && $inmembmod ne 'yes') {
    &error("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0) {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        &error("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
        &error("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

my %Mode = (
    'add' => \&add,
    'del' => \&del,
);
if ($Mode{$action}) {
    $Mode{$action}->();
}
elsif (($in_forum ne "") && ($action eq "list")) {&list;}
else {&error("普通错误&请以正确的方式访问本程序");}
&output($board_name, \$output);

sub add {
    $cleartoedit = "no";

    &mischeader("标记精华贴子");
    if (($member_code eq "ad") && ($in_password eq $password)) {$cleartoedit = "yes";}
    if (($member_code eq "smo") && ($in_password eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($member_code ne "amo") && ($in_password eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no") {&error("标记精华贴子&您不是本论坛坛主或版主，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        unlink("${lbdir}cache/forumstop$in_forum.pl");
        unlink("${lbdir}cache/forumstopic$in_forum.pl");
        my $file = "$lbdir" . "boarddata/jinghua$in_forum.cgi";
        if (open(ENT, $file)) {
            @toptopic = <ENT>;
            close(ENT);
            $jhdata = join("\_", @toptopic);
            $jhdata = "\_$jhdata\_";
            $jhdata =~ s/\W//isg;
            if (open(ENT, ">$file")) {
                undef @intopictemp;
                $jhdata1 = "\_";
                foreach (@intopic) {
                    chomp $_;
                    if ((-e "${lbdir}forum$in_forum/$_.thd.cgi") && ($_ ne "")) {
                        print ENT "$_\n";
                        $jhdata1 = "\_$_$jhdata1";
                        push(@intopictemp, $_);
                    }
                }
                undef $in_topictemp1;
                foreach $ttemp (@toptopic) {
                    chomp $ttemp;
                    if ((-e "${lbdir}forum$in_forum/$ttemp.thd.cgi") && ($ttemp ne "") && ($jhdata1 !~ /\_$ttemp\_/)) {
                        print ENT "$ttemp\n";
                        $jhdata1 = "$jhdata1\_$ttemp";
                    }
                    else {
                        $in_topictemp1 = "$in_topictemp1\_$ttemp";
                    }
                }
                close(ENT);
            }
        }
        else {
            if (open(ENT, ">$file")) {
                $jhdata = "\_";
                undef @intopictemp;
                foreach (@intopic) {
                    chomp $_;
                    if ((-e "${lbdir}forum$in_forum/$_.thd.cgi") && ($_ ne "") && ($jhdata !~ /\_$_\_/)) {
                        print ENT "$_\n";
                        $jhdata = "\_$_$jhdata";
                        push(@intopictemp, $_);
                    }
                }
                close(ENT);
            }
        }
        if ($in_topictemp1 ne "") {
            undef @intopictemp1;
            $in_topictemp1 = "$in_topictemp1\_";
            foreach (@intopictemp) {
                chomp $_;
                push(@intopictemp1, $_) if ($in_topictemp1 !~ /\_$_\_/);
            }
            @intopictemp = @intopictemp1;
        }
        @intopic = @intopictemp;
        undef @intopictemp;
        $alloldposts = @intopic;
        if ($movetoid ne "") {
            if ($movetoid == $in_forum) {&error("拷贝主题&不允许在同个论坛上拷贝主题！");}
            if (open(FILE, "${lbdir}forum$movetoid/foruminfo.cgi")) {
                $readdisktimes++;
                $forums = <FILE>;
                close(FILE);
                (undef, undef, undef, $newforumname, undef) = split(/\t/, $forums);
            }
            else {
                &error("拷贝主题&目标论坛不存在！")
            }

            my @inforumwrite;
            $alloldthreadposts = 0;
            opendir(DIR, "${imagesdir}$usrdir/$in_forum");
            @files = readdir(DIR);
            closedir(DIR);
            @files = grep (/^$in_forum\_$in_topic(\.|\_)/, @files);

            foreach $in_topic (@intopic) {
                $currenttime = time;
                if ($newthreadnumber eq "") {
                    if (open(FILE, "${lbdir}boarddata/lastnum$movetoid.cgi")) {
                        $newthreadnumber = <FILE>;
                        close(FILE);
                        chomp $newthreadnumber;
                        $newthreadnumber++;
                    }
                }
                else {$newthreadnumber++;}
                unless ((!(-e "${lbdir}forum$movetoid/$newthreadnumber.pl")) && ($newthreadnumber =~ /^[0-9]+$/)) {
                    opendir(DIR, "${lbdir}forum$movetoid");
                    @sorteddirdata = readdir(DIR);
                    closedir(DIR);
                    @sorteddirdata = grep (/.thd.cgi$/, @sorteddirdata);
                    @sorteddirdata = sort {$b <=> $a} (@sorteddirdata);
                    $highestno = $sorteddirdata[0];
                    undef @sorteddirdata;
                    $highestno =~ s/.thd.cgi$//;
                    $newthreadnumber = $highestno + 1;
                }

                $in_topic =~ s/\W//isg;
                chomp $in_topic;
                open(ENT, "${lbdir}forum$in_forum/$in_topic.pl");
                $in = <ENT>;
                close(ENT);
                chomp $in;
                ($topicid, $topictitle, $topicdescription1, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon, $inposttemp, $addmetemp) = split(/\t/, $in);

                $in_forumwrite = "$newthreadnumber\t$topictitle\t\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t$lastinposticon\t$inposttemp\t$addmetemp\t";
                if (open(FILE, ">${lbdir}forum$movetoid/$newthreadnumber.pl")) {
                    print FILE "$in_forumwrite";
                    close(FILE);
                }
                push(@inforumwrite, "$newthreadnumber");

                $filetoopen = "${lbdir}forum$in_forum/$in_topic.thd.cgi";
                open(FILE, "$filetoopen");
                my @oldforummessages = <FILE>;
                close(FILE);
                $oldthreadposts = @oldforummessages - 1;
                $alloldthreadposts = $alloldthreadposts + $oldthreadposts;

                copy("${lbdir}forum$in_forum/$in_topic.thd.cgi", "${lbdir}forum$movetoid/$newthreadnumber.thd.cgi") if (-e "${lbdir}forum$in_forum/$in_topic.thd.cgi");
                copy("${lbdir}forum$in_forum/$in_topic.mal.pl", "${lbdir}forum$movetoid/$newthreadnumber.mal.pl") if (-e "${lbdir}forum$in_forum/$in_topic.mal.pl");
                copy("${lbdir}forum$in_forum/$in_topic.poll.cgi", "${lbdir}forum$movetoid/$newthreadnumber.poll.cgi") if (-e "${lbdir}forum$in_forum/$in_topic.poll.cgi");
                copy("${lbdir}forum$in_forum/rate$in_topic.file.pl", "${lbdir}forum$movetoid/rate$newthreadnumber.file.pl") if (-e "${lbdir}forum$in_forum/rate$in_topic.file.pl");
                copy("${lbdir}forum$in_forum/rateip$in_topic.file.pl", "${lbdir}forum$movetoid/rateip$newthreadnumber.file.pl") if (-e "${lbdir}forum$in_forum/rateip$in_topic.file.pl");


                ##########旧的附件copy，为了兼容，保留 路杨
                @files1 = grep (/^$in_forum\_$in_topic\./, @files);
                $files1 = @files1;
                if ($files1 > 0) {
                    foreach (@files1) {
                        (my $name, my $ext) = split(/\./, $_);
                        copy("${imagesdir}$usrdir/$in_forum/$name.$ext", "${imagesdir}$usrdir/$movetoid/$movetoid\_$newthreadnumber\.$ext");
                    }
                }

                @files1 = grep (/^$in_forum\_$in_topic\_/, @files);
                $files1 = @files1;
                if ($files1 > 0) {
                    foreach (@files1) {
                        (my $name, my $ext) = split(/\./, $_);
                        (my $name1, my $name2, my $name3) = split(/\_/, $name);
                        copy("${imagesdir}$usrdir/$in_forum/$name.$ext", "${imagesdir}$usrdir/$movetoid/$movetoid\_$newthreadnumber\_$name3\.$ext");
                    }
                }
                ###########
                require "dopost.pl";                                                     #路杨
                &moveallupfiles($in_forum, $in_topic, $movetoid, $newthreadnumber, "yes"); #新的附件copy 路杨
            }

            $file = "$lbdir" . "boarddata/listno$movetoid.cgi";
            &winlock($file) if ($OS_USED eq "Nt");
            open(LIST, "$file");
            flock(LIST, 1) if ($OS_USED eq "Unix");
            sysread(LIST, $listall, (stat(LIST))[7]);
            close(LIST);
            $listall =~ s/\r//isg;
            open(LIST, ">$file");
            flock(LIST, 2) if ($OS_USED eq "Unix");
            foreach (@inforumwrite) {
                chomp $_;
                print LIST "$_\n" if ($_ ne "");
            }
            print LIST $listall;
            close(LIST);
            &winunlock($file) if ($OS_USED eq "Nt");

            $newthreadnumber++;
            if (open(FILE, ">${lbdir}boarddata/lastnum$movetoid.cgi")) {
                print FILE $newthreadnumber;
                close(FILE);
            }

            $filetoopen = "${lbdir}boarddata/foruminfo$movetoid.cgi";
            my $filetoopens = &lockfilename($filetoopen);
            if (!(-e "$filetoopens.lck")) {
                &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

                open(FILE, "+<$filetoopen");
                ($lastposttime, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/, <FILE>);

                $threads = $alloldposts + $threads;
                $posts = $posts + $alloldthreadposts;
                $lastposter = $startedby if ($lastposter eq "");
                $topictitle =~ s/^＊＃！＆＊//;
                my $newthreadnumber = $newthreadnumber - 1;
                $lastposttime = "$currenttime\%\%\%$newthreadnumber\%\%\%$topictitle";
                seek(FILE, 0, 0);
                print FILE "$lastposttime\t$threads\t$posts\t$todayforumpost\t$lastposter\t\n";
                close(FILE);
                $posts = 0 if ($posts eq "");
                $threads = 0 if ($threads eq "");
                open(FILE, ">${lbdir}boarddata/forumposts$movetoid.pl");
                print FILE "\$threads = $threads;\n\$posts = $posts;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
                close(FILE);

                &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            }
            else {
                unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 30);
            }

            $filetomake = "${lbdir}data/boardstats.cgi";
            require "$filetomake";

            $totalthreads = $totalthreads + $alloldposts;
            $totalposts = $totalposts + $alloldthreadposts;
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

        $newforumname = "并复制到 $newforumname" if ($newforumname ne "");
        if ($alloldposts == 1) {
            &addadminlog("标记精华贴子$newforumname", $in_topic);
        }
        else {
            &addadminlog("批量标记精华贴子 $alloldposts 篇$newforumname");
        }
        &UpdateNo(\@intopic, $in_forum, "+");
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>标记精华贴子成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>具体情况：<ul>
<li><a href="jinghua.cgi?action=list&forum=$in_forum">返回精华区</a>
<li><a href="forums.cgi?forum=$in_forum">返回论坛</a>
<li><a href="leobbs.cgi">返回论坛首页</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $in_member_name =~ s/\_/ /g;
        open(FILE, "${lbdir}data/allforums.cgi");
        my @forums = <FILE>;
        close(FILE);
        $jumphtml .= "<option value=\"\">选择一个论坛\n</option><option value=\"\">不做任何拷贝\n</option>";
        $a = 0;
        foreach (@forums) {
            chomp $_;
            next if (length("$_") < 30);
            $a = sprintf("%09d", $a);
            ($movetoforumid, $category, $categoryplace, $forumname, $forumdescription, $noneed, $noneed, $noneed, $noneed, $startnewthreads, $noneed, $noneed, $noneed, $noneed, $noneed, $miscad2, $noneed, $forum_pass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $_);
            $categoryplace = sprintf("%09d", $categoryplace);
            $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$movetoforumid\t$forumgraphic\t$startnewthreads\t$miscad2\t$misc\t$forum_pass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
            push(@rearrangedforums, $rearrange);
            $a++;
        }

        @finalsortedforums = sort (@rearrangedforums);
        foreach (@finalsortedforums) {
            ($categoryplace, my $a, $category, $forumname, $forumdescription, $movetoforumid, $forumgraphic, $startnewthreads, $miscad2, $misc, $forum_pass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $_);

            if ((($startnewthreads eq "no") || ($startnewthreads eq "cert")) && ($movetoforumid ne $in_forum)) {
                $jumphtml .= "<option value=\"$movetoforumid\">$forumname\n</option>";
            }
        }
        $in_topic = @intopic;
        &error("标记精华帖子&请先选择帖子再进行标记！") if ($in_topic <= 0);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="add">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="@intopic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [标记 $in_topic 个精华帖子]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$in_member_name</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>拷贝一份至精华区：</b></font></td>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><select name="movetoid">$jumphtml</select></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub del {
    &mischeader("取消精华贴子");
    $cleartoedit = "no";
    if (($member_code eq "ad") && ($in_password eq $password)) {$cleartoedit = "yes";}
    if (($member_code eq "smo") && ($in_password eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($member_code ne "amo") && ($in_password eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no") {&error("取消精华贴子&您不是本论坛坛主或版主，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        unlink("${lbdir}cache/forumstop$in_forum.pl");
        unlink("${lbdir}cache/forumstopic$in_forum.pl");
        my $file = "$lbdir" . "boarddata/jinghua$in_forum.cgi";
        if (-e $file) {
            open(ENT, $file);
            @toptopic = <ENT>;
            close(ENT);

            if (open(ENT, ">$file")) {
                $jhdel = 0;
                foreach (@toptopic) {
                    chomp $_;
                    if ($_ ne $in_topic) {
                        print ENT "$_\n" if ((-e "${lbdir}forum$in_forum/$_.thd.cgi") && ($_ ne ""));
                    }
                    else {
                        $jhdel = 1;
                    }
                }
                close(ENT);
            }
        }
        &addadminlog("取消精华贴子标记", $in_topic);
        &UpdateNo($in_topic, $in_forum, "-") if ($jhdel eq 1);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>取消精华贴子成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>具体情况：<ul>
<li><a href="jinghua.cgi?action=list&forum=$in_forum">返回精华区</a>
<li><a href="forums.cgi?forum=$in_forum">返回论坛</a>
<li><a href="leobbs.cgi">返回论坛首页</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $in_member_name =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="del">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [取消精华贴子]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$in_member_name</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub list {
    &mischeader("本版精华贴子");
    if ("$privateforum" eq "yes") {
        if ($in_member_name eq "客人") {
            print "<script language='javascript'>document.location = 'loginout.cgi?forum=$in_forum'</script>";
            exit;
        }
        $test_entry = cookie("forumsallowed$in_forum");
        if ((($test_entry eq $forum_pass) && ($test_entry ne "")) || (($userregistered ne "no") && ($allowed_entry{$in_forum} eq "yes")) || ($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {
            if ($in_password ne $password) {&error("进入论坛&密码错误，你不允许进入该论坛！");}
        }
        else {require "accessform.pl";}
    }
    if (($startnewthreads eq "cert") && (($member_code ne "ad" && $member_code ne "smo" && $member_code ne "cmo" && $member_code ne "amo" && $member_code ne "mo" && $member_code !~ /^rz/) || ($in_member_name eq "客人")) && ($userincert eq "no")) {&error("进入论坛&一般会员不允许进入此论坛！");}

    $defaultsmilewidth = "width=$defaultsmilewidth" if ($defaultsmilewidth ne "");
    $defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        if ($privateforum ne "yes") {
            &whosonline("$in_member_name\t$forumname\tboth\t查看论坛上的精华贴子\t");
        }
        else {
            &whosonline("$in_member_name\t$forumname(密)\tboth\t查看保密论坛上的精华贴子\t");
        }
    }

    $output .= qq~
<style>
TABLE {BORDER-TOP: 0px; BORDER-LEFT: 0px; BORDER-BOTTOM: 1px; }
TD {BORDER-RIGHT: 0px; BORDER-TOP: 0px; color: $fontcolormisc; }
.ha {color: $fonthighlight; font: bold;}
.hb {color: $menufontcolor; font: bold;}
.dp {padding: 4px 0px;}
</style>
<span id=forum>
<SCRIPT>valigntop()</SCRIPT>
<table cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td height=1></td></tr></table><center>
<table cellpadding=0 cellspacing=0 width=$tablewidth height=24 bordercolor=$tablebordercolor border=1>
<tr><td bgcolor=$titlecolor width=32 align=center $catbackpic><font color=$titlefontcolor><b>状态</b></td>
<td bgcolor=$titlecolor width=* align=center $catbackpic><font color=$titlefontcolor><b>主　题</b> (点心情符为新闻方式阅读)</td>
<td bgcolor=$titlecolor align=center width=80 $catbackpic><font color=$titlefontcolor><b>作 者</b></td>
<td bgcolor=$titlecolor align=center width=32 $catbackpic><font color=$titlefontcolor><b>回复</b></td>
<td bgcolor=$titlecolor align=center width=32 $catbackpic><font color=$titlefontcolor><b>点击</b></td>
<td bgcolor=$titlecolor width=195 align=center $catbackpic><font color=$titlefontcolor><b>　 最后更新 　 | 最后回复人</b></td>
</tr></table>
	~;

    $icon_num = int(myrand(10));
    $topcount = 0;
    $filetoopen = "$lbdir" . "boarddata/jinghua$in_forum.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        @ontop = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }
    else {undef @ontop;}
    $topcount = @ontop;
    $numberofpages = $topcount / $maxthreads;

    if ($topcount > $maxthreads) {
        $showmore = "yes";
        if ($inshow eq "" || $inshow < 0) {$inshow = 0;}
        if ($inshow > 0) {$startarray = $inshow;}
        else {$startarray = 0;}
        $endarray = $inshow + $maxthreads - 1;
        if ($endarray < ($topcount - 1)) {$more = "yes";}
        elsif (($endarray > ($maxthreads - 1)) && ($more ne "yes")) {$endarray = $topcount - 1;}
    }
    else {
        $showmore = "no";
        $startarray = 0;
        $topicpages = qq~<font color=$menufontcolor>本精华区只有一页</font>~;
        $endarray = $topcount - 1;
    }

    if ($showmore eq "yes") {
        if ($maxthreads < $topcount) {
            ($integer, $decimal) = split(/\./, $numberofpages);
            if ($decimal > 0) {$numberofpages = $integer + 1;}
            $mypages = $numberofpages;
            #分页
            $intshow = $inshow / (12 * $maxthreads);
            ($intshow, $mydecimal) = split(/\./, $intshow);
            $intshow = $intshow + 1;
            $preshow = ($intshow - 1) * 12 * $maxthreads - $maxthreads;
            $nextshow = $intshow * 12 * $maxthreads;
            $pages = qq~<a href="$thisprog?action=list&forum=$in_forum&show=$preshow"><font color=$menufontcolor><b>←</b></font></a> ~ if ($intshow > 1);
            if ($numberofpages > ($intshow * 12)) {
                $numberofpages = ($intshow * 12);
                $isnext = qq~<a href="$thisprog?action=list&forum=$in_forum&show=$nextshow"><font color=$menufontcolor><b>→</b></font></a> ~;
            }
            $pagestart = ($intshow - 1) * 12 * $maxthreads;
            $counter = ($intshow - 1) * 12;
            while ($numberofpages > $counter) {
                $counter++;
                if ($inshow ne $pagestart) {$pages .= qq~<a href="$thisprog?action=list&forum=$in_forum&show=$pagestart"><font color=$menufontcolor><b>$counter</b></font></a> ~;}
                else {$pages .= qq~<font color=$fonthighlight><b>$counter</b></font> ~;}
                $pagestart = $pagestart + $maxthreads;
            }
            $pages .= $isnext;
            #分页end
        }
        $topicpages = qq~<font color=$menufontcolor><b>本精华区共有 <font color=$fonthighlight>$mypages</font> 页</b> [ $pages ]~;
    }
    if ($topcount > 0) {

        for ($i = $startarray; $i <= $endarray; $i++) {
            $id = $ontop[$i];
            chomp $id;
            $rr = &readthreadpl($in_forum, $id);
            if ($rr ne "") {push(@toptopic, $rr);}
        }
    }
    else {undef @toptopic;}

    $topiccount = 0;
    foreach $topic (@toptopic) {
        chomp $topic;
        ($lastpostdate, $topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $posticon, $posttemp) = split(/\t/, $topic);
        next if ($topicid eq "");
        if ($posticon ne "") {
            $poll = 0;
            if ($posticon =~ /<br>/i) {
                $posticon = int(myrand(23));
                $posticon = "0$posticon" if ($posticon < 10);
                $posticon = qq~<img src=$imagesurl/posticons/$posticon.gif border=0 alt="新闻方式浏览">~;
            }
            else {
                $posticon = qq~<img src=$imagesurl/posticons/$posticon border=0 alt="新闻方式浏览">~;
            }
        }
        else {
            $posticon = int(myrand(23));
            $posticon = "0$posticon" if ($posticon < 10);
            $posticon = qq~<img src=$imagesurl/posticons/$posticon.gif border=0 alt="新闻方式浏览">~;
        }

        $topictitle =~ s/^＊＃！＆＊//;
        $lastpostdatetemp = $lastpostdate;

        $lastpostdate = $lastpostdatetemp;
        $topcount = $threadposts + 1;
        $topcount = $topcount / $maxtopics;
        $counter = 0;
        if ($topcount > $maxtopics) {
            if ($maxtopics < $topcount) {
                ($integer, $decimal) = split(/\./, $topcount);
                if ($decimal > 0) {$topcount = $integer + 1;}
                $pagestart = 0;
                while ($topcount > $counter) {
                    $counter++;
                    $threadpages .= qq~<a href=topic.cgi?forum=$in_forum&topic=$topicid&start=$pagestart><font color=$fonthighlight><b>$counter</b></font></a> ~;
                    $pagestart = $pagestart + $maxtopics;
                }
            }
            $pagestoshow = qq~<font color=$forumfontcolor>　　[第 $threadpages 页]</font>~;
        }

        if ($lastpostdate ne "") {
            $lastpostdate = $lastpostdate + ($timedifferencevalue * 3600) + ($timezone * 3600);
            $longdate = &dateformatshort("$lastpostdate");
            $lastpostdate = qq~<font color=$fontcolormisc>$longdate</font>~;
        }
        else {
            $lastpostdate = qq~<font color=$fontcolormisc>没有~;
            $lastpoststamp = "";
        }
        $startedpostdate = $startedpostdate + ($timedifferencevalue * 3600) + ($timezone * 3600);
        $startedlongdate = &shortdate("$startedpostdate");
        $startedshorttime = &shorttime("$startedpostdate");
        $startedpostdate = qq~<font color=$fontcolormisc>$startedlongdate</font>~;
        $screenmode = $query->cookie("screenmode");
        $topictitlemax = 54;

        if ($tablewidth > 100) {
            if ($tablewidth > 1000) {$topictitlemax = 84;}
            elsif ($tablewidth > 770) {$topictitlemax = 71;}
            else {$topictitlemax = 40;}
        }
        else {
            if ($screenmode >= 10) {$topictitlemax = 84;}
            elsif ($screenmode >= 8) {$topictitlemax = 71;}
            else {$topictitlemax = 40;}
        }

        $posttemp = "(无内容)" if ($posttemp eq "");
        if (length($topictitle) > $topictitlemax) {$topictitletemp = substr($topictitle, 0, $topictitlemax - 4) . " ...";}
        else {$topictitletemp = $topictitle;}
        $topictitle = qq~<ACRONYM TITLE="最后回复摘要：\n\n$posttemp"><a href=topic.cgi?forum=$in_forum&topic=$topicid target=_blank>$topictitletemp</a></ACRONYM>~;
        $startedbyfilename = $startedby;
        $startedbyfilename =~ s/ /\_/isg;
        $startedbyfilename =~ tr/A-Z/a-z/;
        if ($startedby =~ /\(客\)/) {
            $startedby =~ s/\(客\)//isg;
            $startedby = qq~<font color=$postfontcolorone title="此为未注册用户">$startedby</font>~;
        }
        else {$startedby = qq~<a href=profile.cgi?action=show&member=~ . uri_escape($startedbyfilename) . qq~>$startedby</a>~;}
        if (($threadstate eq "poll") || ($threadstate eq "pollclosed")) {$outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=63 rowspan=2><ACRONYM TITLE="回复数：$threadposts， 点击数：$threadviews">共 $size 票</ACRONYM></font></td>~;}
        else {$outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadposts</font></td><td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadviews</font></td>~;}

        if ($lastposter) {
            $lastposterfilename = $lastposter;
            $lastposterfilename =~ s/ /\_/isg;
            if ($lastposter =~ /\(客\)/) {
                $lastposter =~ s/\(客\)//isg;
                $lastposter = qq~<font color=$postfontcolorone title="此为未注册用户">$lastposter</font>~;
            }
            else {
                $lastposter = qq~<a href=profile.cgi?action=show&member=~ . uri_escape($lastposterfilename) . qq~>$lastposter</a>~;
            }
        }
        else {$lastposter = qq~<font color=$fontcolormisc>--------</a>~;}

        $topicdescriptiontemp = $topicdescription;

        $topicdescriptiontemp =~ s/\s*(.*?)\s*\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/$3/isg;
        $topicdescriptiontemp =~ s/\<\/a\>//isg;

        if (length($topicdescriptiontemp) > ($topictitlemax - 4)) {
            $topicdescriptiontemp = substr($topicdescriptiontemp, 0, $topictitlemax - 8) . " ...";
            $topicdescription =~ s/\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/\<a $1\>$topicdescriptiontemp\<\/a\>/isg;
        }

        if ($topicdescription) {$topicdescription = qq~<br>　　-=> $topicdescription~;}

        if ($counter == 0) {$pagestoshowtemp1 = 0;}
        else {$pagestoshowtemp1 = 7;}
        $totlelength = $counter * 3.3 + $pagestoshowtemp1 + length($topictitletemp) + 4; #标题栏的总长度
        undef $pagestoshowtemp1;

        if (($member_code eq "ad") || ($member_code eq "smo") || ($inmembmod eq "yes")) {
            $admini = qq~<DIV ALIGN=Right><font color=$titlecolor>|<a href=jinghua.cgi?action=del&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>除</font></a>|<a href=jinghua.cgi?action=add&forum=$in_forum&topic=$topicid><font color=$titlecolor>提</font></a>|<a href=postings.cgi?action=lock&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>锁</font></a>|<a href=postings.cgi?action=unlock&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|</font>&nbsp;</DIV>~;
        }
        else {
            $admini = "";
        }
        $topicicon = "<img src=$imagesurl/images/jh.gif border=0>";

        if (($threadstate eq "poll") || ($threadstate eq "pollclosed")) {
            $size = 0;
            if (open(FILE, "${lbdir}forum$forumid/$topicid.poll.cgi")) {
                my @allpoll = <FILE>;
                close(FILE);
                $size = @allpoll;
            }
        }

        if (($threadstate eq "poll") || ($threadstate eq "pollclosed")) {$outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=63 rowspan=2><ACRONYM TITLE="回复数：$threadposts， 点击数：$threadviews">共 $size 票</ACRONYM></font></td>~;}
        else {$outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadposts</font></td><td bgcolor=$forumcolortwo align=center width=30><font color=$forumfontcolor>$threadviews</font></td>~;}

        $topictitle = $topictitle . "<BR>" if ($totlelength > $topictitlemax + 5);
        $output .= qq~
		<table cellspacing=0 width=$tablewidth bordercolor=$tablebordercolor border=1><tr><td align=center width=30 bgcolor=$forumcolorone><a href=topic.cgi?forum=$in_forum&topic=$topicid target=_blank>$topicicon</a></td>
<td width=* class=dp bgColor=$forumcolortwo onmouseover="this.bgColor='$forumcolorone';" onmouseout="this.bgColor='$forumcolortwo';">&nbsp;<a href=view.cgi?forum=$in_forum&topic=$topicid target=_blank>$posticon</a>&nbsp;<span id=forum>$topictitle$pagestoshow$topicdescription$admini</span></td>
<td align=center width=78 bgcolor=$forumcolorone>$startedby</td>$outputtemp<td width=193 bgcolor=$forumcolorone>&nbsp;$lastpostdate<font color=$fonthighlight> | </font>$lastposter</td></tr></table>
	    ~;
        $pagestoshow = undef;
        $threadpages = undef;
        $topiccount++;
    }
    $output .= qq~
        </tr></table></td>
        </tr></table><SCRIPT>valignend()</SCRIPT></span>
        <table cellpadding=0 cellspacing=2 width=$tablewidth align=center>
	<tr height=4></tr>
        <tr>
        <td>$topicpages</td>
                   </tr></table>
            </tr>
            </table>
	    <br>
        ~;
}

sub UpdateNo {
    #R2
    my ($tid, $fid, $act) = @_;
    my ($no, $mn);
    my (@member_list, @topic_list);
    if (ref($tid) eq "ARRAY") {
        @topic_list = @{$tid};
    }
    else {
        @topic_list = ();
        $topic_list[0] = $tid;
    }

    foreach $tid (@topic_list) {
        my $file = "$lbdir" . "forum$fid/$tid.pl";
        open(ENT, $file);
        my $in = <ENT>;
        close(ENT);
        my ($no, $topictitle, $no, $no, $no, $no, $mn, $no, $no, $no, $no) = split(/\t/, $in);
        my $nametocheck = $mn;
        $nametocheck =~ s/ /\_/g;
        $nametocheck =~ tr/A-Z/a-z/;
        push(@member_list, $nametocheck);
        &sendtoposter("$in_member_name", "$mn", "", "jinghua", "$fid", "$tid", "$topictitle", "") if (($sendmanageinfo eq "yes") && (lc($in_member_name) ne lc($mn)) && ($act eq "+"));
    }
    if ($act eq "+") {
        foreach $mn (@member_list) {
            &getmember("$mn", "no");
            next if ($userregistered eq "no");
            $jhcount = 0 if ($jhcount eq "");
            $jhcount = int($jhcount);
            $jhcount = $jhcount + 1;
            &upmember($mn, $jhcount);
        }
    }
    else {
        foreach $mn (@member_list) {
            &getmember("$mn", "no");
            next if ($userregistered eq "no");
            $jhcount = 0 if ($jhcount eq "");
            $jhcount = int($jhcount);
            $jhcount = $jhcount - 1;
            &upmember($mn, $jhcount);
        }
    }
}

sub upmember {
    my ($nametocheck, $jhcount) = @_; # 用户名、精华数

    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    unlink("${lbdir}cache/meminfo/$nametocheck.pl");
    unlink("${lbdir}cache/myinfo/$nametocheck.pl");

    if (($nametocheck ne "") && ($jhcount ne "")) {
        my $namenumber = &getnamenumber($nametocheck);
        &checkmemfile($nametocheck, $namenumber);
        my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";
        if ((-e $filetoopen) && ($nametocheck !~ /^客人/)) {
            &winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
            if (open(FILE, ">$filetoopen")) {
                print FILE "$membername\t$password\t$membertitle\t$member_code\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
                close(FILE);
            }
            &winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
        }
    }
}
