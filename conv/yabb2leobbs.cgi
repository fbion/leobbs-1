#!/usr/bin/perl

##########################################
# YaBB 用户资料 --> LeoBBS 用户资料转换器#
##########################################

$yabbdir   = "/path/to/YaBB members dir/";	#YaBB 用户目录，最后不要遗漏 / 
$leobbsdir = "/path/to/LeoBBS members dir/"; 	#LeoBBS 用户目录，最后不要遗漏 / ，注意设置 777 属性

print "Content-type: text/html\n\n";
print "YaBB --> LeoBBS 用户数据转换器<BR><BR>\n";

opendir (DIR, "$yabbdir");
@dirdata = readdir(DIR);
closedir (DIR);

@yabbers = grep(/dat/,@dirdata);
$time = time;

foreach (@yabbers) {
    open (YABB, "$yabbdir/$_");
    @member = <YABB>;
    close (YABB);

    $username = $_;
    $username =~ s/\.dat//g;

    foreach (@member) {
        chomp $_;
        }
    $membercode = "me";
    $password = $member[0];
    $name     = $member[1];
    $email    = $member[2];
    $www      = $member[4];
    $sig      = $member[5];
    $posts    = $member[6];
    $title    = $member[7];
    $icq      = $member[8];

    $sig =~ s/\&\&/<br>/g;

    if ($title ne "Administrator") { $title = "Member"; $membercode = "me"; }
    else { $membercode = "ad"; }

    $name = y/ /_/;

    my $file_name = "$leobbsdir" . "$name" . ".cgi";
    open (IKON, ">$file_name");
    print IKON "$name\t$password\t$title\t$membercode\t$posts\t$email\tyes\txxx.xx.xxx.xx\t$www\t\t$icq\t\t\t$time\t\%\%\%$time\%\%\%\t$sig\t0\t\t\t\t\t\t\t\t\t\n";
    close (IKON);
    $membercount ++;
    $lastmember = "$username";
    print "用户 $username 已经成功转换成 LeoBBS 用户了！<BR><BR>";
    $www = ""; $sig = ""; $icq = "";
    }
    
    print "总共转换了 $newtotal 个用户！<BR><BR>\n";
    exit;




