#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

###获取真实的 IP 地址
use strict;
use warnings;
use diagnostics;

$ipaddress = $ENV{'REMOTE_ADDR'};
$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
$ipaddress = $trueipaddress if (($trueipaddress ne "") && ($trueipaddress ne "unknown"));
$trueipaddress = $ENV{'HTTP_CLIENT_IP'};
$ipaddress = $trueipaddress if (($trueipaddress ne "") && ($trueipaddress ne "unknown"));
$ipaddress =~ s/[^\d\.]//g;

###获取进程随机ID
eval('use Digest::MD5 qw(md5_hex);');
$sessionid = int(&myrand(100000));
$sessionid = crypt($sessionid, aun);
$sessionid =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
$sessionid =~ s/\.//g;
$sessionid =~ s/\|//g;
$sessionid = substr($sessionid, 4, 7);
$sessionid = md5_hex($sessionid);

###生成随机验证码
$verifynum = int(&myrand(10000));
$verifynum = sprintf("%04d", $verifynum);

###获取当前时间
$currenttime = time;

#清除过期校验文件
mkdir("${imagesdir}verifynum", 0777) unless (-d "${imagesdir}verifynum");
chmod(0777, "${imagesdir}verifynum");
opendir(DIR, "${imagesdir}verifynum");
@verifyfiles = readdir(DIR);
closedir(DIR);
@verifyfiles1 = grep (/\.bmp$/i, @verifyfiles);
foreach (@verifyfiles1) {unlink("${imagesdir}verifynum/$_") if (-M "${imagesdir}verifynum/$_" > 0.004);}
@verifyfiles1 = grep (/\.png$/i, @verifyfiles);
foreach (@verifyfiles1) {unlink("${imagesdir}verifynum/$_") if (-M "${imagesdir}verifynum/$_" > 0.004);}

mkdir("${lbdir}verifynum", 0777) unless (-d "${lbdir}verifynum");
chmod(0777, "${lbdir}verifynum");
opendir(DIR, "${lbdir}verifynum");
@verifyfiles = readdir(DIR);
closedir(DIR);
@verifyfiles = grep (/\.cgi$/i, @verifyfiles);
foreach (@verifyfiles) {unlink("${lbdir}verifynum/$_") if (-M "${lbdir}verifynum/$_" > 0.004);}

###将当前进程验证码保存
my $filetomake = "${lbdir}verifynum/$sessionid.cgi";
open(FILE, ">$filetomake");
print FILE "$verifynum\t$currenttime\t$ipaddress";
close(FILE);

if ($verifyusegd eq "no") {
    #BMP图片生成
    local @n0 = ("3c", "66", "66", "66", "66", "66", "66", "66", "66", "3c");
    local @n1 = ("1c", "0c", "0c", "0c", "0c", "0c", "0c", "0c", "1c", "0c");
    local @n2 = ("7e", "60", "60", "30", "18", "0c", "06", "06", "66", "3c");
    local @n3 = ("3c", "66", "06", "06", "06", "1c", "06", "06", "66", "3c");
    local @n4 = ("1e", "0c", "7e", "4c", "2c", "2c", "1c", "1c", "0c", "0c");
    local @n5 = ("3c", "66", "06", "06", "06", "7c", "60", "60", "60", "7e");
    local @n6 = ("3c", "66", "66", "66", "66", "7c", "60", "60", "30", "1c");
    local @n7 = ("30", "30", "18", "18", "0c", "0c", "06", "06", "66", "7e");
    local @n8 = ("3c", "66", "66", "66", "66", "3c", "66", "66", "66", "3c");
    local @n9 = ("38", "0c", "06", "06", "3e", "66", "66", "66", "66", "3c");

    for (my $i = 0; $i < 10; $i++) {
        for (1 .. 6) {
            my $a1 = substr("012", int(myrand(3)), 1) . substr("012345", int(myrand(6)), 1);
            my $a2 = substr("012345", int(myrand(6)), 1) . substr("0123", int(myrand(4)), 1);
            int(myrand(2)) eq 1 ? push(@{"n$i"}, $a1) : unshift(@{"n$i"}, $a1);
            int(myrand(2)) eq 0 ? push(@{"n$i"}, $a1) : unshift(@{"n$i"}, $a2);
        }
    }

    my @bitmap = ();

    for (my $i = 0; $i < 20; $i++) {
        for (my $j = 0; $j < 4; $j++) {
            my $n = substr($verifynum, $j, 1);
            my $bytes = ${"n$n"}[$i];
            my $a = int(myrand(15));
            $a eq 1 ? $bytes =~ s/9/8/g : $a eq 3 ? $bytes =~ s/c/e/g : $a eq 6 ? $bytes =~ s/3/b/g : $a eq 8 ? $bytes =~ s/8/9/g : $a eq 0 ? $bytes =~ s/e/f/g : 1;
            push(@bitmap, $bytes);
        }
    }
    for ($i = 0; $i < 8; $i++) {
        my $a = substr("012", int(myrand(3)), 1) . substr("012345", int(myrand(6)), 1);
        unshift(@bitmap, $a);
        push(@bitmap, $a);
    }

    my $image = '424d9e000000000000003e0000002800';
    $image .= "00002000000018000000010001000000";
    $image .= "00006000000000000000000000000000";
    $image .= "00000000000000000000FFFFFF00";
    $image .= join('', @bitmap);
    $image = pack('H*', $image);

    ###生成图片文件
    my $filetomake = "${imagesdir}verifynum/$sessionid.bmp";
    open(FILE, ">$filetomake");
    binmode(FILE);
    print FILE $image;
    close(FILE);
}
else {
    my $a = length $verifynum;
    my $font = GD::gdGiantFont();
    my $dx = int(($font->width + 11) * $a);
    my $dy = 29 + $font->height;
    my $image = GD::Image->new($dx, $dy);
    my $background = $image->colorAllocate(0, 0, 0);
    my $txt = $image->colorAllocate(255, 255, 255);
    $image->filledRectangle(0, 0, $dx, $dy, $background);
    $addwidth = 0;
    foreach (0 .. $a) {
        $addwidth1 = $_ + int(myrand(7) + 1) * int(myrand(2) + 1) - 1;
        $addwidth = $addwidth + $addwidth1;
        $addheight = int(myrand(30)) + 2;
        $image->string($font, $addwidth, $addheight, substr($verifynum, $_, 1), $txt);
        $image->string($font, $addwidth + int(myrand(2)) + 1, $addheight, substr($verifynum, $_, 1), $txt);
        $addwidth = $addwidth + $font->width;
    }
    foreach (0 .. int($a * $a * $a)) {
        my $tmpx = int(myrand(30)) + 1;
        my $tmpx1 = int(myrand($dx - 30)) + 1;
        my $tmpy = int(myrand(5)) + 1;
        my $tmpy1 = int(myrand($dy - 5)) + 1;
        $image->setPixel($tmpx + 1, $tmpy1 + 1, $txt);
        $image->setPixel($dx - $tmpx - 1, $tmpy1 + 1, $txt);
        $image->setPixel($tmpx1 + 1, $tmpy + 1, $txt);
        $image->setPixel($tmpx1 + 1, $dy - $tmpy - 1, $txt);
    }
    $image->line(int(myrand(15)), int(myrand(5)), $dx - int(myrand(20)), $dy - int(myrand(5)), $txt);

    $image->line(0, int(myrand(10)), $dx, int(myrand(10)), $txt);

    $image->line(0, $dy - int(myrand(10)), $dx, $dy - int(myrand(10)), $txt);

    $image->line(0, $dx - int(myrand(10)), $dx, int(myrand(10)), $txt);

    $image->line(0, 25, $dx, 25, $txt);

    my $filetomake = "${imagesdir}verifynum/$sessionid.png";
    open(FILE, ">$filetomake");
    binmode(FILE);
    print FILE $image->png;
    close(FILE);
}
1;

sub myrand {
    my $max = shift;
    my $result;
    $max ||= 1;
    eval("\$result = rand($max);");
    return $result if ($@ eq "");
    $randseed = time unless ($randseed);
    my $x = 0xffffffff;
    $x++;
    $randseed *= 134775813;
    $randseed++;
    $randseed %= $x;
    return $randseed * $max / $x;
}
