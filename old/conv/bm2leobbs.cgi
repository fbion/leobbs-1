#!/usr/bin/perl 

##################################
# BM200X --> LeoBBS 用户资料转换器
##################################

$userhead= "g:/www/9438/bm2000/";       #BM2000 用户目录，最后不要遗漏 /
$leoBBSmember = "g:/www/9438/leobbs/";  #LeoBBS 用户目录，最后不要遗漏 /，注意设置 777 属性

###############以下不必修改################# 
$nowtime = time;
$ending = ".cgi";
print ("Content-type: text/html\n\n");
$userdir=$userhead;
chop $userdir;
opendir (MEMBERDIR, "$userdir");
  @stats = readdir(MEMBERDIR);
closedir (MEMBERDIR);
@stats = grep(/\.txt/, @stats);
@stats = sort @stats;
$totaluserdata=$#stats+1;
for ($i=0;$i<$totaluserdata;$i++) { 
    $name = @stats[$i]; 
    $filesname="$userhead$name"; 
    open(file,"$filesname"); 
    @array=<file>;     
    close(file); 
    $wuyu = "@array";               
    $TotalPosts,$a,$UserName,$Password,$b,$Email,$ICQnumber,$e,$DateRegistered,$Signature,$AvatarWording,$f,$c,$d,$whatever,$URL,$OICQnumber,$Location)=split(/,/,$wuyu);               
    ($name,$temp)=split(/\./,$name);
    $name =~ s/ /_/gi;
    $name =~ tr/A-Z/a-z/;
    open(IBMEMBER,">$leoBBSmember$name$ending"); 
    print IBMEMBER "$UserName\t$Password\tMember\tme\t$TotalPosts\t$Email\tyes\txxx.xxx.xxx.xxx\t$URL\t$OICQnumber\t$ICQnumber\t$Location\t$DateRegistered\t$nowtime\tNot Posted\t$Signature\t\t\tnoavatar\t\t\t\t$AvatarWording\t80\t80\t\n"; 
    close(IBMEMBER); 
    print "用户 $UserName 已经成功转换成 LeoBBS 用户了！<BR><BR>"; 
}
