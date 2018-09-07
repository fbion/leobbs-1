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
use File::Copy;
$loadcopymo = 1;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
require "data/cityinfo.cgi";

$|++;

$thisprog = "foruminit.cgi";

$query = new LBCGI;

$action          = $query -> param('action');
$inmember        = $query -> param('member');
$inmember        = &unHTML("$inmember");
$action          = &unHTML("$action");

$noofone         = $query -> param('noofone');
$noofone         = &unHTML("$noofone");
$beginone        = $query -> param('beginone');
$beginone        = &unHTML("$beginone");

$noofone      = 2000 if ($noofone !~ /^[0-9]+$/);
$beginone     = 0 if ($beginone !~ /^[0-9]+$/);

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
        
&getmember("$inmembername","no");
        
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 论坛初始化</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'updatecount'        =>    \&docount,
            'uptop'       	 =>    \&dotop,
            'uptopnext'       	 =>    \&dotopnext,
            'upemot'       	 =>    \&doemot,
            'upuser'       	 =>    \&doava,
            'delxzb'             =>    \&dodelallxzb,
            'shareforums'      	 =>    \&doshareforums,
            'dellock'      	 =>    \&dodellock,
            'changedir'		 =>    \&dochangedir,
            'uponlineuser'     	 =>    \&douponlineuser,
            'upconter'		 =>    \&doupconter,
            'init'        	 =>    \&doinit,
            'upupload'        	 =>    \&doupload,
            'uppost'        	 =>    \&dopost,
            'upmessage'        	 =>    \&domessage,
            'delmessage'         =>    \&dodalmessage,
            'delcache'           =>    \&dodelcache,
            'delans'             =>    \&dodelans,
            'dogetold'           =>    \&dogetold,
            'dogetoldnext'       =>    \&dogetoldnext,
            'upskinselect'       =>    \&upskinselect,

            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &doinit; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        

sub upskinselect {
opendir (DIR, "${lbdir}data/skin"); 
my @dirdata = readdir(DIR);
closedir (DIR);
my @skinselectdata = grep(/\.(cgi)$/i,@dirdata);
map(s/\.cgi$//is, @skinselectdata);
    $skincount = @skinselectdata;
    my $userskin = qq~<div class="menuitems">&nbsp;<a href="index.cgi?action=change_skin&thisprog=' + url + '&skin="><font color=#000000>默认风格</font></a>&nbsp;</div>~;
    for (my $i=0;$i<$skincount;$i++){
    	eval{ require "${lbdir}data/skin/$skinselectdata[$i].cgi"; };
    	next if ($@);
    	if ($cssname ne "") { $skinnames = $cssname; } else { $skinnames = $skinselectdata[$i]; }
        $skinselectdata[$i] = uri_escape($skinselectdata[$i]);
        $userskin.= qq~<div class="menuitems">&nbsp;<a href="index.cgi?action=change_skin&thisprog=' + url + '&skin=$skinselectdata[$i]"><font color=#000000>$skinnames</font></a>&nbsp;</div>~;
        $cssname = "";
    }

    $userskins = qq~
<script>
var url = new String (window.document.location);
url = url.replace (/&/g, "%26");
url = url.replace (/\\\\//g, "%2F");
url = url.replace (/:/g, "%3A");
url = url.replace (/\\\\?/g, "%3F");
url = url.replace (/=/g, "%3D");
linkset[3]='$userskin'</script>~;

$skinselect = qq~<img src=\$imagesurl/images/fg.gif width=1> <span style=cursor:hand onMouseover="showmenu(event,linkset[3])" onMouseout="delayhidemenu()">论坛风格&nbsp;</span>~;
			open(FILE, ">${lbdir}data/skinselect.pl");
    print FILE qq(\$userskins = qq~$userskins~;\n);
    print FILE qq(\$skinselect = qq~$skinselect~;\n);
    print FILE "1;\n";
			close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化论坛风格选择列表</b><p>
                    
        <font color=#333333>所有论坛风格选择列表已经更新！</font>
                    
        </td></tr>
         ~;
}

sub doupload {
    chmod (0777,"$imagesdir");
    chmod (0777,"${imagesdir}$usrdir");
    chmod (0777,"${imagesdir}usravatars");
    chmod (0777,"${lbdir}FileCount");

    chmod (0777,"${lbdir}boarddata");
    chmod (0777,"${lbdir}lock");
    chmod (0777,"${lbdir}$saledir");
    chmod (0777,"${lbdir}memfav");
    chmod (0777,"${lbdir}memfriend");
    chmod (0777,"${lbdir}search");
    chmod (0777,"${lbdir}data");
    chmod (0777,"${lbdir}$memdir");
    chmod (0777,"${lbdir}$memdir/old");
    chmod (0777,"${lbdir}$msgdir");
    $filetoopen = "$lbdir" . "data/allforums.cgi";
    if (-e "$filetoopen") {
        open(FILE,"$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);
        
        foreach $_ (@allforums) {
            chomp $_;
            (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription,my $no) = split(/\t/,$_);
            next if (($forumid eq "")||($forumid !~ /^[0-9]+$/)||($category eq "")||($categoryplace eq "")||($forumname eq "")||($forumdescription eq ""));
            $dirtomake = "$lbdir" . "FileCount/$forumid";
            mkdir ("$dirtomake", 0777) if (!(-e "$dirtomake"));
            chmod (0777,"$dirtomake");
            $dirtomake = "$imagesdir" . "$usrdir/$forumid";
            mkdir ("$dirtomake", 0777) if (!(-e "$dirtomake"));
            chmod (0777,"$dirtomake");

	    &changemod("${lbdir}FileCount/$forumid");
	    &changemod("${imagesdir}$usrdir/$forumid");
	}
    }
    require "autochangeusrdir.pl";
    print qq~<tr>
<td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>文件上传目录属性初始化完成！</b><p>
<font color=#333333>请立即测试上传功能是否已经正常，如果还不正常，请参照论坛的属性说明文档用 FTP 软件自行设置！！</font>
</td></tr>
~;
}

sub dodelcache { 
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/\.pl$/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }

    opendir (DIRS, "${lbdir}");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^CGItemp/i, @files);
    foreach (@files) {unlink ("${lbdir}$_") if ((-M "${lbdir}$_") *86400 > 600);}

    opendir (DIRS, "${lbdir}cache/meminfo");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/meminfo/$_");
    }
    opendir (DIRS, "${lbdir}cache/mymsg");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/mymsg/$_");
    }

    opendir (DIRS, "${lbdir}cache/myinfo");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/myinfo/$_");
    }
    opendir (DIRS, "${lbdir}cache/id");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/id/$_");
    }
    opendir (DIRS, "${lbdir}cache/online");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/online/$_");
    }
   print qq~<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000><b>论坛缓存已经全部清空！</b><p> 
</td></tr> 
~; 
}

sub dodalmessage { 
   $inbox = "${lbdir}$msgdir/in"; 
   opendir (DIR, "$inbox"); 
   my @inboxdata = readdir(DIR); 
   closedir (DIR);
   $inboxcount = @inboxdata;
   $inboxcount = $inboxcount - 2;
   foreach $filename(@inboxdata){ 
   $filepath=$inbox."/".$filename; 
   unlink ($filepath); 
   } 
   $outbox = "${lbdir}$msgdir/out"; 
   opendir (DIR, "$outbox"); 
   my @outboxdata = readdir(DIR); 
   closedir (DIR); 
   $outboxcount = @outboxdata;
   $outboxcount = $outboxcount - 2;
   foreach $filename(@outboxdata){ 
   $filepath=$outbox."/".$filename; 
   unlink ($filepath); 
   } 
   $outbox = "${lbdir}$msgdir/main"; 
   opendir (DIR, "$outbox"); 
   my @outboxdata = readdir(DIR); 
   closedir (DIR); 
   foreach $filename(@outboxdata){ 
   $filepath=$outbox."/".$filename; 
   unlink ($filepath); 
   } 
    opendir (DIRS, "${lbdir}cache/mymsg");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/mymsg/$_");
    }
   print qq~<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000><b>短消息文件清空完成！</b><p> 
<font color=#333333>收件箱共删除 $inboxcount 个,发件箱共删除 $outboxcount 个</font> 
</td></tr> 
~; 
}

sub domessage {

    mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod (0777,"${lbdir}$msgdir");
    mkdir ("${lbdir}$msgdir/in", 0777) if (!(-e "${lbdir}$msgdir/in"));
    mkdir ("${lbdir}$msgdir/out", 0777) if (!(-e "${lbdir}$msgdir/out"));
    mkdir ("${lbdir}$msgdir/main", 0777) if (!(-e "${lbdir}$msgdir/main"));
    chmod (0777,"${lbdir}$msgdir/in");
    chmod (0777,"${lbdir}$msgdir/out");
    chmod (0777,"${lbdir}$msgdir/main");

    $dirtoopen = "${lbdir}$msgdir";
    opendir (DIR, "$dirtoopen");
    my @dirdata = readdir(DIR);
    closedir (DIR);
	
    @data1 = grep(/\_msg\.cgi/i,@dirdata);
    foreach (@data1) {
	copy("${lbdir}$msgdir/$_","${lbdir}$msgdir/in/$_");
    }
    @data1 = grep(/\_out\.cgi/i,@dirdata);
    foreach (@data1) {
	copy("${lbdir}$msgdir/$_","${lbdir}$msgdir/out/$_");
    }
    @data1 = grep(/\_main\.cgi/i,@dirdata);
    foreach (@data1) {
	copy("${lbdir}$msgdir/$_","${lbdir}$msgdir/main/$_");
    }

    $dirtoopen = "${lbdir}$msgdir";
    opendir (DIR, "$dirtoopen");
    my @files = readdir(DIR);
    closedir (DIR);
    foreach (@files) {
        chomp $_;
        unlink ("${lbdir}$msgdir/$_");
    }

    &changemod("${lbdir}$msgdir/in");
    &changemod("${lbdir}$msgdir/out");
    &changemod("${lbdir}$msgdir/main");

    print qq~<tr>
<td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>短消息目录和文件属性初始化完成！</b><p>
<font color=#333333>请立即测试短消息功能是否已经正常，如果还不正常，请参照论坛的属性说明文档用 FTP 软件自行设置！！</font>
</td></tr>
~;
}

sub dopost {

    mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod (0777,"${lbdir}boarddata");
    chmod (0777,"${lbdir}lock");
    chmod (0777,"${lbdir}$saledir");
    chmod (0777,"${lbdir}memfav");
    chmod (0777,"${lbdir}memfriend");
    chmod (0777,"${lbdir}search");
    chmod (0777,"${lbdir}data");
    chmod (0777,"${lbdir}data/skin");
    chmod (0777,"${lbdir}$memdir");
    chmod (0777,"${lbdir}$memdir/old");

    chmod (0777,"${lbdir}FileCount");
    chmod (0777,"${lbdir}$msgdir");
    chmod (0777,"$imagesdir");
    chmod (0777,"${imagesdir}$usrdir");
    chmod (0777,"${imagesdir}usravatars");


    &changemod("${lbdir}boarddata");
    &changemod("${lbdir}lock");
    &changemod("${lbdir}$saledir");
    &changemod("${lbdir}memfav");
    &changemod("${lbdir}memfriend");
    &changemod("${lbdir}search");
    &changemod("${lbdir}data");
    &changemod("${lbdir}data/skin");
    &changemod("${lbdir}$memdir");
    &changemod("${lbdir}$memdir/old");
   chmod (0777,"${lbdir}data/lbmail");
   chmod (0777,"${lbdir}data/myskin");
   chmod (0777,"${lbdir}data/skin");
   chmod (0777,"${lbdir}data/template");

    $filetoopen = "$lbdir" . "data/allforums.cgi";
    if (-e "$filetoopen") {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE,"$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        
        foreach $_ (@allforums) {
            chomp $_;
            (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription,my $no) = split(/\t/,$_);
            next if (($forumid eq "")||($forumid !~ /^[0-9]+$/)||($category eq "")||($categoryplace eq "")||($forumname eq "")||($forumdescription eq ""));
            $dirtomake = "$lbdir" . "forum$forumid";
            mkdir ("$dirtomake", 0777) if (!(-e "$dirtomake"));
            chmod (0777,"$dirtomake");
	    &changemod("${lbdir}forum$forumid");
	}
    }
    print qq~<tr>
<td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>论坛帖子目录和数据文件属性初始化完成！</b><p>
<font color=#333333>请立即测试论坛数据是否已经正常，如果还不正常，请参照论坛的属性说明文档用 FTP 软件自行设置！！</font>
</td></tr>
~;
}

sub changemod {
    my $dirname =shift;
    opendir (DIR, $dirname);
    my @dirdata = readdir(DIR);
    closedir (DIR);
    foreach (@dirdata) {
    	chomp $_;
    	next if (($_ eq ".")||($_ eq ".."));
        chmod (0666, "$dirname/$_");
    }
    return;
}

sub docount {

    opendir (DIR, "${lbdir}$memdir/old"); 
    @filedata = readdir(DIR);
    closedir (DIR);
    @countvar = grep(/\.cgi$/i,@filedata);
    $newtotalmembers = @countvar;

        require "$lbdir" . "data/boardstats.cgi";
        
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$newtotalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
    
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>计算用户总数</b><p>
                    
        <font color=#333333>当前共有 $newtotalmembers 个注册用户，数据已经更新！</font>
                    
        </td></tr>
         ~;

}

sub dogetold {

    chmod (0777,"${lbdir}$memdir");
    mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod (0777,"${lbdir}$memdir/old");

    opendir (DIR, "${lbdir}$memdir"); 
    @filedata = readdir(DIR);
    closedir (DIR);
    @countvar = grep(/\.cgi$/i,@filedata);
    
    open(FILE,">${lbdir}data/allname.pl");
    foreach (@countvar) {
        print FILE "$_\n";
    }
    $totaluserdata = @countvar;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>注册用户整理</b><br>
                    
        <font color=#333333><B>当前共有 $totaluserdata 个注册用户需要整理，准备工作已经完成。</b><BR><BR><BR>
	<form action="foruminit.cgi" method=get>
        <input type=hidden name="action" value="dogetoldnext">输入每次进行整理的用户数 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=3 maxlength=3 value=300>
        <input type=submit value="开始整理">
        </form>
	为了减少资源占用，请输入每次进行排名的用户数，默认 300，<BR>一般不要超过 600，如果发现进行排名无法正常完成，请尽量减少这个数目，延长排名时间。
	<BR><BR>
        </td></tr>
         ~;
} # end routine

sub dogetoldnext {

    open(FILE,"${lbdir}data/allname.pl");
    @allname = <FILE>;
    close(FILE);
    $allnamenum = @allname;
    $currenttime = time;
    
    if ($beginone < $allnamenum) {
        $lastone = $beginone + $noofone;
        $lastone = $allnamenum if ($lastone > $allnamenum);

	for ($i = $beginone; $i < $lastone; $i ++) {
	    $memberfile = $allname[$i];
	    chomp $memberfile;
	    ($memberfile, $no) = split(/\./,$memberfile);
	    my $namenumber = &getnamenumber($memberfile);
	    &checkmemfile($memberfile,$namenumber);
	    $usrfileopen = "${lbdir}$memdir/$namenumber/$memberfile.cgi";

	        open (FILE, "$usrfileopen");
	        $line = <FILE>;
	        close (FILE);
	        chomp $line;
	        @memberdaten = split(/\t/,$line);
	        $lastgone = $memberdaten[26] + 6*3600*24;
    	        open(FILE,">${lbdir}$memdir/old/$memberfile.cgi");
	        print FILE "$line\n";
	        close(FILE);
	} 

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>用户整理</b><p>
        <font color=#333333><B>当前共有 $allnamenum 个注册用户需要整理，已经进行整理了 $lastone 个用户。。。</b><BR><BR><BR>
        <font color=#333333>如果无法自动开始下 $noofone 个用户的整理，请点击下面的链接继续<p>
        >> <a href="$thisprog?action=dogetoldnext&beginone=$lastone&noofone=$noofone">继续进行用户整理</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=dogetoldnext&beginone=$lastone&noofone=$noofone">
	<BR><BR>
        </td></tr>
         ~;
     }
     else {

    opendir (DIR, "${lbdir}$memdir"); 
    @filedata = readdir(DIR);
    closedir (DIR);
    @countvar = grep(/\.cgi$/i,@filedata);
    $totaluserdata = @countvar;
    
    unlink ("${lbdir}data/allname.pl");

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>用户整理</b><p>
                    
        <font color=#333333>用户整理已经结束！<BR><BR>
        </td></tr>
         ~;
     }

}

sub dotop {
	
    opendir (DIR, "${lbdir}$memdir/old");
    @filedata = readdir(DIR);
    closedir (DIR);
    @countvar = grep(/\.cgi$/i,@filedata);
    $totaluserdata = @countvar;
    
    open(FILE,">${lbdir}$memdir/allname.pl");
    foreach (@countvar) {
        print FILE "$_\n";
    }
    close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>用户排名初始化</b><br>
                    
        <font color=#333333><B>当前共有 $totaluserdata 个注册用户，准备工作已经完成。</b><BR><BR><BR>
	<form action="foruminit.cgi" method=get>
        <input type=hidden name="action" value="uptopnext">输入每次进行排名的用户数 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="开始排名">
        </form>
	为了减少资源占用，请输入每次进行排名的用户数，默认 2000，<BR>一般不要超过 3000，如果发现进行排名无法正常完成，请尽量减少这个数目，延长排名时间。
	<BR><BR>
        </td></tr>
         ~;
} # end routine

sub dotopnext {

    $filename = "alluser.pl";
    open(FILE,"${lbdir}$memdir/allname.pl");
    @allname = <FILE>;
    close(FILE);
    $allnamenum = @allname;
    if ($beginone < $allnamenum) {
        $lastone = $beginone + $noofone;
        $lastone = $allnamenum if ($lastone > $allnamenum);

        if ($beginone == 0) {
            unlink ("${lbdir}data/lbmember.cgi")  ;
            unlink ("${lbdir}data/lbmember0.cgi")  ;
            unlink ("${lbdir}data/lbmember1.cgi") ;
            unlink ("${lbdir}data/lbmember3.cgi") ;
            unlink ("${lbdir}data/lbmember4.cgi") ;
        }

	open  (MEMFILE, ">>${lbdir}data/lbmember.cgi");
	flock (MEMFILE, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE0, ">>${lbdir}data/lbmember0.cgi");
	flock (MEMFILE0, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE1, ">>${lbdir}data/lbmember1.cgi");
	flock (MEMFILE1, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE3, ">>${lbdir}data/lbmember3.cgi");
	flock (MEMFILE3, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE4, ">>${lbdir}data/lbmember4.cgi");
	flock (MEMFILE4, 2) if ($OS_USED eq "Unix");

	for ($i = $beginone; $i < $lastone; $i ++) {
	    $memberfile = $allname[$i];
	    chomp $memberfile;
	    ($memberfile, $no) = split(/\./,$memberfile);
	    my $namenumber = &getnamenumber($memberfile);
	    &checkmemfile($memberfile,$namenumber);
	    
	    my $usrfileopen = "${lbdir}$memdir/$namenumber/$memberfile.cgi";
	    open (FILE, "$usrfileopen");
	    flock (FILE, 1) if ($OS_USED eq "Unix");
	    $line = <FILE>;
	    close (FILE);
	    chomp $line;
	    @memberdaten = split(/\t/,$line);
	    $username =$memberdaten[0];   
	    $userad=$memberdaten[3];
	    $anzahl = $memberdaten[4];
	    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
	    $anzahl1 = 0 if ($anzahl1 eq "");
	    $anzahl2 = 0 if ($anzahl2 eq "");
	    $anzahl   = $anzahl1 + $anzahl2;
	    $useremail=$memberdaten[5];
	    $date1    = $memberdaten[13];
	    $logtime = $memberdaten[27];
	    $jifen   = $memberdaten[45];
	    $mymoney = $memberdaten[30];
	    $postdel = $memberdaten[31];
	    $jhcount = $memberdaten[40];
	    $jifen = $memberdaten[45];

	    $logtime = 0 if ($logtime eq "");
	    $mymoney = 0 if ($mymoney eq "");
	    $postdel = 0 if ($postdel eq "");
	    $jhcount = 0 if ($jhcount eq "");

	if ($jifen eq "") {
		$jifen = $anzahl1 * $ttojf + $anzahl2 * $rtojf - $postdel * $deltojf;
  }

    $mymoney = $anzahl1 * $addmoney + $anzahl2 * $replymoney + $logtime * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

	    $birthday = $memberdaten[36];

	    print MEMFILE  "$username\t$userad\t$anzahl\t$date1\t$useremail\t$mymoney\t$jhcount\t$jifen\t\n";   
	    print MEMFILE0 "$username\t$anzahl\t\n" if ($anzahl > 0);   
	    print MEMFILE1 "$useremail\t$username\n";   
	    print MEMFILE3 "$username\t$birthday\t\n" if (($birthday ne "")&&($birthday ne "//"));  
	    print MEMFILE4 "$username\t".$memberdaten[7]."\t\n" if ($memberdaten[7] =~/^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$/);  
	} 
	close(MEMFILE4);
	close(MEMFILE3);
	close(MEMFILE1);
	close(MEMFILE0);
	close(MEMFILE);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>计算用户排名</b><p>
        <font color=#333333><B>当前共有 $allnamenum 个注册用户，已经进行排名了 $lastone 个用户。。。</b><BR><BR><BR>
        <font color=#333333>如果无法自动开始下 $noofone 个用户的排名，请点击下面的链接继续<p>
        >> <a href="$thisprog?action=uptopnext&beginone=$lastone&noofone=$noofone">继续进行排名用户</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=uptopnext&beginone=$lastone&noofone=$noofone">
	<BR><BR>
        </td></tr>
         ~;
     }
     else {


open (FILE, "$lbdir/data/lbmember0.cgi");
flock(FILE, 1) if ($OS_USED eq "Unix");
my @file = <FILE>;
close (FILE);
foreach my $line (@file) {
my @tmpuserdetail = split (/\t/, $line);
chomp @tmpuserdetail;
$postundmember {"$tmpuserdetail[0]"} = $tmpuserdetail[1];
}
my @sortiert = reverse sort { $postundmember{$a} <=> $postundmember{$b} } keys(%postundmember);

open  (MEMFILE0, ">${lbdir}data/lbmember0.cgi");
flock (MEMFILE0, 2) if ($OS_USED eq "Unix");
foreach my $member (@sortiert[0 ... 99]) {
    next if ($member eq "");
    print MEMFILE0 "$member\t$postundmember{\"$member\"}\t\n";
}
close(MEMFILE0);

open (MEMFILE, "${lbdir}data/lbmember3.cgi");
@birthdaydata = <MEMFILE>;
close (MEMFILE);
foreach(@birthdaydata){
chomp $_;
next if($_ eq "");
(my $biruser, my $borns) = split(/\t/,$_);
(my $biryear, my $birmon, my $birday) = split(/\//, $borns);
$birmon = $birmon - 0;
next if ($birmon > 12 || $birmon < 1);
$birdayinfo[$birmon] = "$birdayinfo[$birmon]$_\n";
}
for ($i=1;$i<=12;$i++) {
open(FILE, ">${lbdir}calendar/borninfo$i.cgi");
print FILE "$birdayinfo[$i]";
close(FILE);
}

mkdir("${lbdir}data/lbemail",0777) unless (-e "${lbdir}data/lbemail");
chmod(0777,"${lbdir}data/lbemail");

open(MEMFILE, "${lbdir}data/lbmember1.cgi");
my @emails = <MEMFILE>;
close(MEMFILE);
for (0..255)
{
       my $char = chr($_);
       next if ($char =~ /[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|A-Z]/);
       $char = '\$char' if ($char eq '[' || $char eq ']' || $char eq '.');
       my @thismails = grep(m/^$char/i, @emails);
       open(FILE, ">${lbdir}data/lbemail/$_.cgi");
       foreach (@thismails) {print FILE $_;}
       close(FILE);
}

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>计算用户排名</b><p>
                    
        <font color=#333333>当前共有 $allnamenum 个注册用户，计算用户排名已经结束！<BR><BR>
        </td></tr>
         ~;
     }

}

sub doemot {

$dirtoopen = "$imagesdir" . "emot";
opendir (DIR, "$dirtoopen"); 
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/\.(gif|jpg)$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbemot.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);
			open(FILE, "${lbdir}data/lbemot.cgi");
			my @emoticondata = <FILE>;
			close(FILE);
			chomp(@emoticondata);
			map(s/\.gif$//is, @emoticondata);

			$emoticoncode = join('|', @emoticondata);
			$emoticoncode = "\$\$post =~ s/\\:($emoticoncode)\\:/<img src=\${imagesurl}\\/emot\\/\$1\\.gif>/isg;";

			open(FILE, ">${lbdir}data/emot.pl");
			print FILE $emoticoncode;
			close(FILE);

$dirtoopen = "$imagesdir" . "posticons";
opendir (DIR, "$dirtoopen");
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/\.(gif|jpg)$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbpost.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化EMOT和POST图片</b><p>
                    
        <font color=#333333>所有EMOT和表情图片已经更新！</font>
                    
        </td></tr>
         ~;
}         
     
sub doava {
$dirtoopen = "$imagesdir" . "avatars";
opendir (DIR, "$dirtoopen");
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/\.(gif|jpg)$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbava.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化用户头像图片</b><p>
                    
        <font color=#333333>所有用户头像图片已经更新！</font>
                    
        </td></tr>
         ~;

}

sub doupconter {
	my $onlinemaxtime = time;
	my $filetomake = "$lbdir" . "data/counter.cgi";
	open(FILE,">$filetomake");
        print FILE "1\t1\t1\t$onlinemaxtime\t";
	close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>初始化在线统计及访问次数</b><p>
                    
        <font color=#333333>访问次数数据已经初始化！</font>
                    
        </td></tr>
         ~;

}
	
sub douponlineuser {
	$currenttime = time;
        open(FILES,">${lbdir}data/onlinedata.cgi");
	print FILES "$inmembername\t$currenttime\t$currenttime\t管理区\t保密\t保密\t保密\t管理区\t保密\t$membercode\t" ;
	close (FILES);
        open(FILES,">${lbdir}data/onlinedata.cgi.cgi");
	print FILES "$inmembername\t$currenttime\t$currenttime\t管理区\t保密\t保密\t保密\t管理区\t保密\t$membercode\t" ;
	close (FILES);

        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>初始化在线统计及访问次数</b><p>
<font color=#333333>在线人数统计数据已经初始化！</font></td></tr>
~;
}

sub dodelallxzb {
    opendir (DIRS, "${lbdir}boarddata");
    my @files = readdir(DIRS);
    closedir (DIRS);
    my @files = grep(/^xzb/i, @files);
    foreach (@files) {
    	chomp $_;
	unlink ("${lbdir}boarddata/$_");
    }
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>初始化所有论坛的小字报</b><p>
<font color=#333333>所有论坛的小字报已经初始化！</font>
</td></tr>
~;
}

sub dodelans {
    opendir (DIRS, "${lbdir}data");
    my @files = readdir(DIRS);
    closedir (DIRS);
    my @files = grep(/^new/i, @files);
    foreach (@files) {
    	chomp $_;
	unlink ("${lbdir}data/$_");
    }
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>初始化所有论坛的公告</b><p>
<font color=#333333>所有论坛的公告已经初始化！</font>
</td></tr>
~;

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata = grep(/^announce/,@dirdata);
foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
}	

sub doshareforums {
	my $filetoopen = "$lbdir" . "data/shareforums.cgi";
	open(FILE, ">$filetoopen");
	print FILE "雷傲科技\thttp:\/\/www.leoBBS.com\/\tLeoBBS 最新版本介绍，最新版本免费下载，论坛技术支持，虚拟主机以及域名申请等。。\t1\t$imagesurl\/images\/leotech8831.gif\t\n";
	print FILE "极酷超级论坛\thttp:\/\/bbs.leobbs.com\/\t最新软件、影视、音乐、网络安全、图形艺术、游戏、CGI 知识等综合论坛，还可以聊天。。。\t2\t$imagesurl\/images\/leobbs8831.gif\t\n";
	close(FILE);
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>初始化论坛联盟数据为空</b><p>
<font color=#333333>在线联盟数据已经初始化！</font>
</td></tr>
~;

if (open(SFFILE,"${lbdir}data/shareforums.cgi")) {
#    flock(SFFILE, 1) if ($OS_USED eq "Unix");
    @lmforums = <SFFILE>;
    close(SFFILE);
    $lmforums = @lmforums;
}
$uniontitle="<font color=$fontcolormisc>（共有 $lmforums 个联盟论坛）</font>";
$unionoutput = "";
  if (($lmforums ne "")&&($lmforums > 0)) {
    $unionoutput .= qq~
<tr><td bgcolor=\$titlecolor colspan=2  \$catbackpic>
<font color=\$titlefontcolor><b>-=> 联盟论坛 $uniontitle</b>　 [<a href=leobbs.cgi?action=union><font color=$fontcolormisc>\$unionview</font></a>]　 [<span style="cursor:hand" onClick="javascript:openScript('lmcode.cgi',480,240)">论坛联盟代码</span>]
</td></tr>~;

$unionoutput1 = "";
	$lmtexts = "";
	$lmlogos = "";
	foreach $lmforum (@lmforums) {
	    chomp $lmforum;
            next if ($lmforum eq "");
            ($lmforumname,$lmforumurl,$lmforuminfo,$lmforumorder,$lmweblogo) = split(/\t/,$lmforum);
            if (($lmweblogo ne "")&&($lmweblogo ne "http:\/\/")) { $lmlogos .= qq~<a href=$lmforumurl target=_blank onmouseover="document.all.lmforum.stop();" onmouseout="document.all.lmforum.start();"><img src=$lmweblogo width=88 height=31 border=0 title="$lmforumname\n$lmforuminfo"></a> ~; }
            else { $lmtexts .= qq~<a href=$lmforumurl target=_blank title="$lmforuminfo" onmouseover="document.all.lmforum1.stop();" onmouseout="document.all.lmforum1.start();">$lmforumname</a>　~; }
	}
	$unionoutput1 .= qq~<tr><td bgcolor=\$forumcolorone width=26 align=center><img src=$imagesurl/images/\$skin/shareforum.gif width=16></td><td bgcolor=\$forumcolortwo width=*><table width=100% cellpadding=0 cellspacing=0><tr><td width=100%><img src=\$imagesurl/images/none.gif width=500 height=1><BR><marquee name="lmforum" id="lmforum"  behavior="alternate" direction="left" scrollamount="4" scrolldelay="1" hspace="0" vspace="0">$lmlogos</marquee></td><td width=100 align=right><a href=http://bbs.leobbs.com/ target=_blank><img src=$imagesurl/images/leobbs8831.gif width=88 height=31 border=0 title="极酷超级论坛最新软件、影视、音乐、网络安全、图形艺术、游戏、CGI 知识等综合论坛，还可以聊天。。。"></a></td></tr></table></td></tr>~ if ($lmlogos ne "");
	$unionoutput1 .= qq~<tr><td bgcolor=\$forumcolorone width=26 align=center><img src=$imagesurl/images/\$skin/shareforum.gif width=16></td><td bgcolor=\$forumcolortwo width=*><table width=100% cellpadding=0 cellspacing=0><tr><td width=100%><img src=\$imagesurl/images/none.gif width=500 height=1><BR><marquee name="lmforum1" id="lmforum1"  behavior="alternate" direction="left" scrollamount="4" scrolldelay="1" hspace="0" vspace="0">$lmtexts</marquee></td></tr></table></td></tr>~ if ($lmtexts ne "");

  }

mkdir ("${lbdir}cache", 0777) if (!(-e "${lbdir}cache"));
open (FILE, ">${lbdir}data/unionoutput.pl");
$unionoutput   =~ s/\(/\\\(/isg;
$unionoutput   =~ s/\)/\\\)/isg;
$unionoutput1  =~ s/\(/\\\(/isg;
$unionoutput1  =~ s/\)/\\\)/isg;
print FILE qq~if (\$union==0) { \$unionview="显示联盟列表"; } else { \$unionview="关闭联盟列表"; }\n
\$output .= qq($unionoutput);\n
\$output .= qq($unionoutput1) if (\$union == 1);
~;
print FILE "1;\n";
close (FILE);

}
sub dochangedir {

    my $x = &myrand(1000000000);
    $x = crypt($x, aun);
    $x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
    $x =~ s/[^\w\d]//g;
    $x = substr($x, 2, 9);
    $memdir    = "members$x"  if (rename("$lbdir$memdir",     "${lbdir}members$x"));
    $msgdir    = "messages$x" if (rename("$lbdir$msgdir",     "${lbdir}messages$x"));

    opendir (DIRS, "$lbdir");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^\w+?$/i, @files);
    my @ftpdir = grep(/^ftpdata/i, @files);
    $ftpdir = $ftpdir[0];
    my @memfavdir = grep(/^memfav/i, @files);
    $memfavdir = $memfavdir[0];
    my @saledir = grep(/^sale/i, @files);
    $saledir = $saledir[0];
    my @searchdir = grep(/^search/i, @files);
    $searchdir = $searchdir[0];
    my @recorddir = grep(/^record/i, @files);
    $recorddir = $recorddir[0];
    my $x = &myrand(1000000000);
    $x = crypt($x, aun);
    $x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
    $x =~ s/[^\w\d]//g;
    $x = substr($x, 2, 9);
    $searchdir = "search$x"   if (rename("$lbdir$searchdir",  "${lbdir}search$x"));
    $ftpdir    = "ftpdata$x"  if (rename("$lbdir$ftpdir",     "${lbdir}ftpdata$x"));
    $memfavdir = "memfav$x"   if (rename("$lbdir$memfavdir",  "${lbdir}memfav$x"));
    $recorddir = "record$x"   if (rename("$lbdir$recorddir",  "${lbdir}record$x"));
    $saledir   = "sale$x"     if (rename("$lbdir$saledir",    "${lbdir}sale$x"));

my $x = &myrand(1000000000);
$x = crypt($x, aun);
$x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
$x =~ s/[^\w\d]//g;
$x = substr($x, 2, 9);
$usrdir    = "usr$x"      if (rename("$imagesdir$usrdir", "${imagesdir}usr$x"));

    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>重要目录名称变换</b><p>
<font color=#333333>所有重要目录的名称都已经变化完成！</font>
</td></tr>
~;

}

sub dodellock {
    opendir (DIRS, "${lbdir}lock");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	chomp $_;
	unlink ("${lbdir}lock/$_");
    }
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>初始化锁定文件</b><p>
<font color=#333333>所有锁定文件已经初始化！</font>
</td></tr>
~;
}

sub doinit  {
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>初始化论坛数据</b><p>
<font color=#333333>首次运行论坛必须运行，以后如果更新了论坛表情图片等，也需要运行！<BR>没有特别说明的初始化是不会丢失数据的，请放心使用！</font><BR><BR>
</td></tr>
<tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>* <b><a href="$thisprog?action=upskinselect">初始化初始化论坛风格选择列表</a></b>　 <font color=red>(第一次安装后必须运行一次)</font><br>
    初始化论坛风格选择列表其实不会自动更新的，除非你在这儿更新一下。如果更新论坛风格，也需要运行！<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>1．<b><a href="$thisprog?action=uptop">初始化用户排名</a></b>　 <font color=red>(第一次安装后必须运行一次)</font><br>
    用户排名其实不会自动更新的，除非你在这儿更新一下。<BR><BR>
    </td>
    </tr>
    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>2．<b><a href="$thisprog?action=dogetold">用户数据整理</a></b>　 <font color=red>(第一次安装后必须运行一次)</font><br>
    对用户数据进行整理，保证论坛高速运行。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>3．<b><a href="$thisprog?action=upemot">初始化表情图片和 EMOT 图片</a></b>　 <font color=red>(第一次安装后必须运行一次)</font><br>
    表情图片和 EMOT 其实不会自动更新的，除非你在这儿更新一下。<BR><BR>
    </td>
    </tr>
    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>4．<b><a href="$thisprog?action=upuser">初始化用户头像图片</a></b>　 <font color=red>(第一次安装后必须运行一次)</font><br>
    用户头像其实不会自动更新的，除非你在这儿更新一下。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>5．<b><a href="$thisprog?action=upupload">初始化文件上传目录属性！</a></b>　 <font color=red>(第一次安装后必须运行一次)</font><br>
    如果您的论坛无法正常支持帖子内贴文件上传、上传头像文件、文件下载计数时，可以在这里初始化一下，大部分问题都可以解决(如果论坛的文件上传正常的话，则无须运行此步)。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>6．<b><a href="$thisprog?action=uppost">初始化论坛帖子目录和数据文件属性</a></b>　 <font color=red>(第一次安装后必须运行一次)</font><br>
    如果您的论坛有些数据无法更新、帖子无法发表或回复之类时，可以在这里初始化一下，大部分问题都可以解决(如果论坛的数据正常的话，则无须运行此步)。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>7．<b><a href="$thisprog?action=upmessage">初始化短消息目录和文件属性</a></b>　 <font color=red>(第一次安装后必须运行一次)</font><br>
    如果您的论坛短消息的收发有问题时，可以在这里初始化一下，大部分问题都可以解决(如果论坛的短消息收发正常的话，则无须运行此步)。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>8．<b><a href="$thisprog?action=dellock">初始化锁定文件</a></b><br>
    如果你的锁定文件目录中有多余的或者删除不掉的锁定文件的话，可以在这里初始化一下。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>9．<b><a href="$thisprog?action=changedir">重要目录名称变化</a></b><br>
    重要目录的名称在安装之时就已经变化保密，为了更加保证安全，您可以在这里重新变化目录名称。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>10．<b><a href="$thisprog?action=uponlineuser" OnClick="return confirm('此操作是不可恢复的，确定么？');">初始化在线统计</a></b><br>
    如果你的在线人数统计数据出错的话(比如总是只有你一个人在线)，可以在这里初始化一下(所有的用户将全部被视为不在线)。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>11．<b><a href="$thisprog?action=upconter" OnClick="return confirm('此操作是不可恢复的，确定么？');">初始化访问次数</a></b><br>
    如果你的访问次数统计和最大在线人数等数据出错的话(比如访问次数总是1)，可以在这里初始化一下(访问次数统计和最大在线人数都将清空)。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>12．<b><a href="$thisprog?action=shareforums" OnClick="return confirm('此操作是不可恢复的，确定么？');">初始化联盟数据</a></b><br>
    如果你的联盟数据删除不掉或是出错的话，可以在这里初始化一下。(所有的联盟数据将全部丢失)<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>13．<b><a href="$thisprog?action=delxzb" OnClick="return confirm('此操作是不可恢复的，确定么？');">初始化所有论坛的小字报</a></b><br>
    如果您要清除所有论坛的小字报时，可以在这里初始化一下(所有的小字报将全部丢失)。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>14．<b><a href="$thisprog?action=delans" OnClick="return confirm('此操作是不可恢复的，确定么？');">初始化所有论坛的公告</a></b><br>
    如果您要清除所有论坛的公告时，可以在这里初始化一下(所有的公告将全部丢失)。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>15．<b><a href="$thisprog?action=delmessage" OnClick="return confirm('此操作是不可恢复的，确定么？');">清空所有短消息</a></b><br>
    如果您要清除所有的短消息时，可以在这里初始化一下(所有的短消息将全部丢失)。<BR><BR>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>16．<b><a href="$thisprog?action=delcache">清空所有缓存</a></b><br>
    如果您要清除所有的缓存时，可以在这里初始化一下(为了提高系统效率，最好10-20天定期清空一次)。<BR><BR>
    </td>
    </tr>
         ~;
}     

print qq~</td></tr></table></body></html>~;
exit;