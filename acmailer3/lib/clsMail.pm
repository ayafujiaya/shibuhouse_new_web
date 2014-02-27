#!/usr/bin/perl
# 
# メール送信用クラス（デコメール対応）

package clsMail;

use strict;

use Jcode;
#use Encode;
require 'mimew.pl';
require 'jcode.pl';
require 'mobileimg.cgi';
use strict;

# コンストラクタ
# 引　数：外部さーば利用　ホスト名　ポート　認証ユーザ　認証パスワード　認証方法
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
		
		# 各キャリアごとにメールの配信を変える
		if ($to =~ /docomo\.ne\.jp$/) {
		#if (1) {
			# ドコモ
			
			($mailhead, $subject, $body, $mailfoot) = $this->make_docomo($subject, $body);
			$ismobile = 1;
		} elsif ($to =~ /ezweb\.ne\.jp$/) {
			# EZWEB
			($mailhead, $subject, $body, $mailfoot) = $this->make_ezweb($subject, $body);
			$ismobile = 1;
		} elsif ($sb) {
			# ソフトバンク
			($mailhead, $subject, $body, $mailfoot) = $this->make_softbank($subject, $body);
			$ismobile = 1;
		} else {
			# それ以外のPCなどのHTMLメール
			
			#件名、本文を一度拡張SJISに変換
# 			Encode::from_to($subject, "euc-jp","cp932");
# 			Encode::from_to($body, "euc-jp","cp932");
# 			Jcode::convert(\$subject, "cp932", "euc");
# 			Jcode::convert(\$body, "cp932", "euc");
			# 件名、本文をJISに
			&jcode::convert(\$subject, "jis");
			&jcode::convert(\$body, "jis");
			
			$mailhead = 'multipart/related; boundary="nextpt01"'."\n\n\n\n";
			$mailhead .= "--nextpt01\n".'Content-Type:multipart/alternative; boundary="nextpt02"'."\n\n\n";
			$mailhead .= '--nextpt02
Content-Type: text/html; charset="iso-2022-jp"
Content-Transfer-Encoding: 7bit

';

			# 画像
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
# 		#件名、本文を一度拡張SJISに変換
# 		Encode::from_to($subject, "euc-jp","cp932");
# 		Encode::from_to($body, "euc-jp","cp932");
# 		# 件名、本文をJISに
 		&jcode::convert(\$subject, "jis");
 		&jcode::convert(\$body, "jis");
# 		
		$subject = $this->sencode($subject);
#  			Encode::from_to($subject, "euc-jp","iso-2022-jp");
#  			Encode::from_to($body, "euc-jp","iso-2022-jp");
		
	}
	
	
	#未入力エラー
	#if (!$sendmail){return 0;}
	if (!$to){return 0;}
	if (!$from){return 0;}
	
	
	# to,replyto,returnpathはメールアドレスのみ抽出
	my $to_m = &getmail($this, $to);
	$replyto = &getmail($this, $replyto);
	$returnpath = &getmail($this, $returnpath);
	
	
	
	# FROMとTOのエンコード
	#Encode::from_to($from, "euc-jp","cp932");
	&jcode::convert(\$from, "jis");
	#Encode::from_to($to, "euc-jp","cp932");
	&jcode::convert(\$to, "jis");
	
#	if (!$ismobile) {
#		#件名、本文をJISに変換
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


	#メールHEADER定義
	my $senddata = "";
	$senddata .= "Return-Path: $returnpath \n" if $returnpath;
	$senddata .= "X-Mailer: acmailer3.0 http://www.ahref.org/\n";
	$senddata .= "X-SENDTO: $to\n";
	$senddata .= "X-HID: $hid\n";
	$senddata .= "X-SCD: $writing\n";
	$senddata .= "Reply-To: $replyto\n" if $replyto;
	$senddata .= main::mimeencode("To: $to\n");
	# 送信者名にメールアドレスや特殊な文字があった場合に正常にエンコードしてくれないため
	#$senddata .= main::mimeencode("From: $from\n");
	$senddata .= "From: ".&sencode_from($this, $from)."\n";
	$senddata .= "Subject: $subject \n";
	$senddata .= "MIME-Version: 1.0\n";
	$senddata .= "Date:".&date($this)."\n";
	$senddata .= "Content-Type: $mailhead";
	#メール本文定義
	$senddata .= $body;
	
	# マルチパートの場合
	if ($mail_type eq "multi") {
		$senddata .= "

--nextpt02
";
		$senddata .= "Content-Type: text/plain; charset=\"ISO-2022-JP\"\n";
		$senddata .= "Content-Transfer-Encoding: 7bit\n\n";
		$senddata .= $body;
	}


	# フッタ
	$senddata .= $mailfoot;


	if ( $this->{relay_use} && $this->{relay_host} ) {

        # 外部サーバにより送信
        if ( ! &relay_sendmail($this, $to, $from, $returnpath, $senddata) ) {

            # 外部サーバ接続がエラーになった
        }
	}
    else {

        my @options;

        # qmail
        if ( $this->{qmail} ) {
            push @options, "-f $returnpath";
        }

        # iオプション
        if ( $this->{sendmail_i_option} ) {
            push @options, '-i';
        }

        # オプション生成
        my $option = join(' ', @options);


        # sendmailの起動
        open(MAIL,"| $sendmail $option $to") || return undef;
        print MAIL $senddata;
        close(MAIL);
	}
	return 1;
}


# DOCOMO用メール作成
# 戻り値：ヘッダ　件名　本文　フッタ
sub make_docomo() {
	my $this = shift;
	my $subject = shift;
	my $body = shift;
	
	my ($mailhead, $mailmiddle, $mailfoot);
	
	#件名、本文を一度拡張SJISに変換
	#Encode::from_to($subject, "euc-jp","cp932");
	#Encode::from_to($body, "euc-jp","cp932");
	# 件名、本文をJISに
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
	
	# DOCOMOはキャリアコードが２
	my $career = 1;
	# 絵文字挿入
	$subject = $this->insert_emoji($career, $subject);
	$body = $this->insert_emoji($career, $body);
	
	# 画像
	($body, $mailmiddle) = $this->insert_image($body);
	
	use MIME;
	$body = MIME::encode_quoted($body);
	
	# 件名をエンコード
	$subject = $this->sencode($subject);
	
	# フッタ作成
	
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

# SoftBank用
# 戻り値：ヘッダ　件名　本文　フッタ
sub make_softbank() {
	my $this = shift;
	my $subject = shift;
	my $body = shift;
	my ($mailhead, $mailmiddle, $mailfoot);
	

	# 件名、本文をUTFに変換
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
	
	# SOFTBANKはキャリアコードが２
	my $career = 3;
	# 絵文字挿入
	$subject = $this->insert_emoji($career, $subject);
	$body = $this->insert_emoji($career, $body);
	
	# 画像
	($body, $mailmiddle) = $this->insert_image($body);
	
	# 件名エンコード
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

# EZWEB用
sub make_ezweb() {
	my $this = shift;
	my $subject = shift;
	my $body = shift;
	my ($mailhead, $mailmiddle, $mailfoot);
	
	#件名、本文を一度拡張SJISに変換
#	Encode::from_to($subject, "utf8","cp932");
#	Encode::from_to($body, "utf8","cp932");
	# 件名、本文をJISに
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
	
	# EZWEBはキャリアコードが２
	my $career = 2;
	# 絵文字挿入
	$subject = &insert_emoji($this, $career, $subject);
	$body = &insert_emoji($this, $career, $body);
	
	# 画像
	($body, $mailmiddle) = &insert_image($this, $body);
	
	use MIME;
	$body = MIME::encode_quoted($body);
	
	# 件名をエンコード
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

# 絵文字挿入
sub insert_emoji($$) {
	my $this = shift;
	my $career = shift;
	my $str = shift;
	
	my $emoji = main::mobilemailimg($career);
	# 絵文字
	foreach my $n (keys %$emoji) {
		my $moji = $emoji->{$n};
		$str =~ s/{$n}/$moji/g;
	}
	return $str;
}

# 画像挿入
# 戻り値：本文　ミドルヘッダ
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
			# 画像データ作成
			open IN,"<./upload/$n" or main::error("ファイルが開けません。$n $!");
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
	# 名前とemailを分ける
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
		$mail =~ s/($mail_regex)(.*)/$1/go;		# メールアドレスの最後以降を削除
		$mail =~ s/(.*)[^\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+($mail_regex)/$2/go;		# メールアドレスまでを削除
	}
	return $mail;
}

sub relay_sendmail {
	# 送信先・件名・本文
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
			print "Net::SMTP もしくは Net::POP3のモジュールの読み込に失敗しました。外部サーバを利用することはできません。$@\n";
			return 0;
		} else {
			return 0;
		}
	}
	
	
	# SMTP 認証の場合
	if ($sendmode eq "smtp_auth") {

		my $SMTP = Net::SMTP->new($relay_host,Port=>$relay_port,Debug =>$debug);
		
		if (!$SMTP) { print "SMTPサーバへの接続へ失敗しました。"; return 0; }
		
		# デバッグ用
		if ($debug) {
			open(STDERR, ">&STDOUT");
		}
		
		# SMTP認証
		$SMTP->datasend("AUTH LOGIN\n");
		$SMTP->response();

		# ID
		$SMTP->datasend(encode_base64($relay_user) );
		$SMTP->response();

		#  PASS
		$SMTP->datasend(encode_base64($relay_pass) );
		$SMTP->response();

		# 送信元
		$SMTP->mail($rcpt);

		# 送信先
		if ($SMTP->to($to)) {
			
		} else {
			return 0;
		}

		$SMTP->data();

		# ヘッダ作成
		$SMTP->datasend($senddata);
		$SMTP->datasend("\n");
		$SMTP->dataend();
		$SMTP->quit;
		return 1;
	} elsif ($sendmode eq "popbefore") {
			# オブジェクト生成
			my $pop = Net::POP3->new("$relay_host");
			if (!$pop) { die "POPサーバ接続失敗"; }
			my $auth = $pop->login($relay_user, $relay_pass);

			# POPサーバにユーザIDとパスワードで接続
			if ($auth >= 0 && $auth ne "") {
				# 接続できれば終了
				$pop->quit;
			} else {
				# 接続エラー
				print "POP認証失敗しました。";
				return 0;
			}
	}

	my $SMTP = Net::SMTP -> new( "$relay_host",		# SMTPサーバー名を指定
					Port=>$relay_port,				# PORT指定
					Hello => "$relay_host",			# SMTPドメイン名を指定
					Timeout => 60,Debug =>$debug);					# 接続待ち許容時間（秒）
	if (!$SMTP) { print "SMTPサーバへの接続へ失敗しました。"; return 0; }
	# デバッグ用
	if ($debug) {
		open(STDERR, ">&STDOUT");
	}

	#ヘッダ部の組み立て
	$SMTP->mail($rcpt);							# 送信元メールアドレスを指定
	if (!$SMTP->to($to)) { return 0; }			# 宛先メールアドレスを指定

	#データ部の組み立て
	$SMTP -> data();
	$SMTP -> datasend($senddata);				# 送信元(データ部）
	$SMTP->datasend("\n");
	$SMTP -> dataend();							# データ終端、メール送信
	$SMTP -> quit;								# SMTP接続の終了

	
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
