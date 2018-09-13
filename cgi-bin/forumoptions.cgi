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
require "bbs.lib.pl";
require "rebuildlist.pl";
require "recooper.pl";
require "dopost.pl";

$|++;
$thisprog = "forumoptions.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$checked = $query->param('checked');
$in_forum = $query->param('forum');
$in_topic = $query->param('topic');
$action = $query->param('action');
$admin = $query->param('admin');
$prunedays = $query->param('prunedays');
$in_member_name = $query->param('membername');
$in_password = $query->param('password');
$inaddline = $query->param('addline');
if ($in_password ne "") {
    eval {$in_password = md5_hex($in_password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
    unless ($@) {$in_password = "lEO$in_password";}
}

$movetoid = $query->param('movetoid');
$action = &stripMETA("$action");

&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic) && ($in_topic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($movetoid) && ($movetoid !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}
$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
if (($in_forum !~ m|([0-9\G]+$)|g) or (!$in_forum)) {&error("普通错误&请不要修改生成的 URL！");}
if (($prunedays) && ($prunedays !~ /^[0-9]+$/)) {&error("普通错误&请不要修改生成的 URL！");}
if (!$in_member_name) {$in_member_name = $query->cookie("amembernamecookie");}
if (!$in_password) {$in_password = $query->cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ((!$in_member_name) or ($in_member_name eq "客人")) {$in_member_name = "客人";}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    if ($in_password ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
}

&getoneforum("$in_forum");

if ($action eq "prune") {
    $cleartoedit = "no";
    &mischeader("批量管理");
    if ($in_password eq $password) {
        $pwok = "密码不显示";
    }
    else {
        $pwok = $in_password;
    }
    $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
    my $thistime = time;
    if ($admin eq 'delete') {
        $filetomake = "$lbdir" . "data/baddel.cgi";

        $maxdeloneday = 9 if (($maxdeloneday eq "") || ($maxdeloneday <= 0));
        if ($member_code ne "ad") {
            open(FILE, "$filetomake");
            my @delfile = <FILE>;
            close(FILE);
            my $delcount = 0;
            my $delcou = 0;
            my $totime = time - 86400;
            foreach (@delfile) {
                chomp($_);
                (my $delname, my $no, my $noip, $no, $no, my $notime) = split(/\t/, $_);
                if (lc($delname) eq lc($in_member_name)) {
                    if ($notime > $totime) {
                        $delcount++;
                    }
                }
                if ($noip eq "$ENV{'REMOTE_ADDR'}") {
                    if ($notime > $totime) {
                        $delcou++;
                    }
                }
            }
            if ($delcount > $maxdeloneday) {&error("删除主题&你今天删除帖子太多，请明天继续！");}
            if ($delcou > $maxdeloneday) {&error("删除主题&你今天删除帖子太多，请明天继续！");}
            undef $delcount;
            undef $delcou;
        }
        if (open(FILE, ">>$filetomake")) {
            print FILE "$in_member_name\t$pwok\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t批量删除$forumname $prunedays天前的贴子\t$thistime\t\n";
            close(FILE);
        }
    }
    elsif ($admin eq 'move') {
        $filetomake = "$lbdir" . "data/badmove.cgi";
        $maxmoveoneday = 9 if (($maxmoveoneday eq "") || ($maxmoveoneday <= 0));
        if ($member_code ne "ad") {
            open(FILE, "$filetomake");
            my @movefile = <FILE>;
            close(FILE);
            my $movecount = 0;
            my $movecou = 0;
            my $totime = time - 86400;
            foreach (@movefile) {
                chomp $_;
                (my $movename, my $no, my $noip, $no, $no, my $notime) = split(/\t/, $_);
                if (lc($movename) eq lc($in_member_name)) {
                    if ($notime > $totime) {
                        $movecount++;
                    }
                }
                if ($noip eq "$ENV{'REMOTE_ADDR'}") {
                    if ($notime > $totime) {
                        $movecou++;
                    }
                }
            }
            if ($movecount > $maxmoveoneday) {&error("移动主题&你今天移动帖子太多，请明天继续！");}
            if ($movecou > $maxmoveoneday) {&error("移动主题&你今天移动帖子太多，请明天继续！");}
            undef $movecount;
            undef $movecou;
        }
        if (open(FILE, ">>$filetomake")) {
            print FILE "$in_member_name\t$pwok\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t批量移动$forumname $prunedays天前的帖子\t$thistime\t\n";
            close(FILE);
        }
    }
    undef $thistime;

    if ((($member_code eq "ad") || ($member_code eq 'smo')) && ($in_password eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($member_code ne 'amo') && ($in_password eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("使用批量管理&您不是本论坛坛主、管理员或是您的密码输入错误！");}
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        if ($prunedays < 20) {&error("使用批量管理&指定管理的天数要大于 20 ！");}

        if ($admin eq 'delete') {

            if (-e "${lbdir}boarddata/jinghua$in_forum.cgi") {
                open(FILE, "${lbdir}boarddata/jinghua$in_forum.cgi");
                my @jhdatas = <FILE>;
                close(FILE);
                $jhdata = join("\_", @jhdatas);
                $jhdata = "\_$jhdata\_";
                $jhdata =~ s/\W//isg;
            }

            $dirtoopen = "$lbdir" . "forum$in_forum";
            opendir(DIR, "$dirtoopen");
            my @dirdata = readdir(DIR);
            closedir(DIR);
            @entry = grep (/\.thd\.cgi$/, @dirdata);
            @entry = sort numerically(@entry);

            $dirtoopen2 = "$imagesdir" . "$usrdir/$in_forum";
            opendir(DIR, "$dirtoopen2");
            @dirdata1 = readdir(DIR);
            closedir(DIR);
            @dirdata1 = grep (/^$in_forum\_/i, @dirdata1);

            opendir(DIRS, "${lbdir}$saledir");
            @files2 = readdir(DIRS);
            closedir(DIRS);
            @files2 = grep (/^$in_forum\_/i, @files2);

            foreach (@entry) {
                (my $topicid, my $tr) = split(/\./, $_);
                next if ($jhdata =~ /\_$topicid\_/);

                $file1 = "$lbdir" . "forum$in_forum/$topicid.thd.cgi";
                open(TMP1, "$file1");
                flock(TMP1, 1) if ($OS_USED eq "Unix");
                my @tmp = <TMP1>;
                close(TMP1);
                $postcount = @tmp;
                $postcount--;
                my $tmp1 = $tmp[-1];
                (my $no, my $no, my $no, my $no, my $no, my $lastpostdate, my $no, $no) = split(/\t/, $tmp1);

                $currenttime = time;
                $threadagelimit = $currenttime - $prunedays * 86400;
                if ($lastpostdate < $threadagelimit) {
                    $filetotrash = "$lbdir" . "forum$in_forum/$topicid.thd.cgi";
                    unlink $filetotrash;
                    $filetotrash = "$lbdir" . "forum$in_forum/$topicid.mal.pl";
                    unlink $filetotrash;
                    $filetotrash = "$lbdir" . "forum$in_forum/$topicid.poll.pl";
                    unlink $filetotrash;
                    $filetotrash = "$lbdir" . "forum$in_forum/$topicid.pl";
                    unlink $filetotrash;
                    $filetounlink = "$lbdir" . "forum$in_forum/rate$topicid.file.pl";
                    unlink $filetounlink;
                    $filetounlink = "$lbdir" . "forum$in_forum/rateip$topicid.file.pl";
                    unlink $filetounlink;

                    &delallupfiles($in_forum, $topicid);

                    my @files2 = grep (/^$in_forum\_$topicid\_/i, @files2);
                    foreach (@files2) {
                        chomp $_;
                        unlink("${lbdir}$saledir/$_");
                    }

                    @files = grep (/^$in_forum\_$topicid(\.|\_)/, @dirdata1);
                    foreach (@files) {
                        unlink("$dirtoopen2/$_");
                    }
                    $totaltopics_deleted++;
                    $totalposts_deleted = $totalposts_deleted + $postcount;
                }
            }

            my $info = rebuildLIST(-Forum => "$in_forum");
            ($threadcount, $topiccount) = split(/\|/, $info);
            $threadcount = 0 if ($threadcount < 0);
            $topiccount = 0 if ($topiccount < 0);

            open(FILE, "${lbdir}boarddata/listno$in_forum.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
            my $rr = &readthreadpl($forumid, $topicid);
            (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp, my $addmetemp) = split(/\t/, $rr);

            open(FILE, "+<${lbdir}boarddata/foruminfo$in_forum.cgi");
            ($no, $no, $no, $todayforumpost, $no) = split(/\t/, <FILE>);

            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
            $lastposter = $startedby if ($lastposter eq "");
            seek(FILE, 0, 0);
            print FILE "$lastforumpostdate\t$threadcount\t$topiccount\t$todayforumpost\t$lastposter\t\n";
            close(FILE);
            $posts = 0 if ($posts eq "");
            $threads = 0 if ($threads eq "");
            open(FILE, ">${lbdir}boarddata/forumposts$in_forum.pl");
            print FILE "\$threads = $threadcount;\n\$posts = $topiccount;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

            require "$lbdir" . "data/boardstats.cgi";
            $filetomake = "$lbdir" . "data/boardstats.cgi";
            $totalthreads = $totalthreads - $totaltopics_deleted;
            $totalposts = $totalposts - $totalposts_deleted;
            &winlock($filetomake) if ($OS_USED eq "Nt");
            if (open(FILE, ">$filetomake")) {
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE "\$lastregisteredmember = \"$lastregisteredmember\"\;\n";
                print FILE "\$totalmembers = \"$totalmembers\"\;\n";
                print FILE "\$totalthreads = \"$totalthreads\"\;\n";
                print FILE "\$totalposts = \"$totalposts\"\;\n";
                print FILE "\n1\;";
                close(FILE);
            }
            &winunlock($filetomake) if ($OS_USED eq "Nt");
            if (!$totaltopics_deleted) {$totaltopics_deleted = "0";}
            if (!$totalposts_deleted) {$totalposts_deleted = "0";}
            &addadminlog("批量删除 $prunedays 天以前的主题共 $totaltopics_deleted 篇");
            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>论坛文章已经被删除</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
            统计资料：
            <ul>
            <li>共删除主题：$totaltopics_deleted 篇
            <li>共删除回复：$totalposts_deleted 篇
            <li><a href="forums.cgi?forum=$in_forum">返回论坛$savetopicid</a>
            <li><a href="leobbs.cgi">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
	    ~;
        }
        else {
            if ($movetoid == $in_forum) {&error("移动主题&不允许在同一论坛上移动！");}

            if (-e "${lbdir}boarddata/jinghua$in_forum.cgi") {
                open(FILE, "${lbdir}boarddata/jinghua$in_forum.cgi");
                my @jhdatas = <FILE>;
                close(FILE);
                $jhdata = join("\_", @jhdatas);
                $jhdata = "\_$jhdata\_";
                $jhdata =~ s/\W//isg;
            }
            $currenttime = time;

            $filetoopen = "$lbdir" . "data/allforums.cgi";
            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            open(FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @forums = <FILE>;
            close(FILE);
            &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            foreach $forumline (@forums) {
                #start foreach @forums
                ($tempno, $trash) = split(/\t/, $forumline);
                if ($in_forum eq $tempno) {
                    ($trash, $trash, $trash, $oldforumname, $trash) = split(/\t/, $forumline);
                    last;
                }
            }

            foreach $forumline (@forums) {
                #start foreach @forums
                ($tempno, $trash) = split(/\t/, $forumline);
                if ($movetoid eq $tempno) {
                    ($trash, $trash, $trash, $newforumname, $trash) = split(/\t/, $forumline);
                    last;
                }
            }
            if ($inaddline eq "yes") {
                $moveinfo = qq~此贴转移自： <a href=forums.cgi?forum=$in_forum target=_self>$oldforumname</a>~;
            }

            $filetoopen = "$lbdir" . "boarddata/lastnum$movetoid.cgi";
            if (-e $filetoopen) {
                open(FILE, "$filetoopen");
                flock(FILE, 1) if ($OS_USED eq "Unix");
                $newthreadnumber = <FILE>;
                close(FILE);
                chomp $newthreadnumber;
                $newthreadnumber++;
            }
            $dirtoopen2 = "$imagesdir" . "$usrdir/$in_forum";
            opendir(DIR, "$dirtoopen2");
            @dirdata2 = readdir(DIR);
            closedir(DIR);
            @files = grep (/^$in_forum\_/, @dirdata2);

            $dirtoopen = "$lbdir" . "forum$in_forum";
            opendir(DIR, "$dirtoopen");
            my @dirdata = readdir(DIR);
            closedir(DIR);
            @entry = grep (/\.thd\.cgi$/, @dirdata);
            foreach (@entry) {
                (my $topicid, my $tr) = split(/\./, $_);

                next if ($jhdata =~ /\_$topicid\_/);

                $file1 = "$lbdir" . "forum$in_forum/$topicid.thd.cgi";
                open(TMP1, "$file1");
                flock(TMP1, 1) if ($OS_USED eq "Unix");
                my @tmp = <TMP1>;
                close(TMP1);
                my $tmp1 = $tmp[-1];
                (my $no, my $no, my $no, my $no, my $no, my $lastpostdate, my $no, $no) = split(/\t/, $tmp1);

                $currenttime = time;
                $threadagelimit = $currenttime - $prunedays * 86400;
                if ($lastpostdate < $threadagelimit) {
                    &MoveTopic("$topicid", $#tmps);
                    $totaltopics_moved++;
                }
            }

            my $truenumber = rebuildLIST(-Forum => "$in_forum");
            ($tpost, $treply) = split(/\|/, $truenumber);

            open(FILE, "${lbdir}boarddata/listno$in_forum.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
            my $rr = &readthreadpl($forumid, $topicid);
            (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split(/\t/, $rr);

            open(FILE, "+<${lbdir}boarddata/foruminfo$in_forum.cgi");
            ($no, $no, $no, $todayforumpost, $no) = split(/\t/, <FILE>);
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
            $lastposter = $startedby if ($lastposter eq "");
            seek(FILE, 0, 0);
            print FILE "$lastforumpostdate\t$tpost\t$treply\t$todayforumpost\t$lastposter\t\n";
            close(FILE);
            $posts = 0 if ($posts eq "");
            $threads = 0 if ($threads eq "");
            open(FILE, ">${lbdir}boarddata/forumposts$in_forum.pl");
            print FILE "\$threads = $tpost;\n\$posts = $treply;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

            my $truenumber = rebuildLIST(-Forum => "$movetoid");
            ($tpost, $treply) = split(/\|/, $truenumber);

            open(FILE, "${lbdir}boarddata/listno$movetoid.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
            my $rr = &readthreadpl($forumid, $topicid);
            (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp, my $addmetemp) = split(/\t/, $rr);

            open(FILE, "+<${lbdir}boarddata/foruminfo$movetoid.cgi");
            ($no, $no, $no, $todayforumpost, $no) = split(/\t/, <FILE>);
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
            $lastposter = $startedby if ($lastposter eq "");
            seek(FILE, 0, 0);
            print FILE "$lastforumpostdate\t$tpost\t$treply\t$todayforumpost\t$lastposter\t\n";
            close(FILE);
            $posts = 0 if ($posts eq "");
            $threads = 0 if ($threads eq "");
            open(FILE, ">${lbdir}boarddata/forumposts$movetoid.pl");
            print FILE "\$threads = $tpost;\n\$posts = $treply;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

            if (!$totaltopics_moved) {$totaltopics_moved = "0";}

            &addadminlog("批量转移 $prunedays 天以前的主题共 $totaltopics_moved 篇到 $newforumname");

            $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>论坛文章已经被移动</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
            统计资料：
            <ul>
            <li>共移动主题：$totaltopics_moved 篇
            <li><a href="forums.cgi?forum=$in_forum">返回原论坛</a>
            <li><a href="forums.cgi?forum=$movetoid">返回新论坛</a>
            <li><a href="leobbs.cgi">返回论坛首页</a>
			</ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
	    ~;
        }

    }
    else {
        &mischeader("批量管理");
        if ((($member_code eq "ad") || ($member_code eq 'smo')) && ($in_password eq $password)) {$cleartoedit = "yes";}
        if (($inmembmod eq "yes") && ($member_code ne "amo") && ($in_password eq $password)) {$cleartoedit = "yes";}
        unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
        if ($cleartoedit eq "no" && $checked eq "yes") {&error("使用批量管理&您不是本论坛坛主、管理员或是您的密码输入错误！");}
        $filetoopen = "$lbdir" . "data/allforums.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @forums = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        $jumphtml .= "<option value=\"\">选择一个论坛\n</option>";
        $a = 0;
        foreach my $forum (@forums) {
            #start foreach @forums
            $a = sprintf("%09d", $a);
            chomp $forum;
            next if (length("$forum") < 30);
            (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription, my $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, $tmp, my $hiddenforum, $tmp, $tmp, $tmp, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $forum);
            next if ($forumid !~ /^[0-9]+$/);
            next if ($categoryplace !~ /^[0-9]+$/);
            $categoryplace = sprintf("%09d", $categoryplace);
            $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$miscad2\t$misc\t$forum_pass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
            push(@rearrangedforums, $rearrange);
            $a++;
        }

        @finalsortedforums = sort (@rearrangedforums);

        foreach my $sortedforums (@finalsortedforums) {
            (my $categoryplace, my $a, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $miscad2, my $misc, my $forum_pass, my $hiddenforum, my $indexforum, my $teamlogo, my $teamurl, my $fgwidth, my $fgheight, my $miscad4, my $todayforumpost, my $miscad5) = split(/\t/, $sortedforums);
            $categoryplace = sprintf("%01d", $categoryplace);
            if ($categoryplace ne $lastcategoryplace) {
                $jumphtml .= "<option value=\"\" style=background-color:$titlecolor>╋$category\n</option>";
            }
            if ($hiddenforum eq "yes") {$hidden = "(隐含)";}
            else {$hidden = "";}
            $child = ($category =~ /^childforum-[0-9]+/) ? "　|" : "";
            $jumphtml .= "<option value=\"$forumid\">$child　|-$forumname$hidden\n</option>" if (($disphideboard eq "yes") || ($hidden eq "") || ($member_code eq "ad") || ($member_code eq "smo") || ($member_code eq "cmo") || ($member_code eq "mo") || ($member_code eq "amo"));
            $lastcategoryplace = $categoryplace;
        }
        $jumphtml .= qq~</select>\n~;

        $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr><td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="prune">
            <input type=hidden name="checked" value="yes">
            <input type=hidden name="forum" value="$in_forum">
            <font face="$font" color=$fontcolormisc><b>请输入您的详细资料以便进入管理模式[批量管理]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$in_member_name</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
	<tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>选择管理的模式</font></td>
            <td bgcolor=$miscbackone valign=middle><input type="radio" name="admin" value="delete">删除 <input type="radio" name="admin" value="move">移动</td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>转移至：</b>(只对批量移动有效)</font></td>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><select name="movetoid">$jumphtml</select><BR><input type="checkbox" name="addline" value="yes" checked>在帖子下显示转移字样</font></td></tr>
            <tr>
            <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc><b>一旦您选择删除文章，将不能够恢复！</b><br>下面将删除发表时间超过一定天数外的所有文章。<br>如果您确定这样做，请仔细检查您输入的信息。</font></td></tr>
			<tr>
            <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>管理多少天以外的文章<br>例如：输入'30'，将管理超过 30 天的所有文章。</font></td>
            <td bgcolor=$miscbackone valign=middle><input type=text name="prunedays"></td></tr>
            <tr>
            <td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name="submit" value="提 交"></td></tr></form></table></td></tr></table>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
	    ~;
    }
}
else {&error("普通错误&未指定功能名！");}
&output("$board_name - 批量管理", \$output);
exit;

sub MoveTopic {
    my ($in_topic, $nums) = shift;
    do {
        $newthreadnumber++;
    } while (-e "${lbdir}forum$movetoid/$newthreadnumber.thd.cgi");

    open(ENT, "${lbdir}forum$in_forum/$in_topic.pl");
    my $in = <ENT>;
    close(ENT);
    chomp($in);
    my ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $lastinposticon, $inposttemp, $addmetemp) = split(/\t/, $in);

    if (open(FILE, ">${lbdir}forum$movetoid/$newthreadnumber.pl")) {
        print FILE "$newthreadnumber\t$topictitle\t$moveinfo\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$lastinposticon\t$inposttemp\t$addmetemp\t";
        close(FILE);
    }

    rename("${lbdir}forum$in_forum/$in_topic.thd.cgi", "${lbdir}forum$movetoid/$newthreadnumber.thd.cgi");
    rename("${lbdir}forum$in_forum/$in_topic.mal.pl", "${lbdir}forum$movetoid/$newthreadnumber.mal.pl") if (-e "${lbdir}forum$in_forum/$in_topic.mal.pl");
    rename("${lbdir}forum$in_forum/$in_topic.poll.cgi", "${lbdir}forum$movetoid/$newthreadnumber.poll.cgi") if (-e "${lbdir}forum$in_forum/$in_topic.poll.cgi");
    rename("${lbdir}forum$in_forum/rate$in_topic.file.pl", "${lbdir}forum$movetoid/rate$newthreadnumber.file.pl") if (-e "${lbdir}forum$in_forum/rate$in_topic.file.pl");
    rename("${lbdir}forum$in_forum/rateip$in_topic.file.pl", "${lbdir}forum$movetoid/rateip$newthreadnumber.file.pl") if (-e "${lbdir}forum$in_forum/rateip$in_topic.file.pl");
    for (0 .. $nums) {rename("${lbdir}forum$in_forum/$in_topic\_$_.sale.cgi", "${lbdir}forum$movetoid/$newthreadnumber\_$_.sale.cgi");}
    unlink("${lbdir}forum$in_forum/$in_topic.pl");
    unlink("${lbdir}FileCount/$in_forum/$in_forum\_$in_topic.pl");

    $OldHackDetail = "${lbdir}FileCount/$in_forum/$in_forum\_$in_topic.cgi";
    $NewHackDetail = "${lbdir}FileCount/$movetoid/$movetoid\_$newthreadnumber.cgi";

    if (-e $OldHackDetail) {
        open(HACK, "$OldHackDetail");
        @AllHackDetail = <HACK>;
        close(HACK);
        open(NHACK, ">$NewHackDetail");
        foreach $HackDetail (@AllHackDetail) {
            chomp $HackDetail;
            ($ThisHackName, $ThisFileName, $ThisHackDT) = split(/\=/, $HackDetail);
            ($hackforumno, $hacktopicno, $hackreplyno) = split(/\_/, $ThisHackName);
            ($file_name, $file_ext) = split(/\./, $ThisFileName);
            ($fileforumno, $filetopicno, $filereplyno) = split(/\_/, $file_name);
            if ($filereplyno) {$ReplyNo = "\_$filereplyno";}
            else {$ReplyNo = "";}
            $NewHackName = "$movetoid\_$newthreadnumber\_$hackreplyno";
            $NewFileName = "$movetoid\_$newthreadnumber$ReplyNo\.$file_ext";
            print NHACK "$NewHackName\=$NewFileName\=$ThisHackDT\n";
        }
        close(NHACK);
        unlink $OldHackDetail;
    }

    &moveallupfiles($in_forum, $in_topic, $movetoid, $movetoid, "yes"); #新的方式

    my @files1 = grep (/^$in_forum\_$in_topic(\.|\_)/, @dirdata1);
    foreach (@files1) {
        chomp;
        my (undef, $ext) = split(/\./, $_);
        rename("${imagesdir}$usrdir/$in_forum/$_", "${imagesdir}$usrdir/$movetoid/$movetoid\_$newthreadnumber.$ext");
    }
}
