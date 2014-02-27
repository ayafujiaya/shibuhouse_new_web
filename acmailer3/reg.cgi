#!/usr/bin/perl

use lib "./lib/";
require "setup.cgi";
require 'jcode.pl';
require 'mimew.pl';
use clsMail;
use strict;
our $SYS;

my %FORM = &form("noexchange", "noencode");

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();
my $objMail = create_clsMail($admindata);

# 自動返信メールテンプレート情報取得
my $rowform = $objAcData->GetRowData('form', 'FORM');

# 送信者のメールアドレス
my $sendername = &SetFromName($admindata->{admin_email}, $admindata->{admin_name});

# sendmailへのパス
my $sendmailpath = $admindata->{sendmail_path};

# 不正サイトからの登録禁止
# メールアドレス登録フォームを設置しているURLを書きます。（例：$limit = "http://www.ahref.org/cgi/acmailer/";）
my $limit = '';
&limit_access($limit) || &error("不正なアクセスです。") if $limit;

($FORM{email} = lc($FORM{email})) =~ s/\r\n|\r|\n//g;

# メールアドレス正規表現チェック
if ($FORM{reg} eq "edit") {
	if (!&CheckMailAddress($FORM{newemail})) {
		# 変更後メールアドレス
		&error("変更後メールアドレスを正しく入力してください。");
	} elsif (!&CheckMailAddress($FORM{oldemail})) {
		# 変更前メールアドレス
		&error("変更前メールアドレスを正しく入力してください。");
	}
} else {
	if($FORM{mode} ne "autoreg" && !&CheckMailAddress($FORM{email}) && $FORM{mode} ne "autoedit"){
		&error("恐れ入ります。<br>メールアドレスを正しく記入してください。");
	}
}

# データーファイルの読み込み
my @NEWDATA_ORG = $objAcData->GetData('mail', 'MAIL');
my @NEWDATA_ORG_BUF = $objAcData->GetTempMailLoopData();

# 管理人へのメールにつける投稿者情報
my %TIME = &getdatetime();
my $ml_comment_admin=
"
----------------------------------------
DATE              : $TIME{nowdate}
SERVER_NAME       : $ENV{'SERVER_NAME'}
HTTP_USER_AGENT   : $ENV{'HTTP_USER_AGENT'}
REMOTE_HOST       : $ENV{'REMOTE_HOST'}
REMOTE_ADDR       : $ENV{'REMOTE_ADDR'}
----------------------------------------
";


# 改行取り除き
foreach my $n (keys %FORM) {
    if ($n =~ /^col.*/) {
        $FORM{$n} =~ s/\r\n|\r|\n//g;
    }
}


# チェックボックスの値を変更して取得
%FORM = &ChangeCheckboxValue(\%FORM);


# 文字コード調査
my $enc;
if ( $FORM{force} ) {
    $enc = $FORM{force};
}
else {
    if ( $FORM{encode} ) {
        my $code = getcode($FORM{encode});
        if ( $code ne "euc" && $code ne "ascii") {
            $enc = $code;
        }
    }
}


# 文字コード変換
if ( $enc ) {
    foreach my $n (keys %FORM) {
        next if ref $FORM{$n};
        &Jcode::convert(\$FORM{$n}, "euc", $enc);
    }
}



my $xmailer = '';

# ////////////////////////////////////////////////////////////////////////// #
# メイン処理

# 新規登録、削除、
if (defined $FORM{reg}){
	if ($admindata->{double_opt} && $FORM{reg} eq "add") {
		&doubleopt();
	} elsif ($admindata->{double_opt} && $FORM{reg} eq "edit") {
		&doubleopt_edit();
	} elsif ($admindata->{reg} eq "edit") {
		&edit();
	} else {
		&regdel if ($FORM{reg} eq "del");
		&regadd if $FORM{reg} eq "add";
		&regedit if $FORM{reg} eq "edit";
	}
} elsif ($FORM{mode} eq "autoreg") {
	&regdoubleopt;
} elsif ($FORM{mode} eq "autoedit") {
	&editdoubleopt;
} elsif ($FORM{mode} eq "autoform") {
	&regautoform();
}

&error("不正なアクセスです。");

exit;
# ////////////////////////////////////////////////////////////////////////// #

sub doubleopt{
	$FORM{id} = time.$$;
	$FORM{id} = &md5sum($FORM{id});

	my $error_data;
	# エラーチェック(必須項目チェック）
	if (!$objAcData->RegCheckExists(\%FORM, $SYS->{max_colnum}, \$error_data)) {
		&error($error_data);
	}
	
	# 配信フラグの立っているデータあるかどうか
	# フォームからの登録が許可されていない場合
	if (!$admindata->{double_reg_form}) {
		if (!$objAcData->RegCheckDouble($FORM{email}, 1)) {
			&error("そのアドレスは既に登録されています。");
		}
	}
	
	# 2010/11/12 再登録防止機能追加
	if ($admindata->{'regdeny'}) {
		$objAcData->checkRegDeny($FORM{'email'});
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
	$objMail->send($sendmailpath,$FORM{email},$rowform->{form_temp_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	#}
	
	
	my $param;
	
	# 共通変数読み込み
	&set_common_value(\$param, $admindata);
	if (&isMobile()) {
		# 携帯端末の場合
		&printhtml_tk($param, "tmpl/m_reg_temp_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC版
		&printhtml_tk($param, "tmpl/reg_temp_finish.tmpl");
	}
	exit;

}


# 編集版ダブルオプト
sub doubleopt_edit{
	$FORM{id} = time.$$;
	$FORM{id} = &md5sum($FORM{id});
	
	# 変更前データ取得
	my $beforedata = $objAcData->GetMailData("", $FORM{oldemail});
	# 変更後データ取得
	my $afterdata = $objAcData->GetMailData("", $FORM{newemail});
	
	if ($FORM{newemail} eq $FORM{oldemail}) { &error("変更前と変更後とでメールアドレスが同一です。"); }
	# フォームからの重複登録が許可されていない場合
	if (!$admindata->{double_reg_form}) {
		if ($afterdata->{id} && $afterdata->{status}) { &error("変更後メールアドレスは既に登録されています。"); }
	}
	if (!$beforedata->{id} || ($beforedata->{id} && !$beforedata->{status})) { &error("変更前メールアドレスが見つかりません。"); }
	
	# 仮変更データ登録
	$objAcData->AddTempChangeData(\%FORM, $SYS->{max_colnum});
	
	my $body = $rowform->{form_temp_change_mailbody};
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
	$objMail->send($sendmailpath,$FORM{newemail},$rowform->{form_temp_change_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	
	my $param;
	
	# 共通変数読み込み
	&set_common_value(\$param, $admindata);
	
	if (isMobile()) {
		# 携帯版
		&printhtml_tk($param, "tmpl/m_edit_temp_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC版
		&printhtml_tk($param, "tmpl/edit_temp_finish.tmpl");
	}
	exit;
}

# 編集確定用
sub editdoubleopt{
	
	# エラーチェック
	if (!$FORM{id}) { &error("パラメータエラーです。"); }
	
	# 新規登録時の日付セット
	my %TIME = &getdatetime();
	$FORM{'edit_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	
	# 対象データ取得
	my $bufdata = $objAcData->GetData('change', 'TEMPCHANGE', $FORM{id});
	
	if (!$bufdata->{id} || !$bufdata->{newemail}) { &error("対象のデータ取得に失敗しました。<br>既に処理が確定されているか、仮手続きがおこなわれていません。"); }
	
	
	# 変更前データ取得
	my $beforedata = $objAcData->GetMailData("", $bufdata->{oldemail});
	# 変更後データ取得
	my $afterdata = $objAcData->GetMailData("", $bufdata->{newemail});
	
	if (!$beforedata->{email} || ($beforedata->{email} && !$beforedata->{status})) { &error("変更前メールアドレスが見つかりません。"); }
	# フォームからの重複登録が許可されている場合
	if (!$admindata->{double_reg_form}) {
		if ($afterdata->{email} && $afterdata->{status}) { &error("変更後メールアドレスが既に存在します。"); }
	}
	
	# 同じE-mailの仮登録データ削除
	$objAcData->DelSameMailTempChangeData($bufdata->{oldemail});
	
	# メールアドレス変更
	$objAcData->RegChangeEmail($bufdata->{oldemail}, $bufdata->{newemail});
	
	# 新旧のメールアドレスを挿入
	$beforedata->{oldemail} = $bufdata->{oldemail};
	$beforedata->{newemail} = $bufdata->{newemail};
	
	my $body = $rowform->{form_change_mailbody};
	# 置換作業
	$body = $objAcData->ReplaceMailBody($body, $admindata, $beforedata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# 登録者へメール
		$objMail->send($sendmailpath,$bufdata->{newemail},$rowform->{form_change_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	if ($admindata->{merumaga_adminmail}) {
		# 管理人へメール
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_change_mailtitle}.$bufdata->{newemail},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	
	my $param;
	
	# 共通変数読み込み
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $bufdata->{newemail};
	$param->{newemail} = $bufdata->{newemail};
	$param->{oldemail} = $bufdata->{oldemail};
	
	if (isMobile()) {
		# 携帯版
		&printhtml_tk($param, "tmpl/m_edit_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC版
		&printhtml_tk($param, "tmpl/edit_finish.tmpl");
	}
	exit;
	
}

# メールアドレス変更
sub regedit{
	
	# 変更前データ取得
	my $beforedata = $objAcData->GetMailData("", $FORM{oldemail});
	# 変更後データ取得
	my $afterdata = $objAcData->GetMailData("", $FORM{newemail});

	# 新規登録時の日付セット
	my %TIME = &getdatetime();
	$FORM{'edit_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	
	if ($FORM{newemail} eq $FORM{oldemail}) { &error("変更前と変更後とでメールアドレスが同一です。"); }
	# フォームからの重複登録が許可されていない場合
	if (!$admindata->{double_reg_form}) {
		if ($afterdata->{id} && $afterdata->{status}) { &error("変更後メールアドレスは既に登録されています。"); }
	}
	if (!$beforedata->{id}) { &error("変更前メールアドレスが見つかりません。"); }
	
	# 同じE-mailの仮登録データ削除
	$objAcData->DelSameMailTempChangeData($FORM{oldemail});
	
	# メールアドレス変更
	$objAcData->RegChangeEmail($FORM{oldemail}, $FORM{newemail});
	
	$beforedata->{newemail} = $FORM{newemail};
	$beforedata->{oldemail} = $FORM{oldemail};
	my $body = $rowform->{form_change_mailbody};
	# 置換作業
	$body = $objAcData->ReplaceMailBody($body, $admindata, $beforedata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# 登録者へメール
		$objMail->send($sendmailpath,$FORM{newemail},$rowform->{form_change_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	if ($admindata->{merumaga_adminmail}) {
		# 管理人へメール
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_change_mailtitle}.$FORM{newemail},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	
	my $param;
	
	# 共通変数読み込み
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $beforedata->{newemail};
	$param->{newemail} = $beforedata->{newemail};
	$param->{oldemail} = $beforedata->{oldemail};
	
	if (isMobile()) {
		# 携帯版
		&printhtml_tk($param, "tmpl/m_edit_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC版
		&printhtml_tk($param, "tmpl/edit_finish.tmpl");
	}
	exit;
}

sub regdoubleopt{
	
	# エラーチェック
	if (!$FORM{id}) { &error("パラメータエラーです。"); }
	
	# 新規登録時の日付セット
	my %TIME = &getdatetime();
	$FORM{'add_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	$FORM{'edit_date'} = $FORM{'add_date'};
	
	# 対象データ取得
	my $bufdata = $objAcData->GetData('mailbuf', 'TEMPMAIL', $FORM{id});
	
	# 対象行取得失敗
	if (!$bufdata->{id} || !$bufdata->{email}) { &error("対象のデータ取得に失敗しました。<br>既に登録されているか、仮登録されていません。"); }

	# 配信フラグの立っているデータあるかどうか
	#if (!$objAcData->RegCheckDouble($bufdata->{email})) {
	#	&error("そのアドレスは既に登録されています。");
	#}
	
	# 登録されているかどうか
	my $targetdata = $objAcData->GetMailData("", $bufdata->{email});
	# フォームからの重複登録が許可されていない場合
	if (!$admindata->{double_reg_form}) {
		if ($admindata->{delmode} eq "del") {
			if ($targetdata->{id}) { &error("対象のアドレスは既に登録されています。"); }
		} else {
			if ($targetdata->{status}) {
				&error("対象のアドレスは既に登録されています。");
			}
		}
	}
	
	# 同じメールアドレスのデータを削除
	$objAcData->DelSameMailTempData($bufdata->{email});
	
	# 対象データがないかフォームからの重複がOKの場合
	if (!$targetdata->{id} || $admindata->{double_reg_form}) {
		# データ登録
		foreach my $n (keys %$bufdata) {
			$FORM{$n} = $bufdata->{$n};
		}
		$objAcData->RegEmail(\%FORM);
	} else {
		# 登録データを全て上書きする 10/03/24
		foreach my $n (keys %$bufdata) {
			$FORM{$n} = $bufdata->{$n};
		}
		$FORM{id} = $targetdata->{id};
		$FORM{status} = 1;
		$objAcData->UpdData('mail', 'MAIL', $targetdata->{id}, \%FORM);
		
		
		# 配信ステータス変更
		#my $CHANGE;
		#$CHANGE->{$bufdata->{email}} = 1;
		#$FORM{"send_flg".$targetdata->{id}} = 1;
		#$FORM{"hid_email".$targetdata->{id}} = 1;
		#$objAcData->UpdMailStatus(\%FORM);
	}
	
	my $body = $rowform->{form_mailbody};
	# 置換作業
	$body = $objAcData->ReplaceMailBody($body, $admindata, $bufdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	# 再登録防止リストからクリア
	$objAcData->CleanRegDenyByEmail($bufdata->{email});
	
	if ($admindata->{merumaga_usermail}) {
		# 登録者へメール
		$objMail->send($sendmailpath,$bufdata->{email},$rowform->{form_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	if ($admindata->{merumaga_adminmail}) {
		# 管理人へメール
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_mailtitle}.$bufdata->{email},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	
	my $param;
	
	# 共通変数読み込み
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $bufdata->{email};
	
	if (&isMobile()) {
		# 携帯版
		&printhtml_tk($param, "tmpl/m_reg_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC版
		&printhtml_tk($param, "tmpl/reg_finish.tmpl");
	}
	exit;
}


sub regautoform {
	
	# エラーチェック
	if (!$FORM{id}) { &error("パラメータエラーです。"); }
	
	# 新規登録時の日付セット
	my %TIME = &getdatetime();
	$FORM{'add_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	$FORM{'edit_date'} = $FORM{'add_date'};
	
	# 対象データ取得
	my $bufdata = $objAcData->GetData('mailbuf', 'TEMPMAIL', $FORM{id});
	
	# 対象行取得失敗
	if (!$bufdata->{id} || !$bufdata->{email}) { &error("対象のデータ取得に失敗しました。<br>既に登録されているか、仮登録されていません。"); }
	
	# 登録されているかどうか
	my $targetdata = $objAcData->GetMailData("", $bufdata->{email});
	# フォームからの重複登録が許可されていない場合
	if (!$admindata->{double_reg_form}) {
		if ($admindata->{delmode} eq "del") {
			if ($targetdata->{id}) { &error("対象のアドレスは既に登録されています。"); }
		} else {
			if ($targetdata->{status}) {
				&error("対象のアドレスは既に登録されています。");
			}
		}
	}
	
	# 2010/11/12 再登録防止機能追加
	if ($admindata->{'regdeny'}) {
		$objAcData->checkRegDeny($bufdata->{'email'});
	}
	
	
	# エラーチェック(必須項目チェック）
	my $error_data;
	if (!$objAcData->RegCheckExists(\%FORM, $SYS->{max_colnum}, \$error_data)) {
		&error($error_data);
	}
	
	# 同じメールアドレスのデータを削除
	$objAcData->DelSameMailTempData($bufdata->{email});
	
	# 対象データがないかフォームからの重複がOKの場合
	if (!$targetdata->{id} || $admindata->{double_reg_form}) {
		$objAcData->RegEmail(\%FORM);
	} else {
		$FORM{id} = $targetdata->{id};
		$FORM{status} = 1;
		$objAcData->UpdData('mail', 'MAIL', $targetdata->{id}, \%FORM);
	}
	
	# 再登録防止リストからクリア
	$objAcData->CleanRegDenyByEmail($bufdata->{email});
	
	my $body = $rowform->{form_mailbody};
	# 置換作業
	$body = $objAcData->ReplaceMailBody($body, $admindata, \%FORM, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# 登録者へメール
		$objMail->send($sendmailpath,$bufdata->{email},$rowform->{form_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	if ($admindata->{merumaga_adminmail}) {
		# 管理人へメール
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_mailtitle}.$bufdata->{email},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	
	my $param;
	
	# 共通変数読み込み
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $bufdata->{email};
	
	if (&isMobile()) {
		# 携帯版
		&printhtml_tk($param, "tmpl/m_reg_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC版
		&printhtml_tk($param, "tmpl/reg_finish.tmpl");
	}
	exit;
}
sub regadd{
	
	# 新規登録時の日付セット
	my %TIME = &getdatetime();
	$FORM{'add_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	$FORM{'edit_date'} = $FORM{'add_date'};
	
	my $error_data;
	# エラーチェック(必須項目チェック）
	if (!$objAcData->RegCheckExists(\%FORM, $SYS->{max_colnum}, \$error_data)) {
		&error($error_data);
	}
	
	# 配信フラグの立っているデータあるかどうか
	#if (!$objAcData->RegCheckDouble($FORM{email}, 1)) {
	#	&error("そのアドレスは既に登録されています。");
	#}
	
	# 対象のメールアドレスを取得
	my $maildata = $objAcData->GetMailData('', $FORM{'email'}) ;
	# フォームからの重複登録が許可されていない場合
	if (!$admindata->{double_reg_form}) {
		if ($maildata->{email} && $maildata->{status}) {
			&error("対象のアドレスは既に登録されています。");
		}
	}
	
	# 2010/11/12 再登録防止機能追加
	if ($admindata->{'regdeny'}) {
		$objAcData->checkRegDeny($FORM{'email'});
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
		
		## 配信フラグ更新
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
		$objMail->send($sendmailpath,$FORM{email},$rowform->{form_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	if ($admindata->{merumaga_adminmail}) {
		# 管理人へメール
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_mailtitle}.$FORM{email},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	
	my $param;
	
	# 共通変数読み込み
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $FORM{email};
	
	if (isMobile()) {
		# 携帯版
		&printhtml_tk($param, "tmpl/m_reg_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC版
		&printhtml_tk($param, "tmpl/reg_finish.tmpl");
	}
	exit;
	
}

sub regdel{
	
	# 既に削除済みかチェック
	my @DELMAIL = $objAcData->GetData('mail', 'MAIL');
	my $exist = 0;
	foreach my $ref (@DELMAIL) {
		if ($FORM{email} eq $ref->{email} && $ref->{status}) {
			$exist = 1;
		}
	}
	
	if(!$exist){
		&error("そのメールアドレスは登録されていません。");
	}

	# 対象行取得
	my $data = $objAcData->GetMailData("", $FORM{email});
	
	
	# 削除確認を使用するかどうか
	if ($admindata->{delconfirm} && !$FORM{checkok}) {
		my $param;
		# 確認画面表示
		$param = \%FORM;
		
		# 共通変数読み込み
		&set_common_value(\$param, $admindata);
	
		if (isMobile()) {
			# 携帯版
			&printhtml_tk($param, "tmpl/m_del_confirm.tmpl", "", "Shift_JIS");
		} else {
			# PC版
			&printhtml_tk($param, "tmpl/del_confirm.tmpl");
		}
		exit;
	}
	
	# メールデータ一式取得
	#my @DELMAIL = $objAcData->GetData('mail', 'MAIL');
	foreach my $ref (@DELMAIL) {
		if ($FORM{email} eq $ref->{email}) {
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
		$objMail->send($sendmailpath,$FORM{email},$rowform->{form2_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	if ($admindata->{merumaga_adminmail}) {
		# 管理人へメール
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form2_mailtitle}.$FORM{email},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
	}
	
	my $param;
	
	# 共通変数読み込み
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $FORM{email};
	
	if (isMobile()) {
		# 携帯版
		&printhtml_tk($param, "tmpl/m_del_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC版
		&printhtml_tk($param, "tmpl/del_finish.tmpl");
	}
	exit;
	
}

# ////////////////////////////////////////////////////////////////////////// #


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
