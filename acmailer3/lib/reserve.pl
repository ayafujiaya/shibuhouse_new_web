#!/usr/bin/perl

my $myfilepath = '/home/admin2/project/acmailer3.8/';
chdir $myfilepath;
use lib "./lib/";

use POSIX;
use MIME::Base64;
use File::Copy;
require 'clsMail.pm';
#require $myfilepath.'lib/jcode.pl';
#require $myfilepath.'lib/mimew.pl';
require 'setup.cgi';

our $SYS;
$SYS->{data_dir} = $myfilepath."data/";

# 管理者のデータ取得
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();


my %FORM;
my %TIME = &getdatetime();

# 予約データを引き当てて、データを取得
my @SENDDATA = $objAcData->UpdHistReserveStatusData(\%TIME);;
foreach my $row (@SENDDATA) {
	$row->{mail_body} =~ s/__<<BR>>__/\n/gi;
}

# 送信
foreach my $ref (@SENDDATA) {
	if (!$ref) { next; }
	
	# 送信先一覧
	my @DATA = $objAcData->GetData('mail', 'MAIL');

	# 検索絞り込み
	my %SEARCH;
	foreach my $n (keys %$ref) {
		$SEARCH{$n} = $ref->{$n};
	}
	my @DATA = $objAcData->SearchEmail(\@DATA, \%SEARCH, $SYS->{max_colnum});

	my @data;
	my $sendertotal = 0;
	foreach my $row (@DATA){
		
		# 配信停止は無視
		if (!$row->{status}) { next; }
		$row->{i} = $i+1;
		
		
		my %TIME = &getdatetime();
		# プレビューは10件だけ

		$row->{subject} = $objAcData->ReplaceMailBody($ref->{mail_title}, $admindata, $row, $SYS->{max_colnum});
		$row->{body} = $objAcData->ReplaceMailBody($ref->{mail_body}, $admindata, $row, $SYS->{max_colnum});
		
		$row->{subject} =~ s/\t/ /gi;
		$row->{body} =~ s/\t/ /gi;
	
		push (@data,$row);
	}
	if ($ref->{send_type} == 1){
		&sendmail_div(\@data, $ref->{id});
	}elsif($admindata->{send_type} == 0){
		&sendmail(\@data, $ref->{id});
	} else {
		&sendmail(\@data, $ref->{id});
	}
}


exit;

sub sendmail{
	my $p_data = shift;
	my $histid = shift;
	my @NEWDATA_ORG = @{$p_data};
	# 対象データ取得
	my $target = $objAcData->GetData('hist', 'HIST', $histid);
	
	my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));
	my $return_path = $admindata->{admin_email};
	if ($admindata->{errmail} && $admindata->{errmail_email}) {
		$return_path = $admindata->{errmail_email};
	}
	my @hist;
	my $objMail = create_clsMail($admindata);
	foreach my $row (@NEWDATA_ORG){
		my $return = 1;
		
		$return = $objMail->send($admindata->{sendmail_path},$row->{email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$return_path, $target->{mail_type}, $histid);
		
		# 一定間隔待つ
		if ($admindata->{'send_span'}) { select(undef, undef, undef, $admindata->{'send_span'}); }
		
		if ($return){
			my $hist;
			$hist->{email} = $row->{email};
			push(@hist, $hist);
		}else{
		}
		
	}
	

	my %ENDTIME = &getdatetime();
	my %UPDATE;
	foreach my $n (keys %$target) {
		$UPDATE{$n} = $target->{$n};
	}
	$UPDATE{end_send_date} = "$ENDTIME{year}$ENDTIME{mon}$ENDTIME{mday}$ENDTIME{hour}$ENDTIME{min}$ENDTIME{sec}";	# 送信終了時間
	$UPDATE{total_count} = ($#NEWDATA_ORG + 1);
	$UPDATE{status} = 2;
	# 更新
	$objAcData->UpdData('hist', 'HIST', $histid, \%UPDATE);
	
}

sub sendmail_div{
	my $p_data = shift;
	my $histid = shift;
	my @NEWDATA_ORG = @{$p_data};

	# 対象データ取得
	my $target = $objAcData->GetData('hist', 'HIST', $histid);
	
	my $waittime = $admindata->{divwait};
	my $start = $SYS->{start};
	my $end = $start + $admindata->{divnum};

	my $c = 0;
	my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));
	my $return_path = $admindata->{admin_email};
	if ($admindata->{errmail} && $admindata->{errmail_email}) {
		$return_path = $admindata->{errmail_email};
	}
	
	my $data_num = ($#NEWDATA_ORG + 1);
	my $objMail = create_clsMail($admindata);
	foreach my $row (@NEWDATA_ORG){
		if($c >= $start && $c < $end){
			my $return = 1;
			$return = $objMail->send($admindata->{sendmail_path},$row->{email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$return_path, $target->{mail_type}, $histid);
			
			# 一定間隔待つ
			if ($admindata->{'send_span'}) { select(undef, undef, undef, $admindata->{'send_span'}); }
			
		}
		$c++;
	}
	if($data_num > $end){
		sleep $waittime;
		$SYS->{start} = $end;
		&sendmail_div(\@NEWDATA_ORG, $histid);
	}

	if($data_num > $end){
		
	}else{
		
		my %ENDTIME = &getdatetime();
		my %UPDATE;
		foreach my $n (keys %$target) {
			$UPDATE{$n} = $target->{$n};
		}
		$UPDATE{end_send_date} = "$ENDTIME{year}$ENDTIME{mon}$ENDTIME{mday}$ENDTIME{hour}$ENDTIME{min}$ENDTIME{sec}";	# 送信終了時間
		$UPDATE{total_count} = ($#NEWDATA_ORG + 1);
		$UPDATE{status} = 2;
		# 更新
		$objAcData->UpdData('hist', 'HIST', $histid, \%UPDATE);
		
		$SYS->{start} = 0;
		
	}
}


sub cons_error() {
	$errordata = shift;
	print $errordata;
	exit;
}
