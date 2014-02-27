#!/usr/bin/perl
# 
# �᡼�������ѥ��饹�ʥǥ��᡼���б���

package clsMail;

use strict;

use Jcode;
#use Encode;
require 'mimew.pl';
require 'jcode.pl';
require 'mobileimg.cgi';
use strict;

# ���󥹥ȥ饯��
# ���������������������ѡ��ۥ���̾���ݡ��ȡ�ǧ�ڥ桼����ǧ�ڥѥ���ɡ�ǧ����ˡ
sub new {
	my $pkg = shift;
	my $relay_use = shift;
	my $relay_host = shift;
	my $relay_port = shift;
	my $relay_user = shift;
	my $relay_pass = shift;
	my $relay_send_mode = shift;
	my $qmail = shift;
	my $fail_send_local = shift;
        my $sendmail_i_option = shift;
	
	my @softbank = ('softbank.ne.jp', 't.vodafone.ne.jp', 'd.vodafone.ne.jp', 'h.vodafone.ne.jp', 'c.vodafone.ne.jp', 'r.vodafone.ne.jp', 'k.vodafone.ne.jp', 'n.vodafone.ne.jp', 's.vodafone.ne.jp', 'q.vodafone.ne.jp', 'disney.ne.jp', 'i.softbank.jp');
	
	bless {
		relay_use	  => $relay_use,
		relay_host	  => $relay_host,
		relay_port	  => $relay_port,
		relay_user	  => $relay_user,
		relay_pass	  => $relay_pass,
		relay_send_mode	  => $relay_send_mode,
		qmail             => $qmail,
		fail_send_local	  => $fail_send_local,
                sendmail_i_option => $sendmail_i_option,
		softbank	  => \@softbank,
	} ,$pkg;
}


sub send{
	my $this = shift;
	my $sendmail=shift;
	my $to=shift;
	my $subject=shift;
	my $body=shift;
	my $from=shift;
	my $replyto=shift;
	my $xmailer=shift;
	my $returnpath = shift;
	my $mail_type = shift;
	my $hid = shift;
	my $multi_text_body = shift;
	
	my $relay_host = shift;
	
	my $mailhead = "";
	my $mailfoot = "";
	my $mailmiddle = "";
	
	my $ismobile = 0;
	
	if ($mail_type eq "html" || $mail_type eq "multi") {
		
		my @softbank = @{$this->{softbank}};
		my $sb=0;
		foreach my $n (@softbank) {
			if ($to =~ /$n$/) {
				$sb = 1;
			}
		}
		
		# �ƥ���ꥢ���Ȥ˥᡼����ۿ����Ѥ���
		if ($to =~ /docomo\.ne\.jp$/) {
		#if (1) {
			# �ɥ���
			
			($mailhead, $subject, $body, $mailfoot) = $this->make_docomo($subject, $body);
			$ismobile = 1;
		} elsif ($to =~ /ezweb\.ne\.jp$/) {
			# EZWEB
			($mailhead, $subject, $body, $mailfoot) = $this->make_ezweb($subject, $body);
			$ismobile = 1;
		} elsif ($sb) {
			# ���եȥХ�
			($mailhead, $subject, $body, $mailfoot) = $this->make_softbank($subject, $body);
			$ismobile = 1;
		} else {
			# ����ʳ���PC�ʤɤ�HTML�᡼��
			
			#��̾����ʸ����ٳ�ĥSJIS���Ѵ�
# 			Encode::from_to($subject, "euc-jp","cp932");
# 			Encode::from_to($body, "euc-jp","cp932");
# 			Jcode::convert(\$subject, "cp932", "euc");
# 			Jcode::convert(\$body, "cp932", "euc");
			# ��̾����ʸ��JIS��
			&jcode::convert(\$subject, "jis");
			&jcode::convert(\$body, "jis");
			
			$mailhead = 'multipart/related; boundary="nextpt01"'."\n\n\n\n";
			$mailhead .= "--nextpt01\n".'Content-Type:multipart/alternative; boundary="nextpt02"'."\n\n\n";
			$mailhead .= '--nextpt02
Content-Type: text/html; charset="iso-2022-jp"
Content-Transfer-Encoding: 7bit

';

			# ����
			my $mailmiddle;
			($body, $mailmiddle) = $this->insert_image($body);
	
			$mailfoot = "

--nextpt02--
";
			$mailfoot .= $mailmiddle;
			$mailfoot .= "
--nextpt01--

";
			$subject = $this->sencode($subject);
		}
	} else {
		$mailhead = "text/plain; charset=\"ISO-2022-JP\"\n";
		$mailhead .= "Content-Transfer-Encoding: 7bit\n\n";
		# 
# 		#��̾����ʸ����ٳ�ĥSJIS���Ѵ�
# 		Encode::from_to($subject, "euc-jp","cp932");
# 		Encode::from_to($body, "euc-jp","cp932");
# 		# ��̾����ʸ��JIS��
 		&jcode::convert(\$subject, "jis");
 		&jcode::convert(\$body, "jis");
# 		
		$subject = $this->sencode($subject);
#  			Encode::from_to($subject, "euc-jp","iso-2022-jp");
#  			Encode::from_to($body, "euc-jp","iso-2022-jp");
		
	}
	
	
	#̤���ϥ��顼
	#if (!$sendmail){return 0;}
	if (!$to){return 0;}
	if (!$from){return 0;}
	
	
	# to,replyto,returnpath�ϥ᡼�륢�ɥ쥹�Τ����
	my $to_m = &getmail($this, $to);
	$replyto = &getmail($this, $replyto);
	$returnpath = &getmail($this, $returnpath);
	
	
	
	# FROM��TO�Υ��󥳡���
	#Encode::from_to($from, "euc-jp","cp932");
	&jcode::convert(\$from, "jis");
	#Encode::from_to($to, "euc-jp","cp932");
	&jcode::convert(\$to, "jis");
	
#	if (!$ismobile) {
#		#��̾����ʸ��JIS���Ѵ�
#		&jcode::convert(\$subject, "jis");
#		&jcode::convert(\$body, "jis");
#	}
	

	open (IN,"./data/writing.cgi");
	my $writing;
	while(<IN>){
		$writing .= $_;
	}
	close (IN);
    $writing =~ s/(\r\n|\n)//g;


	#�᡼��HEADER���
	my $senddata = "";
	$senddata .= "Return-Path: $returnpath \n" if $returnpath;
	$senddata .= "X-Mailer: acmailer3.0 http://www.ahref.org/\n";
	$senddata .= "X-SENDTO: $to\n";
	$senddata .= "X-HID: $hid\n";
	$senddata .= "X-SCD: $writing\n";
	$senddata .= "Reply-To: $replyto\n" if $replyto;
	$senddata .= main::mimeencode("To: $to\n");
	# ������̾�˥᡼�륢�ɥ쥹���ü��ʸ�������ä���������˥��󥳡��ɤ��Ƥ���ʤ�����
	#$senddata .= main::mimeencode("From: $from\n");
	$senddata .= "From: ".&sencode_from($this, $from)."\n";
	$senddata .= "Subject: $subject \n";
	$senddata .= "MIME-Version: 1.0\n";
	$senddata .= "Date:".&date($this)."\n";
	$senddata .= "Content-Type: $mailhead";
	#�᡼����ʸ���
	$senddata .= $body;
	
	# �ޥ���ѡ��Ȥξ��
	if ($mail_type eq "multi") {
		$senddata .= "

--nextpt02
";
		$senddata .= "Content-Type: text/plain; charset=\"ISO-2022-JP\"\n";
		$senddata .= "Content-Transfer-Encoding: 7bit\n\n";
		$senddata .= $body;
	}


	# �եå�
	$senddata .= $mailfoot;


	if ( $this->{relay_use} && $this->{relay_host} ) {

        # ���������Фˤ������
        if ( ! &relay_sendmail($this, $to, $from, $returnpath, $senddata) ) {

            # ������������³�����顼�ˤʤä�
        }
	}
    else {

        my @options;

        # qmail
        if ( $this->{qmail} ) {
            push @options, "-f $returnpath";
        }

        # i���ץ����
        if ( $this->{sendmail_i_option} ) {
            push @options, '-i';
        }

        # ���ץ��������
        my $option = join(' ', @options);


        # sendmail�ε�ư
        open(MAIL,"| $sendmail $option $to") || return undef;
        print MAIL $senddata;
        close(MAIL);
	}
	return 1;
}


# DOCOMO�ѥ᡼�����
# ����͡��إå�����̾����ʸ���եå�
sub make_docomo() {
	my $this = shift;
	my $subject = shift;
	my $body = shift;
	
	my ($mailhead, $mailmiddle, $mailfoot);
	
	#��̾����ʸ����ٳ�ĥSJIS���Ѵ�
	#Encode::from_to($subject, "euc-jp","cp932");
	#Encode::from_to($body, "euc-jp","cp932");
	# ��̾����ʸ��JIS��
	&jcode::convert(\$subject, "jis");
	&jcode::convert(\$body, "jis");
	
	
	$mailhead = 'multipart/mixed; boundary="nextpt00"
Content-Transfer-Encoding: 7bit

--nextpt00
Content-Type: multipart/related; boundary="nextpt01"

--nextpt01
Content-Type: multipart/alternative; boundary="nextpt02"


--nextpt02
Content-Type: text/html; charset="iso-2022-jp"
Content-Transfer-Encoding: quoted-printable

';
	
	$body = '<HTML><HEAD><META http-equiv=3D"Content-Type" content=3D"text/html; charset=3Diso-2022-jp"></HEAD>'.$body.'</BODY></HTML>';
	
	# DOCOMO�ϥ���ꥢ�����ɤ���
	my $career = 1;
	# ��ʸ������
	$subject = $this->insert_emoji($career, $subject);
	$body = $this->insert_emoji($career, $body);
	
	# ����
	($body, $mailmiddle) = $this->insert_image($body);
	
	use MIME;
	$body = MIME::encode_quoted($body);
	
	# ��̾�򥨥󥳡���
	$subject = $this->sencode($subject);
	
	# �եå�����
	
	$mailfoot = "
--nextpt02--
";
	$mailfoot .= "
";
	$mailfoot .= $mailmiddle."";
	$mailfoot .= "--nextpt01--
";
	$mailfoot .= "--nextpt00--

";
	return ($mailhead, $subject, $body, $mailfoot);
}

# SoftBank��
# ����͡��إå�����̾����ʸ���եå�
sub make_softbank() {
	my $this = shift;
	my $subject = shift;
	my $body = shift;
	my ($mailhead, $mailmiddle, $mailfoot);
	

	# ��̾����ʸ��UTF���Ѵ�
	Jcode::convert(\$body, "utf8");
	Jcode::convert(\$subject, "utf8");
	
	#Encode::from_to($subject, "euc-jp", "utf8");
	#Encode::from_to($body, "euc-jp", "utf8");
	
	$mailhead = 'multipart/related;
	boundary="nextpt01"


--nextpt01
Content-Type:multipart/alternative;
	boundary="nextpt02"


--nextpt02
Content-Type:text/html;charset=utf-8
Content-Transfer-Encoding:7bit


';
	
	# SOFTBANK�ϥ���ꥢ�����ɤ���
	my $career = 3;
	# ��ʸ������
	$subject = $this->insert_emoji($career, $subject);
	$body = $this->insert_emoji($career, $body);
	
	# ����
	($body, $mailmiddle) = $this->insert_image($body);
	
	# ��̾���󥳡���
	$subject = $this->sencode_utf($subject);
	
	$mailfoot = "

--nextpt02--
";
	$mailfoot .= $mailmiddle;
	$mailfoot .= "
--nextpt01--

";

	return ($mailhead, $subject, $body, $mailfoot);
}

# EZWEB��
sub make_ezweb() {
	my $this = shift;
	my $subject = shift;
	my $body = shift;
	my ($mailhead, $mailmiddle, $mailfoot);
	
	#��̾����ʸ����ٳ�ĥSJIS���Ѵ�
#	Encode::from_to($subject, "utf8","cp932");
#	Encode::from_to($body, "utf8","cp932");
	# ��̾����ʸ��JIS��
	&jcode::convert(\$subject, "jis");
	&jcode::convert(\$body, "jis");
	
	$mailhead = 'multipart/mixed; boundary="nextpt01"'."




";
	$mailhead .= '--nextpt01'."
Content-Type:multipart/alternative; ".'boundary="nextpt02"'."



";
 	$mailhead .= '--nextpt02
Content-Type: text/plain; charset="iso-2022-jp"
Content-Transfer-Encoding: 7bit




';
	$mailhead .= '--nextpt02'."
Content-Type:text/html; charset=\"iso-2022-jp\"\nContent-Transfer-Encoding: quoted-printable

";
	
	# EZWEB�ϥ���ꥢ�����ɤ���
	my $career = 2;
	# ��ʸ������
	$subject = &insert_emoji($this, $career, $subject);
	$body = &insert_emoji($this, $career, $body);
	
	# ����
	($body, $mailmiddle) = &insert_image($this, $body);
	
	use MIME;
	$body = MIME::encode_quoted($body);
	
	# ��̾�򥨥󥳡���
	$subject = &sencode($this, $subject);
	
	$mailfoot = "

--nextpt02--
";
	$mailfoot .= $mailmiddle;
	$mailfoot .= "
--nextpt01--

";
	
	return ($mailhead, $subject, $body, $mailfoot);
}

# ��ʸ������
sub insert_emoji($$) {
	my $this = shift;
	my $career = shift;
	my $str = shift;
	
	my $emoji = main::mobilemailimg($career);
	# ��ʸ��
	foreach my $n (keys %$emoji) {
		my $moji = $emoji->{$n};
		$str =~ s/{$n}/$moji/g;
	}
	return $str;
}

# ��������
# ����͡���ʸ���ߥɥ�إå�
sub insert_image($$) {
	my $this = shift;
	my $body = shift;
	my $mailmiddle = "";
	my @img = main::get_uploadimage();
	foreach my $ref (@img) {
		my $n = $ref->{file_name};
		my $num = $n;
		my $suf = "";
		my $serial = '@'.time.$$;
		if ($num =~ /^([0-9]*)\.([a-z]*)$/) {
			$num = $1;
			$suf = $2;
		}
		if ($suf =~ /jpg|jpeg/i) {
			$suf = "jpeg";
		}
		my $imgtag = "<img src= \"cid:img_cid_00$num$serial\">";
		
		if ($body =~ s/{img_$n}/$imgtag/g) {
			# �����ǡ�������
			open IN,"<./upload/$n" or main::error("�ե����뤬�����ޤ���$n $!");
			flock IN, 2;
			my $data = "";
			foreach my $n (<IN>) {
				$data .= $n;
			}
			flock IN, 8;
			close IN;
			use MIME::Base64;
			$data = MIME::Base64::encode_base64($data);
			$mailmiddle .= '--nextpt01
Content-Type: image/'.$suf.'; name="'.$n.'"
Content-Transfer-Encoding: base64
Content-ID: <img_cid_00'.$num.$serial.'>

'.$data;
		}
	}
	
	return ($body, $mailmiddle);
}





sub sencode_utf {
	my $this = shift;
	my ($subject) = shift;
	use MIME::Base64;
	$subject =~ s/\r\n|\r|\n//g;
	$subject = encode_base64($subject);
	$subject =~ s/\r\n|\r|\n//g;
	return("=?utf-8?B?$subject?=");
}


sub sencode {
	my $this = shift;
	my ($subject) = shift;
	use MIME::Base64;
	$subject =~ s/\r\n|\r|\n//g;
	$subject = encode_base64($subject);
	$subject =~ s/\r\n|\r|\n//g;
	return("=?ISO-2022-JP?B?$subject?=");
}

sub sencode_from {
	
	my $this = shift;
	my ($from) = shift;
	use MIME::Base64;
	# ̾����email��ʬ����
	if ($from =~ /^(.*)\<(.*)\>$/) {
		$from = $1;
		my $email = $2;
		$from =~ s/\r\n|\r|\n//g;
		$from = encode_base64($from);
		$from =~ s/\r\n|\r|\n//g;
		return("=?ISO-2022-JP?B?$from?= <".$email.">");
	} else {
		return $from;
	}
	
}


sub getmail{
	my $this = shift;
	my $mail = shift;
	my $mail_regex = q{([\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)\@([\w|\!\#\$\%\'\(\)\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)};
	if($mail =~ /$mail_regex/o){
		$mail =~ s/($mail_regex)(.*)/$1/go;		# �᡼�륢�ɥ쥹�κǸ�ʹߤ���
		$mail =~ s/(.*)[^\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+($mail_regex)/$2/go;		# �᡼�륢�ɥ쥹�ޤǤ���
	}
	return $mail;
}

sub relay_sendmail {
	# �����衦��̾����ʸ
	my $this = shift;
	my $relay_host = $this->{relay_host};
	my $relay_port = $this->{relay_port};
	my $relay_user = $this->{relay_user};
	my $relay_pass = $this->{relay_pass};
	my $sendmode = $this->{relay_send_mode};
	my $to = shift;
	my $from = shift;
    my $return_path = shift;
	my $senddata = shift;
	my $debug = shift;


    my $rcpt = $return_path || $from;

	eval{
		require Net::SMTP;
		require Net::POP3;
	};
	if($@){
		if ($debug) {
			print "Net::SMTP �⤷���� Net::POP3�Υ⥸�塼����ɤ߹��˼��Ԥ��ޤ��������������Ф����Ѥ��뤳�ȤϤǤ��ޤ���$@\n";
			return 0;
		} else {
			return 0;
		}
	}
	
	
	# SMTP ǧ�ڤξ��
	if ($sendmode eq "smtp_auth") {

		my $SMTP = Net::SMTP->new($relay_host,Port=>$relay_port,Debug =>$debug);
		
		if (!$SMTP) { print "SMTP�����Фؤ���³�ؼ��Ԥ��ޤ�����"; return 0; }
		
		# �ǥХå���
		if ($debug) {
			open(STDERR, ">&STDOUT");
		}
		
		# SMTPǧ��
		$SMTP->datasend("AUTH LOGIN\n");
		$SMTP->response();

		# ID
		$SMTP->datasend(encode_base64($relay_user) );
		$SMTP->response();

		#  PASS
		$SMTP->datasend(encode_base64($relay_pass) );
		$SMTP->response();

		# ������
		$SMTP->mail($rcpt);

		# ������
		if ($SMTP->to($to)) {
			
		} else {
			return 0;
		}

		$SMTP->data();

		# �إå�����
		$SMTP->datasend($senddata);
		$SMTP->datasend("\n");
		$SMTP->dataend();
		$SMTP->quit;
		return 1;
	} elsif ($sendmode eq "popbefore") {
			# ���֥�����������
			my $pop = Net::POP3->new("$relay_host");
			if (!$pop) { die "POP��������³����"; }
			my $auth = $pop->login($relay_user, $relay_pass);

			# POP�����Ф˥桼��ID�ȥѥ���ɤ���³
			if ($auth >= 0 && $auth ne "") {
				# ��³�Ǥ���н�λ
				$pop->quit;
			} else {
				# ��³���顼
				print "POPǧ�ڼ��Ԥ��ޤ�����";
				return 0;
			}
	}

	my $SMTP = Net::SMTP -> new( "$relay_host",		# SMTP�����С�̾�����
					Port=>$relay_port,				# PORT����
					Hello => "$relay_host",			# SMTP�ɥᥤ��̾�����
					Timeout => 60,Debug =>$debug);					# ��³�Ԥ����ƻ��֡��á�
	if (!$SMTP) { print "SMTP�����Фؤ���³�ؼ��Ԥ��ޤ�����"; return 0; }
	# �ǥХå���
	if ($debug) {
		open(STDERR, ">&STDOUT");
	}

	#�إå������Ȥ�Ω��
	$SMTP->mail($rcpt);							# �������᡼�륢�ɥ쥹�����
	if (!$SMTP->to($to)) { return 0; }			# ����᡼�륢�ɥ쥹�����

	#�ǡ��������Ȥ�Ω��
	$SMTP -> data();
	$SMTP -> datasend($senddata);				# ������(�ǡ�������
	$SMTP->datasend("\n");
	$SMTP -> dataend();							# �ǡ�����ü���᡼������
	$SMTP -> quit;								# SMTP��³�ν�λ

	
	return 1;
}

sub date {
	$ENV{'TZ'} = "JST-9";
	my ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
	my @week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	my @month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	my $d = sprintf("%s, %d %s %04d %02d:%02d:%02d +0900 (JST)",
	$week[$wday],$mday,$month[$mon],$year+1900,$hour,$min,$sec);
	return $d;
}
1;
