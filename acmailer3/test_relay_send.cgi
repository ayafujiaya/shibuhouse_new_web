#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use clsMail;
use strict;

our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# クッキーよりセッションデータ取得
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my %FORM = &form("noexchange");

if (!$FORM{'to'} || !$FORM{'from'} || !$FORM{'relay_host'}) {
	&error("送信者、送信先、送信サーバを設定してください");
}

my $return_path;
if ($admindata->{errmail} && $admindata->{errmail_email}) {
    $return_path = $admindata->{errmail_email};
}


my $senddata = "";
my $subject = 'ACMAILERよりテスト送信';
my $body = "ACMAILERより外部サーバを利用しての送信テストです。";

#件名、本文をJISに変換
&jcode::convert(\$subject, "jis");
&jcode::convert(\$body, "jis");

my $objMail = new clsMail(1, $FORM{relay_host}, $FORM{port}, $FORM{relay_user}, $FORM{relay_pass}, $FORM{relay_send_mode});

#メールHEADER定義
$senddata .= "Return-Path: $FORM{from} \n" if $FORM{from};
$senddata .= "X-Mailer: acmailer3.0 http://www.ahref.org/\n";
$senddata .= "X-SENDTO: $FORM{to}\n";
$senddata .= &mimeencode("To: $FORM{to}\n");
$senddata .= &mimeencode("From: $FORM{from}\n");
$senddata .= "Subject: ".$objMail->sencode($subject)."\n";
$senddata .= "MIME-Version: 1.0\n";
$senddata .= "Content-Transfer-Encoding: 7bit\n\n";
#メール本文定義
$senddata .= $body;


print "Content-type: text/html; charset=EUC-JP\n\n";
print '<div align="center">';
print "実行結果<br>";
print '<textarea style="width:400px;height:200px;">';
# 外部サーバにより送信
my $rs = $objMail->relay_sendmail($FORM{to}, $FORM{from}, $return_path, $senddata, 1);
print '</textarea>';
print "<CENTER>";
if ($rs) {
	print "テストメールの送信に成功しました。送信先に届いているかご確認ください。";
} else {
	print "<font color=\"red\">送信に失敗しました。設定を再度ご確認ください。</font>";
}
print '<center><br><br><br><input type="button" value="閉じる" onclick="javascript:window.close();">';
print '</div>';
exit;
