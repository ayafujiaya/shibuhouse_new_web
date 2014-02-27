#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# セッションデータ取得とログインチェック
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);

my $data_ref;

if ($FORM{'mode'} eq "admin") {
	# 管理者データ
	my $data = $objAcData->ReadFile($SYS->{data_dir}."admin.cgi");
	output($data, "admin");
} elsif ($FORM{'mode'} eq "freecol") {
	# 自由項目データ
	my $data = $objAcData->ReadFile($SYS->{data_dir}."freecol.cgi");
	output($data, "freecol");
} elsif ($FORM{'mode'} eq "errmail") {
	# エラーメール
	my $data = $objAcData->ReadFile($SYS->{data_dir}."errmail.cgi");
	output($data, "errmail");
} elsif ($FORM{'mode'} eq "form") {
	# 自動返信メール
	my $data = $objAcData->ReadFile($SYS->{data_dir}."form.cgi");
	output($data, "form");
} elsif ($FORM{'mode'} eq "template") {
	# 配信テンプレート
	my $data = $objAcData->ReadFile($SYS->{data_dir}."template.cgi");
	output($data, "template");
} elsif ($FORM{'mode'} eq "hist") {
	# 履歴データ
	my $data = $objAcData->ReadFile($SYS->{data_dir}."hist.cgi");
	output($data, "hist");
} elsif ($FORM{'mode'} eq "dispcol") {
	# 検索用表示項目
	my $data = $objAcData->ReadFile($SYS->{data_dir}."dispcol.cgi");
	output($data, "dispcol");
} elsif ($FORM{'mode'} eq "license") {
	# 検索用表示項目
	my $data = $objAcData->ReadFile($SYS->{data_dir}."enc.cgi");
	output($data, "enc");
} elsif ($FORM{'mode'} eq "autoform") {
	# フォーム設定データ
	my $data = $objAcData->ReadFile($SYS->{data_dir}."autoform.cgi");
	output($data, "autoform");
}
# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# フォームの値
$data_ref->{form} = \%FORM;

# HTML表示
&printhtml_tk($data_ref);
exit;

sub output() {
	my $data = shift;
	my $name = shift;
	my $size = length $data;
	my %DATE = &getdatetime();
	print "Content-Type: application/octet-stream\n"; 
	print "Content-Disposition: attachment; filename=$name$DATE{year}$DATE{mon}$DATE{mday}.csv\n"; 
	print "Content-Length: $size\n\n"; 

	print $data;
	exit;
	
}
