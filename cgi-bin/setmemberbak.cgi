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
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "setmemberbak.cgi";

$query = new LBCGI;
$action = $query->param('action');
$action = &unHTML("$action");
$checkaction = $query->param('checkaction');
$member = $query->param('member');
$member = &unHTML("$member");
$noofone = $query->param('noofone');
$noofone = &unHTML("$noofone");
$beginone = $query->param('beginone');
$beginone = &unHTML("$beginone");
$totolerepire = $query->param('totolerepire');
$totolerepire = &unHTML("$totolerepire");

$inmembername = $query->cookie("adminname");
$inpassword = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$noofone = 2000 if ($noofone !~ /^[0-9]+$/);
$beginone = 0 if ($beginone !~ /^[0-9]+$/);
$totolerepire = 0 if ($totolerepire !~ /^[0-9]+$/);

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;

&getmember("$inmembername", "no");

if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

    print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>欢迎来到论坛管理中心 / 用户库备份及还原</b></td></tr>~;
    my %Mode = (
        'backup'      => \&backup,
        'backupnext'  => \&backupnext,
        'repire'      => \&repire,
        'repirenext'  => \&repirenext,
        'repireone'   => \&repireone,
        'restore'     => \&restore,
        'restorenext' => \&restorenext
    );
    if ($Mode{$action}) {$Mode{$action}->();}
    else {&memberoptions;}
    print qq~</table></td></tr></table>~;
}
else {
    &adminlogin;
}
print qq~</td></tr></table></body></html>~;
exit;

sub backup {

    opendir(DIR, "${lbdir}$memdir/old");
    @filedata = readdir(DIR);
    closedir(DIR);
    @countvar = grep (/\.cgi$/i, @filedata);
    $totaluserdata = @countvar;

    open(FILE, ">${lbdir}$memdir/allname.pl");
    foreach (@countvar) {
        print FILE "$_\n";
    }
    close(FILE);

    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库备份</b><br>
        <font color=#333333><B>当前共有 $totaluserdata 个注册用户，准备工作已经完成。</b><BR><BR><BR>
	<form action="setmemberbak.cgi" method=get>
        <input type=hidden name="action" value="backupnext">输入每次备份的用户数 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="开始备份">
        </form>
	为了减少资源占用，请输入每次备份的用户数，默认 2000，<BR>一般不要超过 3000，如果发现备份无法正常完成，请尽量减少这个数目，延长备份时间。<BR><BR>
        </td></tr>
    ~;
}

sub backupnext {
    open(FILE, "${lbdir}$memdir/allname.pl");
    @allname = <FILE>;
    close(FILE);
    $allnamenum = @allname;
    if ($beginone < $allnamenum) {
        $lastone = $beginone + $noofone;
        $lastone = $allnamenum if ($lastone > $allnamenum);
        unlink("${lbdir}$memdir/alluser.pl") if ($beginone == 0);
        open(FILE, ">>${lbdir}$memdir/alluser.pl");
        print FILE "nodisplay.cgi\t11111\tnodisplay\t11111\tnodisplay\t11111\tnodisplay\t11111\tnodisplay\t11111\tnodisplay\t11111\tnodisplay\t11111\t\n" if ($beginone == 0);
        for ($i = $beginone; $i < $lastone; $i++) {
            chomp $allname[$i];
            ($nametocheck, $no) = split(/\./, $allname[$i]);
            my $namenumber = &getnamenumber($nametocheck);
            &checkmemfile($nametocheck, $namenumber);
            $usrnames = "${lbdir}$memdir/$namenumber/$allname[$i]";
            open(USRFILE, "$usrnames");
            $userinfo = <USRFILE>;
            close(USRFILE);
            chomp $userinfo;
            $allname[$i] =~ tr/A-Z/a-z/;
            print FILE "$allname[$i]\t$userinfo\n";
        }
        close(FILE);

        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库备份</b><br>
        <font color=#333333><B>当前共有 $allnamenum 个注册用户，已经备份了 $lastone 个用户。。。</b><BR><BR><BR>
        <font color=#333333>如果无法自动开始下 $noofone 个用户的备份，请点击下面的链接继续<p>
        >> <a href="$thisprog?action=backupnext&beginone=$lastone&noofone=$noofone">继续备份用户库</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=backupnext&beginone=$lastone&noofone=$noofone">
	<BR><BR></td></tr>
         ~;
    }
    else {
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库备份</b><p>
        <font color=#333333>当前共有 $allnamenum 个注册用户，数据已经备份结束！<BR><BR>
        备份的用户保存在 LeoBBS 的用户库专用目录下（cgi-bin 下的 $memdir 目录），<BR>绝对路径为</font> ${lbdir}$memdir/alluser.pl<font color=#333333> ，<BR>为了安全起见，请你立即用 ftp 下载保存，然后删除此文件。</font></td></tr>
         ~;
    }
}

sub restore {
    if (-e "${lbdir}$memdir/alluser.pl") {
        open(FILE, "${lbdir}$memdir/alluser.pl");
        my @allname = <FILE>;
        close(FILE);
        $allname = @allname;
        $allname--;
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库还原</b><br>
        <font color=#333333><B>当前共有 $allname 个注册用户，准备工作已经完成。</b><BR><BR><BR>
	<form action="setmemberbak.cgi" method=get>
        <input type=hidden name="action" value="restorenext">输入每次还原的用户数 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="开始还原">
        </form>
	为了减少资源占用，请输入每次还原的用户数，默认 2000，<BR>一般不要超过 3000，如果发现还原无法正常完成，请尽量减少这个数目，延长还原时间。
	<BR><BR></td></tr>
         ~;
    }
    else {
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库备份文件没有找到</b><p>~;
    }
}

sub restorenext {
    $memberfiletitle = $inmembername;
    $memberfiletitle =~ y/ /_/;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitle .= ".cgi";
    open(FILE, "${lbdir}$memdir/alluser.pl");
    @alluser = <FILE>;
    close(FILE);
    $allusernum = @alluser;
    if ($beginone < $allusernum) {
        $lastone = $beginone + $noofone;
        $lastone = $allusernum if ($lastone > $allusernum);

        for ($i = $beginone; $i < $lastone; $i++) {
            chomp $alluser[$i];
            next if (($alluser[$i] =~ /^nodisplay/i) || ($alluser[$i] eq ""));
            my ($userfilename, @userinfo) = split(/\t/, $alluser[$i]);
            next if ($userfilename eq "");
            $userinfo = join("\t", @userinfo);
            if ($memberfiletitle ne $userfilename) {
                if (open(FILE, ">${lbdir}$memdir/old/$userfilename")) {
                    print FILE "$userinfo\n";
                    close(FILE);
                }
                ($nametocheck, $no) = split(/\./, $userfilename);
                my $namenumber = &getnamenumber($nametocheck);
                if (open(FILE, ">${lbdir}$memdir/$namenumber/$userfilename")) {
                    print FILE "$userinfo\n";
                    close(FILE);
                }
            }
        }
        $allusernum--;
        #        $lastone --;
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库备份</b><br>
        <font color=#333333><B>当前共有 $allusernum 个注册用户，已经还原了 $lastone 个用户。。。</b><BR><BR><BR>
        <font color=#333333>如果无法自动开始下 $noofone 个用户的还原，请点击下面的链接继续<p>
        >> <a href="$thisprog?action=restorenext&beginone=$lastone&noofone=$noofone">继续还原用户库</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=restorenext&beginone=$lastone&noofone=$noofone">
	<BR><BR></td></tr>
         ~;
    }
    else {
        $allusernum--;
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库还原</b><p>
        <font color=#333333>用户数据已经还原(坛主 $inmembername 数据未更新)，用户备份库中共有 $allusernum 个注册用户！<BR><BR>
        </td></tr>
         ~;
    }
}

sub repire {
    if (-e "${lbdir}$memdir/alluser.pl") {
        open(FILE, "${lbdir}$memdir/alluser.pl");
        my @allname = <FILE>;
        close(FILE);
        $allname = @allname;
        $allname--;
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库还原</b><br>
        <font color=#333333><B>当前共有 $allname 个注册用户，准备工作已经完成。</b><BR><BR><BR>
	<form action="setmemberbak.cgi" method=get>
        <input type=hidden name="action" value="repirenext">输入每次检查修复的用户数 
        <input type=hidden name="beginone" value=0>
        <input type=hidden name="totolerepire" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="开始检查修复">
        </form>
	为了减少资源占用，请输入每次检查修复的用户数，默认 2000，<BR>一般不要超过 3000，如果发现检查修复无法正常完成，请尽量减少这个数目，延长检查修复时间。
	<BR><BR></td></tr>
         ~;
    }
    else {
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库备份文件没有找到</b><p>~;
    }
}

sub repirenext {
    $memberfiletitle = $inmembername;
    $memberfiletitle =~ y/ /_/;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitle .= ".cgi";
    open(FILE, "${lbdir}$memdir/alluser.pl");
    my @alluser = <FILE>;
    close(FILE);
    $allusernum = @alluser;
    if ($beginone < $allusernum) {
        $lastone = $beginone + $noofone;
        $lastone = $allusernum if ($lastone > $allusernum);

        for ($i = $beginone; $i < $lastone; $i++) {
            chomp $alluser[$i];
            next if (($alluser[$i] =~ /^nodisplay/i) || ($alluser[$i] eq ""));
            ($userfilename, @userinfo) = split(/\t/, $alluser[$i]);
            next if ($userfilename eq "");
            $userinfo = join("\t", @userinfo);
            next if ($userinfo eq "");
            if ($memberfiletitle ne $userfilename) {
                ($nametocheck, $no) = split(/\./, $userfilename);
                my $namenumber = &getnamenumber($nametocheck);
                &checkmemfile($nametocheck, $namenumber);
                $usrfiles = "${lbdir}$memdir/$namenumber/$userfilename";
                open(FILE, "$usrfiles");
                $userdatanow = <FILE>;
                close(FILE);
                chomp $userdatanow;

                my ($membername1, $password1, $no) = split(/\t/, $userdatanow);
                if (($membername1 eq "") || ($password1 eq "")) {
                    if (open(FILE, ">${lbdir}$memdir/$namenumber/$userfilename")) {
                        print FILE "$userinfo\n";
                        close(FILE);
                    }
                    if (open(FILE, ">${lbdir}$memdir/old/$userfilename")) {
                        print FILE "$userinfo\n";
                        close(FILE);
                    }
                    $totolerepire++;
                }
            }
        }
        $allusernum--;
        if ($lastone > $allusernum) {$lastone1 = $allusernum;}
        else {$lastone1 = $lastone;}

        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库备份</b><br>
        <font color=#333333><B>当前共有 $allusernum 个注册用户，已经检查了 $lastone1 个用户，修复了 $totolerepire 个用户 。。。</b><BR><BR><BR>
        <font color=#333333>如果无法自动开始下 $noofone 个用户的检查，请点击下面的链接继续<p>
        >> <a href="$thisprog?action=repirenext&beginone=$lastone&noofone=$noofone&totolerepire=$totolerepire">继续修复用户库</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=repirenext&beginone=$lastone&noofone=$noofone&totolerepire=$totolerepire">
	<BR><BR></td></tr>
         ~;
    }
    else {
        $allusernum--;
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>还原数据被破坏的用户</b><p>
        <font color=#333333>$totolerepire 个数据被破坏的用户已经还原，目前用户备份库中共有 $allusernum 个注册用户！<BR><BR>
        </td></tr>
         ~;
    }
}

sub repireone {
    if ($checkaction eq "yes") {
        $memberfilename = $member;
        $memberfilename =~ y/ /_/;
        $memberfilename =~ tr/A-Z/a-z/;
        $memberfilename .= ".cgi";
        if (-e "${lbdir}$memdir/alluser.pl") {
            open(FILE, "${lbdir}$memdir/alluser.pl");
            my @totlename = <FILE>;
            close(FILE);
            $totaluserdata = $#totlename;
            $repireuser = 0;
            foreach (@totlename) {
                chomp $_;
                next if (($_ =~ /^nodisplay/i) || ($_ eq ""));
                my ($userfilename, @userinfo) = split(/\t/, $_);
                next if ($userfilename eq "");
                my $userinfo = join("\t", @userinfo);
                next if ($userinfo eq "");
                if ($memberfilename eq $userfilename) {
                    if (open(FILE, ">${lbdir}$memdir/$userfilename")) {
                        print FILE "$userinfo\n";
                        close(FILE);
                    }
                    $repireuser = 1;
                }
            }
            if ($repireuser eq 1) {
                print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>还原数据被破坏的用户</b><p>
        	<font color=#333333>用户 $member 的资料已经还原，目前用户备份库中共有 $totaluserdata 个注册用户！<BR><BR></td></tr>
         	~;
            }
            else {
                print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>还原数据被破坏的用户</b><p>
	        <font color=#333333>用户备份库中没有用户 $member 的资料，目前用户备份库中共有 $totaluserdata 个注册用户！<BR><BR></td></tr>
         	~;
            }
        }
        else {
            print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#990000><b>用户库备份文件没有找到</b><p>~;
        }
    }
    else {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>警告！！</b></td></tr>
        <tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#333333>只有点击下面的链接才可以还原 $member 用户的数据<p>
        >> <a href="$thisprog?action=repireone&member=$member&checkaction=yes">确定还原此用户的数据</a> <<
        </td></tr></table></td></tr></table>
        ~;
    }
}


sub memberoptions {
    $backupfile = "$lbdir" . "$memdir/alluser.pl";
    if (-e $backupfile) {
        $last_backup = (stat("$backupfile"))[9];
        $longdatebackup = &fulldatetime("$last_backup");
        $last_backup = "$longdatebackup";
        $bakuptrue = 0;
    }
    else {
        $last_backup = "用户库备份文件没有找到，可能没有备份过";
        $bakuptrue = 1;
    }

    print qq~<tr><td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>请选择一项</b></td></tr>          
    <tr><td bgcolor=#FFFFFF colspan=2><UL>
    <font color=#333333><BR>用户库备份文件路径： <B>$backupfile</B><BR>用户库最后备份日期： <B>$last_backup</B><BR><BR></td></tr>
    <tr><td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=backup">备份用户数据库</a></b><br>
    可以防止用户数据破坏，也可以方便转移用户库数据。<BR>注意：无需时时备份，一般每 3 - 5 日备份一次为宜。<BR><BR></td></tr>
    ~;
    print qq~<tr><td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=restore">还原用户数据库</a></b>　<font color=#990000>(为了安全起见，坛主 $inmembername 资料不会还原)</font><br>
    转移用户库数据后，或者用户数据被破坏，就可以使用此功能把备份的用户库数据全部还原。<BR>
    注意：自备份之后的用户所有更新数据将<font color=#990000><B>全部丢失</B></font>，请慎重使用。<BR><BR>
    </td></tr>
    ~ if ($bakuptrue == 0);

    print qq~<tr><td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=repire">利用备份用户库修复丢失的用户</a></b><br>
    当由于意外导致部分的用户数据破坏，就可以用此功能恢复。<BR>正常的用户资料不会被还原，只还原被破坏了的用户资料<BR><BR></td></tr>
    <tr><td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>还原单个指定用户的数据</b><br>
    当由于意外导致某个用户的数据被破坏，或者需要还原某个用户的资料，就可以用此功能。<BR>
	<form action="setmemberbak.cgi" method=get>
        <input type=hidden name="action" value="repireone">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="恢复此用户的资料">
        </form>
    <BR><BR></td></tr>
    ~;
}
