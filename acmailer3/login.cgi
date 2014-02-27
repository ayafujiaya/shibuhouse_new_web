#!/usr/bin/perl

our $SYS;
use lib "./lib/";
require "./lib/setup.cgi";
use clsMail;
use strict;

# 管理情報取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

my $data_ref = $admindata;
my %FORM = &form();
my $template;


if ($FORM{mode} eq "forget") {
	if ($FORM{send}) {
		if (!$FORM{email}) {
			$data_ref->{error_message} = "メールアドレスを入力してください。";
		} elsif ($FORM{email} ne $admindata->{admin_email}) {
			$data_ref->{error_message} = "メールアドレスが一致しません。";
		} else {
			# メールの送信
			my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

			my $subject = "パスワード再送信";
			my $body = "パスワードを再送信します。
あなたの登録されているパスワードは ".$admindata->{login_pass}."です。";
			my $objMail = new clsMail();
			$objMail->send($admindata->{sendmail_path},$FORM{email},$subject,$body,$sendername,$admindata->{admin_email},'',$admindata->{admin_email}) || &error("メールアドレスの送信に失敗しました。<br>お手数ですが管理人「$sendername」にご連絡ください。");
			$data_ref->{sendok} = 1;
		}
	}
	# パスワード再送信画面を表示
	$template = "tmpl/forget.tmpl";
} elsif ($data_ref->{login_id} && $data_ref->{login_pass}) {

} else {
	# SENDMAILパスを探す
	if (-e "/usr/sbin/sendmail") {
		$data_ref->{sendmail_path} = "/usr/sbin/sendmail";
	} elsif (-e "/usr/lib/sendmail") {
		$data_ref->{sendmail_path} = "/usr/lib/sendmail";
	}
	# CGI設置URLを抽出
	my $regcgi = $ENV{REQUEST_URI};
	if ($regcgi =~ /(.*)\/[^\/]*login\.cgi.*$/) {
		$regcgi = $1;
		if ($data_ref->{ssl}) {
			$data_ref->{homeurl} = "https://".$ENV{HTTP_HOST}.$1."/";
		} else {
			$data_ref->{homeurl} = "http://".$ENV{HTTP_HOST}.$1."/";
		}
	}
	
	# pwdコマンドでCGI設置場所を取得
	my $path = `pwd`;
	$path =~ s/(.*)[\s]*$/$1/;
	$data_ref->{mypath} = $path;
	
	# HTMLテンプレートオープン
	$template = "tmpl/init.tmpl";
}

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref, $template);
exit;
