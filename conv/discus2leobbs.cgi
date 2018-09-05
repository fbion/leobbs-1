#!/usr/bin/perl

############################################
# Discus 用户资料 --> LeoBBS 用户资料转换器#
############################################

$discusmember = "/path/to/UBB members dir/";   	# 输入 Discus 用户资料所在的目录的绝对路径，最后不要遗漏 / 。
$leobbsmember = "/path/to/leobbs members dir/"; # 请输入 LeoBBS 用户资料所在的目录的绝对路径，最后不要遗漏 / ，注意设置 777 属性。

$date = time();
print "Content-Type: text/html\n\n";
print "<html><body>";
print "<center><h1><b><u>用户转换 （Discus --> LeoBBS）</u></b></h1><br><br><br><br><br><br><br><center><h2><b>开始处理</b></h2>";
open(DATEI,"${discusmember}user.txt") || die "Discus 用户库没有找到";
@memberlist=<DATEI>;
close(DATEI);
mkdir(newmember,0777);
$i=0;
$point=0;
foreach $zeile (@memberlist)
{
$i++;
$point++;
print "<b>.<b>";
if ($point > 100)
{
print "<br>";
$point = 0
}
$zeile =~ tr/[:]/[|]/;
@member = split(/\|/,$zeile);
$name = @member[0];
$passwort = @member[1];
$email = @member[2];
$filenames = $name;
$filenames =~ s/ /_/gi;
$filenames =~ tr/A-Z/a-z/;

$memberarray = "$name\t$passwort\tMember\tme\t0|0\t$email\tno\t\thttp://\t\t\t\t\t$date\tNot Posted\t\t\t\tnoavatar\t";
@memberarray = ($memberarray);
open(MEMBERDATEI,">${leobbsmember}$filenames.cgi");
print MEMBERDATEI "@memberarray";
close(MEMBERDATEI);
}
print "<BR><BR>总共转换了 $i 个用户！<BR><BR>\n";
exit;
