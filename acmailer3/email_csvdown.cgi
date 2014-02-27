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

# ��ͳ���ܼ���
my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
my $colname;
foreach my $ref (@freecol) {
	$colname .= $ref->{"colname"}.",";
}
$colname .= "���ơ�����,";

my $mail = "E-MAIL,$colname\n";

# �᡼��ǡ���������
my @DATA = $objAcData->GetData('mail', 'MAIL');

my $col = $objAcData->{MAIL_COL};
my @col = @$col;
foreach my $row (@DATA){
	foreach my $n (@col) {
		if ($n eq "id") { next; }
		$mail .= $row->{$n}.",";
	}
	$mail .= "\n";
}

&jcode::convert(\$mail, "sjis", "euc");
my %DATE = &getdatetime;

my $size = length $mail;
print "Content-Type: application/octet-stream\n"; 
print "Content-Disposition: attachment; filename=maildata$DATE{year}$DATE{mon}$DATE{mday}.csv\n"; 
print "Content-Length: $size\n\n"; 

print $mail;
exit;
