#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
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
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "search.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

for ('TYPE_OF_SEARCH', 'NAME_SEARCH', 'POST_SEARCH', 'FORUMS_TO_SEARCH', 'action', 'forum', 'SEARCH_STRING',
    'REFINE_SEARCH', 'CUR_TIME', 'nextforum', 'start', 'JH_SEARCH', 'CAT_TO_SEARCH', 'SEARCH_DAY', 'SEARCH_TIME') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    $tp =~ s/[\a\b\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    ${$_} = $tp;
}

&error("打开文件&老大，别乱黑我的程序呀！") if (($forum) && ($forum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

&error("打开文件&老大，别乱黑我的程序呀！") if (($CUR_TIME) && ($CUR_TIME !~ /^[0-9]+$/));
$SEARCH_STRING =~ s/^system //g;
$SEARCH_STRING = &stripMETA($SEARCH_STRING);

$ipaddress = $ENV{'REMOTE_ADDR'};
if (!$in_member_name) {$in_member_name = $query->cookie("amembernamecookie");}
if (!$in_password) {$in_password = $query->cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ((!$in_member_name) or ($in_member_name eq "客人")) {
    $in_member_name = "客人";
    $file_name = "客人$ipaddress";
    $file_name =~ s/\.//g;
}
else {
    &getmember("$in_member_name", "no");
    if ($in_password ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
    if ($userregistered eq "no") {&error("论坛搜索&你还没注册呢！");}
    $file_name = $in_member_name;
}
$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

opendir(DIRS, "$lbdir");
my @files = readdir(DIRS);
closedir(DIRS);
@files = grep (/^\w+?$/i, @files);
my @searchdir = grep (/^search/i, @files);
$searchdir = $searchdir[0];

if ($searchopen eq "99") {&error("搜索&搜索功能已经被关闭！");}

if (($searchopen ne "") && ($searchopen ne "0")) {
    if (($member_code ne "ad") && ($member_code ne "smo") && ($member_code ne "cmo") && ($member_code ne "mo") && ($member_code ne "amo")) {
        if (($member_code eq "masked") || ($member_code eq "banned")) {&error("搜索&搜索功能只允许普通会员使用");}
        if (($searchopen eq 1) && ($in_member_name eq "客人")) {&error("搜索&搜索功能只允许注册会员使用，请注册！");}
        if ($searchopen eq 2) {if ($member_code !~ /^rz/) {&error("搜索&搜索功能只允许认证会员或以上级别使用！");}}
        if ($searchopen eq 3) {&error("搜索&搜索功能只允许版主或以上级别使用！");}
    }
    if (($searchopen eq 4) && ($member_code ne "ad")) {&error("搜索&搜索功能目前只允许坛主使用！");}
}

$file_name =~ y/ /_/;
$file_name =~ tr/A-Z/a-z/;
$savefilename = "$lbdir" . "$searchdir/$file_name\_sav.cgi";
$searchfilename = "$lbdir" . "$searchdir/$file_name\_sch.cgi";

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

&mischeader("贴子搜索");

$output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=8 cellspacing=1 width=100%>
~;

if ($action eq "") {
    &ipbanned; #封杀一些 ip
    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$in_member_name\t搜索\tboth\t搜索符合要求的贴子\t");
    }
    opendir(DIR, "${lbdir}$searchdir");
    my @dirdata = readdir(DIR);
    closedir(DIR);
    @dirdata = grep (/\_sch.cgi$/, @dirdata);
    foreach (@dirdata) {
        if ((stat("${lbdir}$searchdir/$_"))[9] < (time - 30 * 60)) {
            unlink("${lbdir}$searchdir/$_");
        }
    }
}

if ($action eq "saveresults") {
    if ($in_member_name eq "客人") {&error("保存搜索结果&客人不能保存搜索结果！");}
    $file_name = $in_member_name;
    $file_name =~ y/ /_/;
    $file_name =~ tr/A-Z/a-z/;
    copy("${lbdir}$searchdir/$file_name\_sch.cgi", "${lbdir}$searchdir/$file_name\_sav.cgi");
    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>搜索结果保存成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>具体情况：
<ul><li><a href="$boardurl/$thisprog?action=display">返回当前搜索结果</a>
<li><a href="forums.cgi?forum=$in_forum">返回论坛</a>
<li><a href="leobbs.cgi">返回论坛首页</a>
</ul></td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=display">
~;
    &output("$board_name - 贴子搜索", \$output);
}
elsif ($action eq "loadresults") {
    if ($in_member_name eq "客人") {&error("调入搜索结果&客人无法调入搜索结果！");}
    $file_name = $in_member_name;
    $file_name =~ y/ /_/;
    $file_name =~ tr/A-Z/a-z/;
    $savefilename = "${lbdir}$searchdir/$file_name\_sav.cgi";
    open(READ, "$savefilename") or &error("调入搜索结果&你还没有保存过搜索结果！");
    copy("${lbdir}$searchdir/$file_name\_sav.cgi", "${lbdir}$searchdir/$file_name\_sch.cgi") if (!-e "${lbdir}$searchdir/$file_name_sch.cgi");
    $output .= qq~<meta http-equiv="refresh" content="0; url=$thisprog?action=display">~;
}
elsif ($action eq "startsearch") {
    $SEARCH_STRING =~ s/\, /\,/g;
    if ($CAT_TO_SEARCH eq "all") {
        @FORUMS_TO_SEARCH = ("all");
    }
    elsif ($CAT_TO_SEARCH =~ /^cat[0-9]+$/) {
        $filetoopen = "$lbdir" . "data/allforums.cgi";
        #    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        open(FILE, "$filetoopen");
        #    flock(FILE, 1) if ($OS_USED eq "Unix");
        @forums = <FILE>;
        close(FILE);
        #    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        @FORUMS_TO_SEARCH = ();
        $CAT_TO_SEARCH =~ s/^cat//;
        foreach (@forums) {
            chomp $_;
            @getforum = split(/\t/, $_);
            push(@FORUMS_TO_SEARCH, $getforum[0]) if ($getforum[2] eq $CAT_TO_SEARCH);
        }
    }
    else {
        @FORUMS_TO_SEARCH = $query->param("FORUMS_TO_SEARCH");
        $FORUMS_TO_SEARCH = @FORUMS_TO_SEARCH;
        &error("搜索&请至少选择一个要搜索的论坛！") if ($FORUMS_TO_SEARCH <= 0);
    }
    &error("搜索&请至少输入一个关键字！") if ($SEARCH_STRING eq "");
    if ($TYPE_OF_SEARCH eq "username_search") {
        $REFINE_SEARCH = "$NAME_SEARCH";
    }
    else {
        $REFINE_SEARCH = "$POST_SEARCH";
    }
    $SEARCH_DAY = ($SEARCH_DAY != 1 && $SEARCH_DAY != 7 && $SEARCH_DAY != 14 && $SEARCH_DAY != 30 && $SEARCH_DAY != 60 && $SEARCH_DAY != 90 && $SEARCH_DAY != 180 && $SEARCH_DAY != 365) ? "any" : $SEARCH_DAY;
    $SEARCH_TIME = ($SEARCH_TIME eq "b") ? "b" : "f";

    $CUR_TIME =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $SEARCH_STRING =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $TYPE_OF_SEARCH =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $SEARCH_DAY =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $SEARCH_TIME =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $REFINE_SEARCH =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $JH_SEARCH =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    foreach (@FORUMS_TO_SEARCH) {
        $_ =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\?]//isg;
    }

    open(SEARCH, ">$searchfilename");
    print SEARCH "$CUR_TIME\n";
    print SEARCH "$SEARCH_STRING\n";
    print SEARCH "$TYPE_OF_SEARCH,$SEARCH_DAY,$SEARCH_TIME\n";
    print SEARCH "$REFINE_SEARCH\n";
    print SEARCH "@FORUMS_TO_SEARCH,$JH_SEARCH\n";
    close(SEARCH);

    $relocurl = "$thisprog?action=continue";

    $output .= qq~<tr>
<td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>搜索中....</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
请等待程序完成搜索。<br>
<b>当前搜索情况：</b>
<ul>
<li>搜索情况....
</ul>
</tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$relocurl">
~;
}
elsif ($action eq "display") {
    &displayresults;
}
elsif ($action eq "continue") {
    open(INSEARCH, "$searchfilename");
    @searchparam = <INSEARCH>;
    close(INSEARCH);

    my $SEARCH_STRING = $searchparam[1];
    chomp $SEARCH_STRING;
    (my $TYPE_OF_SEARCH, my $DAY_TO_SEARCH, my $TIME_TO_SEARCH) = split(/\,/, $searchparam[2]);
    chomp($TYPE_OF_SEARCH, $DAY_TO_SEARCH, $TIME_TO_SEARCH);
    my $REFINE_SEARCH = $searchparam[3];
    chomp $REFINE_SEARCH;
    chomp $searchparam[4];
    (my $FORUMS_TO_SEARCH, my $JH_SEARCH) = split(/\,/, $searchparam[4]);
    @FORUMS_TO_SEARCH = split(/\s/, $FORUMS_TO_SEARCH);

    @KEYWORDS = split(/\,/, $SEARCH_STRING);

    $filetoopen = "$lbdir" . "data/allforums.cgi";
    #    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(FILE, "$filetoopen");
    #    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
    #    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

    @checkforums = @forums;
    @checkforums = reverse(@checkforums);

    $search_in_forum = $FORUMS_TO_SEARCH;

    if ($FORUMS_TO_SEARCH eq "all") {
        @search_in_forum = split(/\t/, $forums[$nextforum]);
        $search_in_forum = $search_in_forum[0];
        $checkforums = @forums;
        $nextforum++;
        if ($nextforum >= $checkforums) {$FORUMS_TO_SEARCH = "done";}
    }
    elsif ($FORUMS_TO_SEARCH =~ m/\s/isg) {
        $search_in_forum = $FORUMS_TO_SEARCH[$nextforum];
        @checkforums = @FORUMS_TO_SEARCH;
        @checkforums = reverse(@checkforums);
        $checkforums = @checkforums;
        $nextforum++;
        if ($nextforum >= $checkforums) {$FORUMS_TO_SEARCH = "done";}
    }
    else {
        $search_in_forum = $FORUMS_TO_SEARCH;
        $FORUMS_TO_SEARCH = "done";
    }
    my $filetoopen = "${lbdir}forum$search_in_forum/foruminfo.cgi";
    if (-e $filetoopen) {
        &getoneforum($search_in_forum);
        $nofile = "true" if (($privateforum eq "yes") && ($allowed_entry{$search_in_forum} ne "yes") && ($member_code ne "ad") && ($member_code ne 'smo'));
    }
    else {
        $nofile = "true";
    }

    open(FILE, "${lbdir}boarddata/listall$search_in_forum.cgi") or $nofile = "true";
    @topics = <FILE>;
    close(FILE);

    if ($nofile ne "true") {
        #start nofile
        foreach $topic (@topics) {
        # start topic foreach
            chomp $topic;
            ($topicid, $topictitle, $startedby, $startedpostdate) = split(/\t/, $topic);
            $topictitle =~ s/^＊＃！＆＊//;
            if ($DAY_TO_SEARCH ne "any") {
                if ($TIME_TO_SEARCH eq "b") {
                    next if (time - $startedpostdate < (86400 * $DAY_TO_SEARCH));
                }
                elsif ($TIME_TO_SEARCH eq "f") {
                    next if (time - $startedpostdate > (86400 * $DAY_TO_SEARCH));
                }
            }

            if ($TYPE_OF_SEARCH eq "keyword_search") {
                if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "topictitle_search") {
                    foreach (@KEYWORDS) {
                        if (($topictitle =~ m|$_|gi) and ("$lida" ne "$topicid")) {
                            $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$startedpostdate\t找到关键字： <B>$_</B>");
                            push(@founditems, $founditem);
                            $lida = $topicid;
                        }
                    }
                }

                if (($REFINE_SEARCH eq "both_search") or ($REFINE_SEARCH eq "post_search")) {
                    $filetoopen = "$lbdir" . "forum$forumid/$topicid.thd.cgi";
                    open(THREAD, "$filetoopen") or next;
                    @thddata = <THREAD>;
                    close(THREAD);

                    foreach (@thddata) {
                        ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon, $topicvalue, $water) = split(/\t/, $_);
                        foreach (@KEYWORDS) {
                            if (($post =~ m|$_|gi) and ("$lida" ne "$topicid")) {
                                $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$postdate\t找到 <B>$_</B> 处");
                                push(@founditems, $founditem);
                                $lida = $topicid;
                            }
                        }
                    }
                }
            } # END MAIN IF 'keyword_search'
            elsif ($TYPE_OF_SEARCH eq "username_search") {
                if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "topictitle_search") {
                    foreach (@KEYWORDS) {
                        if (($startedby =~ m|$_|gi) and ("$lidc" ne "$topicid")) {
                            $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$startedpostdate\t主题作者： <B>$_</B>");
                            push(@founditems, $founditem);
                            $lidc = $topicid;
                        }
                    }
                }

                if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "post_search") {
                    $filetoopen = "$lbdir" . "forum$forumid/$topicid.thd.cgi";
                    open(THREAD, "$filetoopen") or next;
                    @thddata = <THREAD>;
                    close(THREAD);
                    $toptttt = 0;
                    foreach (@thddata) {
                        $toptttt++;
                        next if ($toptttt == 1);
                        ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon, $topicvalue, $water) = split(/\t/, $_);
                        foreach (@KEYWORDS) {
                            if (($membername =~ m|$_|gi) and ($lidc != $topicid)) {
                                # s 'if' n1
                                $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$postdate\t回复人： <B>$membername</B>");
                                push(@founditems, $founditem);
                                $lidc = $topicid;
                            }
                        }
                        $toptttt++;
                    }
                }
            } # END MAIN ELSIF 'username_search'
        }     # end main foreach list loop

        # What do we do next? First push all the data to the text file

        $matches_in_forum = @founditems;
        $matches_so_far = @searchparam - 5;

        open(OUT, ">>$searchfilename");
        foreach (@founditems) {
            chomp $_;
            print OUT "$_\n";
        }
        close(OUT);
        undef @founditems;
        undef @KEYWORDS;
    } # end if no file

    if ($FORUMS_TO_SEARCH ne "done") {
        $relocurl = "$thisprog?action=continue&nextforum=$nextforum";
    }
    else {
        $relocurl = "$thisprog?action=display";
    }

    if (!$matches_in_forum) {$matches_in_forum = "处理中...";}
    else {$matches_in_forums = " 次" if ($matches_in_forum);}

    $matches_so_far = "处理中..." if (!$matches_so_far);
    $forumname = "处理中..." if (!$forumname);

    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>搜索中....</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
请等待，程序正在搜索中。<br><b>当前搜索情况：</b>
<ul><li>详细情况....<BR>
<li>搜索论坛： <b>$forumname</b>
<li>搜索结果： <b>$matches_so_far</b>
<li>匹配符合： <b>$matches_in_forum</b>$matches_in_forums
</ul><center><a href=$thisprog?action=display><b>>> 停 止 搜 索 <<</b></a></center>
</tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$relocurl">
~;
}
else {
    $filetoopen = "$lbdir" . "data/allforums.cgi";
    #    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(FILE, "$filetoopen");
    #    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
    #    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    $a = 0;
    foreach $forum (@forums) {
        #start foreach @forums
        $a = sprintf("%09d", $a);
        chomp $forum;
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forum_pass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $forum);
        next if (($forumid !~ /^[0-9]+$/) || ($categoryplace !~ /^[0-9]+$/));
        $categoryplace = sprintf("%09d", $categoryplace);
        if ((($privateforum eq "yes") && ($userregistered ne "no") && ($allowed_entry{$forumid} eq "yes")) || ($member_code eq "ad") || ($member_code eq 'smo')) {
            $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$miscad2\t$misc\t$forum_pass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
        }
        elsif ($privateforum ne "yes") {
            $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$miscad2\t$misc\t$forum_pass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
        }
        push(@rearrangedforums, $rearrange);
        $a++;
    } # end foreach (@forums)
    @rearrangedforums = sort (@rearrangedforums);
    $count = 1;
    foreach (@rearrangedforums) {
        chomp $_;
        (my $categoryplace, my $a, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $miscad2, my $misc, my $forum_pass, my $hiddenforum, my $indexforum, my $teamlogo, my $teamurl, my $fgwidth, my $fgheight, my $miscad4, my $todayforumpost, my $miscad5) = split(/\t/, $_);
        $categoryplace = sprintf("%01d", $categoryplace);
        $child = ($category =~ /^childforum-[0-9]+/) ? "　|" : "";
        if ($hiddenforum eq "yes") {$hidden = "(隐含)";}
        else {$hidden = "";}
        if ($categoryplace ne $lastcategoryplace) {
            $jumphtml .= "<option value=\"\" style=background-color:$titlecolor>╋$category\n</option>";
            $jumphtml2 .= qq(<input type="radio" name="CAT_TO_SEARCH" value="cat$categoryplace">$category<BR>);
            $jumphtml .= "<option value=\"$forumid\">$child　|- $forumname$hidden\n</option>" if ($hidden eq "" || $member_code eq "ad");
        }
        else {
            $jumphtml .= "<option value=\"$forumid\">$child　|- $forumname$hidden\n</option>" if ($hidden eq "" || $member_code eq "ad");
        }
        $lastcategoryplace = $categoryplace;
    }
    if ($forum) {$jumphtml =~ s/\ value="$forum"/\ value="$forum" selected/isg;}

    $currenttime = time;
    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align="center">
<p><FORM action="$thisprog" method="post" name="Search">
<input type=hidden name="action" value="startsearch">
<input type=hidden name="CUR_TIME" value="$currenttime">
<input type=hidden name="JH_SEARCH" value="no">
<font face="$font" color=$fontcolormisc>$ssboom<b>请输入要搜索的关键字</b></font></td></tr>
<tr><td bgcolor=$miscbackone width colspan=2 align="center" valign="middle"><font face="$font" color=$fontcolormisc>
(多个关键字之间使用逗号 ',' 分隔，关键字中不要使用 # \$ < > ( ) { } & ; | * ? 这些特殊符号)</font><br><br>
<input type=text size=40 name="SEARCH_STRING"></td></tr>
<tr><td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc><b>搜索选项</b></font></td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<b>作者搜索</b></font>&nbsp;<input name="TYPE_OF_SEARCH" type="radio" class=1 value="username_search"></td>
<td bgcolor="$miscbackone" align="left" valign="middle">
<select name="NAME_SEARCH">
<option value="topictitle_search">搜索主题作者
~;
    $output .= qq~
<option value="post_search">搜索回复作者
<option value="both_search">两者都搜索
~ if ($searchall ne "no" || $member_code eq "ad");
    $output .= qq~
</select>
</td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<b>关键字搜索</b></font>&nbsp;<input name="TYPE_OF_SEARCH" type="radio" class=1 value="keyword_search" checked></td>
<td bgcolor="$miscbackone" align="left" valign="middle">
<select name="POST_SEARCH">
<option value="topictitle_search">在主题中搜索关键字
~;
    $output .= qq~
<option value="post_search">在贴子内容中搜索关键字
<option value="both_search">在主题和贴子内容中搜索关键字
~ if ($searchall ne "no" || $member_code eq "ad");
    $output .= qq~
</select>
</td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<b>搜寻日期</b></font></td>
<td bgcolor="$miscbackone" align="left" valign="middle">自
<select name="SEARCH_DAY"><option value="any" selected>任何日期<option value="1">  1 天<option value ="7"> 1 周<option value = "14"> 2 周<option value="30"> 1 个月<option value="90"> 3 个月<option value="180"> 6 个月<option value="365"> 1 年</select>
<select name="SEARCH_TIME"><option value="b" selected>之前<option value="f">之后</select>
</td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<b>请选择要搜索的论坛或分类</b></font></td>
<td bgcolor="$miscbackone" align="left" valign="middle">
<input type="radio" name="CAT_TO_SEARCH" value="all"$Seleced[0]>所有论坛<BR>$jumphtml2
</td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<input type="radio" name="CAT_TO_SEARCH" value="select"$Seleced[1] checked><b>自选论坛</b><br>按 Ctrl 键多选,分类无效</font></td>
<td bgcolor="$miscbackone" align="left" valign="middle">
<select name="FORUMS_TO_SEARCH" size="6" width=100% multiple>$jumphtml</select>
</td></tr>
<tr>
<td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center><BR>
<input type=submit value="开始搜索">　　<input value="调入搜索结果" type=button onclick="javascript:location.href='$boardurl/$thisprog?action=loadresults'">
</td></form></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
}

&output("$board_name - 贴子搜索", \$output);
exit;

sub displayresults {
    open(READ, "$searchfilename") or &error("搜索结果&对不起，搜索结果只能保存 30 分钟，请重新搜索！");
    @completed_search = <READ>;
    close(READ);

    foreach (@completed_search) {
        push(@TRUE_RESULTS, $_) if ($_ =~ /\t/)
    }

    $total_results = @TRUE_RESULTS;

    $SEARCH_STRING = $completed_search[1];
    chomp $SEARCH_STRING;
    ($TYPE_OF_SEARCH, $DAY_TO_SEARCH, $TIME_TO_SEARCH) = split(/\,/, $completed_search[2]);
    chomp($TYPE_OF_SEARCH, $DAY_TO_SEARCH, $TIME_TO_SEARCH);
    $REFINE_SEARCH = $completed_search[3];
    chomp $REFINE_SEARCH;
    chomp $completed_search[4];
    ($FORUMS_TO_SEARCH, $JH_SEARCH) = split(/\,/, $completed_search[4]);

    $TYPE_OF_SEARCH = "关键字" if ($TYPE_OF_SEARCH eq "keyword_search");
    $TYPE_OF_SEARCH = "作者" if ($TYPE_OF_SEARCH eq "username_search");

    $REFINE_SEARCH = "主题" if ($REFINE_SEARCH eq "topictitle_search");
    $REFINE_SEARCH = "贴子内容" if ($REFINE_SEARCH eq "post_search");
    $REFINE_SEARCH = "主题和回复" if ($REFINE_SEARCH eq "both_search");

    $TYPE_SEARCH = "所有帖子" if ($JH_SEARCH eq "no");
    $TYPE_SEARCH = "精华帖子" if ($JH_SEARCH eq "jinghua");
    $TYPE_SEARCH = "回收帖子" if ($JH_SEARCH eq "recycle");
    $TYPE_SEARCH = "投票帖子" if ($JH_SEARCH eq "poll");
    $TYPE_SEARCH = "锁定帖子" if ($JH_SEARCH eq "lock");
    $TYPE_SEARCH = "热门帖子" if ($JH_SEARCH eq "hot");
    $TYPE_SEARCH = "置顶帖子" if ($JH_SEARCH eq "top");

    if ($total_results > 0) {
        $result_line = qq(使用<b>$TYPE_OF_SEARCH</b>搜索方式，在<b>$REFINE_SEARCH</b>中搜索到 <b>$total_results</b> 个相匹配的贴子);
    }
    else {
        $result_line = qq(对不起，使用<b>$TYPE_OF_SEARCH</b>搜索方式，在<b>$REFINE_SEARCH</b>中<b>没有</b>搜索到任何相匹配的贴子);
    }

    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=3 align=center>
<font face="$font" color=$fontcolormisc>$result_line</font>
</td></tr>
<tr><td bgcolor=$miscbackone valign=middle align=center>
<font face="$font" color=$fontcolormisc><b>主题</b></font></td>
<td bgcolor=$miscbackone valign=middle align=center>
<font face="$font" color=$fontcolormisc><b>发表时间、位置</b></font></td>
<td bgcolor=$miscbackone valign=middle align=center>
<font face="$font" color=$fontcolormisc><b>关键字匹配说明</b></font></font>
</td></tr>
~;

    $maxthreads = 25;
    $numberofitems = $total_results;
    $numberofpages = $numberofitems / $maxthreads;
    $instart = $start;

    if ($numberofitems > $maxthreads) {
        $showmore = "yes";
        if ($instart eq "" || $instart < 0) {$instart = 0;}
        if ($instart > 0) {$startarray = $instart;}
        else {$startarray = 0;}
        $endarray = $instart + $maxthreads - 1;
        if ($endarray < ($numberofitems - 1)) {$more = "yes";}
        if (($endarray > ($maxthreads - 1)) && ($more ne "yes")) {$endarray = $numberofitems - 1;}
    }
    else {
        $showmore = "no";
        $startarray = 0;
        $pages = qq~<font face="$font" color=$menufontcolor>搜索结果只有一页</font>~;
        $endarray = $numberofitems - 1;
    }

    if ($showmore eq "yes") {
        #1
        if ($maxthreads < $numberofitems) {
        #2
            ($integer, $decimal) = split(/\./, $numberofpages);
            if ($decimal > 0) {$numberofpages = $integer + 1;}
            $pagestart = 0;
            $counter = 0;
            while ($numberofpages > $counter) {
                #3
                $counter++;
                if ($instart ne $pagestart) {$pages .= qq~<a href="$thisprog?action=display&start=$pagestart"><font face="$font" color=$menufontcolor><b>$counter</b></font></a> ~;}
                else {$pages .= qq~<font face="$font" color=$fonthighlight><b>$counter</b></font> ~;}
                $pagestart = $pagestart + $maxthreads;
            } #e3
        }     #e2
        $pages = qq~<font face="$font" color=$menufontcolor><b>搜索结果含有多页</b> [ $pages ]~;
    } #1

    $timeadd = $timedifferencevalue * 3600 + $timezone * 3600;
    foreach (@TRUE_RESULTS[$startarray .. $endarray]) {
        # start foreach loop
        ($forumid, $topicid, $topictitle, $topicdescription, $forumname, $postdate, $string_returned) = split(/\t/, $_);
        $topictitle =~ s/^＊＃！＆＊//;
        $postdate = $postdate + $timeadd;
        $longdate = &longdate("$postdate");
        $topicdescription = qq(&nbsp;-=> $topicdescription) if $topicdescription;

        $in_forum = $forumid;
        if (($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {
            $admini = qq~<DIV ALIGN=Right><font color=$titlecolor>|<a href=jinghua.cgi?action=add&forum=$in_forum&topic=$topicid><font color=$titlecolor>精</font></a>|<a href=postings.cgi?action=locktop&forum=$in_forum&topic=$topicid><font color=$titlecolor>固</font></a>|<a href=postings.cgi?action=puttop&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>提</font></a>|<a href=postings.cgi?action=lock&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>锁</font></a>|<a href=postings.cgi?action=unlock&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|<a href=delpost.cgi?action=delete&forum=$in_forum&topic=$topicid><font color=$titlecolor>删</font></a>|<a href=delpost.cgi?action=movetopic&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>移</font></a>|</font>&nbsp;</DIV>~;
        }
        elsif ((lc($in_member_name) eq lc($startedby)) && ($in_password eq $password) && ($in_member_name !~ /^客人/)) {
            if ($arrowuserdel eq "on") {
                $admini = qq~<DIV ALIGN=Right><font color=$titlecolor>| <a href=postings.cgi?action=lock&forum=$in_forum&topic=$topicid><font color=$titlecolor>锁定此贴，不允许别人回复</font></a> | <a href=delpost.cgi?action=delete&forum=$in_forum&topic=$topicid><font color=$titlecolor>删除此贴</font></a> |</font>&nbsp;&nbsp;</DIV>~;
            }
            else {undef $admini;}
        }
        else {undef $admini;}

        $output .= qq(<tr><td bgcolor=$miscbackone valign=middle>
<font face="$font" color=$fontcolormisc><B><a href="topic.cgi?forum=$forumid&topic=$topicid" target=_blank>$topictitle</a></B><br>
$topicdescription$admini</td>
<td bgcolor=$miscbackone valign=middle>
<font face="$font" color=$fontcolormisc>所处论坛： <a href="forums.cgi?forum=$forumid">$forumname</a><BR>发表时间： $longdate</font></td>
<td bgcolor=$miscbackone valign=middle align=center>
<font face="$font" color=$fontcolormisc>$string_returned</font></td></tr>
);
        undef $topicdescription;
    } # end foreach

    $output .= qq(<tr><td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center>
<font face="$font" color=$fontcolormisc>$pages</font></td>
<td bgcolor="$miscbacktwo" valign=middle colspan=1 align=center>
<font face="$font" color=$fontcolormisc>
<img src=$imagesurl/images/icon.gif align=absmiddle border=0> <a href="$thisprog"><b>再次搜索 </b></a>
</font><br><font face="$font" color=$fontcolormisc>
<img src=$imagesurl/images/saveas.gif align=absmiddle> <a href="$thisprog?action=saveresults"><b>保存搜索结果 </b></a>
</font></td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
);
    &output("$board_name - 搜索结果", \$output);

}
exit;
