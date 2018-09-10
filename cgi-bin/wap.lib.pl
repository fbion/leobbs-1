#########################
# 手机论坛WAP版
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
use strict;
use warnings;
use diagnostics;

($memdir, $msgdir, $usrdir, $saledir) = split(/\|/, getdir());
sub dofilter {
    my $infiltermessage = shift;
    if (open(FILE, "${lbdir}data/wordfilter.cgi")) {
        $wordfilter = <FILE>;
        close(FILE);
        chomp $wordfilter;
        $wordfilter =~ s/(\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\])//ig;
        $wordfilter =~ s/\t/\|/ig;
        $wordfilter =~ s/\|\|/\|/ig;
        $wordfilter =~ s/^\|//ig;
        $wordfilter =~ s/\|$//ig;
    }
    else {$wordfilter = "";}
    my $tempinfilter = $infiltermessage;
    if ($wordfilter) {$tempinfilter =~ s/$wordfilter/ *** /isg;}
    if ($tempinfilter ne $infiltermessage) {&error("有问题&你所写的内容中也许包含了一些本论坛不允许发布的言论，请仔细检查后，重新发布，谢谢！");}
    $tempinfilter =~ s/\&nbsp\;//ig;
    $tempinfilter =~ s/\<.+?\>//ig;
    $tempinfilter =~ s/\[.+?\]//g;
    $tempinfilter =~ s/ |　|\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\]//g;
    my $tempinfilter1 = $tempinfilter;
    if ($wordfilter) {$tempinfilter1 =~ s/$wordfilter/ *** /isg;}
    if ($tempinfilter1 ne $tempinfilter) {&error("有问题&你所写的内容中也许包含了一些本论坛不允许发布的言论，请仔细检查后，重新发布，谢谢！！");}
    if (open(FILE, "${lbdir}data/badwords.cgi")) {
        $badwords = <FILE>;
        close(FILE);
        $badwords =~ s/[\a\f\n\e\0\r\t]//ig;
        $badwords =~ s/(\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\])//ig;
    }
    else {$badwords = "";}
    if ($badwords) {
        study($infiltermessage);
        my @pairs = split(/\&/, $badwords);
        foreach (@pairs) {
            my ($bad, $good) = split(/=/, $_);
            chomp $good;
            $infiltermessage =~ s/$bad/$good/isg;
        }
    }
    return $infiltermessage;
}
sub getoneforum {
    local $inforum = shift;
    return if ($inforum eq "");
    if (-e "${lbdir}cache/forumsone$inforum.pl") {
        eval {require "${lbdir}cache/forumsone$inforum.pl";};
        if ($@) {
            unlink("${lbdir}cache/forumsone$inforum.pl");
            require "dogetoneforum.pl";
        }
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $no, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forumpass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $forums);
        unlink("${lbdir}cache/forumsone$inforum.pl") if ((-M "${lbdir}cache/forumsone$inforum.pl") * 86400 > 600);
    }
    else {
        require "dogetoneforum.pl";
    }
    $forummodnamestemp = ",$forummoderator,";
    my $tempinmembername = ",$inmembername,";
    $inmembmod = $forummodnamestemp =~ /\Q$tempinmembername\E/i || (($membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && ($forummodnamestemp =~ /,全体版主,/ || $forummodnamestemp =~ /,全体斑竹,/)) ? "yes" : "no";
    return;
}

sub moderator {
    local $inforum = shift;
    return if ($inforum eq "");
    if (-e "${lbdir}cache/forums$inforum.pl") {
        eval {require "${lbdir}cache/forums$inforum.pl";};
        if ($@) {
            unlink("${lbdir}cache/forums$inforum.pl");
            require "domoderator.pl";
        }
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forumpass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $thisforums);

        if ($forummodnamestemp =~ /\Q\,$inmembername\,\E/i || (($membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && ($forummodnamestemp =~ /,全体版主,/ || $forummodnamestemp =~ /,全体斑竹,/))) {$inmembmod = "yes";}
        else {$inmembmod = "no";}
        unlink("${lbdir}cache/forums$inforum.pl") if ((-M "${lbdir}cache/forums$inforum.pl") * 86400 > 600);
    }
    else {
        require "domoderator.pl";
    }
    eval {require "${lbdir}boarddata/forumposts$inforum.pl";} if ($thisprog eq "forums.cgi");
    return;
}

sub checkmemfile {
    my ($nametocheck, $namenumber) = @_;
    if (-e "${lbdir}$memdir/$nametocheck.cgi") {
        my @fileinfo = stat("${lbdir}$memdir/$nametocheck.cgi");
        my $filelength = $fileinfo[7];
        if ($filelength <= 50) {unlink("${lbdir}$memdir/$nametocheck.cgi");}
        else {
            if ($loadcopymo ne 1) {
                eval('use File::Copy;');
                $loadcopymo = 1;
            }
            copy("${lbdir}$memdir/$nametocheck.cgi", "${lbdir}$memdir/$namenumber/$nametocheck.cgi");
            unlink("${lbdir}$memdir/$nametocheck.cgi");
        }
    }

    my @fileinfo = stat("${lbdir}$memdir/$namenumber/$nametocheck.cgi");
    my $filelength = $fileinfo[7];
    if ((!(-e "${lbdir}$memdir/$namenumber/$nametocheck.cgi")) || ($filelength <= 50)) {
        if (-e "${lbdir}$memdir/old/$nametocheck.cgi") {
            if ($loadcopymo ne 1) {
                eval('use File::Copy;');
                $loadcopymo = 1;
            }
            copy("${lbdir}$memdir/old/$nametocheck.cgi", "${lbdir}$memdir/$namenumber/$nametocheck.cgi");
        }
    }
}

sub getnamenumber {
    my $nametocheck = shift;
    my $namenumber = ((ord(substr($nametocheck, 0, 1)) & 0x3c) << 3) | ((ord(substr($nametocheck, 1, 1)) & 0x7c) >> 2);
    mkdir("${lbdir}$memdir/$namenumber", 0777) if (!(-e "${lbdir}$memdir/$namenumber"));
    chmod(0777, "${lbdir}$memdir/$namenumber");
    return $namenumber;
}

sub getmember {
    my ($nametocheck, $readtype) = @_;
    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    my $namenumber = &getnamenumber($nametocheck);
    &checkmemfile($nametocheck, $namenumber);
    $userregistered = "";
    undef $filedata;
    my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";

    if ($readtype eq "check") {
        if ((-e $filetoopen) && ($nametocheck !~ /^客人/) && ($nametocheck ne "")) {
            return 1;
        }
        else {
            return 0;
        }
    }

    if ((-e $filetoopen) && ($nametocheck !~ /^客人/) && ($nametocheck ne "")) {
        &winlock($filetoopen) if (($OS_USED eq "Nt") && ($readtype ne "no"));
        open(FILE3, "$filetoopen");
        flock(FILE3, 1) if (($OS_USED eq "Unix") && ($readtype ne "no"));
        my $filedata = <FILE3>;
        close(FILE3);
        &winunlock($filetoopen) if (($OS_USED eq "Nt") && ($readtype ne "no"));
        chomp($filedata);
        ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
        $showemail = "no" if ($dispmememail eq "no");
        $membername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
        $password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
        if (($password !~ /^lEO/) && ($password ne "")) {
            eval {$password = md5_hex($password);};
            if ($@) {eval('use Digest::MD5 qw(md5_hex);$password = md5_hex($password);');}
            unless ($@) {$password = "lEO$password";}
        }
        $membercode ||= "me";

        $onlinetime = "3000" if ($onlinetime < 0);

        $timedifferencevalue = $timedifference;
        ($numberofposts, $numberofreplys) = split(/\|/, $numberofposts);
        $numberofposts ||= "0";
        $numberofreplys ||= "0";
        $jifen = $numberofposts * 2 + $numberofreplys - $postdel * 5 if ($jifen eq "");
        chomp $privateforums;
        if ($privateforums) {
            my @private = split(/&/, $privateforums);
            foreach (@private) {
                chomp $_;
                ($access, $value) = split(/=/, $_);
                $allowedentry{$access} = $value;
            }
        }
        return 1;
    }
    else {
        $userregistered = "no";
        $membercode = "";
        return 0;
    }
}

sub doonoff {
    #$mainoff 主，$mainonoff　分论坛
    return if ($membercode eq "ad");
    if (($mainoff == 2) && ($mainonoff ne 2)) {
        $mainoff = 1;
        my (undef, undef, $hour, $mday, undef, undef, $wday, undef) = localtime(time + $timezone * 3600);
        $mainautovalue =~ s/[^\d\-]//sg;
        my ($starttime, $endtime) = split(/-/, $mainautovalue);
        if ($mainauto eq "day") {
            $mainoff = 0 if ($hour == $starttime && $endtime eq "");
            $mainoff = 0 if ($hour >= $starttime && $hour < $endtime);
        }
        elsif ($mainauto eq "week") {
            $wday = 7 if ($wday == 0);
            $mainoff = 0 if ($wday == $starttime && $endtime eq "");
            $mainoff = 0 if ($wday >= $starttime && $wday <= $endtime);
        }
        elsif ($mainauto eq "month") {
            $mainoff = 0 if ($mday == $starttime && $endtime eq "");
            $mainoff = 0 if ($mday >= $starttime && $mday <= $endtime);
        }
    }
    if ($mainonoff == 2) {
        $mainonoff = 1;
        my (undef, undef, $hour, $mday, undef, undef, $wday, undef) = localtime(time + $timezone * 3600);
        $mainautovalue1 =~ s/[^\d\-]//sg;
        my ($starttime, $endtime) = split(/-/, $mainautovalue1);
        if ($mainauto1 eq "day") {
            $mainonoff = 0 if ($hour == $starttime && $endtime eq "");
            $mainonoff = 0 if ($hour >= $starttime && $hour < $endtime);
        }
        elsif ($mainauto1 eq "week") {
            $wday = 7 if ($wday == 0);
            $mainonoff = 0 if ($wday == $starttime && $endtime eq "");
            $mainonoff = 0 if ($wday >= $starttime && $wday <= $endtime);
        }
        elsif ($mainauto1 eq "month") {
            $mainonoff = 0 if ($mday == $starttime && $endtime eq "");
            $mainonoff = 0 if ($mday >= $starttime && $mday <= $endtime);
        }
    }

    if (($mainoff == 1) || ($mainonoff == 1)) {require "doinmaintenance.pl";}
}
1;
