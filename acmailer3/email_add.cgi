#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# セッションデータ取得とログインチェック
my %COOKIE = &getcookie;
my $query = new CGI;
my %FORM = &form_multi($query);
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);

my $data_ref;
my $template_file = '';

my $sid = "";
if ($FORM{sid}) {
	$sid = "&sid=".$FORM{sid};
}

if ($FORM{check}) {

	# フォームよりCSVファイル＆CSVデーター受け取り
	$data_ref->{emailall} = $objAcData->GetAddEmail(\%FORM, $SYS->{max_colnum}, \$data_ref);
	
	my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
	$data_ref->{freecol_list} = \@freecol;

	# テンプレート選択
	$template_file = 'tmpl/email_add_check.tmpl';
	if ($FORM{sid}) { $template_file = 'tmpl/m_email_add_check.tmpl'; }
} elsif ($FORM{add}) {
	# データ追加
	$objAcData->AddEmail(\%FORM, $SYS->{max_colnum});
	
	print "Location: $SYS->{homeurl_ssl}email_list.cgi?okadd=1$sid \n\n";
	exit;
}

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref, $template_file);
exit;
