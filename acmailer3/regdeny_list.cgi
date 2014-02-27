#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

if ($FORM{del}) {
    # 削除
	if ($FORM{'id'}) {
		$objAcData->DelData("regdeny", "REGDENY", $FORM{'id'});
		$data_ref->{'oktext'} = "１件削除されました。";
	} else {
	    $objAcData->CleanRegDeny(\%FORM);
	    $data_ref->{oktext} = "$FORM{delnum}件削除されました。";
	}
} elsif ($FORM{'alldel'}) {
	# 全削除
	my %REG;
	$objAcData->ResetData("regdeny", "REGDENY", \%REG);
	$data_ref->{'oktext'} = "全件削除されました。";
} elsif ($FORM{'mode'} eq "change") {
	# 再登録拒否設定変更
	my $regdata = $admindata;
	$regdata->{'regdeny'} = $FORM{'regdeny'} ? "1" : "";
	
	# 管理者データ更新
	$objAcData->UpdAdminData($regdata);
	
	# 管理者データを再取得
	$admindata = $objAcData->GetAdminData();

}

# 仮登録データ取得
my @DATA = $objAcData->GetData('regdeny', 'REGDENY');
foreach my $row (@DATA) {
	# 削除日
	#$row->{del_date_disp} = substr($row->{del_date}, 0, 4)."/".substr($row->{del_date}, 4, 2)."/".substr($row->{del_date}, 6, 2);
	$row->{del_date_disp} = $row->{del_date};
	$row->{del_date_disp} =~ s/^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})$/$1\/$2\/$3 $4:$5:$6/;
	# 期限日
	if ($row->{limit_date}) {
		$row->{limit_date_disp} = $row->{limit_date};
		#$row->{limit_date_disp} = substr($row->{limit_date}, 0, 4)."/".substr($row->{limit_date}, 4, 2)."/".substr($row->{limit_date}, 6, 2);
		$row->{limit_date_disp} =~ s/^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})$/$1\/$2\/$3 $4:$5:$6/;
	}
}
my @SEARCH;
if ($FORM{'search'} && $FORM{'search_word'}) {
	# 絞り込み
	foreach my $row (@DATA) {
		if ($row->{'email'} =~ /$FORM{search_word}/) {
			push(@SEARCH, $row);
		}
	}
	@DATA = @SEARCH;
}

# ソート
@DATA = sort {$b->{'del_date_disp'} cmp $a->{'del_date_disp'}} @DATA;

# パラメータ引きずり
if ($FORM{'search'}) {
	$data_ref->{'para'} = "&search=1&search_word=".&urlencode($FORM{'search_word'});	
}

# ページング処理
my $objPaging = new clsPaging($FORM{dispnum}, $FORM{page}, $data_ref->{'para'});
@DATA = $objPaging->MakePaging(\@DATA, \$data_ref);

$data_ref->{loop} = \@DATA;

# フォームの値
$data_ref->{form} = \%FORM;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
