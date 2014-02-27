#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# 変更しました。

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# セッションデータ取得とログインチェック
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;
my $tmpl_file = 'mail';

if ($FORM{display}) {
	$tmpl_file = $FORM{display};
} else {
	$FORM{display} = 'mail';
}

if ($FORM{'edit'}) {
	
	my %REGDATA;
	foreach my $n (keys %$admindata) {
		$REGDATA{$n} = $admindata->{$n};
	}
	foreach my $n (keys %FORM) {
		$REGDATA{$n} = $FORM{$n};
	}
	# ライセンス取得
	my $li = &getlicense;
	foreach my $n (keys %$li) {
		$REGDATA{$n} = $li->{$n};
	}
	
	# 各設定のチェックボックスとラジオボタン処理
	if ($FORM{display} eq "mail") {
		foreach my $n (qw()) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "default") {
		foreach my $n (qw(relay_use send_type qmail relay_send_mode fail_send_local sendmail_i_option)) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "autoreg") {
		
	} elsif ($FORM{display} eq "reserve") {
		foreach my $n (qw(reserve)) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "errmail") {
		foreach my $n (qw(errmail)) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "system") {
		foreach my $n (qw(backnumber_disp merumaga_usermail merumaga_adminmail double_reg double_reg_form double_opt delmode counter_disp rireki_email str_check delconfirm regdeny regdeny_timelimit)) {
			$REGDATA{$n} = $FORM{$n};
		}
		
	} elsif ($FORM{display} eq "license") {
		foreach my $n (qw(writing_hide license1 license2 license3 license4)) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "topmemo") {
		
	} elsif ($FORM{display} eq "mobile") {
		
	}
	
	# エラーチェック
	if (&error_check(\%REGDATA, \$data_ref->{error_message})) {
		if ($FORM{"display"} eq "autoform") {
			# 自動フォーム設定
			# 改行を置換
			for(1..$SYS->{max_colnum}) {
				$FORM{"col".$_."text"} =~ s/\r\n|\r|\n/__<<BR>>__/g;
			}
			$objAcData->ResetData("autoform", "AUTOFORM", \%FORM);
		} else {
			# 管理者データ更新
			$objAcData->UpdAdminData(\%REGDATA);
		}
		
		if ($FORM{display} eq "free") {
			# 自由項目更新
			$objAcData->UpdFreeColData(\%REGDATA);
		}
		
		# システム設定の場合
		if ($FORM{display} eq "system") {
			$S{login_id} = $FORM{login_id};
			$S{login_pass} = $FORM{login_pass};
			# セッション保存
			&setsession($COOKIE{sid},%S);
		}
		
		# 管理者データを再取得
		$admindata = $objAcData->GetAdminData();
		$data_ref = $admindata;
		$data_ref->{okedit} = 1;
	} else {
		foreach my $n (keys %REGDATA) {
			$data_ref->{$n} = $REGDATA{$n};
		}
	}
} else {
	# 管理者データを取得
	$data_ref = $admindata;
}
$data_ref->{login_pass_org} = $data_ref->{login_pass};

# システム情報取得
my $command = 'ls /etc -F | grep "release$\|version$"';
$data_ref->{os_type} = `$command`;
my $command = ' cat /etc/`ls /etc -F | grep "release$\|version$"`';
$data_ref->{os_version} = `$command`;
$data_ref->{perl_version} = $];
$data_ref->{jcode_version} = $Jcode::VERSION;

$data_ref->{os_type} =~ s/\r\n|\r|\n//g;
$data_ref->{os_version} =~ s/\r\n|\r|\n//g;
$data_ref->{perl_version} =~ s/\r\n|\r|\n//g;
$data_ref->{jcode_version} =~ s/\r\n|\r|\n//g;

# システム情報ダウンロード
if ($FORM{mode} eq "sysdown") {
	&sysdown($data_ref);
}

# 送信タイプラジオボタン
if (!$data_ref->{send_type}) { $data_ref->{send_type} = 0; }

# sendmailパスが合っているかどうか
if(-x $data_ref->{sendmail_path}){
	$data_ref->{sendmail_path_check} = "サーバー上のパスと一致しました。";
}else{
	$data_ref->{sendmail_path_check} = "サーバー上のパスと一致しません。";
}

# 空メールモジュールが組み込まれている場合
if (-e "./lib/autoreg.pl") {
	$data_ref->{autoreg} = "1";
	if (!$data_ref->{mypath}) {
		# pwdコマンドで取得
		my $path = `pwd`;
		$data_ref->{mypath} = $path;
	} else {
		$data_ref->{mypath_ok} = 1;
	}
}


my $license = $objAcData->GetLicense();
foreach my $n (qw(license1 license2 license3 license4)) {
	$data_ref->{$n} = $license->{$n};
}
$data_ref->{license_kind} = $SYS->{license_kind};

# 自由項目
my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{freecol_list} = \@freecol;

# チェックボックスのものはあらかじめ文字列を作成
foreach my $n (@freecol) {
	if ($n->{coltype} eq "checkbox") {
		$data_ref->{checkbox_list} .= ",col".$n->{num};
	}
}

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# フォームの値
$data_ref->{form} = \%FORM;

# HTML表示
&printhtml_tk($data_ref, 'tmpl/admin_'.$tmpl_file.'_edit.tmpl');
exit;

# エラーチェック
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my %FORM = %$p_FORM;
	my @error;
	
	#エラーチェック
	if (!$FORM{admin_name}) {
		push(@error, "差出人名を入力してください。");
	#} elsif ($FORM{admin_name} =~ /[\"\'\@\;\:\,\.\<\>\\\[\]]/) {
	} elsif ($FORM{admin_name} =~ /[\"\'\<\>]/) {
		# 使用できない文字は "'<>に変更
		push(@error, "差出人名の中に「'」「\"」「<」「>」は使用できません。");
	}
	if (!$FORM{login_id}) {
		push(@error, "IDを入力してください。");
	} elsif($FORM{login_id} && ($FORM{login_id} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_id}) > 12)){
		push(@error, "IDは半角英数字で12桁以内でご指定下さい。");
	}
	
	if (!$FORM{login_pass}) {
		push(@error, "パスワードを入力してください。");
	}
	
	if ($FORM{display} eq "system" && $FORM{login_pass_org} ne $FORM{login_pass}) {
		if (!$FORM{login_pass2}) {
			push(@error, "パスワード（確認用）を入力してください。");
		}
	}
	
	if($FORM{login_pass} && ($FORM{login_pass} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_pass}) > 12)){
		push(@error, "パスワードは半角英数字で12桁以内でご指定下さい。");
	}
	if($FORM{login_pass2} && ($FORM{login_pass2} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_pass2}) > 12)){
		push(@error, "パスワード（確認用）は半角英数字で12桁以内でご指定下さい。");
	}
	
	if($FORM{login_pass_org} ne $FORM{login_pass}){
	
		if($FORM{login_pass} ne $FORM{login_pass2}){
			push(@error, "パスワードが一致しません。");
		}
	}
	
	if (!$FORM{admin_email}) {
		push(@error, "e-mailアドレスを入力してください。");
	} elsif (!&CheckMailAddress($FORM{admin_email})) {
		push(@error, "e-mailアドレスを正しく入力してください。");
	}
	
	if($FORM{divnum} && ($FORM{divnum} !~ /^[0-9]+$/ || $FORM{divnum} < 10)){
		push(@error, "分割送信件数を10以上の半角数値で設定してください。");
	}
	if($FORM{divwait} && ($FORM{divwait} !~ /^[0-9]+$/)){
		push(@error, "分割待ち時間を半角数値で設定してください。");
	}
	if($FORM{send_type} == 1 && (!$FORM{divnum} || $FORM{divnum} < 10)){
		push(@error, "送信モードが分割送信の場合、分割送信件数を10以上の半角数値で設定してください。");
	}

	if($FORM{send_type} == 1 && (!$FORM{divwait})){
		push(@error, "送信モードが分割送信の場合、分割待ち時間を半角数値で設定してください。");
	}
	if ($FORM{homeurl} && $FORM{homeurl} !~ /^https{0,1}\:\/\/.*/) {
		push(@error, "CGI設置URLはhttps://www.abc.com/acmailer/のような形式で入力してください。");
	} elsif ($FORM{homeurl} !~ /^.*\/$/) {
		$$p_FORM{homeurl} .= "/";
	}
	if ($FORM{mypath} && $FORM{mypath} !~ /\/$/) {
		$$p_FORM{mypath} .= "/";
	}
	if ($FORM{errmail_email}) {
		if (!&CheckMailAddress($FORM{errmail_email})) {
			push(@error, "不着メール管理用メールアドレスを正しく入力してください。");
		}
	}
	
	if ($FORM{send_stop} && $FORM{send_stop} =~ /[^0-9]/) {
		push(@error, "自動停止を行う不着回数は数値項目です。");
	}
	if ($FORM{errmail_log_num} && $FORM{errmail_log_num} =~ /[^0-9]/) {
		push(@error, "不着処理ログ保存件数は数値項目です。");
	}
	
	if ($FORM{double_reg_form} && !$FORM{double_reg}) {
		push(@error, "フォームからの重複データを許可する場合は管理画面からの重複データの登録も許可してください。");
	}
	
	# SMTPサーバを利用する場合
	if ($FORM{'relay_use'}) {
		
		# ホスト名は必須
		if (!$FORM{'relay_host'}) {
			push(@error, "外部のSMTPサーバを利用する場合はホスト名を入力してください。");
		}
		# ポートも必須
		if (!$FORM{'relay_port'}) {
			push(@error, "外部のSMTPサーバを利用する場合はポート番号を設定してください。");
		}
		if ($FORM{'relay_port'} =~ /[^0-9]/) {
			push(@error, "ポート番号に不正な文字が入力されています。");
		}
	}
	
	# 再登録防止機能を利用する場合
	if ($FORM{'regdeny'}) {
		if ($FORM{'regdeny_timelimit'} eq "") {
			push(@error, "再登録拒否機能を利用する場合は、拒否時間を入力してください。");
		}
	}
	if ($FORM{'regdeny_timelimit'} && $FORM{'regdeny_timelimit'} !~ /[0-9\.]/) {
			push(@error, "再登録拒否時間は数値項目です。");
	}
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;
	
}

# データ登録
sub sysdown() {
	my $data = shift;
	my $text = "ostype:".$data->{os_type}."\n";
	$text .= "osversion:".$data->{os_version}."\n";
	$text .= "acversion:".$SYS->{version}."\n";
	$text .= "perl:".$data->{perl_version}."\n";
	$text .= "Jcode:".$data->{jcode_version}."\n";
	
	my $size = length $text;
	print "Content-Type: application/octet-stream\n"; 
	print "Content-Disposition: attachment; filename=sysinfo.txt\n"; 
	print "Content-Length: $size\n\n"; 
	
	print $text;
	exit;
	
}
