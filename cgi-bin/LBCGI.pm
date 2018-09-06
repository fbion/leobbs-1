package LBCGI;
require 5.005;
# Writed by LeoBBS Team
# Hacked by EasunLee 2005

use strict;
use Exporter;
use CGI qw (header param cookie redirect);
@LBCGI::ISA = qw (Exporter CGI);
@LBCGI::EXPORT = qw (header param cookie redirect uri_escape temppost lbhz cleaninput unclean unHTML HTML cleanarea stripMETA dateformatshort dateformat fulldatetime longdate shortdate dispdate longdateandtime shorttime helpfiles helpnewfiles getdir lockfilename winlock winunlock myrand encodeemail unescape);

initialize_globals();

sub new {
    my $class = shift;
    my $this = $class->SUPER::new( @_ );
       $this ->_initCGI(); #('gb2312');

    if ($CGI::MOD_PERL) {
        if ($CGI::MOD_PERL == 1) {
        my $r = Apache->request;
            $r->register_cleanup(\&LBCGI::_reset_globals);
        } elsif ($CGI::MOD_PERL == 2) {
            my $r = Apache2::RequestUtil->request;
            $r->pool->cleanup_register(\&LBCGI::_reset_globals);
        }
    }
    $class->_reset_globals if $CGI::PERLEX;

    return bless $this, $class;
}

sub _reset_globals {
   initialize_globals();
   #以下3行完全没有必要，写到这里仅仅是为了_reset_globals 调用，即MOD_PERL使用。
   $CGI::HEADERS_ONCE = $LBCGI::HEADERS_ONCE;
   $CGI::POST_MAX = $LBCGI::POST_MAX;
   $CGI::DISABLE_UPLOADS = $LBCGI::DISABLE_UPLOADS;
}

sub initialize_globals {
   $CGI::DefaultClass = __PACKAGE__;
   $LBCGI::AutoloadClass = 'CGI';

   # 初始值
   $LBCGI::LBCHARSET = 'gb2312';
   $LBCGI::HEADERS_ONCE = 1;
   $LBCGI::POST_MAX=2000;
   $LBCGI::DISABLE_UPLOADS = 1;
   # 初始 END

   $LBCGI::VERSION='0.03 Hacked By EasunLee';  #  版本号码
   $LBCGI::randseed = 0;
}

sub _initCGI {  #外部敷值
   # my($self,$str)= @_;
   my $self = shift;
   #$self ->charset($str);
   $self ->charset($LBCGI::LBCHARSET);
   $CGI::HEADERS_ONCE = $LBCGI::HEADERS_ONCE;
   $CGI::POST_MAX = $LBCGI::POST_MAX;
   $CGI::DISABLE_UPLOADS = $LBCGI::DISABLE_UPLOADS;
   return;
}

sub escape {
        my($self,$str)= CGI::self_or_CGI(@_);
        return $str if ($str =~ /\%/);
        return if !defined $str;
        $str=~ s/([^@\w\.\*\-\x20\:\/])/uc sprintf('%%%02x',ord($1))/eg;
        $str=~ tr/ /+/;
        $str;
}

sub uri_escape{
        my ($self, $str) = CGI::self_or_CGI(@_);
        return $str if ($str =~ /\%/);
        return unless (defined($str));
        $str =~ s/([^;\/?:@&=+\$,A-Za-z0-9\-_.!~*'()])/uc sprintf('%%%02x', ord($1))/eg;
        $str =~ tr/ /+/;
        return $str;
}

sub getdir {
        opendir (DIRS, "$main::lbdir");
        my @files = readdir(DIRS);
        closedir (DIRS);
        @files = grep(/^\w+?$/i, @files);
        my @memdir = grep(/^members/i, @files);
        my $memdir = $memdir[0];
        #    $memdir = "members" if ($memdir eq "");
        my @msgdir = grep(/^messages/i, @files);
        my $msgdir = $msgdir[0];
        #    $msgdir = "messages" if ($msgdir eq "");
        my @saledir = grep(/^sale/i, @files);
        my $saledir = $saledir[0];
        #    $memdir = "members" if ($memdir eq "");
        opendir(DIRS, $main::imagesdir);
        my @files = readdir(DIRS);
        closedir(DIRS);
        @files = grep(/^\w+?$/i, @files);
        my @usrdir = grep(/^usr/i, @files);
        my $usrdir = $usrdir[0];
        $usrdir = $usrdir[1] if (lc($usrdir) eq 'usravatars');
        return ("$memdir|$msgdir|$usrdir|$saledir");
}

sub helpnewfiles {
        my ($self, $helptype) = CGI::self_or_CGI(@_);
        #    my $helptype = shift;
        $helptype = uri_escape($helptype) if ($main::uri_escape ne "no");
        my $helpurl = qq~<span style="cursor: help" onClick="openScript('help.cgi?helpnew=$helptype', 500, 400)">~;
        return $helpurl;
}

sub helpfiles {
        my ($self, $helptype) = CGI::self_or_CGI(@_);
        #    my $helptype = shift;
        $helptype = uri_escape($helptype) if ($main::uri_escape ne "no");
        my $helpurl = qq~<span style="cursor: help" onClick="openScript('help.cgi?helpon=$helptype', 500, 400)">~;
        return $helpurl;
}

sub dateformatshort
{
        my ($self, $time) = CGI::self_or_CGI (@_);
        my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($time);
        sprintf ('%04d/%02d/%02d %02d:%02d', $year + 1900, $mon + 1, $mday, $hour, $min);
}

sub dateformat
{
        my ($self, $time) = CGI::self_or_CGI (@_);
        my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($time);
        sprintf ('%04d/%02d/%02d %02d:%02d%s', $year + 1900, $mon + 1, $mday, ($hour % 12), $min, ($hour > 11) ? 'pm' : 'am');
}

sub fulldatetime
{
        my ($self, $time) = CGI::self_or_CGI (@_);
        my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($time);
        sprintf ('%04d年%02d月%02d日 %02d:%02d%s', $year + 1900, $mon + 1, $mday, ($hour % 12), $min, ($hour > 11) ? 'pm' : 'am');
}

sub longdate
{
        my ($self, $time) = CGI::self_or_CGI (@_);
        my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($time);
        sprintf ('%04d年%02d月%02d日', $year + 1900, $mon + 1, $mday);
}

sub shortdate
{
        my ($self, $time) = CGI::self_or_CGI (@_);
        my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($time);
        sprintf ('%04d/%02d/%02d', $year + 1900, $mon + 1, $mday);
}

sub dispdate
{
        my ($self, $time) = CGI::self_or_CGI (@_);
        my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($time);
        sprintf ('%02d.%02d', $mon + 1, $mday);
}

sub longdateandtime
{
        my ($self, $time) = CGI::self_or_CGI (@_);
        my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($time);
        sprintf ('%04d年%02d月%02d日 %02d:%02d%s', $year + 1900, $mon + 1, $mday, ($hour % 12), $min, ($hour > 11) ? 'pm' : 'am');
}

sub shorttime
{
        my ($self, $time) = CGI::self_or_CGI (@_);
        my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ($time);
        sprintf ('%02d:%02d%s', ($hour % 12), $min, ($hour > 11) ? 'pm' : 'am');
}


sub temppost {
        my ($self, $tmp) = CGI::self_or_CGI(@_);
        study($tmp);
        $tmp =~ s/[\a\f\n\e\0\r\t]//isg;
        $tmp =~ s/(\&\#35\;|#)Moderation Mode//isg;
        $tmp =~ s/\[quote\](.*)\[\/quote\]//isg;
        $tmp =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg;
        $tmp =~ s/\[hide\](.+?)\[\/hide\]//isg;
        $tmp =~ s/\[(.+?)\]//isg;
        $tmp =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|jpeg|bmp|gif|swf)//isg;
        $tmp =~ s/<(.|\n)+?>//isg;
        $tmp =~ s/\:.{0,20}\://isg;
        $tmp =~ s/  / /isg;
        $tmp =~ s/^( )+//isg;
        $tmp =~ s/\[USECHGFONTE\]//sg;
        $tmp =~ s/\[DISABLELBCODE\]//sg;
        $tmp =~ s/\[POSTISDELETE=(.+?)\]//sg;
        return $tmp;
}

sub cleaninput {
        my ($self, $text) = CGI::self_or_CGI(@_);
        #    my $text = shift;
        study($text);
        $text =~ s/[\a\f\e\0\r\t]//isg;
        $text =~ s/\&nbsp;/ /g;
        $text =~ s/\@ARGV/\&\#64\;ARGV/isg;
        $text =~ s/\;/\&\#59\;/isg;
        $text =~ s/\&/\&amp;/g;
        $text =~ s/\&amp;\#/\&\#/isg;
        $text =~ s/\&amp\;(.{1,6})\&\#59\;/\&$1\;/isg;
        $text =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
        $text =~ s/"/\&quot;/g;
        $text =~ s/  / \&nbsp;/g;
        $text =~ s/</\&lt;/g;
        $text =~ s/>/\&gt;/g;
        $text =~ s/  / /g;
        $text =~ s/\n\n/<p>/g;
        $text =~ s/\n/<br>/g;
        $text =~ s/document.cookie/documents\&\#46\;cookie/isg;
        $text =~ s/'/\&\#039\;/g;
        $text =~ s/\$/&#36;/isg;
        $text =~ s/#/&#35;/isg;
        $text =~ s/&&#35;/&#/isg;
        return $text;
}
sub unclean {
        my ($self, $text) = CGI::self_or_CGI(@_);
        $text =~ s/\&\#35\;/#/isg;
        $text =~ s/\&amp;/\&/g;
        $text =~ s/\&quot;/"/g;
        $text =~ s/ \&nbsp;/　/g;
        $text =~ s/\&\#039\;/'/g;
        return $text;
}
sub unHTML {
        my ($self, $text) = CGI::self_or_CGI(@_);
        $text =~ s/\&/\&amp;/g;
        $text =~ s/"/\&quot;/g;
        $text =~ s/  / \&nbsp;/g;
        $text =~ s/</\&lt;/g;
        $text =~ s/>/\&gt;/g;
        $text =~ s/[\a\f\e\0\r\t]//isg;
        $text =~ s/document.cookie/documents\&\#46\;cookie/isg;
        $text =~ s/'/\&\#039\;/g;
        $text =~ s/\$/&#36;/isg;
        return $text;
}
sub HTML {
        my ($self, $text) = CGI::self_or_CGI(@_);
        $text =~ s/\&amp;/\&/g;
        $text =~ s/\&quot;/"/g;
        $text =~ s/ \&nbsp;/　/g;
        $text =~ s/\&lt;/</g;
        $text =~ s/\&gt;/>/g;
        $text =~ s/documents\&\#46\;cookie/document.cookie/isg;
        $text =~ s/\&\#039\;/'/g;
        $text =~ s/&#36;/\$/isg;
        return $text;
}
sub cleanarea {
        my ($self, $text) = CGI::self_or_CGI(@_);
        study($text);
        $text =~ s/[\a\f\e\0\r\t]//isg;
        $text =~ s/\&nbsp;/ /g;
        $text =~ s/\@ARGV/\&\#64\;ARGV/isg;
        $text =~ s/\;/\&\#59\;/isg;
        $text =~ s/\&/\&amp;/g;
        $text =~ s/\&amp;\#/\&\#/isg;
        $text =~ s/\&amp\;(.{1,6})\&\#59\;/\&$1\;/isg;
        $text =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
        $text =~ s/"/\&quot;/g;
        $text =~ s/  / \&nbsp;/g;
        $text =~ s/</\&lt;/g;
        $text =~ s/>/\&gt;/g;
        $text =~ s/  / /g;
        $text =~ s/\n\n/<p>/g;
        $text =~ s/\n/<br>/g;
        $text =~ s/document.cookie/documents\&\#46\;cookie/isg;
        $text =~ s/'/\&\#039\;/g;
        $text =~ s/\$/&#36;/isg;
        $text =~ s/#/&#35;/isg;
        $text =~ s/&&#35;/&#/isg;
        return $text;
}
sub stripMETA {
        my ($self, $file) = CGI::self_or_CGI(@_);
        $file =~ s/[<>\^\(\)\{\}\a\f\n\e\0\r\"\`\&\;\|\*\?]//g;
        return $file;
}
sub lbhz {
        my ($self, $str, $maxlen) = CGI::self_or_CGI(@_);
        return $str if (length($str) <= $maxlen);
        $str = substr($str, 0, $maxlen-4);
        if ($str =~ /^([\000-\177]|[\200-\377][\200-\377])*([\000-\177]|[\200-\377][\200-\377])$/){return $str . " ...";}
        else{chop($str);return $str . "　...";}
}
sub lockfilename{
        my ($self, $lockfilename) = CGI::self_or_CGI(@_);
        $lockfilename =~ s/\\/\//isg;
        $lockfilename =~ s/\://isg;
        $lockfilename =~ s/\//\_/isg;
        $lockfilename =~ s/\.\.//isg;
        $lockfilename = "${main::lbdir}lock/$lockfilename";
        return $lockfilename;
}
sub winlock{
        my ($self, $lockfile) = CGI::self_or_CGI(@_);
        my $i = 0;
        $lockfile =~ s/\\/\//isg;
        $lockfile =~ s/\://isg;
        $lockfile =~ s/\//\_/isg;
        $lockfile =~ s/\.\.//isg;
        $lockfile = "${main::lbdir}lock/$lockfile.lck";
        while (-e $lockfile){
                last if ($i >= 15);
                select(undef, undef, undef, 0.2);
                $i++;
        }
       open(LOCKFILE, ">$lockfile");
       close(LOCKFILE);
       return;
}
sub winunlock{
        my ($self, $lockfile) = CGI::self_or_CGI(@_);
        $lockfile =~ s/\\/\//isg;
        $lockfile =~ s/\://isg;
        $lockfile =~ s/\//\_/isg;
        $lockfile = "${main::lbdir}lock/${lockfile}.lck";
        unlink($lockfile);
        return;
}
sub myrand{
        my ($self, $max) = CGI::self_or_CGI(@_);
        my $result;
        my $randseed =$LBCGI::randseed ;
        $max ||= 1;
        eval("\$result = rand($max);");
        return $result unless ($@);
        $randseed = time unless ($randseed);
        my $x = 0xffffffff;
        $x++;
        $randseed *= 134775813;
        $randseed++;
        $randseed %= $x;
        return $randseed * $max / $x;
}
sub unescape {
        my($self,$str)= CGI::self_or_CGI(@_);
        return if !defined $str;
        $str=~ tr/+/ /;
        $str=~ s/%([0-9a-fA-F]{2})/chr hex($1)/eg;
        $str;
}
sub toGMTstring {
        my($self,$time,$format)= CGI::self_or_CGI(@_);
        $format ||= 'http';
        my @MON=qw/Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec/;
        my @WDAY=qw/Sun Mon Tue Wed Thu Fri Sat/;
        my %mult=( 's'=>1,'m'=>60,'h'=>60*60,'d'=>60*60*24,'M'=>60*60*24*30,'y'=>60*60*24*365);
        if (!$time || (lc($time) eq 'now') || $time =~/^\s*$/) {$time = time;}
        elsif ($time=~ /^\s*\d+\s*$/){$time = scalar($time);}
        elsif ($time=~/^([+-]?(?:\d+|\d*\.\d*))([mhdMy]?)/) {$time = time+($mult{$2} || 1)*$1;}
        else{return $time;}
        my($sc)=($format eq "cookie") ? '-' : ' ';
        my($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime($time);
        return sprintf("%s, %02d$sc%s$sc%04d %02d:%02d:%02d GMT",$WDAY[$wday],$mday,$MON[$mon],$year+1900,$hour,$min,$sec);
}


sub encodeemail{
        my ($self, $email) = CGI::self_or_CGI(@_);
        my $char = '';
        while ($email =~ /([a-z\@]{1})/is){
                $char = '&#' . ord($1) . ';';
                $email =~ s/$1/$char/sg;
        }
        return $email;
}
1;