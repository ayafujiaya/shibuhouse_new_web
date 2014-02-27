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

if ($FORM{reg}) {

	if ($FORM{id}) {
		# 更新
		if (error_check(\%FORM, \$data_ref->{error_message})) {
			$FORM{template_name} =~ s/\t/ /gi;
			$FORM{mail_title} =~ s/\t/ /gi;
			$FORM{mail_body} =~ s/\t/ /gi;
			$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
			
			# 更新
			$objAcData->UpdData("template", "TEMPLATE", $FORM{id}, \%FORM);
			
			# 一覧へ
			print "Location: mailtemplate_list.cgi?updok=1 \n\n";
			exit;
		} else {
			foreach my $n (keys %FORM) {
				$data_ref->{$n} = $FORM{$n};
			}
		}
	} else {
		# 新規追加
		if (error_check(\%FORM, \$data_ref->{error_message})) {
			$FORM{id} = time.$$;
			$FORM{template_name} =~ s/\t/ /gi;
			$FORM{mail_title} =~ s/\t/ /gi;
			$FORM{mail_body} =~ s/\t/ /gi;
			$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
			
			# 新規追加
			$objAcData->InsData("template", "TEMPLATE", \%FORM);
			
			# 一覧へ
			print "Location: mailtemplate_list.cgi?addok=1 \n\n";
			exit;
		} else {
			foreach my $n (keys %FORM) {
				$data_ref->{$n} = $FORM{$n};
			}
		}
	}
} elsif ($FORM{del} && $FORM{id}) {
	# 削除
	$objAcData->DelData("template", "TEMPLATE", $FORM{id});
	
	# 一覧へ
	print "Location: mailtemplate_list.cgi?delok=1 \n\n";
	exit;
} elsif ($FORM{default_change}) {
	# デフォルトフラグ更新
	$objAcData->UpdTemplateDefaultFlg($FORM{default});

	# 一覧へ
	print "Location: mailtemplate_list.cgi?updok=1 \n\n";
	exit;
}

# テンプレートデータ取得
if ($FORM{id} && !$data_ref->{error_message}) {
	my $data = $objAcData->GetData("template", "TEMPLATE", $FORM{id});
	foreach my $n (keys %$data) {
		$data_ref->{$n} = $data->{$n};
	}
	$data_ref->{mail_body} =~ s/__<<BR>>__/\n/gi;
}

my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{col_list} = \@freecol;

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
	
	my %FORM = %$p_FORM;
	my @error;
	
	if (!$FORM{template_name}) { push(@error, "テンプレート名を入力してください。"); }
	if (!$FORM{mail_title}) { push(@error, "件名を入力してください。"); }
	if (!$FORM{mail_body}) { push(@error, "本文を入力してください。"); }
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;
	
}
