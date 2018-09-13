########################
#
#上传处理 By 路杨
#
########################

use strict;
use warnings;
use diagnostics;

sub upfileonpost #提交的时候处理临时文件到合适的地方：）更新帖子
{
    my ($inpost, $in_forum, $in_topic) = @_;

    if ($$inpost =~ /\[UploadFile.{0,6}=tmp_([^\]]+?)\]/is) {
        use File::Copy;
        my $tmppath = &getusrdir(1); #临时目录

        $topic = $in_topic % 100;
        my $topath = "${imagesdir}$usrdir/$in_forum/$topic"; #目的目录
        mkdir("${imagesdir}$usrdir/$in_forum", 0777) if (!(-e "${imagesdir}$usrdir/$in_forum"));
        chmod(0777, "${imagesdir}$usrdir/$in_forum");
        mkdir("$topath", 0777) if (!(-e "$topath"));
        chmod(0777, "$topath");

        my $tmpshow = $$inpost;
        while ($tmpshow =~ /\[UploadFile.{0,6}=tmp\_([^\]]+?)\]/i) {
            my $file_name = $1;
            if (!(-e "$tmppath/tmp_$file_name")) {$$inpost =~ s/\[UploadFile.{0,6}=tmp\_$file_name\]//isg;} #删除不在的文件
            else {
                if ($file_name =~ /\.torrent/i) {
                    copy("$tmppath/tmp_$file_name", "$topath/$file_name");
                    unlink("$tmppath/tmp_$file_name");
                    copy("$tmppath/tmp_$file_name.btfile", "$topath/$file_name.btfile");
                    unlink("$tmppath/tmp_$file_name.btfile");
                }
                else {
                    copy("$tmppath/tmp_$file_name", "$topath/$file_name");
                    unlink("$tmppath/tmp_$file_name");
                }
                $tmpprint = "$tmpprint$file_name\n"; #要写进cache的内容
            }
            $tmpshow =~ s/\[UploadFile.{0,6}=tmp\_$file_name\]//isg;
        }

        $$inpost =~ s/(\[UploadFile.{0,6}=)tmp\_(([^\]]+?)\])/$1$2/isg; #更新帖子

        mkdir("${lbdir}FileCount/$in_forum", 0777) if (!(-e "${lbdir}FileCount/$in_forum"));
        chmod(0777, "${lbdir}FileCount/$in_forum");
        open(FILE, ">>${lbdir}FileCount/$in_forum/$in_forum\_$in_topic.pl"); #写进cache
        print FILE "$tmpprint";
        close(FILE);
        my @tmpprint = split(/\n/, $tmpprint);
        $tmpprint = $tmpprint[0];
        my ($up_name, $up_ext) = split(/.*\./, $tmpprint);
        return $up_ext; ##有附件；给BT区留做判断
    }
    else {return 0;} ###无附件当然无BT
}

sub delupfiles #删除当前帖子全部附件（遍历帖子方式）---删除回复时候用
{
    my ($inpost, $in_forum, $in_topic) = @_;
    if ($$inpost =~ /\[UploadFile.{0,6}=([^\]]+?)\]/is) {
        $topic = $in_topic % 100;
        my $topath = "${imagesdir}$usrdir/$in_forum/$topic"; #目的目录

        my $usruploadfile = "${lbdir}FileCount/$in_forum/${inforum}\_${intopic}.pl";
        if (open(FILEUP, "$usruploadfile")) {
            sysread(FILEUP, $tmpprint, (stat(FILEUP))[7]);
            close(FILEUP);
            $tmpprint =~ s/\r//isg;
        }

        my $tmpshow = $$inpost;
        $tmpshow =~ s/\[UploadFile.{0,6}=tmp\_[^\]]+?\]//isg; #临时文件不处理，因为是这次上传的

        while ($tmpshow =~ /\[UploadFile.{0,6}=([^\]]+?)\]/i) {
            my $file_name = $1;
            if ($file_name =~ /\.torrent/i) {
                unlink("$topath/$file_name");
                unlink("$topath/$file_name.btfile");
                $tmpprint =~ s/$file_name//isg;
            }
            else {
                unlink("$topath/$file_name");
                unlink("$topath/$file_name.waterpicture");
                $tmpprint =~ s/$file_name//isg;
            }
            $tmpshow =~ s/\[UploadFile.{0,6}=([^\]]+?)\]//i;
        }
        #    $tmpshow =~ s/(.*?)(\[UploadFile.{0,6}=[^\]]+?\])(.*?)/$2/isg;
        #    $tmpshow=~ s/\[UploadFile.{0,6}=([^\]]+?(\.torrent))\]/unlink\("$topath\/$1"\)\; unlink\("$topath\/$1\.btfile"\)\;  $tmpprint\=\~ s\/$1\/\/isg\;/isg;  ##删除BT文件
        #    $tmpshow=~ s/\[UploadFile.{0,6}=([^\]]+?)\]/ unlink\("$topath\/$1"\)\;/isg; ###unlink\("$topath\/$1"\)\;$tmpprint\=\~ s\/$1\/\/isg\;/isg;

        #    $err=0;
        #   eval $tmpshow; #unlink
        #    if ($@) {$err=1;}

        ### $tmpprint=~ s/$1//isg;  #要写进cache的内容

        $$inpost =~ s/\[UploadFile(.{0,6})=(tmp\_[^\]]+?)\]/\[Uploadhtc$1=$2\]/isg;
        $$inpost =~ s/\[UploadFile.{0,6}=(.+?)\]//isg;
        $$inpost =~ s/\[Uploadhtc(.{0,6})=(tmp\_[^\]]+?)\]/\[UploadFile$1=$2\]/isg;

        $tmpprint =~ s/\n\n/\n/isg;

        open(FILE, ">${lbdir}FileCount/$in_forum/$in_forum\_$in_topic.pl"); #写进cache
        print FILE "$tmpprint";
        close(FILE);
        return $err;
    }
    else {return 0;}
}

sub delallupfiles #删除当前主贴全部附件,全部删除的时候调用（cache方式）
{
    my ($in_forum, $in_topic) = @_;

    $topic = $in_topic % 100;
    my $topath = "${imagesdir}$usrdir/$in_forum/$topic"; #目的目录

    my $usruploadfile = "${lbdir}FileCount/$in_forum/${inforum}\_${intopic}.pl";
    if (open(FILEUP, "$usruploadfile")) {
        sysread(FILEUP, $files, (stat(FILEUP))[7]);
        close(FILEUP);
        $files =~ s/\r//isg;
        my @files = split(/\n/, $files);
        foreach my $line (@files) {
            chomp $line;
            unlink("$topath/$line");
            unlink("$topath/$line.waterpicture");
        }
    }
    unlink("$usruploadfile");
    return;

}

sub moveallupfiles #移动/copy当前主贴全部附件,移动/copy的时候调用（cache方式）
{
    my ($oldforum, $oldtopic, $newforum, $newtopic, $copy) = @_;

    my $topic = $oldtopic % 100;
    my $nowpath = "${imagesdir}$usrdir/$oldforum/$topic"; #原来目录

    $topic = $newtopic % 100;
    my $topath = "${imagesdir}$usrdir/$newforum/$topic"; #目的目录
    mkdir("${imagesdir}$usrdir/$newforum", 0777) if (!(-e "${imagesdir}$usrdir/$newforum"));
    chmod(0777, "${imagesdir}$usrdir/$newforum");
    mkdir("$topath", 0777) if (!(-e "$topath"));
    chmod(0777, "$topath");

    my $usruploadfile = "${lbdir}FileCount/$oldforum/${oldforum}\_${oldtopic}.pl";
    mkdir("${lbdir}FileCount/$newforum", 0777) if (!(-e "${lbdir}FileCount/$newforum"));
    chmod(0777, "${lbdir}FileCount/$newforum");
    my $newusruploadfile = "${lbdir}FileCount/$newforum/${newforum}\_${newtopic}.pl";
    if (open(FILEUP, "$usruploadfile")) {
        sysread(FILEUP, $files, (stat(FILEUP))[7]);
        close(FILEUP);
        $files =~ s/\r//isg;
        my @files = split(/\n/, $files);
        foreach my $line (@files) {
            chomp $line;
            copy("$nowpath/$line", "$topath/$line");
            unlink("$nowpath/$line") if ($copy eq "no");
            unlink("$nowpath/$line.waterpicture") if ($copy eq "no");
        }
    }

    copy("$usruploadfile", "$newusruploadfile");
    open(FILEUP, "$newusruploadfile");
    sysread(FILEUP, $files, (stat(FILEUP))[7]);
    close(FILEUP);
    $files =~ s/\r//isg;
    $files =~ s/$oldforum\_$oldtopic\_/$newforum\_$newtopic\_/isg;
    $files =~ s/$oldforum\_$oldtopic\./$newforum\_$newtopic\./isg;
    open(FILEUP, ">$newusruploadfile");
    print FILEUP "$files";
    close(FILEUP);
    unlink("$usruploadfile") if ($copy eq "no");
    return;

}

sub getusrdir #获取临时文件夹
{
    my $incanshu = shift;
    # my $tmpname = $inmembername;
    my $tmpname = $query->cookie("amembernamecookie");
    $tmpname =~ s/ /\_/g;
    $tmpname =~ tr/A-Z/a-z/;
    $tmpname =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    mkdir("${imagesdir}$usrdir/tmp", 0777) if (!(-e "${imagesdir}$usrdir/tmp"));
    chmod(0777, "${imagesdir}$usrdir/tmp");
    my $pathtocheck = "${imagesdir}$usrdir/tmp/$tmpname";

    mkdir("$pathtocheck", 0777) if (!(-e "$pathtocheck"));
    chmod(0777, "$pathtocheck");

    opendir(DIR, "$pathtocheck"); #第1次
    my @files = readdir(DIR);
    closedir(DIR);

    foreach (@files) {unlink("$pathtocheck/$_") if ((-M "$pathtocheck/$_") * 86400 > 60 * 60);} #临时上传保留60min


    opendir(DIR, "$pathtocheck"); #第2次
    @files = readdir(DIR);
    closedir(DIR);
    $filesno = @files;
    $filesno = $filesno - 2;
    $maxaddnum = 10 if ($maxaddnum eq "" || $maxaddnum < 1);
    if ($incanshu ne 1) {
        if ($filesno > $maxaddnum && $membercode ne "ad" && $membercode ne "smo") {$pathtocheck = "ERR";} ##同时上传到了最大限度##{$thisout="您今天上传的东西太多了或者请不要同时在几个区同时上传，谢谢合作";&thisout("$thisoutput");exit;}
    }
    return "$pathtocheck";
}

sub gettmpname #获取临时文件名字
{
    my $thisname = shift;
    $thisname = uri_escape($thisname); #建议上传的文件不要含中文(路杨)
    $thisname =~ s/%/1/isg;            #建议上传的文件不要含中文(路杨)
    $thisname =~ s/\./2/isg;
    $thisname =~ s/\\/3/isg;
    $thisname =~ s/\//4/isg;
    $thisname =~ s/\=/5/isg;
    $thisname =~ s/\-/6/isg;
    $thisname =~ s/\)/7/isg;
    $thisname =~ s/\(/8/isg;
    $thisname =~ s/\+/9/isg;
    $thisname =~ s/\|/0/isg;
    $thisname =~ s/\$/1/isg;
    $thisname =~ s/\,/2/isg;
    $thisname =~ s/\{/3/isg;
    $thisname =~ s/\}/4/isg;
    $thisname =~ s/\[/5/isg;
    $thisname =~ s/\]/6/isg;
    $thisname =~ s/[\W]/0/isg;
    $thisname = substr($thisname, 0, 16) if (length($thisname) > 16);
    my $prefix = "tmp";
    if ($thisname =~ /^tmp/) {$prefix .= "_up";} #tmp开头作为识别，所以如果开头是tmp则加上up前缀
    my $thistime = time;
    $thisname = "${prefix}_${thisname}_$thistime";
    return "$thisname";
}
1;