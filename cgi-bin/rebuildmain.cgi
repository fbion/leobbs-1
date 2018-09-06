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
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "rebuildmain.cgi";

$query = new LBCGI;

$checkaction   = $query -> param("checkaction");
$checkaction   = &cleaninput("$checkaction");

$inmembername  = $query->cookie("adminname");
$inpassword    = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
&getmember("$inmembername","no");
if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
    if ($checkaction eq "yes") {
        $dirtoopen = "$lbdir";
        opendir (DIR, "$dirtoopen"); 
        @existforum = readdir(DIR);
        closedir (DIR);
        @existforum = grep(/^forum[0-9]+$/,@existforum);
        @existforum = sort @existforum;
        $existforumcount = @existforum;

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        if (-e "$filetoopen") {
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE,"$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @allforums = <FILE>;
            close(FILE);
        }
        else { undef @allforums; }
        undef @allforums1;
        foreach $forum (@allforums) {
            chomp $forum;
	    next if (length("$forum") < 30);
            (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription,my $no, $no, $no, $no, $no, $no, $no, my $threads, my $posts) = split(/\t/,$forum);
            next if ($forumid eq "");
    	    next if ($forumid !~ /^[0-9]+$/);
            next if ($category eq "");
 	    next if ($categoryplace eq "");
    	    next if ($categoryplace !~ /^[0-9]+$/);
            next if ($forumname eq "");
            next if ($forumdescription eq "");
            next if ($threads eq "");
            next if ($posts eq "");
            $dirtoopen = "$lbdir" . "forum$forumid";
 	    next if (!(-e $dirtoopen));
       	    push(@allforums1, $forum);

	    $dirtomake = "$lbdir" . "forum$forumid";
	    $filetomake1 = "$dirtomake/foruminfo.cgi";
	    open(FILE1,">$filetomake1");
            print FILE1 $forum;
            close(FILE1);

 	    undef @existforum1;
            foreach $existforum (@existforum) {
        	next if ($existforum eq "forum$forumid");
        	push(@existforum1, $existforum);
 	    }
 	    @existforum = @existforum1;
        }
        $filetomake = "$lbdir" . "data/allforums.cgi";
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums1) {
            print FILE "$forum\n";
	}
        foreach $existforum (@existforum) {
             $dirtomake = "$lbdir" . "$existforum";
             $filetoopen1 = "$dirtomake/foruminfo.cgi";
             if (-e $filetoopen1){
		open(FILE1,"$filetoopen1");
		$existforuminfo = <FILE1>;
		close(FILE1);
	     	$existforum =~ s/forum//isg;
		chomp $existforuminfo;
		(my $forumid, my $category, my $categoryplace,my $forumname, my $forumdescription, my $forummoderator, my $htmlstate, my $idmbcodestate, my $privateforum, my $startnewthreads, my $lastposter, my $lastposttime, my $threads, my $posts, my $forumgraphic, my $miscad2, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $fgwidth,my $fgheight,my $miscad4,my $todayforumpost,my $miscad5) = split(/\t/,$existforuminfo);
		print FILE "$existforum\t$category\t$categoryplace\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t\n";
	     }
	     else {
	     	$existforum =~ s/forum//isg;
                print FILE "$existforum\t论坛分类丢失\t999\t论坛名称丢失\t论坛描述丢失\t\toff\ton\tno\tyes\t\t\t0\t0\t\tno\t\t\tno\tyes\t\t\t";
	     }
	}
        close(FILE);


        $filetoopen = "$lbdir" . "data/allforums.cgi";
        if (-e "$filetoopen") {
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE,"$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            @allforums = <FILE>;
            close(FILE);
        }
        else { undef @allforums; }

        $filetomake = "$lbdir" . "data/allforums.cgi";
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $forum (@allforums) {
        	chomp $forum;
        	($forumid, $category, $categoryplace, $forumname, my $no) = split(/\t/,$forum);
    		next if ($forumid !~ /^[0-9]+$/);
		if ($category !~ /^childforum-[0-9]+/) {
		    print FILE "$forum\n";
		} else {
		    $topforumno=$category;
		    $topforumno=~s/^childforum-//;
		    @tempcforum = grep(/^$topforumno\t/i, @allforums);
		    if ($#tempcforum >= 0) {
		        print FILE "$forum\n";
		    } else {
			$forum =~ s/^$forumid\t(.+?)\t(.+?)\t/$forumid\t论坛分类丢失\t999\t/isg;
		        print FILE "$forum\n";
		    }
		}
	}


        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        print qq(<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
<b>欢迎来到论坛管理中心 / 重新建立论坛主界面</b></td></tr>
<tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
<font color=#333333><b>重新建立 Allforums.cgi 文件，恢复主界面已经完成!</b>
</td></tr>
);
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/forumcache/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
    }
    else {
        print qq~<tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
<b>欢迎来到论坛管理中心 / 重新建立论坛主界面</b></td></tr>
<tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
<font face=宋体 color=#990000><b>此功能主要用于修复主界面中分论坛信息丢失或者损坏，完全智能化。</b>
</td></tr>
<tr><td bgcolor=#FFFFFF valign=middle align=center colspan=2>
<font face=宋体 color=#333333>如果您确定，那么请点击下面链接<p>
>> <a href="$thisprog?action=delete&checkaction=yes">重新建立 Allforums.cgi 文件，恢复主界面</a> <<
</td></tr></table></td></tr></table>
~;
    }
}
else {
    &adminlogin;
}
print qq~</td></tr></table></body></html>~;
exit;
