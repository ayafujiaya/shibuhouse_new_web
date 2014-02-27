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

# 表示カラム取得
my $dispcol = $objAcData->GetRowData('dispcol', 'DISPCOL');
foreach my $n (keys %$dispcol) {
	$data_ref->{$n} = $dispcol->{$n};
}

if ($FORM{'edit'}) {
	# エラーチェック
	if (&error_check(\%FORM, \$data_ref->{error_message})) {
		# 管理者データ更新
		$objAcData->UpdDispColData(\%FORM);
		
		# 再読み込み
		print "Location: dispcol_edit.cgi?okedit=1 \n\n";
		exit;
		
	} else {
		foreach my $n (keys %FORM) {
			$data_ref->{$n} = $FORM{$n};
		}
	}
} else {

}

my @freecol = $objAcData->GetFreeColLoopData_EmailList($SYS->{max_colnum});
$data_ref->{freecol_list} = \@freecol;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# フォームの値
$data_ref->{form} = \%FORM;

# HTML表示
&printhtml_tk($data_ref);
exit;

# エラーチェック
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my %FORM = %$p_FORM;
	my @error;
	

	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;

}
