#!/usr/bin/perl

######################################
# WDB 帖子+用户资料 --> LeoBBS 转换器#
######################################

$wdbdir = "/path/to/WDB main dir/";       # 请输入WDB 主资料所在的目录的绝对路径，最后不要遗漏 / 。
$leobbsdir = "/path/to/LeoBBS main dir/"; # 请输入 LeoBBS 主资料所在的目录的绝对路径，最后不要遗漏 / ，注意设置好 777 属性。

$userhead= "g:/www/9438/wdbmember/";      # WDB 用户目录，最后不要遗漏 /
$leobbsmember = "g:/www/9438/leobbs/";    # LB5000 用户目录，最后不要遗漏 / ，注意设置 777 属性

################以下不用修改
$nowtime = time;
$ending = ".cgi";
print ("Content-type: text/html\n\n");
$userdir=$userhead;
chop $userdir;
opendir (MEMBERDIR, "$userdir");
  @stats = readdir(MEMBERDIR);
closedir (MEMBERDIR);
@stats = sort @stats;
$totaluserdata=$#stats+1;
for ($i=0;$i<$totaluserdata;$i++) {
$name = @stats[$i];
     $filesname="$userhead$name";
     open(file,"$filesname");
     @array=<file>;
     close(file);
     $wuyu = "@array";
     $wuyu =~ s/^\<\?die\(\)\;\?\>\|//isg;
    ($name,$password,$usericon,$email,$oicq,$regdate,$signature,$homepage,$area,$no,$no,$no,$postamount,$publicemail,$no)=split(/\|/,$wuyu);

    ($name,$temp)=split(/\./,$name);
     $name =~ s/ /_/gi;
     $name =~ tr/A-Z/a-z/;
    open(IBMEMBER,">$leobbsmember$name$ending");
    print IBMEMBER "$name\t$password\tMember\tme\t$postamount\t$email\t$publicemail\txxx.xxx.xxx.xxx\t$homepage\t$oicq\t$icqnumber\t$area\t\t$nowtime\tNot Posted\t$signature\t\t\t$usericon\t\t\t\t\t80\t80\t\n";
    close(IBMEMBER);
    print "用户 $UserName 已经成功转换成 LeoBBS 用户了！<BR>";
}

opendir (DIRS, "$wdbdir");
my @dirs1 = readdir(DIRS);
closedir (DIRS);
my @dirs1 = grep(/^forum/i, @dirs1);
$dir2 = @dirs1;

foreach $dirs1 (@dirs1) {
    if ($dirs1 !~ /forum[0-9]+$/) { $dir2--; next;}
    mkdir ("$leobbsdir/$dirs1", 0777);
    chmod (0777,"$leobbsdir/$dirs1");

    opendir (DIRS, "${wdbdir}$dirs1");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^f\_/i, @files);
    $a = 1;
    foreach $files1 (@files) {
        open (FILE, "${wdbdir}${dirs1}/$files1");
        @allthreads = <FILE>;
        close (FILE);
        open (FILE, ">${leobbsdir}${dirs1}/$a.thd.cgi");
        foreach $thread (@allthreads) {
            ($topictitle,$membername,$post,$postdate,$postipaddresstemp,$posticon,$showsignature) = split (/\|/,$thread);
            if ($showsignature eq 1) { $showsignature = "yes"; } else { $showsignature = "no"; }
            if ($posticon eq "ran") { $posticon = ""; }
            print FILE "$membername\t＊＃！＆＊$topictitle\t$postipaddresstemp=$postipaddresstemp\tyes\t$showsignature\t$postdate\t$post\t$posticon\t\n";
        }
        close (FILE);
        $a++;
    }
}
$dir1 = @dirs1;
print "<BR><BR>总共转换了 $dir2 个分论坛！<BR><BR>请立即进入管理区，修复论坛主界面，并对重建所有论坛一次\n";
exit;
