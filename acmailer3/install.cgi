#!/usr/bin/perl

#use Encode;
#use Jcode;
use Socket;
use FileHandle;

my %FORM = &form();
my $app_name = 'acmailer3.8.15';
my $serial = '13934652837091712_acmailer3.8.15';
my $perl_path = '#!/usr/bin/perl';
my $suexec = '';

select(STDOUT);
$|=1;
select(STDOUT);

&htmlheader;



# PERL�С����������å�
my $perlv = $];
#if ($perlv !~ /5\.008/) {
#	print '�ܥץ�����Perl5.8�ʹߤǤ���ư��ޤ���';
#	exit;
#}

if(!-w "./"){
	

	&error('<b>���󥹥ȡ�����������å�</b></font><br><br>install.cgi�����֤��Ƥ���ǥ��쥯�ȥ�Υѡ��ߥå��������������ꤷ���٤��������������<a href="http://www.acmailer.jp/docs/install">�إ��</a>��');
	
}

if ($FORM{exec}) {
	print '<div id="wrapper">
	<div id="header">
    	<p>'.$app_name.'</p>
    </div>
    <div id="cont_body">
    	<div id="cont_top">
        	<p id="cont_top_title">���������᡼�顼CGI�����ȥ��󥹥ȡ��顼�ؤ褦����</p>
            <p class="cont_top_text"><b><font >�������󥹥ȡ�����Ǥ���������</font></b></p>
            <p class="cont_top_text"></p>
            <ul>
            	<li class="red">�����Ǥ˥ե����뤬¸�ߤ�����Ͼ�񤭤���ޤ��ΤǤ���դ���������</li>
                <li class="red">�����󥹥ȡ��봰λ��ϡ���CGI��install.cgi�פ������Ƥ���������</li>
            </ul>
        </div>
		<div id="message"></div>
        <div id="cont_middle">
        	<div id="loading">
            	<div id="loading_bar">
                	<img src="http://www.ahref.org/cgi/install/img/loading_bar_main.jpg" alt="" style="width:0px;height:20px;" id="progre" />
                </div>
            </div>
            <div id="loading_file"> 
            	<p id="file_name"> <div id="keika" style="display:none;">��50/100��</div></p>
            </div>
        </div>
        <div id="add">
        	<iframe src="http://www.ahref.org/cgi/install/add.html" name="in" width="415" height="100" scrolling="no" frameborder="0"></iframe>
			<p style="font-size:10px;line-height:2em;">������å��ǿ�����������ɥ��������ޤ���</p>
        </div>
    </div>
    <div id="footer">&nbsp;</div>
</div>
';
	&htmlfooter;
} else {
	print '<div id="wrapper">
	<div id="header">
    	<p>'.$app_name.'</p>
    </div>
    <div id="cont_body">
    	<div id="cont_top">
        	<p id="cont_top_title">���������᡼�顼CGI�����ȥ��󥹥ȡ��顼�ؤ褦����</p>
            <p class="cont_top_text">�������'.$app_name.'�פΥ��󥹥ȡ����Ԥ��ޤ���</p>
            <p class="cont_top_text">���γ��ϥܥ���򥯥�å��������󥹥ȡ���򳫻Ϥ��Ƥ���������</p>
            <ul>
            	<li class="red">�����Ǥ˥ե����뤬¸�ߤ�����Ͼ�񤭤���ޤ��ΤǤ���դ���������</li>
                <li class="red">�����󥹥ȡ��봰λ��ϡ���CGI��install.cgi�פ������Ƥ���������</li>
            </ul>
        </div>
		<div id="message"></div>
        <div id="cont_middle" style="display:none;">
        	
			
        </div>
        <div id="add" style="display:none;">
        	
        </div>
    </div>
    <div id="footer"><form action="install.cgi" method="post"><input type="hidden" name="exec" value="1"><input type="submit" value="����"></form></div>
</div>
';
	&htmlfooter;
	exit;
}

# �оݤΥ��ץꥱ������󤬤��뤫
my $serverchk = &get_source('exist', $app_name, '&serial='.&URLEncode($serial));
if ($serverchk eq "NG") {
	
	&error2('������¦�Υե����뤬����ޤ���');
	
	exit;
} elsif ($serverchk eq "LIMIT") {
	&error2('ͭ�������ڤ�Ǥ���');

	exit;
} elsif ($serverchk eq "NOEXIST") {
	&error2('���ꥢ�뤬�����Ǥ���');
	exit;
} elsif ($serverchk eq "NOSERIAL") {
	&error2('�����ʥ��������Ǥ���');
	exit;
}
# ���󥹥ȡ���ե�����ꥹ�ȼ���
my $list = &get_source('getlist', $app_name, '&serial='.&URLEncode($serial));

# �оݥե��������
my @list = split(/\r\n|\r|\n/, $list);
my @file;
my $i = 0;
my $bad = 0;
my $histid = 0;

foreach my $ref (@list) {
	my ($filename, $perm, $dir) = split(/\t/, $ref);
	
	if (!$filename && $perm =~ /^\d*$/) {
		$histid = $perm;
	}
	
	if (!$filename) { next; }
	if ($suexec) {
		$perm = substr($perm, 1, 1)."00";
	}
	push(@file, $filename);
	my $filename_sjis = $filename;
	#Encode::from_to($filename_sjis, "utf8","cp932");
	#&Jcode::convert(\$filename_sjis,"sjis", "utf8");
	
	my $ok = 1;
	# �񤭹���
	if ($dir eq "d") {
		print '<script type="text/javascript"><!--	
document.getElementById(\'file_name\').innerHTML = \'<font color=blue>�ǥ��쥯�ȥ������'.$filename."</font>\'
// --></script>";
		
		if (! -e $filename_sjis) { `mkdir $filename_sjis`; }
		my $test = chown $uid, $gid, $filename_sjis;
		#chmod oct($perm), $filename_sjis;
		if ($suexec) {
			#chmod 0700, $filename_sjis;
		} else {
			chmod 0777, $filename_sjis;
		}
		if (! -e $filename_sjis) { $ok = ""; }
	} else {
		print '<script type="text/javascript"><!--	
document.getElementById(\'file_name\').innerHTML = \''.$filename."�򥤥󥹥ȡ�����\';
// --></script>";

		my $data = &get_source('getsource', &URLEncode($app_name), '&filename='.&URLEncode($filename_sjis).'&serial='.&URLEncode($serial));
		my @data = split(/\r\n|\r|\n/, $data);
		my $datacnt = 0;
		my $regdata;
		
select(STDOUT);
$|=1;
select(STDOUT);
		if ($filename !~ /\.gif|\.jpg|\.jpeg/) {
			foreach my $ref (@data) {
				if ($datacnt == 0 && $ref =~ /\#\!\//) {
					$regdata .= $perl_path."\n";
				} else {
					$regdata .= $ref."\n";
				}
				$datacnt++;
			}
		} else {
			$regdata = $data;
		}
		open F,">$filename_sjis" or $ok = "";
		flock F,2;
		print F $regdata;
		flock F,8;
		close F;
		chown $uid, $gid, $filename_sjis;
		chmod oct($perm), $filename_sjis;
	}
	$i++;
	if ($ok) {
		#print '<script type="text/javascript"><!--	
#document.getElementById(\'file_name\').innerHTML = "'.$i." / ".($#list + 1).'
#// --></script>';
		#print "....................<font color=\"blue\" size=\"-1\">ok</font><br>\n";
	} else {
		#print "....................<font color=\"red\" size=\"-1\">error</font><br>\n";
		$bad = 1;
	}
	print '<script type="text/javascript"><!--	
document.getElementById(\'keika\').innerHTML = "'.$i." / ".($#list + 1).'";
// --></script>';

	my $per = ($i / ($#list + 1));
	$per = 413 * $per;
	if ($per >= 413) { $per = 413; }
	if ($per == 413) {
		print '<script type="text/javascript"><!--	
document.getElementById(\'progre\').src = "http://www.ahref.org/cgi/install/img/loading_bar_fin.jpg";
// --></script>';
	} else {
		print '<script type="text/javascript"><!--	
document.getElementById(\'progre\').style.width = '.$per.' + "px";
// --></script>';
	}
	
}

if ($bad) {
	$serverchk = &get_source('complete', $app_name, '&complete=0&perlv='.$perlv.'&histid='.&URLEncode($serial).'&histid='.$histid);
	print '<script type="text/javascript"><!--	
	document.getElementById(\'cont_top\').innerHTML = \'<p id="cont_top_title">���������᡼�顼CGI�����ȥ��󥹥ȡ��顼�ؤ褦����</p>      <p class="cont_top_text"><font color=red><b>���󥹥ȡ���˼��Ԥ��ޤ���<br><br>��γ��ؤΥѡ��ߥå����ʤɤ��ǧ���Ƥ���������</b></font>��<a href="http://www.ahref.org/cgi/acmailer/acmail.html#install">�إ��</a>��</p>\';
	// --></script>';
} else {
	$serverchk = &get_source('complete', $app_name, '&complete=1&perlv='.$perlv.'&serial='.&URLEncode($serial).'&histid='.$histid);
	print '<script type="text/javascript"><!--	
	document.getElementById(\'cont_top\').innerHTML = \'<p id="cont_top_title">���������᡼�顼CGI�����ȥ��󥹥ȡ��顼�ؤ褦����</p>            <p class="cont_top_text"><font color=blue><b>���󥹥ȡ��봰λ���ޤ�����</b><br><br></font>���������̤ؤ��ʤߤ���������<br><br>�ޤ�������install.cgi�ץ��������פȤʤ뤿�������Ƥ���������</font></p>\';
	// --></script>';
	print '<script type="text/javascript"><!--	
	document.getElementById(\'cont_top\').style.backgroundImage = \'url(http://www.ahref.org/cgi/install/img/cont_top_bg_fin.jpg)\';
	// --></script>';
	print '<script type="text/javascript"><!--	
	document.getElementById(\'add\').style.display = \'none\';
	document.getElementById(\'cont_middle\').style.display = \'none\';
	document.getElementById(\'footer\').innerHTML = "<form action=\"login.cgi\"><input type=\"submit\" value=\"���������̤�\"></font>";
	// --></script>';
	
	
	
}
print '<script type="text/javascript"><!--	
document.getElementById(\'file_name\').style.display = \'none\';
// --></script>';

#chown $uid, $gid, @file;
open (F,"> ./data/writing.cgi");
print(F $serial);
close(F);

exit;


sub get_source {
	my $mode = shift;
	my $app = shift;
	my $other = shift;
	my $param = 'mode='.$mode.'&app_name='.&URLEncode($app).$other;
	my $data;
	$host0 = "www.ahref.org";
	$port0 = getservbyname("http", "tcp");
	$ipaddr = inet_aton($host0)   or print "�ۥ���̾���Х��顼��$host0��<br>\n";
	$sock_addr = pack_sockaddr_in($port0, $ipaddr);
	socket(SOCK, PF_INET, SOCK_STREAM, 0)   or print "�����åȺ������顼��$ipaddr / $port0��<br>\n";
	connect(SOCK, $sock_addr)   or print "�����С���³���顼��$ipaddr / $port0��<br>\n";
#	select(SOCK);
#	$|=1;
#	select(STDOUT);
	my $host = $ENV{REQUEST_URI};
	if ($host =~ /(.*)\/[^\/]*\.cgi.*$/) {
		$host = 'http://'.$ENV{HTTP_HOST}.$1;
	}
	$host = URLEncode($host);
	$param .= "&host=".$host;

	autoflush SOCK (1);
	print SOCK "GET /cgi/install/release.cgi?$param HTTP/1.0\n";
	print SOCK "Host:www.ahref.org \n\n";  

	while(<SOCK>){
		last if m/^\r\n$/;
	}
	while(<SOCK>){
		$data .= $_;
	}
	close SOCK;
	return $data;
}
sub URLEncode($) {
	my $n = shift;
	$n =~ s/([^\w ])/'%' . unpack('H2', $1)/eg;
	$n =~ tr/ /+/;
	$n;
}

sub form {
	my $buffer;
	my %FORM;
	my $noexchange = shift;
	
	# �ե����फ�������
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	}else {
		$buffer = $ENV{'QUERY_STRING'};
	}
	my @pairs = split(/&/,$buffer);
	foreach (@pairs) {
		my ($name, $value) = split(/=/, $_);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
		$name =~ tr/+/ /;
		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
		$name =~ s/\r\n/\n/g;
		$name =~ s/\r/\n/g;
		$value =~ s/\r\n/\n/g;
		$value =~ s/\r/\n/g;

		$name =~ s/SPRIT_STR/ /g;
		$value =~ s/SPRIT_STR/ /g;

		$FORM{$name} = $value;
	
	}
	return %FORM;

}


sub htmlheader{


print <<EOF;
Content-Type: text/html; charset=EUC-JP

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP" />
<title>$app_name ���󥹥ȡ��顼</title>
<link rel="stylesheet" href="http://www.ahref.org/cgi/install/css/common.css" type="text/css" />
<link rel="stylesheet" href="http://www.ahref.org/cgi/install/css/install.css" type="text/css" />
</head>

<body>
EOF
}

# ////////////////////////////////////////////////////////////////////////// #
sub htmlfooter{

# ///////////////////////////////////////////////////////////////// #
# �ڽ��ס����ɽ���ˤĤ���
# 
# AHREF �ե꡼CGI�ǤϤ����Ѥˤ��������ɽ���򤪴ꤤ���Ƥ���ޤ���
# ���ɽ����Ϥ����ˤϤ������������������
# �������ɽ���ˤĤ���
# http://www.ahref.org/cgityosaku.html
# ///////////////////////////////////////////////////////////////// #

print <<EOF;


</body>
</html>


EOF
}

sub error() {
	my $msg = shift;
	
	
	print '<div id="wrapper">
	<div id="header">
    	<p>'.$app_name.'</p>
    </div>
    <div id="cont_body">
    	<div id="cont_top">
        	<p id="cont_top_title">���������᡼�顼CGI�����ȥ��󥹥ȡ��顼�ؤ褦����</p>
            <p class="cont_top_text"><b><font >�������󥹥ȡ�����Ǥ���������</font></b></p>
            <p class="cont_top_text"></p>
            <ul>
            	<li class="red">�����Ǥ˥ե����뤬¸�ߤ�����Ͼ�񤭤���ޤ��ΤǤ���դ���������</li>
                <li class="red">�����󥹥ȡ��봰λ��ϡ���CGI��install.cgi�פ������Ƥ���������</li>
            </ul>
        </div>
		<div id="message"></div>
        <div id="cont_middle" style="display:none;">
        	
			
        </div>
        <div id="add" style="display:none;">
        	
        </div>
    </div>
    <div id="footer">&nbsp;</div>
</div>
';
		print '<script type="text/javascript"><!--	
	document.getElementById(\'cont_top\').innerHTML = \'<p id="cont_top_title">���������᡼�顼CGI�����ȥ��󥹥ȡ��顼�ؤ褦����</p>      <p class="cont_top_text"><font color=red>'.$msg.'<br><br></p>\';
	// --></script>';

	&htmlfooter;
	exit;
	
}



sub error2() {
	my $msg = shift;
	
		print '<script type="text/javascript"><!--	
	document.getElementById(\'cont_top\').innerHTML = \'<p id="cont_top_title">���������᡼�顼CGI�����ȥ��󥹥ȡ��顼�ؤ褦����</p>      <p class="cont_top_text"><font color=red><b>',$msg.'</b></font></p>\';
	// --></script>';

		print '<script type="text/javascript"><!--	
	document.getElementById(\'add\').style.display = \'none\';
	document.getElementById(\'cont_middle\').style.display = \'none\';

// --></script>';

	&htmlfooter;
	exit;
	
}