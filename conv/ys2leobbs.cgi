#!/usr/bin/perl 

#########################################
# 一山草堂论坛用户资料 --> LeoBBS 转换器#
#########################################

$userhead= "/home/httpd/cgi-bin/qlbbs/members/";       	#一山草堂论坛用户目录，最后不要遗漏 /
$leobbsmember = "/home/httpd/cgi-bin/leobbs/members/";  #LeoBBS  用户目录，最后不要遗漏 / ，注意设置 777 属性

###############以下不必修改################# 

$ending = ".cgi";
print ("Content-type: text/html\n\n");
$userdir=$userhead;
chop $userdir;
opendir (MEMBERDIR, "$userdir");
  @stats = readdir(MEMBERDIR);
closedir (MEMBERDIR);
@stats = grep(/cgi$/, @stats);
@stats = sort @stats;
$totaluserdata=$#stats+1;
for ($i=0;$i<$totaluserdata;$i++) {
    $name = @stats[$i];
    $filesname="$userhead$name";
    open(file,"$filesname");
    @array=<file>;
    close(file);
    $wuyu = "@array"; 
#   ($Password,$UserName,$Email,$URL,$DateRegistered,$Signature,$rdsex,$rdwork,$Location,$rdlove,$rdfy,$rdhf,$AvatarWording,$jiao,$iewin,$OICQnumber,$photo)=split(/|/,$wuyu);
    ($UserName,$Password,$Email,$URL,$rdsex,$xx,$yy,$jj,$Signature,$rdwork,$Location1)=split(/\|/,$wuyu);
    $AvatarWording="";$Location="";

    $TotalPosts = $rdfy+$rdhf;
    ($name,$temp)=split(/\./,$name);
    $DateRegistered = time();
    $name =~ s/ /_/gi;
    $name =~ tr/A-Z/a-z/;
    $name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\=\+\\\[\]\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    open(IBMEMBER,">$leobbsmember$name$ending");
    print IBMEMBER "$UserName\t$Password\tMember\tme\t$TotalPosts\t$Email\tyes\t保密\t$URL\t$OICQnumber\t$ICQnumber\t$Location\t\t$DateRegistered\t没有发表过\t$Signature\t0\t\t$AvatarWording\t\t\t\t\t\t\t\n";
    close(IBMEMBER);
    print "用户 $UserName 已经成功转换成 LeoBBS 用户了！<BR><BR>";
}
print "总共转换了 $totaluserdata 个用户！<BR><BR>\n";
exit;
