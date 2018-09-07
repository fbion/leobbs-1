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
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use strict;
use warnings;
use LBCGI;
$LBCGI::POST_MAX = 1024 * 800;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 0;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";

$|++;
$thisprog = "filemanage.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
$data = $query->param('data');

&getadmincheck;
&getmember($inmembername);
print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {
print qq~<tr><td bgcolor=#2159C9 colspan=2><font face=宋体  color=#FFFFFF>
<b>欢迎来到论坛管理中心 / 文件管理器</b>
</td></tr>~;

&user_error ("错误, 为了论坛的安全, 此功能尚未开放, <br>如果需要开放, 请修改 filemanage.cgi 文件,<br> 把第 51 行(&user_error 开头的)删除, 然后上传覆盖即可!", "");

#以下是文件扩展名与相应的图标文件的关联数组。如要更改，格式照抄。
%icons = (
           'ace'         => 'ace.gif',
           'class'       => 'applet.gif',
           'arj'         => 'arj.gif',
           'asp'         => 'asp.gif',
           'bmp'         => 'bmp.gif',
           'cab'         => 'cab.gif',
           'cgi'         => 'cgi.gif',
           'dll'         => 'dll.gif',
           'doc'         => 'doc.gif',
           'xls'         => 'excel.gif',
           'exe'         => 'exe.gif',
           'gif'         => 'gif.gif',
           'htm'         => 'htm.gif',
           'html'        => 'html.gif',
           'hwp'         => 'hwp.gif',
           'tif ico'     => 'img.gif',
           'jpg'         => 'jpg.gif',
           'jpeg'        => 'jpeg.gif',
           'mid'         => 'mid.gif',
           'fla swf'     => 'mov.gif',
           'mov'         => 'movie.gif',
           'mp3'         => 'mp3.gif',
           'mpeg'        => 'mpeg.gif',
           'mpg'         => 'mpg.gif',
           'pdf'         => 'pdf.gif',
           'pl'          => 'pl.gif',
           'png'         => 'png.gif',
           'ppt'         => 'ppt.gif',
           'ra rm'       => 'ra.gif',
           'rtf'         => 'rtf.gif',
           'js'          => 'script.gif',
           'wav'         => 'wav.gif',
           'sql'         => 'sql.gif',
           'tar'         => 'tar.gif',
           'txt'         => 'txt.gif',
           'torrent'     => 'torrent.gif',
           'gz'          => 'uuencoded.gif',
           'shtm shtml'  => 'html.gif',
           'au mod'      => 'sound1.gif',
           'zip'         => 'zip.gif',
           'vso'         => 'visio.gif',
           'rar'         => 'rar.gif',
           folder        => 'folder.gif',
           parent        => 'back.gif',
           unknown       => 'unknow.gif'
);

&main;

sub main {
        $working_dir = $query->param('wd');
        $filename    = $query->param('fn');
        $name        = $query->param('name');
        $newname     = $query->param('newname');
        $directory   = $query->param('dir');
        $newperm     = $query->param('newperm');
        $action      = $query->param('action');

        my ($error);
        ($working_dir, $error) = &is_valid_dir  ($working_dir); $error and &user_error ("无效的目录: '$working_dir'. 原因: $error", "$lbdir/$working_dir");
        ($filename,    $error) = &is_valid_file ($filename);    $error and &user_error ("无效的文件名: '$filename'. 原因: $error", "$lbdir/$working_dir");
        ($name,        $error) = &is_valid_file ($name);        $error and &user_error ("无效的名称: '$name'. 原因: $error", "$lbdir/$working_dir");
        ($newname,     $error) = &is_valid_file ($newname);     $error and &user_error ("无效的文件名: '$newname'. 原因: $error", "$lbdir/$working_dir");
        ($newperm,     $error) = &is_valid_perm ($newperm);     $error and &user_error ("无效的权限: '$newperm'. 原因: $error", "$lbdir/$working_dir");

        ($directory, $error)   = &is_valid_dir  ($directory);   $error and &user_error ("无效的目录: '$directory'. 原因: $error", "$lbdir/$working_dir");
        ($directory, $error)   = &is_valid_file ($directory);   $error and &user_error ("无效的目录: '$directory'. 原因: $error", "$lbdir/$working_dir");

        my ($dir, $url);
        if ($working_dir) {
            $dir   = "$lbdir/$working_dir";
            $url   = "$boardurl/$working_dir";
        } else {
            $dir   = $lbdir;
            $url   = $boardurl;
        }

        my $javascript = qq~
<script language="Javascript">
<!-- Hide from old browsers
function validateFileEntry(validString, field) {
var isCharValid = true;
var inValidChar;
for (i=0 ; i < validString.length ; i++) {
  if (validString.charAt(0) == '.') {
    isCharValid = false;
    i=validString.length;
  }
  if (validateCharacter(validString.charAt(i)) == false) {
    isCharValid = false;
    inValidChar = validString.charAt(i);
    i=validString.length;
  }
}           
if (i < 1) { return false; }           
if (isCharValid == false) {
  if (inValidChar) { alert("无效的文件名. 不能含有 '" + inValidChar + "'.");        }
  else             { alert("无效的文件名. 请重新输入."); }
  if (field)       { field.focus(); field.select(); }
    return false;
  }
  return true;
}
function validateCharacter(character) {
  if (character != '/' && character != '\') return true;
    else return false;
  }
function isNum(passedVal) {
  if (!passedVal) { return false }
  for (i=0; i<passedVal.length; i++) {
    if (passedVal.charAt(i) < "0") { return false }
    if (passedVal.charAt(i) > "7") { return false }
  }
  return true
}
function renameFile ( name ) {
  var newname = window.prompt("改名 '" + name + "' 为: ",'')
  if (newname != null) {
    if (validateFileEntry(newname)) {
      window.location.href = "filemanage.cgi?action=rename&name=" + name + "&newname=" + newname +"&wd=$working_dir"
    }
  }
}
function deleteFile ( name ) {
  if (window.confirm("你真的想删除文件'" + name + "'吗?")) {
    window.location.href = "filemanage.cgi?action=delete&fn=" + name + "&wd=$working_dir"
  }
}
function deleteDir ( name ) {        
  if (window.confirm("你真的想删除目录'" + name + "'吗?")) {
    window.location.href = "filemanage.cgi?action=removedir&dir=" + name + "&wd=$working_dir"
  }
}        
function changePermissions ( name ) {
  var newperm = window.prompt("改变文件'" + name + "' 的权限为: ",'')
  if (newperm == null) {  return;  }
  if (!isNum(newperm) || (newperm == "") || (length.newperm > 2)) {
    alert ("只需要三个数字! 输入八进制的权限数字. 如 755.")
  } else {
    window.location.href = "filemanage.cgi?action=permissions&name=" + name + "&newperm=" + newperm +"&wd=$working_dir"
  }
}
        
function serverFileName() {
  var fileName = window.document.Upload.data.value.toLowerCase();
  window.document.Upload.fn.value = fileName.substring(fileName.lastIndexOf("\\\\") + 1,fileName.length);
}
// -->
</script>
~;                

        my $nojavascript = qq~        
<noscript>
<table bgcolor="#FFFFFF" cellpadding=5 cellspacing=3 width=100% valign=top><tr><td><font color="red"><B>注意:&nbsp;&nbsp; </B></font><FONT COLOR="black">你的浏览器目前 <font color="red"><b>关闭了 JavaScript 功能</b></font> -- 文件管理器 必须使用 JavaScript.请进入浏览的参数选择项, 然后 <b>启用 JavaScript 功能</b>. 你可以按 <b>刷新</b> 按钮来继续使用 文件管理器.</FONT></td></tr></table>
</noscript>
~;

        print qq~
<html>
<head>
<title>文件管理器</title>
$javascript
</head>
<body bgcolor="#DDDDDD">
<center>
<table border="0" bgcolor="#FFFFFF" cellpadding="2" cellspacing="1" width="98%" align="center" valign="top">
<tr><td>
~;

        my ($result);
        CASE: {
                ($action eq 'write')           and do {
                                                         $result = &write ($dir, $filename, $data, $url);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'delete')          and do {
                                                         $result = &delete ($dir, $filename);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'makedir')         and do {
                                                         $result = &makedir    ($dir, $directory);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'removedir')       and do {
                                                         $result = &removedir  ($dir, $directory);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'rename')          and do {
                                                         $result = &rename_file ($dir, $name, $newname);
                                                         &list_files   ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'edit')            and do {
                                                         &edit ($dir, $filename, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'upload')          and do {
                                                         my $file_space;
                                                         ($file_space, $result) = &upload ($dir, $data, $filename);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'permissions')     and do {
                                                         $result = &change_perm ($dir, $name, $newperm);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                do {
                      print $nojavascript;
                      &list_files ('列出文件和目录.', $working_dir, $url);
                };
        };
        print qq~</td></tr></table>
  </body>
</html>
~;
}

sub list_files {
        my ($message, $working_dir, $url) = @_;
        my ($directory)   = "$lbdir/$working_dir";

        print qq~
                <P>
                <table bgcolor="#FFFFFF" cellpadding=5 cellspacing=3 width=100% valign=top>
                        <tr>
                                <td><B>目录对应:&nbsp;&nbsp; <a href="$url"><FONT COLOR="blue">$url</font></A></B></td>
                                <td align="right"><a href="filemanage.cgi">返回 CGI 根目录</a>&nbsp;&nbsp;&nbsp;&nbsp;</td><td>&nbsp;</td>
                        </tr>
                        <tr>
                                <td>命令: <font color=red><B>$message</B></font><br></td><td><br></td>
                                <td align="right"></td>
                        </tr>
                </table>
        </td></tr>
        <tr><td>
                <P>
                <table bgcolor="#FFFFFF" cellpadding=5 cellspacing=3 width=100% valign=top>
        ~;

        opendir (DIR, $directory);
        my @ls = readdir(DIR);
        closedir (DIR);

        my (%directory, %text, %graphic);
        my ($temp_dir, $newdir, @nest, $fullfile, $filesize, $filedate, $fileperm, $fileicon, $file);

        FILE: foreach $file (@ls) {
                next FILE if  ($file eq '.');
                next FILE if (($file eq '..') and ($directory eq "$lbdir/"));

                $fullfile = "$directory/$file";
                ($filesize, $filedate, $fileperm) = (stat($fullfile))[7,9,2];
                $fileperm = &print_permissions ($fileperm);
                $filesize = &print_filesize    ($filesize);
                $filedate = &get_date($filedate);

                if (-d $fullfile ) {
                        if ($file eq '..') {
                                @nest = split (/\//, $working_dir);
                                (pop (@nest)) ? 
                                        ($newdir = "filemanage.cgi?wd=" . join ("/", @nest)) :
                                        ($newdir = "filemanage.cgi");                                
                        }
                        else {
                                $working_dir ? ($temp_dir = "$working_dir%2F$file") : ($temp_dir = "$file");
                                $newdir   = "filemanage.cgi?wd=$temp_dir";
                        }
                        $newdir = $query->uri_escape($newdir);
                        if ($file eq '..') {
                                $fileicon = "$imagesurl/icon/$icons{'parent'}";
                                $directory{$file}  = qq~ <tr>\n~;
                                $directory{$file} .= qq~     <td><b><a href="$newdir"><img src="$fileicon" align=middle border=0></a></td> \n~;
                                $directory{$file} .= qq~     <td><a href="$url/$file"><font color=blue>$file</font></a></b></td> \n~;
                                $directory{$file} .= qq~     <td><font color="gray">$fileperm</font></td> \n~;
                                $directory{$file} .= qq~     <td>$filedate</td> \n~;
                                $directory{$file} .= qq~     <td></td>~;
                                $directory{$file} .= qq~     <td><b><a href="$newdir"><font color=black>上一级</font></a></B></td>
                                                                                         <td><br></td></tr>
                                                                        ~;                        
                        }
                        else {
                                $fileicon = "$imagesurl/icon/$icons{'folder'}";
                                $directory{$file}  = qq~ <tr>\n~;
                                $directory{$file} .= qq~     <td><b><a href="$newdir"><img src="$fileicon" align=middle border=0></a></td> \n~;
                                $directory{$file} .= qq~     <td><a href="$newdir"><font color=blue>$file</font></a></td> \n~;
                                $directory{$file} .= qq~     <td><a href="javascript:changePermissions('$file')"><font color="gray">$fileperm</font></a></td> \n~;
                                $directory{$file} .= qq~     <td>$filedate</td> \n~;
                                $directory{$file} .= qq~     <td></td>~;
                                $directory{$file} .= qq~     <td>&nbsp;</td>\n~;
                                $directory{$file} .= qq~     <td><a href="javascript:deleteDir('$file')"><font color=red>删除</font></A></td><td><a href="javascript:renameFile('$file')"><font color=purple>改名</font></a></td>\n~;
                                $directory{$file} .= qq~ </tr>\n~;                                
                        }
                }
                elsif (-T $fullfile) {
                        $fileicon = &get_icon($fullfile);
                        $text{$file}  = qq~  <tr>\n~;
                        $text{$file} .= qq~      <td><b><a href="$url/$file"><img src="$fileicon" align=middle border=0></a></td> \n~;
            		$text{$file} .= qq~      <td><a href="$url/$file"><font color=blue>$file</font></a></td> \n~;
                        $text{$file} .= qq~      <td><a href="javascript:changePermissions('$file')"><font color="gray">$fileperm</font></a></td> \n~;
                        $text{$file} .= qq~      <td>$filedate</td> \n~;
                        $text{$file} .= qq~      <td><b>$filesize</font></b></td> \n~;
                        $text{$file} .= qq~      <td><a href="filemanage.cgi?action=edit&fn=$file&wd=$working_dir"><font color=green>编辑</font></a></td>~;
                        $text{$file} .= qq~      <td><a href="javascript:deleteFile('$file')"><font color=red>删除</font></a></td>
                                                 <td><a href="javascript:renameFile('$file')"><font color=purple>改名</font></a></td></tr>
                        		~;
                }
                else {
                        $fileicon = &get_icon($fullfile);
                        $graphic{$file}  = qq~  <tr>\n~;
                        $graphic{$file} .= qq~      <td><b><a href="$url/$file"><img src="$fileicon" align=middle border=0></a></td> \n~;
                        $graphic{$file} .= qq~      <td><a href="$url/$file"><font color=blue>$file</font></a></td>              \n~;
                        $graphic{$file} .= qq~      <td><a href="javascript:changePermissions('$file')"><font color="gray">$fileperm</font></a></td> \n~;
                        $graphic{$file} .= qq~      <td><i>$filedate</font></i></td> \n~;
                        $graphic{$file} .= qq~      <td><b>$filesize</font></b></td> \n~;
                        $graphic{$file} .= qq~      <td><br></td>
                                                    <td><a href="javascript:deleteFile('$file')"><font color=red>删除</font></a></td>
                                                    <td><a href="javascript:renameFile('$file')"><font color=purple>改名</font></a></td></tr>
                        		   ~;
                }
        }
        foreach (sort keys %directory) {
                print $directory{$_};
        }
        foreach (sort keys %text) {
                print $text{$_};
        }
        foreach (sort keys %graphic) {
                print $graphic{$_};
        }

               print qq~
                        </table>
                </td></tr>
                <tr><td>                        
                        <table cellpadding=5 cellspacing=3 width=80% valign=top>
                                <tr><td align="left" valign="top" width=50%>
                                        <form method=post action="filemanage.cgi" name="createfile">
                                                <input type=hidden name="action" value="edit">
                                                <input type=hidden name="wd"     value="$working_dir">
                                                <font color="black"><B>建立一个新文档:</B><br>文件名: <input type=text name="fn" onBlur="validateFileEntry(this.value, this)" >
                                                <input type=submit value="建立文件"></font>
                                        </form>
                                </td><td align="left" rowspan=2 valign="top" width=50%>
                                        <form method=post action="filemanage.cgi">
                                                <input type=hidden name="action" value="makedir">
                                                <input type=hidden name="wd"     value="$working_dir">
                                                <font color="black"><B>建立一个新目录:</B><br>目录名: <input type=text name="dir" onBlur="validateFileEntry(this.value, this)" >
                                                <input type=submit value="建立目录"></font>
                                        </form>
                                </td></tr><tr><td valign="top" align="left">
                                        <form method=post action="filemanage.cgi" NAME="Upload" ENCTYPE="multipart/form-data">
                                                <input type=hidden name="wd"     value="$working_dir">
                                                <input type=hidden name="action" value="upload">
                                                <font color="black"><B>上传一个文件:</B><br>
                                                        本地文件名: <INPUT NAME="data" TYPE="file" onBlur="serverFileName()"><br>
                                                        远程文件名: <INPUT NAME="fn" onFocus="select()" onBlur="validateFileEntry(this.value, this)">
                                                <input type="submit" value="上传"></font>
                                        </form>
                                </td></tr>
                        </table>
                ~;

}

sub delete {
        my ($directory, $filename) = @_;
        my ($fullfile);

        (!$filename) and return "删除文件: 没有输入文件名!";

        ($directory =~ m,/$,) ? ($fullfile = "$directory$filename") : ($fullfile = "$directory/$filename");

        if (&exists($fullfile)) {
                unlink ($fullfile) ?
                        return "删除文件: '$filename' 已被删除." :
                        return "删除文件: '$filename' 不能被删除. 请检查文件属性.";
        }
        else {
                return "删除文件: '$filename' 不能被删除. 找不到文件.";
        }
}

sub edit {
        my ($directory, $filename, $working_dir, $url) = @_;
        my ($lines, $fullfile, $full_url);

        (!$filename) and return "编辑文件: 没有输入文件名!";

        ($directory =~ m,/$,) ? ($fullfile = "$directory$filename") : ($fullfile = "$directory/$filename");
        $full_url   = "$url/$filename";

        if (&exists($fullfile)) {
                open (DATA, "<$fullfile");
                $lines = join ("", <DATA>);
                $lines =~ s/<\/TEXTAREA/<\/TEXT-AREA/ig;
                close DATA;
                print qq!<p>编辑 <a href="$full_url"><B>$filename</B></A> 中需要修改的部份:</p>!;
        }
        else {
                $lines = qq~
<HTML>
<HEAD>
<TITLE></TITLE>
</HEAD>
        
<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#FF0000" VLINK="#800000" ALINK="#FF00FF">
        
</BODY>
</HTML>
                ~;
                print "<p>这是一个新文件. 在下面输入你的HTML代码:</p>";
        }

        print qq~
                <p><blockquote>
                        完成编辑后, 选择 "保存文档" 来保存 <B>$filename</B> 及返回主菜单
                        .
                </blockquote></p>
                <form method=post action="filemanage.cgi">
                <textarea name="data" rows=40 cols=60 wrap=virtual>$lines</textarea>
                <p>另存为文件名:
                           <input type=text name="fn" value="$filename"><br>
                                (输入另外一个文件名将会不改变 <B>$filename</B>
                                的内容，而你输入的内容将会保存为你输入的另外的文件名. 注意，如果该另外的文件也存在的话, 它将会被覆盖.)<P>
                        <input type=hidden name="action" value="write">
                        <input type=hidden name="wd"     value="$working_dir">
                        <input type=submit               value="保存文档">
                </form>
                </p>                
        ~;
}

sub write {
        my ($directory, $filename, $data, $url) = @_;
        my ($fullfile, $new);

        (!$filename) and return "编辑文件: 没有输入文件名!";        

        ($directory =~ m,/$,) ? ($fullfile = "$directory$filename") : ($fullfile = "$directory/$filename");

        $new = 1;
        (&exists($fullfile)) and ($new = 0);

        $data =~ s,</TEXT-AREA,</TEXTAREA,ig;

        open(FILE,">$fullfile");
                print FILE $data;
        close(FILE);

        if (&exists($fullfile)) {
                ($new eq 'yes') ?
                        return ("编辑文件: '$filename' 已被建立.") :
                        return ("编辑文件: '$filename' 已被编辑.");
        }
        else {
                return  ("编辑文件: 不能保存 '$filename'. 请检查权限.");
        }
}

sub upload {
        my ($directory, $data, $filename) = @_;
        my ($bytesread, $buffer, $fullfile, $file_size);

        if (!$filename) {
             $filename = $data =~ m|([^/:\\]+)$|;
	}
        ($directory =~ m,/$,) ?
                ($fullfile = "$directory$filename") :
                ($fullfile = "$directory/$filename");
        $file_size = 0;

	my $buffer;
        open    (OUTFILE, ">$fullfile");
        binmode (OUTFILE);        # For those O/S that care.
        binmode ($data); #注意
        while (read($data,$buffer,4096)) {
                print OUTFILE $buffer;
                $file_size += 4096;
        }
        close OUTFILE;
        close ($data); #注意
        &exists($fullfile) ?
                return (int($file_size / 1000), "上传文件: '$filename' 已上传.") :
                return (int($file_size / 1000), "上传文件: 不能上传 '$filename'. 请检查权限.");
}

sub makedir {
        my ($root, $new) = @_;
        my ($fulldir);

        (!$new) and return "建立目录: 你忘记输入目录名了!";

        ($root =~ m,/$,) ? ($fulldir = "$root$new") : ($fulldir = "$root/$new");

        if (&exists($fulldir)) {
                return "建立目录: '$new' 已经存在.";
        }
        else {
                mkdir ($fulldir, 0755) ?
                        return "建立目录: '$new' 目录已建立." :
                        return "建立目录: 不能建立目录. 请检查权限.";
        }
}

sub removedir {
        my ($root, $new) = @_;
        my ($fulldir);

        (!$new) and return "删除目录: 没有输入目录名!";

        ($root =~ m,/$,) ? ($fulldir = "$root$new") : ($fulldir = "$root/$new");

        if (!&exists($fulldir)) {
                return "删除目录: '$new' 不存在.";
        }
        else {
                rmdir($fulldir) ?
                        return "删除目录: '$new' 已被删除." :
                        return "删除目录: '$new' <B>不能</B> 删除. 检查目录是否为空.";
        }
}

sub rename_file {
        my ($directory, $oldfile, $newfile) = @_;

        (!$oldfile or !$newfile) and return "改名: 原文件名和目标文件名都必须输入!";

        my ($full_oldfile, $full_newfile);
        ($directory =~ m,/$,) ?
                ($full_oldfile = "$directory$oldfile"  and $full_newfile = "$directory$newfile") :
                ($full_oldfile = "$directory/$oldfile" and $full_newfile = "$directory/$newfile");

        (&exists($full_oldfile)) or  return "改名: 原文件 '$oldfile' 不存在.";
        (&exists($full_newfile)) and return "改名: 新文件 '$newfile' 已存在.";

        rename ($full_oldfile, $full_newfile);
        return "改名: '$oldfile' 已被改名为 '$newfile'.";
}

sub change_perm {
        my ($directory, $file, $newperm) = @_;
        my ($full_filename, $octal_perm);
        
        (!$file)    and return "改变权限: 没有输入文件名!";
        (!$newperm) and        return "改变权限: 没有输入新的权限!";

        $full_filename = "$directory/$file";
        (&exists($full_filename)) or return "改变权限: '$file' 不存在.";

        $octal_perm = oct($newperm);
        chmod ($octal_perm, $full_filename);
        return "改变权限: '$file' 权限已被改变.";
}

sub print_permissions {
        my $octal  = shift;
        my $string = sprintf "%lo", ($octal & 07777);
        my $result = '';
        foreach (split(//, $string)) {
                if    ($_ == 7) { $result .= "rwx "; }
                elsif ($_ == 6) { $result .= "rw- "; }
                elsif ($_ == 5) { $result .= "r-x "; }
                elsif ($_ == 4) { $result .= "r-- "; }
                elsif ($_ == 3) { $result .= "-wx "; }
                elsif ($_ == 2) { $result .= "-w- "; }
                elsif ($_ == 1) { $result .= "--x "; }
                elsif ($_ == 0) { $result .= "--- "; }
                else            { $result .= "unkown '$_'!"; }
        }
        return $result;
}

sub print_filesize {
        
        my $size = shift;
        my $formatted_size = int($size / 1000) . " KB";
        $formatted_size == 0 ?
                return "$size Byte" :
                return $formatted_size;
}

sub exists {
        return -e shift;
}

sub get_icon {
        my ($file) = lc(shift);
        my ($ext)  = $file =~ /\.([^.]+)$/;
        if (!$ext) { return "$imagesurl/icon/$icons{'unknown'}"; }
        foreach (keys %icons) {
                next if (/folder/);
                next if (/unknown/);
                next if (/parent/);
                ($_ =~ /$ext/i) and return "$imagesurl/icon/$icons{$_}";
        }
        return "$imagesurl/icon/$icons{'unknown'}";
}

sub get_date {
        my $time = shift;
        $time or ($time = time);
        my @months = qw!1 2 3 4 5 6 7 8 9 10 11 12!;

        my ($min, $hr, $day, $mon, $yr) = (localtime($time))[1,2,3,4,5];
        $yr = $yr + 1900;
        ($min < 10) and ($min = "0$min");
        ($hr  < 10) and ($hr  = "0$hr");
        ($day < 10) and ($day = "0$day");

        return "$yr-$months[$mon]-$day $hr:$min";

}

sub is_valid_file {
        my ($file, $okfile) = "";
        $file = shift;
	$okfile = $file;
        if ($file =~ m/[\/|\\]/) { return ($dir, "文件名中有非法字符. 不能使用 连结线 和 小数点."); }

        ($file =~ m,\.\.,)   and return ($file, "不允许有连续两个小数点在文件名中 .");
        ($file =~ m,^\.,)    and return ($file, "小数点不能在文件名的头部.");
        (length($file) > 20) and return ($file, "文件名太长. 请保持在 20 个字符以内.");

        return ($okfile, "");
}

sub is_valid_dir {
        my ($dir, $okdir, $last_dir) = "";
        $dir = shift;

        my (@size) = split (/\//, $dir);
        $last_dir  = pop (@size);
	$okdir = $dir;
        if ($dir =~ m/[\/|\\]/) { return ($dir, "目录名中有非法字符. 不能使用 连结线 和 小数点."); }

        ($dir =~ m,\.\.,)   and return ($dir, "不允许有连续两个小数点在文件名中 .");
        ($dir =~ m,^/,)                  and return ($dir, "目录名前不能有 / 号.");
        ($dir =~ m,/$,)                  and return ($dir, "目录名后不能有 / 号.");
        ($#size > 4)                     and return ($dir, "目录级太深.");
        (length($last_dir) > 25) and return ($dir, "目录名太长. 请保持在 25 个字符以内.");

        return ($okdir, "");
}

sub is_valid_perm {
        my ($perm) = shift;
        (!$perm)                                             and return ($perm, "");
        ($perm =~ /^([0-7][0-7][0-7])$/) or return ($perm, "权限值只能为三位数字, 0 to 7.");        
        return ($1, "");
}

sub user_error {
        my ($error, $wd) = @_;

        print qq~
<html>
<head>
        <title>文件管理器</title>
</head>
<body bgcolor="#DDDDDD">
        <center>
             <table bgcolor="#FFFFFF" cellpadding=2 cellspacing=1 width="630" align=center valign=top>
                        <tr><td colspan=3>
                                <p><b>错误!</b> 出现下列错误: </p>
                                <p><blockquote><font color=red><b>$error</b></font></blockquote></p>
                                <p>请按你浏览器的 <a href="javascript:history.go(-1)">返回</a> 键返回并修正错误.</p>
                        </td></tr>
                        <tr><td colspan=3>
                        </td></tr>
                </table>
        </center>
</body>
</html>
        ~;
        exit;
}

} else {
    &adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;