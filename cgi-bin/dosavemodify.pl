#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use strict;
use warnings;
use diagnostics;

if ("$userregistered" eq "no") {&error("修改资料&没有此用户名！"); }
    if ("$oldpassword" eq "") {&error("修改资料&必须输入原来的论坛密码！"); }
    if ($oldpassword ne "") {
        eval {$oldpassword = md5_hex($oldpassword);};
        if ($@) {eval('use Digest::MD5 qw(md5_hex);$oldpassword = md5_hex($oldpassword);');}
        unless ($@) {$oldpassword = "lEO$oldpassword";}
    }
    if ("$oldpassword" ne "$password") {&error("修改资料&论坛密码错误！"); }

    $nowpassword            = $query -> param('nowpassword');
    $newpassword1           = $query -> param('newpassword1');
    $newpassword2           = $query -> param('newpassword2');
    $newshowemail           = $query -> param('newshowemail');
    $newhomepage            = $query -> param('newhomepage');
    $newoicqnumber          = $query -> param('newoicqnumber');
    $newicqnumber           = $query -> param('newicqnumber');
    $newlocation            = $query -> param('newlocation');
    $newinterests           = $query -> param('newinterests');
    $newtimedifference      = $query -> param('newtimedifference');
    $newpersonalavatar      = $query -> param('newpersonalavatar');
    $newpersonalwidth       = $query -> param('newpersonalwidth');
    $newpersonalheight      = $query -> param('newpersonalheight');
    $newemailaddress        = $query -> param('newemailaddress');
    $newmembertitle         = $query -> param('newmembertitle');
    $newjhmp                = $query -> param('newjhmp');
    $inuserflag		    = $query -> param('userflag');
    $inuserxz		    = $query -> param('userxz');
    $inusersx		    = $query -> param('usersx');
    $newyear                = $query -> param('newyear');
    $newmonth               = $query -> param('newmonth');
    $newday                 = $query -> param('newday');
    $newsex                 = $query -> param('newsex');
    $neweducation           = $query -> param('neweducation');
    $newmarry               = $query -> param('newmarry');
    $newwork                = $query -> param('newwork');
    $newsignature           = $query -> param('newsignature');
    $inuseravatar           = $query -> param('useravatar');
    $newuserquestion          = &cleanarea($query -> param('getpassq')."|".$query -> param('getpassa')); 

    $newsignature           = &unHTML("$newsignature");

    $newpassword1           = &cleanarea("$newpassword1");
    $newpassword2           = &cleanarea("$newpassword2");
    $newshowemail           = &cleanarea("$newshowemail");
    $newhomepage            = &cleanarea("$newhomepage");
    $newoicqnumber          = &cleanarea("$newoicqnumber");
    $newicqnumber           = &cleanarea("$newicqnumber");
    $newlocation            = &cleanarea("$newlocation");
    $newinterests           = &cleanarea("$newinterests");
    $newtimedifference      = &cleanarea("$newtimedifference");
    $newpersonalavatar      = &cleanarea("$newpersonalavatar");
    $newpersonalwidth       = &cleanarea("$newpersonalwidth");
    $newpersonalheight      = &cleanarea("$newpersonalheight");
    $newemailaddress        = &cleanarea("$newemailaddress");
    $newmembertitle         = &cleanarea("$newmembertitle");
    $newjhmp                = &cleanarea("$newjhmp");
    $inuserflag		    = &cleanarea("$inuserflag");
    $inuserxz		    = &cleanarea("$inuserxz");
    $inusersx		    = &cleanarea("$inusersx");
    $newyear                = &cleanarea("$newyear");
    $newmonth               = &cleanarea("$newmonth");
    $newday                 = &cleanarea("$newday");
    $neweducation           = &cleanarea("$neweducation");
    $newmarry               = &cleanarea("$newmarry");
    $newwork                = &cleanarea("$newwork");
    $newsignature           = &cleanarea("$newsignature");
    $inuseravatar           = &cleanarea("$inuseravatar");
    $newsex                 = &cleanarea("$newsex");
    $newoldsex              = $query -> param('oldsex');
    $newoldsex              = &cleanarea("$newoldsex");

    if ($userface ne '') {
        if (($newoldsex ne "no")&&($newsex ne $newoldsex)) {
	    &error("错误&由于你已经使用了虚拟形象，所以，你的性别目前不能更改！<BR>如果实在需要更改性别，那么请先去虚拟形象的个人设置中，清空您的资料，然后重试！");
        }
    }

    if ($newsignature) {
        $newsignature =~ s/\t//g;
        $newsignature =~ s/\r//g;
        $newsignature =~ s/  / /g;
        $newsignature =~ s/\&amp;nbsp;/\&nbsp;/g;
        $newsignature =~ s/\n\n/\n\&nbsp;\n/isg;
        $newsignature =~ s/\n/\[br\]/isg;
        $newsignature =~ s/\[br\]\[br\]/\[br\]\&nbsp;\[br\]/isg;
    }

    if ($newinterests) {
        $newinterests =~ s/<P>/<BR>/ig;
        $newinterests =~ s/<BR><BR>/<BR>/ig;
    }

    @testsig = split(/\[br\]/,$newsignature);
    $siglines = @testsig;
    &error("论坛密码提示问题和答案&论坛密码提示问题和答案中，不允许有非法字符，请更换提问和答案！") if ($query -> param('getpassq') =~ /[\||\a|\f|\n|\e|\0|\r|\t]/ || $query -> param('getpassa') =~ /[\||\a|\f|\n|\e|\0|\r|\t]/);
    if(length($newlocation)>16) { &error("修改资料&来自地区过长，请不要超过16个字符（8个汉字）！"); }
    if ($siglines > $maxsignline) { &error("修改资料&对不起，在您的签名中只允许有 $maxsignline 行！"); }
    if (length($newsignature) > $maxsignlegth) { &error("修改资料&对不起，签名不能超过 $maxsignlegth 字符！"); }
    if($newpassword1 =~ /[^a-zA-Z0-9]/)     { &error("修改资料&论坛密码只允许大小写字母和数字的组合！！"); }
    if($newpassword1 =~ /^lEO/)     { &error("用户注册&论坛密码不允许是 lEO 开头，请更换！！"); }

    if(length($newmembertitle)>21) { &error("修改资料&个人头衔过长，请不要超过20个字符（10个汉字）！"); }
    $newmembertitle =~ s/\t//isg;
    if(length($newjhmp)>21) { &error("修改资料&江湖门派过长，请不要超过20个字符（10个汉字）！"); }
    $newjhmp =~ s/\t//isg;

    @testins = split(/\<br\>/,$newinterests);
    $inslines = @testins;
    if ($inslines > $maxinsline) { &error("用户注册&对不起，个人简介只允许有 $maxinsline 行！"); }

    if (length($newinterests) > $maxinslegth) {&error("修改资料&对不起，个人简介不能超过 $maxinslegth 字符！"); }

    $newyear =~ s/\D//g;

    $newyear = "19$newyear"if ($newyear < 1900 && $newyear ne "");
    my (undef, undef, undef, undef, undef, $yeartemp, undef, undef) = localtime(time + $timezone * 3600);
    $yeartemp = 1900 + $yeartemp if ($yeartemp < 1900);

    if ($newyear ne "") {
        &error("用户注册&请正确输入你的出生年份！") if ($newyear <= 1900 || $newyear >= $yeartemp - 3);
    }

    if (($newyear eq "")||($newmonth eq "")||($newday eq "")) {
    	$newyear  = "";
    	$newmonth = "";
    	$newday   = "";
    }
    $newborn = "$newyear/$newmonth/$newday";

    if ($newborn ne "//") { #开始自动判断星座
    	if ($newmonth eq "01") {
    	    if (($newday >= 1)&&($newday <=19)) {
    	        $inuserxz = "z10";
    	    }
    	    else {
    	        $inuserxz = "z11";
    	    }
    	}
        elsif ($newmonth eq "02") {
    	    if (($newday >= 1)&&($newday <=18)) {
    	        $inuserxz = "z11";
    	    }
    	    else {
    	        $inuserxz = "z12";
    	    }
        }
        elsif ($newmonth eq "03") {
    	    if (($newday >= 1)&&($newday <=20)) {
    	        $inuserxz = "z12";
    	    }
    	    else {
    	        $inuserxz = "z1";
    	    }

        }
        elsif ($newmonth eq "04") {
    	    if (($newday >= 1)&&($newday <=19)) {
    	        $inuserxz = "z1";
    	    }
    	    else {
    	        $inuserxz = "z2";
    	    }
        }
        elsif ($newmonth eq "05") {
    	    if (($newday >= 1)&&($newday <=20)) {
    	        $inuserxz = "z2";
    	    }
    	    else {
    	        $inuserxz = "z3";
    	    }
        }
        elsif ($newmonth eq "06") {
    	    if (($newday >= 1)&&($newday <=21)) {
    	        $inuserxz = "z3";
    	    }
    	    else {
    	        $inuserxz = "z4";
    	    }
        }
        elsif ($newmonth eq "07") {
    	    if (($newday >= 1)&&($newday <=22)) {
    	        $inuserxz = "z4";
    	    }
    	    else {
    	        $inuserxz = "z5";
    	    }
        }
        elsif ($newmonth eq "08") {
    	    if (($newday >= 1)&&($newday <=22)) {
    	        $inuserxz = "z5";
    	    }
    	    else {
    	        $inuserxz = "z6";
    	    }
        }
        elsif ($newmonth eq "09") {
    	    if (($newday >= 1)&&($newday <=22)) {
    	        $inuserxz = "z6";
    	    }
    	    else {
    	        $inuserxz = "z7";
    	    }
        }
        elsif ($newmonth eq "10") {
    	    if (($newday >= 1)&&($newday <=23)) {
    	        $inuserxz = "z7";
    	    }
    	    else {
    	        $inuserxz = "z8";
    	    }
        }
        elsif ($newmonth eq "11") {
    	    if (($newday >= 1)&&($newday <=21)) {
    	        $inuserxz = "z8";
    	    }
    	    else {
    	        $inuserxz = "z9";
    	    }
        }
        elsif ($newmonth eq "12") {
    	    if (($newday >= 1)&&($newday <=21)) {
    	        $inuserxz = "z9";
    	    }
    	    else {
    	        $inuserxz = "z10";
    	    }
        }

    }

    if (($newpersonalavatar)&&($newpersonalwidth)&&($newpersonalheight)) {
        if ($newpersonalavatar !~ /^http:\/\/[\w\W]+\.[\w\W]+$/) {
            &error("用户注册&自定义头像的 URL 地址有问题！");
        }
        if (($newpersonalavatar !~ /\.gif$/i)&&($newpersonalavatar !~ /\.jpg$/isg)&&($newpersonalavatar !~ /\.png$/isg)&&($newpersonalavatar !~ /\.bmp$/isg)&&($newpersonalavatar !~ /\.swf$/isg)) {
            &error("用户注册&自定义头像必须为 PNG、GIF、JPG、BMP、SWF 格式") ;
        }
        if (($newpersonalwidth < 20)||($newpersonalwidth > $maxposticonwidth)) {
           &error("用户注册&对不起，您填写的自定义图像宽度必须在 20 -- $maxposticonwidth 像素之间！");
        }
        if (($newpersonalheight < 20)||($newpersonalheight > $maxposticonheight)) {
           &error("用户注册&对不起，您填写的自定义图像高度必须在 20 -- $maxposticonheight 像素之间！");
        }
        $inuseravatar = "noavatar";
        $newpersonalavatar =~ s/${imagesurl}/\$imagesurl/o;
    }
    else {
    	if ($addme){
    	    $newpersonalavatar="";
    	}else{
    	    $newpersonalavatar=""; $newpersonalwidth=""; $newpersonalheight="";
    	}
    }

    $newemailaddress = lc($newemailaddress);
    my $allow_eamil_file = "$lbdir" . "data/allow_email.cgi";
    if(-e $allow_eamil_file) {
	open(AEFILE,$allow_eamil_file);
	my $allowtype = <AEFILE>;
	my $allowmail = <AEFILE>;
	close(AEFILE);
	chomp $allowtype;
	chomp $allowmail;
	my $check_result = 0;
	my $get_email_server = substr($newemailaddress,rindex($newemailaddress,'@')+1);
	if($allowmail ne ""){
	    my @allowmail = split(/\t/,$allowmail);
	    chomp @allowmail;
	    foreach (@allowmail) {
		next if($_ eq "");
		if(lc($get_email_server) eq lc($_)) {
		    $check_result = 1;
		    last;
		}
	    }
	    if ($allowtype eq "allow") {
		if($check_result == 0) {
		    &error("修改资料&必需使用指定的邮箱！<a href=\"javascript:openScript('dispemail.cgi',200,300);\">[列表]</a>");
		}
	    } else {
		if($check_result == 1){
		    &error("修改资料&您提供的邮箱被禁止使用！<a href=\"javascript:openScript('dispemail.cgi',200,300);\">[列表]</a>");
		}
	    }
	}
    }
    if ($newemailaddress eq "") { $blankfields = "yes"; }
    if ($newpassword1 ne $newpassword2)  {&error("修改资料&你输入的两次论坛密码不相同，如果你不想修改论坛密码，请保持这两项为空！"); }

    if (($newpassword1 ne "")&&($newpassword2 ne "")) {
        if(length($newpassword1)<8) { &error("用户注册&论坛密码太短了，请更换！论坛密码必须 8 位以上！"); }
#       if ($newpassword1 =~ /^[0-9]+$/) { &error("用户注册&论坛密码请不要全部为数字，请更换！"); }
        $newpassword = $newpassword1;
	if ($newpassword ne "") {
	    eval {$newpassword = md5_hex($newpassword);};
	    if ($@) {eval('use Digest::MD5 qw(md5_hex);$newpassword = md5_hex($newpassword);');}
	    unless ($@) {$newpassword = "lEO$newpassword";}
	}
    }
    else { $newpassword = $oldpassword; }

    if ($blankfields) {
       &error("修改资料&请输入用户名、邮件地址，这些是必需的！");
    }

    $memberfiletitle = $inmembername;
    $memberfiletitle =~ s/ /\_/isg;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitletemp = unpack("H*","$memberfiletitle");
    
    my $temp = &dofilter("$newsignature\t$newlocation\t$membertitle\t$newinterests\t$jhmp\t$newhomepage");
    ($newsignature,$newlocation,$membertitle,$newinterests,$jhmp,$newhomepage) = split(/\t/,$temp);
    $newhomepage =~ s/[\ \a\f\n\e\0\r\t\|\$\@]//isg;
    $newhomepage =~ s/ARGV//isg;
    $newhomepage =~ s/system//isg;
    
    if ($addme) {
            unlink ("${imagesdir}usravatars/$memberfiletitle.gif");
            unlink ("${imagesdir}usravatars/$memberfiletitle.png");
            unlink ("${imagesdir}usravatars/$memberfiletitle.jpg");
            unlink ("${imagesdir}usravatars/$memberfiletitle.swf");
            unlink ("${imagesdir}usravatars/$memberfiletitle.bmp");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.gif");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.png");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.jpg");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.swf");
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.bmp");


          my ($file_name) = $addme =~ m|([^/:\\]+)$|; #注意,获取文件名字的形式变化

          my @filename = split(/\./,$file_name); #注意
          my $up_name = $file_name[0];
          $fileexp = $file_name[-1];
          $fileexp = lc($fileexp);


        $fileexp = ($fileexp =~ /jpe?g$/i) ? 'jpg'
                  :($fileexp =~ /gif$/i)  ? 'gif'
                  :($fileexp =~ /png$/i)  ? 'png'
                  :($fileexp =~ /swf$/i)  ? 'swf'
                  :($fileexp =~ /bmp$/i)  ? 'bmp'
                  :undef;
        $maxuploadava = 200 if (($maxuploadava eq "")||($maxuploadava < 1));
        if (($fileexp eq "swf")&&($flashavatar ne "yes")) {
            &error("不支持你所上传的图片，请重新选择！&仅支持 GIF，JPG，PNG，BMP 类型!");
        }

        if (!defined $fileexp) {
            &error("不支持你所上传的图片，请重新选择！&仅支持 GIF，JPG，PNG，BMP，SWF 类型!");
        }

        my $filesize=0;
        my $buffer;
        open (FILE,">${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
        binmode (FILE);
        while (((read($addme,$buffer,4096)))&&!(($filesize>$maxupload)&&($membercode ne "ad"))) {
               print FILE $buffer;
               $filesize=$filesize+4;
         }
        close (FILE);
        close ($addme); #注意

        if ($fileexp eq "gif"||$fileexp eq "jpg"||$fileexp eq "bmp"||$fileexp eq "jpeg"||$fileexp eq "png") {
	  eval("use Image::Info qw(image_info);"); 
	  if ($@ eq "") { 
    	    my $info = image_info("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
	    if ($info->{error} eq "Unrecognized file format"){
                unlink ("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
                &error("上传出错&上传文件不是图片文件，请上传标准的图片文件！");
            }
            if ($newpersonalwidth eq "" || $newpersonalwidth eq 0) {
            	if ($info->{width} ne "") { $newpersonalwidth = $info->{width}; }
            	elsif ($info->{ExifImageWidth} ne "") { $newpersonalwidth = $info->{ExifImageWidth}; }
            }
            if ($newpersonalheight eq "" || $newpersonalheight eq 0) {
            	if ($info->{height} ne "") { $newpersonalheight = $info->{height}; }
            	elsif ($info->{ExifImageLength} ne "") { $newpersonalheight = $info->{ExifImageLength}; }
            }
            undef $info;
          }
	}
	if ($filesize>$maxuploadava) {
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
	    &error("上传出错&上传文件大小超过$maxuploadava，请重新选择！");
	}
	if (($newpersonalwidth < 20)||($newpersonalwidth > $maxposticonwidth)) { &error("用户注册&对不起，您填写的自定义图像宽度($newpersonalwidth)必须在 20 -- $maxposticonwidth 像素之间！"); }
        if (($newpersonalheight < 20)||($newpersonalheight > $maxposticonheight)) { &error("用户注册&对不起，您填写的自定义图像高度($newpersonalheight)必须在 20 -- $maxposticonheight 像素之间！"); }

	$inuseravatar="noavatar";
	$newpersonalavatar="\$imagesurl/usravatars/$memberfiletitletemp.$fileexp";
    }

    if($newemailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/) { &error("注册&Email 地址非法$newemailaddress！"); }
    $newemailaddress =~ s/[\ \a\f\n\e\0\r\t\`\~\!\#\$\%\^\&\*\(\)\=\+\\\[\]\{\}\;\'\:\"\,\/\<\>\?\|]//isg;

   &getmember("$inmembername");
    
#    &getmember("$inmembername","no");

    if ($newemailaddress ne $emailaddress) {
	my $charone = substr($newemailaddress, 0, 1);
	$charone = lc($charone);
	$charone = ord($charone);
	my $charone1 = substr($emailaddress, 0, 1);
	$charone1 = lc($charone1);
	$charone1 = ord($charone1);

	$/ = "";
	open (MEMFILE, "${lbdir}data/lbemail/$charone.cgi");
	my $allmemberemails = <MEMFILE>;
	close(MEMFILE);
	open (MEMFILE1, "${lbdir}data/lbemail/$charone1.cgi");
	my $allmemberemails1 = <MEMFILE1>;
	close(MEMFILE1);
	$/ = "\n";
	$allmemberemails = "\n$allmemberemails\n";
	chomp($allmemberemails);
	$allmemberemails = "\t$allmemberemails";

	if (($allmemberemails =~ /\n$newemailaddress\t(.+?)\n/i)&&($oneaccountperemail eq "yes")) {
	   &error("资料修改&对不起，这输入的 Email 已经被注册用户：<u>$1</u> 使用了");
	}
	$allmemberemails1 =~ s/$emailaddress\t$inmembername\n//isg;
	open(MEMFILE1, ">${lbdir}data/lbemail/$charone1.cgi");
	print MEMFILE1 "$allmemberemails1";
	close(MEMFILE1);
	open(MEMFILE, ">>${lbdir}data/lbemail/$charone.cgi");
	print MEMFILE "$newemailaddress\t$inmembername\n";
	close(MEMFILE);
   }
   
    if ($newborn ne $born) {
        $filetomakeopen = "${lbdir}data/lbmember3.cgi";
        open (MEMFILE, "$filetomakeopen");
        @allmembers = <MEMFILE>;
        close (MEMFILE);

	if (open (MEMFILE, ">$filetomakeopen")) {
	    $writeborn=0;
            foreach (@allmembers) {
                chomp $_;
                ($user, $no) = split(/\t/,$_);
                if (lc($user) eq lc($inmembername)) {
	            print MEMFILE "$inmembername\t$newborn\t\n" if (($newborn ne "")&&($newborn ne "//"));
	            $writeborn=1;
                } else {
	            print MEMFILE "$_\n";
                }
            }
	    print MEMFILE "$inmembername\t$newborn\t\n" if (($writeborn==0)&&($newborn ne "")&&($newborn ne "//"));
            close (MEMFILE);
	}

	($oyear,$omonth,$oday) = split(/\//,$born);
	if ($omonth ne "") {
	    $omonth = int($omonth);
	    open (MEMFILE, "${lbdir}calendar/borninfo$omonth.cgi");
	    @birthdaydata = <MEMFILE>;
	    close (MEMFILE);

	    if (open (MEMFILE, ">${lbdir}calendar/borninfo$omonth.cgi")) {
                foreach (@birthdaydata) {
                    chomp $_;
                    ($user, $no) = split(/\t/,$_);
                    next if (lc($user) eq lc($inmembername));
	            print MEMFILE "$_\n";
	        }
            }
            close (MEMFILE);
	}

	if (($newborn ne "")&&($newborn ne "//")) {
	    $newmonth = int($newmonth);
	    open (MEMFILE, ">>${lbdir}calendar/borninfo$newmonth.cgi");
	    print MEMFILE "$inmembername\t$newborn\t\n";
	    close (MEMFILE);
	}
    }

    if (($passwordverification eq "yes") && ($emailfunctions ne "off") && ($newemailaddress ne $emailaddress)) {
	$seed = int(myrand(100000));
	$password = crypt($seed, aun);
	$password =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$password =~ s/\.//g;
        $password =~ s/\|//g;
	$newpassword = substr($password, 0, 8);

	$passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/", -expires => "0");

	eval("use MAILPROG qw(sendmail);");

	$to = $newemailaddress;
	$from = $adminemail_out;
	$subject = "您改变了在 $boardname 中注册的邮件地址";

	$message .= "\n";
	$message .= "$homename <br>\n";
	$message .= "$boardurl/leobbs.cgi\n <br><br>\n <br>\n";
	$message .= "------------------------------------<br>\n";
	$message .= "您的用户名、新论坛密码如下：\n <br><br>\n";
	$message .= "用户名： $inmembername <br>\n";
	$message .= "新论坛密码： $newpassword\n <br><br>\n <br>\n";
	$message .= "请注意：用户名和论坛密码区分大小写！\n <br>\n";
	$message .= "------------------------------------<br>\n";

	&sendmail($from, $adminemail_in, $to, $subject, $message);

	if ($newpassword ne "") {
	    eval {$newpassword = md5_hex($newpassword);};
	    if ($@) {eval('use Digest::MD5 qw(md5_hex);$newpassword = md5_hex($newpassword);');}
	    unless ($@) {$newpassword = "lEO$newpassword";}
	}
    }

    if (($editusertitleself eq "post") && ($jifen >= $needpoststitle)) { $editusertitleself = "on"; }
    
    if ($editusertitleself eq "on") {
        $newmembertitle = "Member" if ($newmembertitle eq "");
        $membertitle = $newmembertitle;
    }

    if (($editjhmpself eq "post") && (($numberofposts + $numberofreplys) >= $needpostsjhmp)) { $editjhmpself = "on"; }

    if ($editjhmpself eq "on") {
        $jhmp = $newjhmp;
    }
    elsif ($editjhmpself eq "system") {
	my $jumpfile="$lbdir" . "data/jhmp.cgi";
	open(FILE,$jumpfile);
	my @JUMP=<FILE>;
	close(FILE);
	chomp @JUMP;
	if($membercode eq "ad" || $membercode eq "smo"){
		@JUMP = grep(/^(.+?)\t[1|0]\t/,@JUMP);
	}else{
        	@JUMP1 = grep(/^$jhmp\t0\t/,@JUMP);
		@JUMP = grep(/^(.+?)\t1\t/,@JUMP);
		push(@JUMP,@JUMP1);
	}
	$newjhmp = 1000 unless(@JUMP && -e $jumpfile);
	$newjhmp = (defined $JUMP[$newjhmp])?$newjhmp:1000;
	($JUMP[$newjhmp],my $no) = split(/\t/,$JUMP[$newjhmp]);
	$jhmp = ($newjhmp < 1000)?$JUMP[$newjhmp]:'无门无派';
    }

    if(($userquestion eq "|")||($userquestion eq "")){ 
	$userquestion = $newuserquestion; 
    }
    
    if (($inmembername ne "")&&($newpassword ne "")) {
	require "dosignlbcode.pl";
	$signature1=&signlbcode($newsignature); 
	$newsignature=$newsignature."aShDFSiod".$signature1;
	my $namenumber = &getnamenumber($memberfiletitle);
	&checkmemfile($memberfiletitle,$namenumber);
	$filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	if (open(FILE, "+<$filetomake")) {
	    flock(FILE, 2) if ($OS_USED eq "Unix");
	    seek(FILE,0,0);
	    print FILE "$inmembername\t$newpassword\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$newemailaddress\t$newshowemail\t$ipaddress\t$newhomepage\t$newoicqnumber\t$newicqnumber\t$newlocation\t$newinterests\t$joineddate\t$lastpostdate\t$newsignature\t$newtimedifference\t$privateforums\t$inuseravatar\t$inuserflag\t$inuserxz\t$inusersx\t$newpersonalavatar\t$newpersonalwidth\t$newpersonalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$newsex\t$neweducation\t$newmarry\t$newwork\t$newborn\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
	    close(FILE);
	}
	if (open(FILE, ">${lbdir}$memdir/old/$memberfiletitle.cgi")) {
	    print FILE "$inmembername\t$newpassword\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$newemailaddress\t$newshowemail\t$ipaddress\t$newhomepage\t$newoicqnumber\t$newicqnumber\t$newlocation\t$newinterests\t$joineddate\t$lastpostdate\t$newsignature\t$newtimedifference\t$privateforums\t$inuseravatar\t$inuserflag\t$inuserxz\t$inusersx\t$newpersonalavatar\t$newpersonalwidth\t$newpersonalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$newsex\t$neweducation\t$newmarry\t$newwork\t$newborn\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
	    close(FILE);
	}
	&winunlock($filetomake) if ($OS_USED eq "Nt");
        unlink ("${lbdir}cache/myinfo/$memberfiletitle.pl");
        unlink ("${lbdir}cache/meminfo/$memberfiletitle.pl");
    }

    $previewsig = $signature1;

    if ($newpassword1 ne "") {
	$info = qq~<ul><li><a href="loginout.cgi"><font color=$fonthighlight>因为你修改了论坛密码，所以请重新登录一次！</font></a></ul>~;
    } else { $info = qq~<ul><li><a href="leobbs.cgi">返回论坛首页</a></ul>~; }
	$output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>个人信息已经保存</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>
具体情况：$info</td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font color=$postfontcolor>
你的新签名预览：<br><hr><br>
$previewsig
<br><hr></font>
</td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
	if (($passwordverification eq "yes") && ($emailfunctions ne "off") && ($newemailaddress ne $emailaddress)) {
	    $output =~ s/具体情况：/<B>由于你修改了 Email，所以你直接修改的论坛密码是无效的，而你的新论坛密码已经通过 Email 发送给你了！<\/B>/g;
	}
1;
