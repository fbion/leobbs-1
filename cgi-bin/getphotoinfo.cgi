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
use ExifTool;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") {$cookiepath = $mycookiepath;}
elsif ($COOKIE_USED eq 1) {$cookiepath = "";}
else {
    $boardurltemp = $boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
    #	$cookiepath =~ tr/A-Z/a-z/;
}

$in_forum = $query->param('forum');
$in_topic = $query->param('topic');
$inreply = $query->param('reply');
$intype = $query->param('ftype');
$inname = $query->param('fname');
$inname =~ s/\.\.//sg;
$inname =~ s/\///sg;
$inname =~ s/\\//sg;
$inname = substr($inname, 0, 32) if (length($inname) > 32);

$out = "";
$out = "老大，别乱黑我的程序呀！1" if ($inreply ne "" && $inname ne "");
$out = "老大，别乱黑我的程序呀！2" if ($inreply ne "" && $inname ne "");
$out = "老大，别乱黑我的程序呀！3" if ($inreply !~ /^[0-9]+$/ && $inreply ne "");
$out = "老大，别乱黑我的程序呀！4" if (($in_forum !~ /^[0-9]+$/) || ($in_topic !~ /^[0-9]+$/));
$out = "老大，别乱黑我的程序呀！！" unless (($intype eq "gif") || ($intype eq "jpg") || ($intype eq "jpe") || ($intype eq "jpeg") || ($intype eq "tif") || ($intype eq "png") || ($intype eq "bmp"));

if ($out eq "") {

    if ($inreply ne "") {
        $inreply--;
        if ($inreply eq 0) {$img = "${imagesdir}$usrdir/$in_forum/$in_forum\_$in_topic\.$intype";}
        else {$img = "${imagesdir}$usrdir/$in_forum/$in_forum\_$in_topic\_$inreply\.$intype";}
        $inreply++;
        $dispinfo = $inreply;
    }
    else {
        $tmptopic = $in_topic % 100;
        $img = "${imagesdir}$usrdir/$in_forum/$tmptopic/$inname\.$intype";
        $dispinfo = $inname;
    }
    my $tags = ExifTool::ImageInfo("$img");

    $name{"Make"} = "厂商";
    $name{"Model"} = "型号";
    $name{"Artist"} = "作者";
    $name{"DateTimeOriginal"} = "拍摄时间";
    $name{"CreateDate"} = "建立时间";
    $name{"DateTimeDigitized"} = "数字化时间";
    $name{"ModifyDate"} = "修改时间";
    $name{"FileSize"} = "文件大小";
    $name{"FileSource"} = "文件来源";
    $name{"Software"} = "软件";
    $name{"ExifImageWidth"} = "相机分辨率宽";
    $name{"ExifImageLength"} = "相机分辨率高";
    $name{"ImageWidth"} = "图像宽度";
    $name{"ImageHeight"} = "图像高度";
    $name{"ImageSize"} = "图像大小";
    $name{"ExposureTime"} = "曝光时间";
    $name{"ShutterSpeed"} = "快门";
    $name{"ShutterSpeedValue"} = "快门值";
    $name{"FNumber"} = "FNumber 光圈";
    $name{"Aperture"} = "Aperture 光圈";
    $name{"ApertureValue"} = "光圈值";
    $name{"MaxApertureValue"} = "最大光圈值";
    $name{"FocalLength"} = "焦距";
    $name{"FocalLengthIn35mmFormat"} = "35mm 焦距";
    $name{"FocalLength35efl"} = "35mm 焦距";
    $name{"DigitalZoomRatio"} = "数码变焦率";
    $name{"FocusMode"} = "变焦模式";
    $name{"ExposureMode"} = "曝光模式";
    $name{"ExposureCompensation"} = "曝光补偿";
    $name{"ExposureIndex"} = "曝光指数";
    $name{"ExposureProgram"} = "曝光控制";
    $name{"BrightnessValue"} = "亮度";
    $name{"ISO"} = "ISO 感光度";
    $name{"Sharpness"} = "锐度";
    $name{"Contrast"} = "对比度";
    $name{"Saturation"} = "饱和度";
    $name{"LightSource"} = "光源";
    $name{"ColorSpace"} = "色隙";
    $name{"Flash"} = "闪光灯";
    $name{"Slowsync"} = "闪光灯模式";
    $name{"WhiteBalance"} = "白平衡";
    $name{"MeteringMode"} = "测光模式";
    $name{"CustomRendered"} = "自定义补偿";
    $name{"ComponentsConfiguration"} = "成分构成";
    $name{"YCbCrPositioning"} = "色相定位";
    $name{"SceneType"} = "场景类型";
    $name{"Orientation"} = "方向";
    $name{"Compression"} = "压缩格式";
    $name{"CompressedBitsPerPixel"} = "压缩率";
    $name{"Quality"} = "压缩质量";
    $name{"XResolution"} = "X 方向分辨率";
    $name{"YResolution"} = "Y 方向分辨率";
    $name{"ResolutionUnit"} = "分辨率单位";
    $name{"FlashPixVersion"} = "FlashPix 版本";
    $name{"ExifVersion"} = "Exif 版本";
    $name{"Macro"} = "宏指令";
    $name{"Version"} = "相机版本";
    $name{"Comment"} = "标记说明";

    foreach ("Make", "Model", "Artist", "DateTimeOriginal", "CreateDate", "DateTimeDigitized", "ModifyDate", "FileSize", "FileSource", "Software", "ExifImageWidth", "ExifImageLength", "ImageWidth", "ImageHeight", "ImageSize", "ExposureTime", "ShutterSpeed", "ShutterSpeedValue", "FNumber", "Aperture", "ApertureValue", "MaxApertureValue", "FocalLength", "FocalLengthIn35mmFormat", "FocalLength35efl", "DigitalZoomRatio", "FocusMode", "ExposureMode", "ExposureCompensation", "ExposureIndex", "ExposureProgram", "BrightnessValue", "ISO", "Sharpness", "Contrast", "Saturation", "LightSource", "ColorSpace", "Flash", "Slowsync", "WhiteBalance", "MeteringMode", "CustomRendered", "ComponentsConfiguration", "YCbCrPositioning", "SceneType", "Orientation", "Compression", "CompressedBitsPerPixel", "Quality", "XResolution", "YResolution", "ResolutionUnit", "FlashPixVersion", "ExifVersion", "Macro", "Version", "Comment") {
        next if (($tags->{$_} eq "") || (length($tags->{$_}) > 30));
        $outfontcolor = "$postfontcolorone" if ($outfontcolor eq "$postfontcolortwo");
        $out .= "<font color=$outfontcolor>&nbsp;&nbsp;&nbsp;&nbsp;$name{$_}";
        $spaceit = "&nbsp;" x (26 - length($name{$_}));
        $out .= "$spaceit$tags->{$_}</font><BR>";
    }

    foreach (sort (keys %$tags)) {
        next if (($_ eq "MakerNoteUnknown") || ($_ eq "FileName"));
        next if (length($tags->{$_}) > 30);
        next if ($name{$_} ne "");
        next if (($tags->{$_} eq "") || ($tags->{$_} eq " ") || ($tags->{$_} eq "  ") || ($tags->{$_} eq "  "));
        $outfontcolor = "$postfontcolorone" if ($outfontcolor eq "$postfontcolortwo");
        $out .= "<font color=$outfontcolor>&nbsp;&nbsp;&nbsp;&nbsp;$_";
        $spaceit = "&nbsp;" x (26 - length($_));
        $out .= "$spaceit$tags->{$_}</font><BR>";
    }
    $out =~ s/\n//g;
    $out =~ s/\'/\\\'/g;
}
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
print <<"HTML";
<html>
<head> 
<title>图片信息</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
<SCRIPT>
<!--
//初始化内容值
parent.followTd$dispinfo.innerHTML='$out';
//已读取
parent.document.images.followImg$dispinfo.loaded='yes';
-->
</SCRIPT>
</body>
</html>
HTML

exit;
