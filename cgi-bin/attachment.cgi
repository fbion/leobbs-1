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

use strict;
use warnings;
use diagnostics;
use diagnostics;

use LBCGI;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
$LBCGI::POST_MAX = 5000000;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "attachment.cgi";
$query = new LBCGI;

$inforum = $query->param('forum');
$intopic = $query->param('topic');

if ($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '' && $pvtdown ne "no") {
    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
    print qq~<script>alert('请不要盗链$boardname的连接');location.href='topic.cgi?forum=$inforum&topic=$intopic';</script>~;
    exit;
}

$inpostno = $query->param('postno');
$fileext = $query->param('type');
$fileext =~ s/\.//sg;
$fileext =~ s/\///sg;
$fileext =~ s/\\//sg;
$fileext = &stripMETA($fileext);
$fileext = lc($fileext);
$filename = $query->param('name');
$filename =~ s/\.\.//sg;
$filename =~ s/\///sg;
$filename =~ s/\\//sg;
$filename = substr($filename, 0, 32) if (length($filename) > 32);

&error('打开文件&老大，别乱黑我的程序呀！！') if ($inpostno !~ /^\d+$/ && $inpostno ne "");
&error('打开文件&老大，别乱黑我的程序呀！！') if ($inforum !~ /^\d+$/ || $intopic !~ /^\d+$/ || $fileext eq '');
require "data/style$inforum.cgi" if (-e "${lbdir}data/style$inforum.cgi");

$inselectstyle = $query->cookie("selectstyle");
$inselectstyle = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~ m/\//) || ($inselectstyle =~ m/\\/) || ($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$inpostno--;

$inmembername = $query->cookie("amembernamecookie") unless ($inmembername);
$inpassword = $query->cookie("apasswordcookie") unless ($inpassword);
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if (!$inmembername || $inmembername eq "客人") {
    if ($regaccess eq 'on' || $privateforum eq 'yes') {
        print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        print qq~<script language="JavaScript">document.location = "loginout.cgi?forum=$inforum";</script>~;
        exit;
    }
    $inmembername = '客人';
    $rating = -6;
    &error("普通错误&客人不能查看附件，请注册或登录后再试") if ($guestregistered eq "off" && $pvtdown ne "no");
}
else {
    &getmember($inmembername, 'no');
    &error('普通错误&此用户根本不存在！') if ($userregistered eq 'no');
    &error('普通错误&密码与用户名不相符，请重新登录！') if ($inpassword ne $password);
}

&getoneforum($inforum);
$testentry = $query->cookie("forumsallowed$inforum");
$allowed = $allowedentry{$inforum} eq 'yes' || ($testentry eq $forumpass && $testentry ne '') || $membercode eq 'ad' || $membercode eq 'smo' || $inmembmod eq 'yes' ? 'yes' : 'no';
&error("进入私有论坛&对不起，您没有权限进入该私有论坛！") if ($privateforum eq 'yes' && $allowed ne 'yes' && $pvtdown ne "no");
&error("进入论坛&你一般会员不允许进入此论坛！") if ($startnewthreads eq 'cert' && (($membercode ne 'ad' && $membercode ne 'smo' && $membercode ne 'cmo' && $membercode ne 'mo' && $membercode !~ /^rz/) || $inmembername eq '客人') && $userincert eq 'no' && $pvtdown ne "no");
&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz !~ /,$membercode,/);
if ($allowusers ne '') {
    &error('进入论坛&你不允许进入该论坛！') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad' && $pvtdown ne "no");
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0) {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        &error("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
        &error("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

if ($filename eq "") {
    $file = $inpostno > 0 ? "$inforum\_$intopic\_$inpostno\.$fileext" : "$inforum\_$intopic\.$fileext";
    &error("打开文件&此文件不存在！") unless (-e "$imagesdir$usrdir/$inforum/$file");
    $filename = $file;
    $newformat = 0;
}
else {
    $tmptopic = $intopic % 100;
    $file = "$tmptopic/$filename\.$fileext";
    &error("打开文件&此文件不存在！") unless (-e "$imagesdir$usrdir/$inforum/$file");
    $filename = "$filename\.$fileext";
    $newformat = 1;
}

if (open(FILE, "${lbdir}forum$inforum/$intopic.thd.cgi")) {
    sysread(FILE, my $thread, (stat(FILE))[7]);
    close(FILE);
    $thread =~ s/\r//isg;
    @threads = split(/\n/, $thread);
}

if ($membercode eq "ad" or $membercode eq "smo" or $inmembmod eq "yes") {
    $viewhide = 1;
}
else {
    $viewhide = 0;
    if ($hidejf eq "yes") {
        my @viewhide = grep (/^$inmembername\t/i, @threads);
        $viewhide = @viewhide;
        $viewhide = 1 if ($viewhide >= 1);
    }
}
$StartCheck = $numberofposts + $numberofreplys;

my ($poster, undef, undef, undef, undef, undef, $post1, undef) = split(/\t/, $threads[$inpostno]);

if ($hidejf eq "yes" && $pvtdown ne "no") {
    if ($post1 =~ /(\[hide\])(.+?)(\[\/hide\])/is) {
        if ($viewhide ne "1") {
            if ($newformat eq 0) {
                &error("普通错误&由于你没有回复过这个主题，所以你无权下载这个加密附件！");
            }
            else {
                while ($post1 =~ /(\[hide\])(.+?)(\[\/hide\])/is) {
                    &error("普通错误&由于你没有回复过这个主题，所以你无权下载这个加密附件！") if ($2 =~ /$filename/);
                    $post1 =~ s/(\[hide\])(.+?)(\[\/hide\])//is;
                }
            }
        }
    }
}

if ($postjf eq "yes" && $pvtdown ne "no") {
    if ($post1 =~ m/\[post=(.+?)\](.+?)\[\/post\]/isg) {
        $viewusepost = $1;
        unless (($StartCheck >= $viewusepost) || ($membercode eq "ad") || ($membercode eq "smo") || ($inmembmod eq "yes") || ($poster eq $inmembername)) {
            if ($newformat eq 0) {
                &error("普通错误&你无权下载这个加密附件！需要发贴达到$viewusepost，而你只有$StartCheck。");
            }
            else {
                while ($post1 =~ /\[post=(.+?)\](.+?)\[\/post\]/is) {
                    &error("普通错误&你无权下载这个加密附件！需要发贴达到$viewusepost，而你只有$StartCheck。") if ($2 =~ /$filename/);
                    $post1 =~ s/\[post=(.+?)\](.+?)\[\/post\]//is;
                }
            }
        }
    }
}

if ($jfmark eq "yes" && $pvtdown ne "no") {
    if ($post1 =~ m/\[jf=(.+?)\](.+?)\[\/jf\]/isg) {
        $jfpost = $1;
        unless (($jfpost <= $jifen) || ($membercode eq "ad") || ($membercode eq "smo") || ($inmembmod eq "yes") || ($poster eq $inmembername)) {
            if ($newformat eq 0) {
                &error("普通错误&你无权下载这个加密附件！积分必须达到 $jfpost，而你只有$jifen。");
            }
            else {
                while ($post1 =~ /\[jf=(.+?)\](.+?)\[\/jf\]/is) {
                    &error("普通错误&你无权下载这个加密附件！积分必须达到 $jfpost，而你只有$jifen。") if ($2 =~ /$filename/);
                    $post1 =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//is;
                }
            }
        }
    }
}

if ($wwjf ne "no" && $pvtdown ne "no") {
    if ($post1 =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/sg) {
        unless (($inmembername eq $poster) || ($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes") || ($rating >= $1)) {
            &error("普通错误&你无权下载这个加密附件！需要威望$1，而你只有$rating。")
        }
    }
}

if ($cansale ne "no" && $pvtdown ne "no") {
    if ($post1 =~ /LBSALE\[(.*?)\]LBSALE/sg) {
        my $postno = $inpostno;
        #    	    $postno ++;
        my $isbuyer = "";
        my $allbuyer = "";
        if (open(FILE, "${lbdir}$saledir/$inforum\_$intopic\_$postno.cgi")) {
            my $allbuyer = <FILE>;
            close(FILE);
            chomp $allbuyer;
            $allbuyer =~ s/\t\t/\t/isg;
            $allbuyer =~ s/\t$//gi;
            $allbuyer =~ s/^\t//gi;
            $allbuyer = "\t$allbuyer\t";
            $isbuyer = "yes" if ($allbuyer =~ /\t$inmembername\t/i);
        }
        unless (($inmembername eq $poster) || ($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes") || ($isbuyer eq "yes")) {
            &error("普通错误&因为你没有购买，所以你无权下载这个加密附件！");
        }
    }
}

$file2 = "$imagesurl/$usrdir/$inforum/$file";
$file = "$imagesdir$usrdir/$inforum/$file";

if ($picwater eq "yes") {
    eval ('use GD;');
    if ($@) {
        $picwater = "no";
    }
}

if ($picwater eq "yes") {
    $picwaterman = 1 if ($picwaterman eq "");

    if ($picwaterman eq "0") {$picwater = "no" if ($inmembername ne '客人');}
    elsif ($picwaterman eq "1") {$picwater = "no" if ($inmembername ne '客人' && $membercode ne "me");}
    elsif ($picwaterman eq "2") {$picwater = "no" if ($inmembername ne '客人' && $membercode ne "me" && $membercode !~ /^rz/);}
    elsif ($picwaterman eq "3") {$picwater = "no" if ($membercode eq "ad" || $membercode eq "smo");}
    elsif ($picwaterman eq "4") {$picwater = "no" if ($membercode eq "ad");}
}

if ($picwater eq "yes" && ($fileext eq 'jpg' || $fileext eq 'jpeg' || $fileext eq 'png')) {
    $filesize = (stat("$file"))[7];
    $fileext = 'jpeg' if ($fileext eq 'jpg');

    if (-e "$file.waterpicture") {
        $BOF = 0;
        $EOF = (-s "$file.waterpicture");
        $fileext = 'jpeg' if ($fileext eq 'jpg');

        $HTTP_RANGE = $ENV{HTTP_RANGE};
        if ($HTTP_RANGE ne '' && $HTTP_RANGE =~ /^bytes=([0-9]+)\-([0-9]+)$/ && $1 > -1 && $1 < $2 && $2 <= $EOF) {
            ($BOF, $EOF) = ($1, $2);
            print "HTTP/1.1 206 Partial Content\n";
            print "Accept-Ranges: bytes\n";
            print "Content-Range: bytes $BOF-$EOF/" . ($EOF + 1) . "\n";
            $EOF++;
        }
        $filesize = $EOF - $BOF;
        print "Accept-Ranges: bytes\n";
        print "Content-Length: $filesize\n";
        print "Content-Disposition:$fileadd filename=$filename\n";
        print "Content-Type: $fileext\n\n";
        binmode(STDOUT);
        print &readattachment("$file.waterpicture", $BOF, $EOF);
        exit;
    }

    print header(-type => "image/$fileext", -attachment => $filename, -expires => '0', -content_length => $filesize);

    if ($fileext eq "jpeg") {
        eval {$image = GD::Image->newFromJpeg($file, 1);};
        $image = GD::Image->newFromJpeg($file) if ($@);
    }
    else {
        eval {$image = GD::Image->newFromPng($file, 1);};
        $image = GD::Image->newFromPng($file) if ($@);
    }

    if ($waterpic eq "") {

        $watername = "http://bbs.leobbs.com/" if ($watername eq "");

        my ($imwidth, $imheight) = $image->getBounds();

        my $font = GD::gdLargeFont();
        my $fontwidth = $font->width * length $watername;

        my $background = $image->colorAllocate(0, 0, 0);
        my $txt1 = $image->colorAllocate(255, 255, 255);
        my $txt2 = $image->colorAllocate(0, 0, 0);

        if ($imheight > 40 && $imwidth > 200) {
            # 小于 200*40 的图片不加水印
            if ($picwaterplace1 eq "yes") {
                # 左上角
                $image->string($font, 10, 11, $watername, $txt2);
                $image->string($font, 11, 11, $watername, $txt2);
                $image->string($font, 9, 10, $watername, $txt1);
                $image->string($font, 10, 10, $watername, $txt1);
            }
            if ($picwaterplace2 eq "yes") {
                # 左下角
                $image->string($font, 10, $imheight - 20 + 1, $watername, $txt2);
                $image->string($font, 11, $imheight - 20 + 1, $watername, $txt2);
                $image->string($font, 9, $imheight - 20, $watername, $txt1);
                $image->string($font, 10, $imheight - 20, $watername, $txt1);
            }
            if ($picwaterplace3 eq "yes") {
                # 右上角
                $image->string($font, $imwidth - $fontwidth - 9 + 1, 11, $watername, $txt2);
                $image->string($font, $imwidth - $fontwidth - 10 + 1, 11, $watername, $txt2);
                $image->string($font, $imwidth - $fontwidth - 9, 10, $watername, $txt1);
                $image->string($font, $imwidth - $fontwidth - 10, 10, $watername, $txt1);
            }
            if ($picwaterplace4 eq "yes") {
                # 右下角
                $image->string($font, $imwidth - $fontwidth - 9 + 1, $imheight - 20 + 1, $watername, $txt2);
                $image->string($font, $imwidth - $fontwidth - 10 + 1, $imheight - 20 + 1, $watername, $txt2);
                $image->string($font, $imwidth - $fontwidth - 9, $imheight - 20, $watername, $txt1);
                $image->string($font, $imwidth - $fontwidth - 10, $imheight - 20, $watername, $txt1);
            }
        }
    }
    else {

        eval {$image1 = GD::Image->newFromPng("${imagesdir}myimages/$waterpic", 1);};
        $image1 = GD::Image->newFromPng("${imagesdir}myimages/$waterpic") if ($@);

        my ($width, $height) = $image1->getBounds();           # 得到水印logo图尺寸
        $image1->transparent($image1->colorAllocate(0, 0, 0)); # 得出黑色以及设logo的黑色为透明

        my ($imwidth, $imheight) = $image->getBounds(); # 得到主图的尺寸
        my ($zwidth, $zheight);

        # 如果主图宽大于logo宽2倍，高大于logo高2倍，则加水印
        if (((int($imwidth / 2)) > $width) && ((int($imheight / 2)) > $height)) {
            if ($picwaterplace1 eq 'yes' || $picwaterplace3 eq 'yes') {
                $zheight = 10;
            }
            else {
                $zheight = int($imheight - $height - 10);
            }

            if ($picwaterplace1 eq 'yes' || $picwaterplace2 eq 'yes') {
                $zwidth = 10;
            }
            else {
                $zwidth = int($imwidth - $width - 10);
            }
            $image->copy($image1, $zwidth, $zheight, 0, 0, $width, $height);
        }

    }

    open(FILEPIC, ">$file.waterpicture");
    binmode(FILEPIC);
    if ($fileext eq "jpeg") {
        print FILEPIC $image->jpeg;
    }
    else {
        print FILEPIC $image->png;
    }
    close(FILEPIC);

    binmode(STDOUT);
    if ($fileext eq "jpeg") {
        print $image->jpeg;
    }
    else {
        print $image->png;
    }
    exit;
}

if ($pvtdown ne "no") {
    $BOF = 0;
    $EOF = (-s $file);
    $fileext = 'jpeg' if ($fileext eq 'jpg');
    $fileext = 'html' if ($fileext eq 'htm');
    $fileext = 'plain' if ($fileext eq 'txt');
    if ($fileext =~ /^(gif|jpeg|png|bmp)$/) {
        $fileext = "image/$fileext";
        $fileadd = "";
    }
    elsif ($fileext eq 'swf') {
        $fileext = "application/x-shockwave-flash";
        $fileadd = "";
    }
    elsif ($fileext eq 'rm' || $fileext eq 'rmvb') {
        $fileext = "audio/x-pn-realaudio";
        $fileadd = "";
    }
    elsif ($fileext eq 'avi') {
        $fileext = "video/x-msvideo";
        $fileadd = "";
    }
    elsif ($fileext eq 'mpeg') {
        $fileext = "video/mpeg";
        $fileadd = "";
    }
    elsif ($fileext =~ /^(plain|html)$/) {
        $fileext = "text/$fileext";
        $fileadd = "";
    }
    else {
        $fileext = "attachment/$fileext";
        $fileadd = " attachment;";
    }

    $HTTP_RANGE = $ENV{HTTP_RANGE};
    if ($HTTP_RANGE ne '' && $HTTP_RANGE =~ /^bytes=([0-9]+)\-([0-9]+)$/ && $1 > -1 && $1 < $2 && $2 <= $EOF) {
        ($BOF, $EOF) = ($1, $2);
        print "HTTP/1.1 206 Partial Content\n";
        print "Accept-Ranges: bytes\n";
        print "Content-Range: bytes $BOF-$EOF/" . ($EOF + 1) . "\n";
        $EOF++;
    }
    $filesize = $EOF - $BOF;
    print "Accept-Ranges: bytes\n";
    print "Content-Length: $filesize\n";
    print "Content-Disposition:$fileadd filename=$filename\n";
    print "Content-Type: $fileext\n\n";
    binmode(STDOUT);
    print &readattachment($file, $BOF, $EOF);
    exit;
}
else {
    print header(-charset => "UTF-8", -location => $file2, -cache => yes);
    exit;
}
exit;

sub readattachment {
    open(FILE, $_[0]);
    binmode(FILE);
    seek(FILE, $_[1], 0);
    read(FILE, my $out, ($_[2] - $_[1]));
    close(FILE);
    $out;
}
