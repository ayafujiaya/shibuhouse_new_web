#!/usr/bin/perl

my $myfilepath = '/home/admin2/project/acmailer3.8/';
chdir $myfilepath;
use lib "./lib/";
require 'clsMail.pm';
use POSIX;
use MIME::Base64;
use File::Copy;
#require $myfilepath.'lib/jcode.pl';
#require $myfilepath.'lib/mimew.pl';
require 'setup.cgi';

my $mode = $ARGV[0];

our $SYS;
# 絶対パスに上書き
$SYS->{data_dir} = $myfilepath."data/";

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();
my $objMail = create_clsMail($admindata);
my %FORM;
# メール内容取得
my $v = getmaildata();

$FORM{email} = $v->{email};
$FORM{body} = $v->{body};

# 自動返信メールテンプレート情報取得
my $rowform = $objAcData->GetRowData('form', 'FORM');

# 送信者のメールアドレス
my $sendername = &SetFromName($admindata->{admin_email}, $admindata->{admin_name});

# sendmailへのパス
my $sendmailpath = $admindata->{sendmail_path};

# チェックボックスの値を変更して取得
%FORM = &ChangeCheckboxValue(\%FORM);

my $ml_comment_admin= "";

my $xmailer = '';

# 登録
if ($mode eq "reg") {
	if ($admindata->{double_opt}) {
		&doubleopt();
	} else {
		&regadd();
	}
} elsif ($mode eq "del") {
	&regdel();
} elsif ($mode eq "autoform") {
	&autoform();
}

exit;

sub autoform() {
	# 登録フォームを表示
	# このモードは強制的にダブルオプトインの機能となります。
	$FORM{id} = time.$$;
	$FORM{id} = &md5sum($FORM{id});
	
	# 配信フラグの立っているデータあるかどうか
	# フォームからの登録が許可されていない場合
	if (!$admindata->{double_reg_form}) {
		if (!$objAcData->RegCheckDouble($FORM{email}, 1)) {
			&error_mail("そのアドレスは既に登録されています。");
		}
	}
	
	# 2010/11/12 再登録防止機能追加
	if ($admindata->{'regdeny'}) {
		$objAcData->checkRegDeny($FORM{'email'}, $objMail, $SYS->{max_column});
	}
	
	# データ登録
	$objAcData->AddTempData(\%FORM, $SYS->{max_colnum});
	
	my $body = $rowform->{form_autoform_mailbody};
	my $userdata;
	foreach my $n (keys %FORM) {
		$userdata->{$n} = $FORM{$n};
	}
	# 置換作業
	$body = $objAcData->ReplaceMailBody($body, $admindata, $userdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/g;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
	}
	
	# 登録者へメール
	$objMail->send($sendmailpath,$FORM{email},$rowform->{form_autoform_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error_mail("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	#}
}

sub doubleopt{
	$FORM{id} = time.$$;
	$FORM{id} = &md5sum($FORM{id});

	# 自由項目取得
	my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');
	# 項目取得
	for(my $i = 1; $i <= $SYS->{max_colnum}; $i++) {
		my $target = $freecol->{"col".$i."name"};
		my @body = split(/\r\n|\r|\n/, $FORM{body});
		foreach my $ref (@body) {
			if ($ref =~ /^$target(\:)(.*)/i) {
				$FORM{"col".$i} = $2;
			}
		}
	}
	
	my $error_data;
	# エラーチェック(必須項目チェック）
	if (!$objAcData->RegCheckExists(\%FORM, $SYS->{max_colnum}, \$error_data)) {
		$error_data =~ s/<BR>/\n/gi;
		&error_mail($error_data);
	}
	
	# 配信フラグの立っているデータあるかどうか
	# フォームからの登録が許可されていない場合
	if (!$admindata->{double_reg_form}) {
		if (!$objAcData->RegCheckDouble($FORM{email}, 1)) {
			&error_mail("そのアドレスは既に登録されています。");
		}
	}
	
	# 2010/11/12 再登録防止機能追加
	if ($admindata->{'regdeny'}) {
		$objAcData->checkRegDeny($FORM{'email'}, $objMail, $SYS->{max_column});
	}
	
	# データ登録
	$objAcData->AddTempData(\%FORM, $SYS->{max_colnum});
	
	my $body = $rowform->{form_temp_mailbody};
	my $userdata;
	foreach my $n (keys %FORM) {
		$userdata->{$n} = $FORM{$n};
	}
	# 置換作業
	$body = $objAcData->ReplaceMailBody($body, $admindata, $userdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/g;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
	}
	
	
	# 登録者へメール
	$objMail->send($sendmailpath,$FORM{email},$rowform->{form_temp_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error_mail("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	#}

}



sub regadd{
	
	# 新規登録時の日付セット
	my %TIME = &getdatetime();
	$FORM{'add_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	$FORM{'edit_date'} = $FORM{'add_date'};
	
	# 自由項目取得
	my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');
	# 項目取得
	for(my $i = 1; $i <= $SYS->{max_colnum}; $i++) {
		my $target = $freecol->{"col".$i."name"};
		my @body = split(/\r\n|\r|\n/, $FORM{body});
		foreach my $ref (@body) {
			if ($ref =~ /^$target(\:)(.*)/i) {
				$FORM{"col".$i} = $2;
			}
		}
	}
	
	my $error_data;
	# エラーチェック(必須項目チェック）
	if (!$objAcData->RegCheckExists(\%FORM, $SYS->{max_colnum}, \$error_data)) {
		$error_data =~ s/<BR>/\n/gi;
		&error_mail($error_data);
	}
	
	# 配信フラグの立っているデータあるかどうか
	#if (!$objAcData->RegCheckDouble($FORM{email}, 1)) {
	#	&error_mail("そのアドレスは既に登録されています。");
	#}
	
	# 対象のメールアドレスを取得
	my $maildata = $objAcData->GetMailData('', $FORM{'email'}) ;
	# フォームからの重複登録が許可されていない場合
	if (!$admindata->{double_reg_form}) {
		if ($maildata->{email} && $maildata->{status}) {
			&error_mail("対象のアドレスは既に登録されています。");
		}
	}
	
	# 2010/11/12 再登録防止機能追加
	if ($admindata->{'regdeny'}) {
		$objAcData->checkRegDeny($FORM{'email'}, $objMail, $SYS->{max_column});
	}
	
	# 文字コード調査
	if ($FORM{force}) {
		# 強制
		for(1..$SYS->{max_colnum}) {
			&Jcode::convert(\$FORM{"col".$_}, "euc", $FORM{force});
		}
	} else {
		if ($FORM{encode}) {
			my $enc = getcode($FORM{encode});
			if ($enc ne "euc") {
				for(1..$SYS->{max_colnum}) {
					&Jcode::convert(\$FORM{"col".$_}, "euc", $enc);
				}
			}
		}
	}
	
	# データ登録
	if ($admindata->{double_reg_form}) {
		# 新規登録
		$objAcData->RegEmail(\%FORM);
	} elsif ($maildata->{email}) {
		# 登録データを全て上書きする 10/03/24
		$FORM{id} = $maildata->{id};
		$FORM{status} = 1;
		$objAcData->UpdData('mail', 'MAIL', $maildata->{id}, \%FORM);
		
		# 配信フラグ更新
		#$FORM{"send_flg".$maildata->{id}} = 1;
		#$FORM{"hid_email".$maildata->{id}} = 1;
		#$objAcData->UpdMailStatus(\%FORM);
	} else {
		# 新規登録
		$objAcData->RegEmail(\%FORM);
	}
	
	# 再登録防止リストからクリア
	$objAcData->CleanRegDenyByEmail($FORM{email});
	
	my $userdata;
	foreach my $n (keys %FORM) {
		$userdata->{$n} = $FORM{$n};
	}
	my $body = $rowform->{form_mailbody};
	# 置換作業
	$body = $objAcData->ReplaceMailBody($body, $admindata, $userdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;

	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# 登録者へメール
		$objMail->send($sendmailpath,$FORM{email},$rowform->{form_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error_mail("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	if ($admindata->{merumaga_adminmail}) {
		# 管理人へメール
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_mailtitle}.$FORM{email},$body.$ml_comment_admin,$sendername,$sendername,$xmailer,$sendername, $rowform->{send_type}) || &error_mail("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	
}


sub getmaildata {
	my %TIME = &getdatetime();
	my $message;
	my $boundary;
	my $email;
	# 一度メールを読み込み保存する
	while (<STDIN>) {
		$message .=  $_;
	}
	
	&jcode::convert(\$message,"euc");
	# ヘッダーと本文に分解&配列化
	my $mail_head = $message;
	$mail_head =~ s/\n\n(.*)//s;
	my $mail_body = $1;
	my @mail_head = split(/\n/,$mail_head);
	my @mail_body = split(/\n/,$mail_body);
	my $kind;
	
	my ($email_f, $subject_f, $body_f);
	foreach (@mail_head) {
		if (/^(.*): (.*)$/i) {
			$kind = $1;
		}
		# 送信元メールアドレス
		if ($kind =~ /from/i) {
			$email .= $_;
			$mail_f = 1;
		}

		# 件名取得
		if (/Subject:(.*)/i) {
			$kind = "subject";
			$subject = $1;
			$subject_f = 1;
		}
		
		
		# boundary取得
		if(/(.*)boundary\=\"(.*)\"/ && $email_f && $subject_f && $body_f) {
			$kind = "boundary";
			$boundary = $2;
		}
		
		
	}

	# DOCOMOとAU対策 "asdf..asdf."@docomo.ne.jpみたいなアドレスできた場合"を外す
	if ($email =~ /[^\"]*(\")([^\"]*)\"(\@.*)$/) {
		$email = $2.$3;
	}

	# メールアドレス取得
	$email = lc(&getmailaddr($email));

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
	# 件名Bエンコードをデコード
	my $lws = '(?:(?:\x0D\x0A|\x0D|\x0A)?[ \t])+';
	my $ew_regex = '=\?ISO-2022-JP\?B\?([A-Za-z0-9+/]+=*)\?=';
	$subject =~ s/($ew_regex)$lws(?=$ew_regex)/$1/gio;
	$subject =~ s/$lws/ /go;
	$subject =~ s/$ew_regex/decode_base64($1)/egio;
	&jcode::convert(\$subject, 'euc', 'jis');
	
	my $v;
	
	
	$v->{email} = $email;
	$v->{subject} = $subject;
	$v->{body} = $bodydata;
	
	return $v;
	
}

sub regdel{
	
	# メールデータ一式取得
	my @DELMAIL = $objAcData->GetData('mail', 'MAIL');
	my $exist = 0;
	my $data;
	foreach my $ref (@DELMAIL) {
		if ($FORM{email} eq $ref->{email}) {
			$data = $ref;	# 対象データ取得
			if ($ref->{status}) { $exist = 1; }
			if ($admindata->{delmode} eq "del") {
				# 物理削除
				$objAcData->DelData('mail', 'MAIL', $ref->{id});
			} else {
				# 配信ステータス変更
				my $CHANGE;
				$CHANGE->{$ref->{id}} = 1;
				$FORM{"send_flg".$ref->{id}} = 0;
				$FORM{"hid_email".$ref->{id}} = 1;
				$objAcData->UpdMailStatus(\%FORM);
			}

			# 2010/11/12 仕様追加　再登録防止機能
			# 再登録防止機能を使う場合はリスト登録する
			if ($admindata->{'regdeny'}) {
				my $deny;
				my %TIME = &getdatetime();
				$deny->{'email'} = $ref->{'email'};
				$deny->{'id'} = time.$$;
				$deny->{'del_date'} = $TIME{'year'}.$TIME{'mon'}.$TIME{'mday'}.$TIME{'hour'}.$TIME{'min'}.$TIME{'sec'};
				# 再登録防止期限を取得
				if ($admindata->{'regdeny_timelimit'}) {
					# 再登録可能日付取得
					my @allowDate = &calcuDateTime($TIME{'year'}, $TIME{'mon'}, $TIME{'mday'}, $TIME{'hour'}, $TIME{'min'}, $TIME{'sec'}, $admindata->{'regdeny_timelimit'} * 3600);
					$deny->{'limit_date'} = sprintf("%04d%02d%02d%02d%02d%02d", $allowDate[0], $allowDate[1], $allowDate[2], $allowDate[3], $allowDate[4], $allowDate[5]);
				}
				
				# 同じメールアドレスが登録されていれば上書き
				my @regdeny = $objAcData->GetData("regdeny", "REGDENY");
				my $deny_exist = 0;
				foreach my $rowregdeny (@regdeny) {
					if ($rowregdeny->{'email'} eq $deny->{'email'}) {
						$objAcData->UpdData("regdeny", "REGDENY", $rowregdeny->{'id'}, $deny);
						$deny_exist = 1;
						last;			
					}
				}
				if (!$deny_exist) {
					$objAcData->InsData('regdeny', 'REGDENY', $deny);
				}
			}
		}
	}
	
	if(!$exist){
		&error_mail("そのメールアドレスは登録されていません。");
	}
	
	my $body = $rowform->{form2_mailbody};
	my $userdata = $data;
	
	# 置換作業
	$body = $objAcData->ReplaceMailBody($body, $admindata, $userdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$ml_comment_admin =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# 登録者へメール
		$objMail->send($sendmailpath,$FORM{email},$rowform->{form2_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error_mail("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	if ($admindata->{merumaga_adminmail}) {
		# 管理人へメール
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form2_mailtitle}.$FORM{email},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error_mail("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	
}


sub error_mail {
	my $str = shift;
	
	if (!$FORM{email}) { $FORM{email} = $admindata->{admin_email}; }
	$objMail->send($sendmailpath,$FORM{email},'エラー',$str,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email});
	exit;
}
sub getmailaddr{
	my $mail = shift;
	# メールアドレス正規表現
	$mail_regex = q{([\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)\@([\w|\!\#\$\%\'\(\)\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)};
	if($mail =~ /$mail_regex/o){
		$mail =~ s/($mail_regex)(.*)/$1/go;		# メールアドレスの最後以降を削除
		$mail =~ s/(.*)[^\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+($mail_regex)/$2/go;		# メールアドレスまでを削除
	}
	return $mail;
}

sub md5sum{
	use integer;
	my ($l,$m,@n,$a,$b,$c,$d,@e,$r);
	# Initial values set
	$a=0x67452301;$b=0xefcdab89;$c=0x98badcfe;$d=0x10325476;
	$m=$_[0];
	# Padding
	$l=length $m;
	$m.="\x80"."\x00"x(($l%64<56?55:119)-$l%64);
	$m.=pack "VV",($l<<3)&0xffffffff,$l<<35;
	# Round
	for(0..($l+8)/64){
	@n=unpack 'V16',substr($m,$_<<6,64);
	@e[0..3]=($a,$b,$c,$d);
	$r=($a+$n[0]+0xd76aa478+($b&$c|(~$b&$d)));$a=$b+(($r<<7)|(($r>>25)&0x7f));
	$r=($d+$n[1]+0xe8c7b756+($a&$b|(~$a&$c)));$d=$a+(($r<<12)|(($r>>20)&0xfff));
	$r=($c+$n[2]+0x242070db+($d&$a|(~$d&$b)));$c=$d+(($r<<17)|(($r>>15)&0x1ffff));
	$r=($b+$n[3]+0xc1bdceee+($c&$d|(~$c&$a)));$b=$c+(($r<<22)|(($r>>10)&0x3fffff));
	$r=($a+$n[4]+0xf57c0faf+($b&$c|(~$b&$d)));$a=$b+(($r<<7)|(($r>>25)&0x7f));
	$r=($d+$n[5]+0x4787c62a+($a&$b|(~$a&$c)));$d=$a+(($r<<12)|(($r>>20)&0xfff));
	$r=($c+$n[6]+0xa8304613+($d&$a|(~$d&$b)));$c=$d+(($r<<17)|(($r>>15)&0x1ffff));
	$r=($b+$n[7]+0xfd469501+($c&$d|(~$c&$a)));$b=$c+(($r<<22)|(($r>>10)&0x3fffff));
	$r=($a+$n[8]+0x698098d8+($b&$c|(~$b&$d)));$a=$b+(($r<<7)|(($r>>25)&0x7f));
	$r=($d+$n[9]+0x8b44f7af+($a&$b|(~$a&$c)));$d=$a+(($r<<12)|(($r>>20)&0xfff));
	$r=($c+$n[10]+0xffff5bb1+($d&$a|(~$d&$b)));$c=$d+(($r<<17)|(($r>>15)&0x1ffff));
	$r=($b+$n[11]+0x895cd7be+($c&$d|(~$c&$a)));$b=$c+(($r<<22)|(($r>>10)&0x3fffff));
	$r=($a+$n[12]+0x6b901122+($b&$c|(~$b&$d)));$a=$b+(($r<<7)|(($r>>25)&0x7f));
	$r=($d+$n[13]+0xfd987193+($a&$b|(~$a&$c)));$d=$a+(($r<<12)|(($r>>20)&0xfff));
	$r=($c+$n[14]+0xa679438e+($d&$a|(~$d&$b)));$c=$d+(($r<<17)|(($r>>15)&0x1ffff));
	$r=($b+$n[15]+0x49b40821+($c&$d|(~$c&$a)));$b=$c+(($r<<22)|(($r>>10)&0x3fffff));
	$r=($a+$n[1]+0xf61e2562+($b&$d|(~$d&$c)));$a=$b+(($r<<5)|(($r>>27)&0x1f));
	$r=($d+$n[6]+0xc040b340+($a&$c|(~$c&$b)));$d=$a+(($r<<9)|(($r>>23)&0x1ff));
	$r=($c+$n[11]+0x265e5a51+($d&$b|(~$b&$a)));$c=$d+(($r<<14)|(($r>>18)&0x3fff));
	$r=($b+$n[0]+0xe9b6c7aa+($c&$a|(~$a&$d)));$b=$c+(($r<<20)|(($r>>12)&0xfffff));
	$r=($a+$n[5]+0xd62f105d+($b&$d|(~$d&$c)));$a=$b+(($r<<5)|(($r>>27)&0x1f));
	$r=($d+$n[10]+0x02441453+($a&$c|(~$c&$b)));$d=$a+(($r<<9)|(($r>>23)&0x1ff));
	$r=($c+$n[15]+0xd8a1e681+($d&$b|(~$b&$a)));$c=$d+(($r<<14)|(($r>>18)&0x3fff));
	$r=($b+$n[4]+0xe7d3fbc8+($c&$a|(~$a&$d)));$b=$c+(($r<<20)|(($r>>12)&0xfffff));
	$r=($a+$n[9]+0x21e1cde6+($b&$d|(~$d&$c)));$a=$b+(($r<<5)|(($r>>27)&0x1f));
	$r=($d+$n[14]+0xc33707d6+($a&$c|(~$c&$b)));$d=$a+(($r<<9)|(($r>>23)&0x1ff));
	$r=($c+$n[3]+0xf4d50d87+($d&$b|(~$b&$a)));$c=$d+(($r<<14)|(($r>>18)&0x3fff));
	$r=($b+$n[8]+0x455a14ed+($c&$a|(~$a&$d)));$b=$c+(($r<<20)|(($r>>12)&0xfffff));
	$r=($a+$n[13]+0xa9e3e905+($b&$d|(~$d&$c)));$a=$b+(($r<<5)|(($r>>27)&0x1f));
	$r=($d+$n[2]+0xfcefa3f8+($a&$c|(~$c&$b)));$d=$a+(($r<<9)|(($r>>23)&0x1ff));
	$r=($c+$n[7]+0x676f02d9+($d&$b|(~$b&$a)));$c=$d+(($r<<14)|(($r>>18)&0x3fff));
	$r=($b+$n[12]+0x8d2a4c8a+($c&$a|(~$a&$d)));$b=$c+(($r<<20)|(($r>>12)&0xfffff));
	$r=($a+$n[5]+0xfffa3942+($b^$c^$d));$a=$b+(($r<<4)|(($r>>28)&0xf));
	$r=($d+$n[8]+0x8771f681+($a^$b^$c));$d=$a+(($r<<11)|(($r>>21)&0x7ff));
	$r=($c+$n[11]+0x6d9d6122+($d^$a^$b));$c=$d+(($r<<16)|(($r>>16)&0xffff));
	$r=($b+$n[14]+0xfde5380c+($c^$d^$a));$b=$c+(($r<<23)|(($r>>9)&0x7fffff));
	$r=($a+$n[1]+0xa4beea44+($b^$c^$d));$a=$b+(($r<<4)|(($r>>28)&0xf));
	$r=($d+$n[4]+0x4bdecfa9+($a^$b^$c));$d=$a+(($r<<11)|(($r>>21)&0x7ff));
	$r=($c+$n[7]+0xf6bb4b60+($d^$a^$b));$c=$d+(($r<<16)|(($r>>16)&0xffff));
	$r=($b+$n[10]+0xbebfbc70+($c^$d^$a));$b=$c+(($r<<23)|(($r>>9)&0x7fffff));
	$r=($a+$n[13]+0x289b7ec6+($b^$c^$d));$a=$b+(($r<<4)|(($r>>28)&0xf));
	$r=($d+$n[0]+0xeaa127fa+($a^$b^$c));$d=$a+(($r<<11)|(($r>>21)&0x7ff));
	$r=($c+$n[3]+0xd4ef3085+($d^$a^$b));$c=$d+(($r<<16)|(($r>>16)&0xffff));
	$r=($b+$n[6]+0x04881d05+($c^$d^$a));$b=$c+(($r<<23)|(($r>>9)&0x7fffff));
	$r=($a+$n[9]+0xd9d4d039+($b^$c^$d));$a=$b+(($r<<4)|(($r>>28)&0xf));
	$r=($d+$n[12]+0xe6db99e5+($a^$b^$c));$d=$a+(($r<<11)|(($r>>21)&0x7ff));
	$r=($c+$n[15]+0x1fa27cf8+($d^$a^$b));$c=$d+(($r<<16)|(($r>>16)&0xffff));
	$r=($b+$n[2]+0xc4ac5665+($c^$d^$a));$b=$c+(($r<<23)|(($r>>9)&0x7fffff));
	$r=($a+$n[0]+0xf4292244+($c^($b|~$d)));$a=$b+(($r<<6)|(($r>>26)&0x3f));
	$r=($d+$n[7]+0x432aff97+($b^($a|~$c)));$d=$a+(($r<<10)|(($r>>22)&0x3ff));
	$r=($c+$n[14]+0xab9423a7+($a^($d|~$b)));$c=$d+(($r<<15)|(($r>>17)&0x7fff));
	$r=($b+$n[5]+0xfc93a039+($d^($c|~$a)));$b=$c+(($r<<21)|(($r>>11)&0x1fffff));
	$r=($a+$n[12]+0x655b59c3+($c^($b|~$d)));$a=$b+(($r<<6)|(($r>>26)&0x3f));
	$r=($d+$n[3]+0x8f0ccc92+($b^($a|~$c)));$d=$a+(($r<<10)|(($r>>22)&0x3ff));
	$r=($c+$n[10]+0xffeff47d+($a^($d|~$b)));$c=$d+(($r<<15)|(($r>>17)&0x7fff));
	$r=($b+$n[1]+0x85845dd1+($d^($c|~$a)));$b=$c+(($r<<21)|(($r>>11)&0x1fffff));
	$r=($a+$n[8]+0x6fa87e4f+($c^($b|~$d)));$a=$b+(($r<<6)|(($r>>26)&0x3f));
	$r=($d+$n[15]+0xfe2ce6e0+($b^($a|~$c)));$d=$a+(($r<<10)|(($r>>22)&0x3ff));
	$r=($c+$n[6]+0xa3014314+($a^($d|~$b)));$c=$d+(($r<<15)|(($r>>17)&0x7fff));
	$r=($b+$n[13]+0x4e0811a1+($d^($c|~$a)));$b=$c+(($r<<21)|(($r>>11)&0x1fffff));
	$r=($a+$n[4]+0xf7537e82+($c^($b|~$d)));$a=$b+(($r<<6)|(($r>>26)&0x3f));
	$r=($d+$n[11]+0xbd3af235+($b^($a|~$c)));$d=$a+(($r<<10)|(($r>>22)&0x3ff));
	$r=($c+$n[2]+0x2ad7d2bb+($a^($d|~$b)));$c=$d+(($r<<15)|(($r>>17)&0x7fff));
	$r=($b+$n[9]+0xeb86d391+($d^($c|~$a)));$b=$c+(($r<<21)|(($r>>11)&0x1fffff));
	$a=($a+$e[0])&0xffffffff;
	$b=($b+$e[1])&0xffffffff;
	$c=($c+$e[2])&0xffffffff;
	$d=($d+$e[3])&0xffffffff;}
	unpack('H*',(pack 'V4',$a,$b,$c,$d));
}
1;
