#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use MailSession;
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

# 管理画面の設定が行われているかどうか
&CheckAdminData_MailSend($admindata);

my $data_ref = $admindata;


# メール送信IDを発行
my $mail_session =
    MailSession->new(
	mail_id     => $FORM{mail_session_id},
	session_dir => $SYS->{dir_session_mail},
    );
$FORM{mail_session_id} = $mail_session->mail_id();



# 戻るの場合
if ($FORM{'back'}) {
	
	foreach my $n (keys %S) {
		my $form_name = $n;
		$form_name =~ s/email_send_//g;
		$FORM{$form_name} = $mail_session->get($n);
		$FORM{$form_name} = &sessionStrDecode($FORM{$form_name});
	}
	
	$FORM{mail_title} =~ s/__<<equal>>__/\=/gi;
	$FORM{mail_body} =~ s/__<<equal>>__/\=/gi;
	$FORM{mail_title} =~ s/__<<semicolon>>__/;/gi;
	$FORM{mail_body} =~ s/__<<semicolon>>__/;/gi;

} else {
	# 初期表示
	my %TIME = &getdatetime();
	if (!$FORM{'send_year'}) { $FORM{'send_year'} = $TIME{'year'}; }
	if (!$FORM{'send_mon'}) { $FORM{'send_mon'} = int $TIME{'mon'}; }
	if (!$FORM{'send_day'}) { $FORM{'send_day'} = int $TIME{'mday'}; }
	if (!$FORM{'send_hour'}) { $FORM{'send_hour'} = int $TIME{'hour'}; }
	if (!$FORM{'send_min'}) { $FORM{'send_min'} = int $TIME{'min'}; }
}

# 履歴からデータを取得
if ($FORM{'id'} && !$FORM{'back'}) {
    my $data = &getHistData($FORM{'id'});

    if ($data->{'id'}) {
	foreach my $n (keys %$data) {
	    $FORM{$n} = $data->{$n};
	}
	#%FORM = %$data;
    }
}

# 検索項目作成
my @search = $objAcData->MakeSearchCol(\%FORM, $SYS->{max_colnum});
$data_ref->{search} = \@search;

# 自由項目取得
my @collist = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{col_list} = \@collist;

# メールアドレス取得
my @DATA = $objAcData->GetData('mail', 'MAIL');

# 重複チェック
&CheckDoubleData(\@DATA, $admindata);

# 登録件数
$data_ref->{totalnum} = $#DATA+1;

$FORM{sendstopnum} = 0;
$FORM{zyunum} = 0;
$FORM{errornum} = 0;
my @DATA = $objAcData->SearchEmail(\@DATA, \%FORM, $SYS->{max_colnum});
$data_ref->{zyunum} = $FORM{zyunum} || 0;
$data_ref->{errornum} = $FORM{errornum} || 0;
$data_ref->{sendstopnum} = $FORM{sendstopnum};


if (!$data_ref->{sendstopnum}) { $data_ref->{sendstopnum} = 0; }
$data_ref->{emailnum} = $data_ref->{totalnum} - $data_ref->{errornum} - $data_ref->{sendstopnum};

# メールテンプレ
my @TEMPLATEDATA = $objAcData->GetData("template", "TEMPLATE");
my $java_array = " var arrtemplate = new Object(); \n";
foreach my $row (@TEMPLATEDATA) {
	$row->{default_mail_body} = $row->{mail_body};
	$row->{default_mail_title} = $row->{mail_title};
	$row->{mail_body} =~ s/__<<BR>>__/\\n/gi;
	$row->{mail_title} =~ s/\"/\\\"/g;
	$row->{mail_body} =~ s/\"/\\\"/g;
	
	#$java_array .= "arrtemplate[\"$row->{id}1\"] = \"".&plantext2html($row->{mail_title})."\";\n";
	#$java_array .= "arrtemplate[\"$row->{id}2\"] = \"".&plantext2html($row->{mail_body})."\";\n";
	$java_array .= "arrtemplate[\"$row->{id}1\"] = \"$row->{mail_title}\";\n";
	$java_array .= "arrtemplate[\"$row->{id}2\"] = \"$row->{mail_body}\";\n";
	
	# デフォルト表示
	if ($row->{default} && !$FORM{mail_body} && !$FORM{mail_title}) {
		
		$FORM{mail_title} = $row->{default_mail_title};
		$FORM{mail_body} = $row->{default_mail_body};
		$FORM{mail_body} =~ s/__<<BR>>__/\n/gi;
		$row->{template_name} .= "(デフォルト)";
		$row->{selected} = " selected ";
	}
}
# テンプレート一覧
$data_ref->{template_list} = \@TEMPLATEDATA;
$data_ref->{java_array} = $java_array;


# 予約配信用日時
if ($data_ref->{reserve}) {
	&MakeYMDSelect(\$data_ref);
}

my $template_file = "";
if ($FORM{mode} eq "deco" && !$FORM{sid}) {
	# 絵文字リスト
	my $emoji = mobilemailimg(99);
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

	# アップロードされているファイル一覧取得
	my @f = &get_uploadimage();
	$data_ref->{file_list} = \@f;
	
	$template_file = 'tmpl/email_send_deco.tmpl';
}


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
&printhtml_tk($data_ref, $template_file);
exit;

# 履歴データからデータを取得
sub getHistData() {
	my $id = shift;
	
	my $data_ref = $objAcData->GetData('hist', 'HIST', $id);
	
	$data_ref->{send_year} = int substr($data_ref->{start_send_date}, 0, 4);
	$data_ref->{send_mon} = int substr($data_ref->{start_send_date}, 4, 2);
	$data_ref->{send_day} = int substr($data_ref->{start_send_date}, 6, 2);
	$data_ref->{send_hour} = int substr($data_ref->{start_send_date}, 8, 2);
	$data_ref->{send_min} = int substr($data_ref->{start_send_date}, 10, 2);
	$data_ref->{send_sec} = int substr($data_ref->{start_send_date}, 12, 2);
	
	$data_ref->{mail_body} =~ s/__<<BR>>__/\n/gi;
	
	$data_ref->{mode} = $data_ref->{deco_mode};

	foreach my $n (keys %$data_ref) {
		if ($n =~ /^search_text([0-9]*)$/ && $data_ref->{$n}) {
			if ($data_ref->{disp_id} < $1) {
				$data_ref->{disp_id} = $1;
			}
		}
	}
	
	return $data_ref;
}
