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

if ($FORM{upd}) {
	# エラーチェック
	if (&error_check(\%FORM, \$data_ref->{error_message})) {
		# 登録
		$objAcData->UpdFormData(\%FORM);
		
		# リロード
		print "Location: form_edit.cgi?okedit=1 \n\n";
		exit;
	} else {
		foreach my $n (keys %FORM) {
			$data_ref->{$n} = $FORM{$n};
		}
	}
} else {
	# フォームデータ取得
	my $data = $objAcData->GetRowData('form', 'FORM');
	$data->{form_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form2_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_temp_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_temp_change_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_change_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_autoform_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_regdeny_mailbody} =~ s/__<<BR>>__/\n/g;
	foreach my $n (%$data) {
		$data_ref->{$n} = $data->{$n};
	}
}

$data_ref->{oktext} = "変更されました。" if $FORM{okedit};

# 自由項目取得
my @collist = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{col_list} = \@collist;

# アンケートデータ取得
my @EDATA = $objAcData->GetData('enq', 'ENQ');
foreach my $row (@EDATA) {
	$row->{enq_data} =~ s/__<<BR>>__/\n/g;
}
$data_ref->{enq_list} = \@EDATA;

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;

# エラーチェック
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my @error;
	if ($FORM{form_mailtitle} eq "") {
		push(@error, "登録用　件名を入力してください。");
	}
	if ($FORM{form_mailbody} eq "") {
		push(@error, "登録用　本文を入力してください。");
	}
	if ($FORM{form2_mailtitle} eq "") {
		push(@error, "解除用　件名を入力してください。");
	}
	if ($FORM{form2_mailbody} eq "") {
		push(@error, "解除用　本文を入力してください。");
	}
	if ($FORM{form_temp_mailtitle} eq "") {
		push(@error, "仮登録用　件名を入力してください。");
	}
	if ($FORM{form_temp_mailbody} eq "") {
		push(@error, "仮登録用　本文を入力してください。");
	}
	if ($FORM{form_change_mailtitle} eq "") {
		push(@error, "変更用　件名を入力してください。");
	}
	if ($FORM{form_change_mailbody} eq "") {
		push(@error, "変更用　本文を入力してください。");
	}
	if ($FORM{form_temp_change_mailtitle} eq "") {
		push(@error, "仮変更用　件名を入力してください。");
	}
	if ($FORM{form_temp_change_mailbody} eq "") {
		push(@error, "仮変更用　本文を入力してください。");
	}
	if ($FORM{form_autoform_mailtitle} eq "") {
		push(@error, "空メールフォーム用　件名を入力してください。");
	}
	if ($FORM{form_autoform_mailbody} eq "") {
		push(@error, "空メールフォーム用　本文を入力してください。");
	}
	if ($FORM{form_regdeny_mailtitle} eq "") {
		push(@error, "再登録拒否用　件名を入力してください。");
	}
	if ($FORM{form_regdeny_mailbody} eq "") {
		push(@error, "再登録拒否用　本文を入力してください。");
	}
	
	
	# 禁止文字置換
	$$p_FORM{form_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form2_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form2_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_temp_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_temp_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_temp_change_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_temp_change_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_change_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_change_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_autoform_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_autoform_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_regdeny_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_regdeny_mailbody} =~ s/\t/ /gi;
	
	if ($#error >= 0) {
		$$error_message = join("<BR>", @error);
		return 0;
	}
	return 1;


}
