#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å����ǡ��������ȥ���������å�
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

# �ۿ����
if ($FORM{mode} eq "send_stop" && $FORM{over_count}) {
	
	my %STOP;
	# �ǡ�������
	my @DATA = $objAcData->GetErrorMailLoopData();
	foreach my $row (@DATA){
		# ����������
		if ($FORM{over_count} && $FORM{over_count} > $row->{count}) { next; }
		$STOP{"send_flg".$row->{email}} = 0;
		$STOP{"hid_email".$row->{email}} = 1;
	}
	# �ۿ����
	$objAcData->UpdMailStatus(\%FORM);
	
} elsif ($FORM{mode} eq "alldel") {
	# �������
	$objAcData->error_mail_hist_alldel($admindata);
} elsif ($FORM{mode} eq "scan") {
	# �������
	$objAcData->error_mail_work($admindata);
} elsif ($FORM{mode} eq "csv") {
	# CSV���������
	
	my $mail = "E-MAIL,������\n";

	#�ե��������������
	my @DATA = $objAcData->GetErrorMailLoopData();

	foreach my $row (@DATA){
		
		# ����������
		if ($FORM{over_count} && $FORM{over_count} > $row->{count}) { next; }
		
		$mail .= "$row->{email},$row->{count}\n";
	}
	
	&jcode::convert(\$mail, "sjis", "euc");
	my %DATE = &getdatetime;

	my $size = length $mail;
	print "Content-Type: application/octet-stream\n"; 
	print "Content-Disposition: attachment; filename=errmaildata$DATE{year}$DATE{mon}$DATE{mday}.csv\n"; 
	print "Content-Length: $size\n\n"; 
	print $mail;
	exit;
	
}


# ���顼�᡼��ǡ�������
my @DATA = $objAcData->GetErrorMailLoopData();

my @data;
foreach my $row (@DATA){
	# ����������
	if ($FORM{over_count} && $FORM{over_count} > $row->{count}) { next; }
	push (@data,$row);
}
# �ڡ����󥰽���
my $objPaging = new clsPaging($FORM{dispnum}, $FORM{page}, '&search=1&over_count='.$FORM{'over_count'});
@data = $objPaging->MakePaging(\@data, \$data_ref);
$data_ref->{loop} = \@data;

$data_ref->{search_url} = '&over_count='.$FORM{over_count};

$data_ref->{oktext} = "$FORM{delnum}��������ޤ�����" if $FORM{okdel};

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;
