#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

sub sendtoposter {
    my ($senduser,$sendto, $moveto,$action,$forum,$topic,$topictitle,$sendly) = @_;
    $sendly = "<BR>理由：<font color=red>$sendly</font><BR>" if ($sendly ne "" && $sendly ne " ");
    $topictitle=~s/＊＃！＆＊//;
    $topictitle = "按此查看" if ($topictitle eq "");
    my $memberfilename = $sendto;
    $memberfilename =~ s/ /\_/g;
    $memberfilename =~ tr/A-Z/a-z/;
    my $currenttime = time;
    my $filetoopen = "${lbdir}$msgdir/in/$memberfilename" . "_msg.cgi";
    $filetoopen = &stripMETA($filetoopen);
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open (FILE, "$filetoopen");
    flock (FILE, 1) if ($OS_USED eq "Unix");
    sysread(FILE, my $inboxmessages,(stat(FILE))[7]);
    close (FILE);
    $inboxmessages =~ s/\r//isg;

    $topictitle = "<a href=topic.cgi?forum=$forum&topic=$topic target=_blank>$topictitle</a>";
    open (FILE, ">$filetoopen");
    flock (FILE, 2) if ($OS_USED eq "Unix");
    if ($action eq "move") {
        print FILE "＊＃！＆＊$senduser\tno\t$currenttime\t管理系统讯息\t你的帖子「$topictitle」已被管理员 $senduser 移至 $moveto <br>若有任何问题可以发短讯给管理员 $senduser 查询<br><br>---------------------------------------<br>雷傲极酷超级论坛 http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "jinghua") {
        print FILE "＊＃！＆＊$senduser\tno\t$currenttime\t管理系统讯息\t你的帖子「$topictitle」已被管理员 $senduser 挑选为精华文章!!感谢您为本论坛带来的好贴子，谢谢。<br><br>若有任何问题可以发短讯给管理员 $senduser 查询<br><br>---------------------------------------<br>雷傲极酷超级论坛 http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "deletethread") {
        print FILE "＊＃！＆＊$senduser\tno\t$currenttime\t管理系统讯息\t你的帖子「$topictitle」已被管理员 $senduser 删除。<br>$sendly<br>若有任何问题可以发短讯给管理员 $senduser 查询<br><br>---------------------------------------<br>雷傲极酷超级论坛 http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "deletepost") {
        print FILE "＊＃！＆＊$senduser\tno\t$currenttime\t管理系统讯息\t你在帖子「$topictitle」中的回复已被管理员 $senduser 删除。<br>$sendly<br>若有任何问题可以发短讯给管理员 $senduser 查询<br><br>---------------------------------------<br>雷傲极酷超级论坛 http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "lock") {
        print FILE "＊＃！＆＊$senduser\tno\t$currenttime\t管理系统讯息\t你的帖子「$topictitle」已被管理员 $senduser 锁定。<br>$sendly<br>若有任何问题可以发短讯给管理员 $senduser 查询<br><br>---------------------------------------<br>雷傲极酷超级论坛 http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "postdeleteonce") {
        print FILE "＊＃！＆＊$senduser\tno\t$currenttime\t管理系统讯息\t你的帖子「$topictitle」已被管理员 $senduser 屏蔽。<br>$sendly<br>若有任何问题可以发短讯给管理员 $senduser 查询<br><br>---------------------------------------<br>雷傲极酷超级论坛 http://bbs.LeoBBS.com\n";
    }
    elsif ($action eq "unpostdeleteonce") {
        print FILE "＊＃！＆＊$senduser\tno\t$currenttime\t管理系统讯息\t你的帖子「$topictitle」已被管理员 $senduser 屏蔽。<br>$sendly<br>若有任何问题可以发短讯给管理员 $senduser 查询<br><br>---------------------------------------<br>雷傲极酷超级论坛 http://bbs.LeoBBS.com\n";
    }
    print FILE "$inboxmessages\n";
    close (FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
}
1;
