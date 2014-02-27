#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
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
my $data_ref;

my $emoji = &mobilemailimg(99);
my @e_image;
foreach my $n (keys %$emoji) {
	my $row;
	if ($n) {
		$row->{image} = $emoji->{$n};
		$row->{image_url} = 'i/'.$emoji->{$n};
		$row->{name} = $n;
		push(@e_image, $row);
	}
}

@e_image = sort {$a->{image} cmp $b->{image}} @e_image;

$data_ref->{image_list} = \@e_image;

# 共通変数読み込み
&set_common_value(\$data_ref, $admindata);

# HTML表示
&printhtml_tk($data_ref);
exit;
