#!/usr/bin/perl

################################
# UBB --> LeoBBS 用户资料转换器#
################################

$ubbmember    = "/path/to/UBB members dir/";   	# 输入 UBB 用户资料所在的目录的绝对路径，最后不要遗漏 / 。
$leobbsmember = "/path/to/LeoBBS members dir/"; # 请输入 LeoBBS 用户资料所在的目录的绝对路径，最后不要遗漏 /  ，注意设置 777 属性。

### 如果你不懂 CGI，以下部分请千万不要修改！
$ending = ".cgi"; 		# LeoBBS 的用户数据文件后缀为 .cgi
$membernumber = 00000001;	# UBB 用户开始编号
$totlenumber = 0;		# 用户个数清 0
$nowtime = time;
print "Content-type: text/html\n\n";
print "UBB --> LeoBBS 用户数据转换器<BR><BR>\n";
while ($membernumber < 100000)    {
   if ($membernumber < 10) 	 { $membernumber = "0000000$membernumber"; }
   elsif ($membernumber < 100)   { $membernumber = "000000$membernumber";  }
   elsif ($membernumber < 1000)  { $membernumber = "00000$membernumber";   }
   elsif ($membernumber < 10000) { $membernumber = "0000$membernumber";   }
   elsif ($membernumber < 100000){ $membernumber = "000$membernumber";   }
   if (open(FILE,"$ubbmember$membernumber$ending")){
      @ubbmem = <FILE>;
      close(FILE);
      print "提取用户文件： $ubbmember$membernumber$ending<BR>\n";
      for ($i=0;$i<=14;$i++) { chop (@ubbmem[$i]); }
      $name = "@ubbmem[0]";
      print "提取用户名： $name<BR>\n";
      $realname = $name;
      $name =~ s/ /_/gi;
      $name =~ tr/A-Z/a-z/;
      $name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\=\+\\\[\]\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
      $filetocheck = "$leobbsmember" . "$name$ending";
      if (-e $filetocheck) { print "用户 $realname 已经存在，不能转换！"; next; }
      open(IBMEMBER,">$leobbsmember$name$ending");
      print IBMEMBER "$realname\t@ubbmem[1]\tMember\tme\t@ubbmem[7]\t@ubbmem[2]\t@ubbmem[11]\txxx.xxx.xxx.xxx\t@ubbmem[3]\t\t@ubbmem[13]\t@ubbmem[6]\t@ubbmem[9]\t$nowtime\tNot Posted\t@ubbmem[12]\t\t\t\t\t\t\t\n";
      close(IBMEMBER);
      print "用户 $realname 已经成功转换成 LeoBBS 用户了！<BR><BR>";
      $totlenumber ++;
   }
   $membernumber = $membernumber+1;
}
print "总共转换了 $totlenumber 个用户！<BR><BR>\n";
exit;
