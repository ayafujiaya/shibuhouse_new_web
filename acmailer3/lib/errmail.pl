#!/usr/bin/perl


my $myfilepath = '/home/admin2/project/acmailer3.8/';
chdir $myfilepath;
use lib "./lib/";
use POSIX;
use MIME::Base64;
use File::Copy;
#require $myfilepath.'lib/jcode.pl';
#require $myfilepath.'lib/mimew.pl';
require 'setup.cgi';

our $SYS;
$SYS->{data_dir} = $myfilepath."data/";

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���������Ԥ��������å�
if (!$admindata->{errmail}) { exit; }

my %FORM;
# �᡼�����Ƽ���
my $v = getmaildata();

# ���򤴤Ȥ˥ե���������
&make_rireki_error($v->{hid}, $v->{sendto});

exit;

sub make_rireki_error() {
	my $hid = shift;
	my $email = shift;
	if (!$hid || !$email) { return 1; }
	
	my $file = $SYS->{data_dir}."hist_".$hid.".cgi";
	
	 # �ɲ���¸
	$objAcData->InsertFile($file, $email);
	chmod(0777, $file);
	
}

sub getmaildata {
	my %TIME = &getdatetime();
	my $message;
	my $boundary;
	my ($email, $to, $sendto, $hid);
	# ���٥᡼����ɤ߹�����¸����
	while (<STDIN>) {
		$message .=  $_;
	}
	
	&jcode::convert(\$message,"euc");

	# �إå�������ʸ��ʬ��&����
	my $mail_head = $message;
	$mail_head =~ s/\n\n(.*)//s;
	my $mail_body = $1;
	my @mail_head = split(/\n/,$mail_head);
	my @mail_body = split(/\n/,$mail_body);
	my $kind;
	my ($email_f, $subject_f, $body_f, $to_f, $sendto_f, $hid_f);
	foreach (@mail_body) {
		my $kind_data;
		if (/^(.*): (.*)$/i) {
			$kind = $1;
			$kind_data = $2;
		}
		# �������᡼�륢�ɥ쥹
		if ($kind =~ /from/i && !$email_f) {
			$email = $_;
			$mail_f = 1;
		}
		# TO�᡼�륢�ɥ쥹
		if ($kind =~ /to/i && !$to_f) {
			$to = $_;
			$to_f = 1;
		}
		
		# X-SENDTO�᡼�륢�ɥ쥹
		if ($kind =~ /x\-sendto/i && !$sendto_f) {
			$sendto = $_;
			$sendto_f = 1;
		}
		
		# X-HID ����
		if ($kind =~ /x\-hid/i && !$hid_f) {
			$hid = $kind_data;
			$hid_f = 1;
		}
		
	}

	# DOCOMO��AU�к� "asdf..asdf."@docomo.ne.jp�ߤ����ʥ��ɥ쥹�Ǥ������"�򳰤�
	if ($email =~ /[^\"]*(\")([^\"]*)\"(\@.*)$/) {
		$email = $2.$3;
	}
	if ($to =~ /[^\"]*(\")([^\"]*)\"(\@.*)$/) {
		$to = $2.$3;
	}
	if ($sendto =~ /[^\"]*(\")([^\"]*)\"(\@.*)$/) {
		$sendto = $2.$3;
	}
	
	
	# �᡼�륢�ɥ쥹����
	$email = lc(&getmailaddr($email));
	$to = lc(&getmailaddr($to));
	$sendto = lc(&getmailaddr($sendto));

	my $bound_count = 0;
	my $flag;
	my $chk_3gp;
	my @data;
	my $bodydata;
	foreach (@mail_body) {
		if ($boundary) {
			if(/(.*)$boundary(.*)/) {
				$bound_count++;
				next;
			}
			if ($bound_count == 1) {
				$bodydata .= $_."\n";
			}
		} else {
			$bodydata .= $_."\n";
		}
	
	}
	# ��̾B���󥳡��ɤ�ǥ�����
	my $lws = '(?:(?:\x0D\x0A|\x0D|\x0A)?[ \t])+';
	my $ew_regex = '=\?ISO-2022-JP\?B\?([A-Za-z0-9+/]+=*)\?=';
	$subject =~ s/($ew_regex)$lws(?=$ew_regex)/$1/gio;
	$subject =~ s/$lws/ /go;
	$subject =~ s/$ew_regex/decode_base64($1)/egio;
	&jcode::convert(\$subject, 'euc', 'jis');
	
	my $v;
		
	$v->{email} = $email;
	$v->{to} = $to;
	$v->{sendto} = $sendto;
	$v->{subject} = $subject;
	$v->{body} = $bodydata;
	$hid =~ s/ //g;
	$hid =~ s/\t//g;
	$hid =~ s/\r//g;
	$hid =~ s/\n//g;

	$v->{hid} = $hid;
	
	
	return $v;
	
}


sub error_mail {
	my $str = shift;
	#print STDERR "$str";
	if (!$FORM{email}) { $FORM{email} = $admindata->{admin_email}; }
	&jmailsend($sendmailpath,$FORM{email},"���顼",$str,$sendername,$sendername,$xmailer,$sendername);
	exit;
}
sub getmailaddr{
	my $mail = shift;
	# �᡼�륢�ɥ쥹����ɽ��
	$mail_regex = q{([\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)\@([\w|\!\#\$\%\'\(\)\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)};
	if($mail =~ /$mail_regex/o){
		$mail =~ s/($mail_regex)(.*)/$1/go;		# �᡼�륢�ɥ쥹�κǸ�ʹߤ���
		$mail =~ s/(.*)[^\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+($mail_regex)/$2/go;		# �᡼�륢�ɥ쥹�ޤǤ���
	}
	return $mail;
}


1;
