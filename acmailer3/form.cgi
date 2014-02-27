#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

my %FORM = &form("noexchange");
my $data_ref;

if ($FORM{id}) {
	# 対象データ取得
	my $doptdata = $objAcData->GetData('mailbuf', 'TEMPMAIL', $FORM{id});
	
	if (!$doptdata->{id} || !$doptdata->{email}) { &error("対象のデータ取得に失敗しました。<br>既に登録されているか、仮登録されていません。"); }
	$data_ref->{doptdata} = $doptdata;
	

} elsif ($FORM{mode} ne "preview") {
	# 通常のフォームとして使用するように
	#&error("不正なアクセスです");
}

# 使用禁止かどうか
if (!$FORM{'preview'} && !$admindata->{'autoform_use'}) {
	&error("現在使用することができません。");
}

# 自由項目
my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{freecol_list} = \@freecol;

# チェックボックスのものはあらかじめ文字列を作成
my $i = 1;

foreach my $n (@freecol) {
	if ($FORM{'preview'}) {
		foreach my $n2 (qw(type name disp text)) {
			$n->{"col".$n2} = $FORM{"col".$i.$n2};
			if ($n2 eq "text") {
				# 改行が含まれている場合
				my @autodata = split(/\r\n|\r|\n/, $n->{"col".$n2});
				my @v2;
				foreach my $n2 (@autodata) {
					if ($n2 eq "") { next; }
					my $row2;
					$row2->{"coltext"} = $n2;
					push(@v2, $row2);
				}
				$n->{"autodatalist"} = \@v2;
			}
		}
	}
	if ($n->{coltype} eq "checkbox") {
		$data_ref->{checkbox_list} .= ",col".$n->{num};
	}
	$i++;
}

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# フォームの値
$data_ref->{form} = \%FORM;

# HTML表示
if (&isMobile()) {
	# 携帯端末の場合
	&printhtml_tk($data_ref, "tmpl/m_form.tmpl", "", "Shift_JIS");
} else {
	# PC版
	&printhtml_tk($data_ref, "tmpl/form.tmpl");
}
exit;
