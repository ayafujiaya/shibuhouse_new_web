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

if ($FORM{'mode'} eq "admin") {
	# �����ԥǡ���
	my $data = $objAcData->ReadFile($SYS->{data_dir}."admin.cgi");
	output($data, "admin");
} elsif ($FORM{'mode'} eq "freecol") {
	# ��ͳ���ܥǡ���
	my $data = $objAcData->ReadFile($SYS->{data_dir}."freecol.cgi");
	output($data, "freecol");
} elsif ($FORM{'mode'} eq "errmail") {
	# ���顼�᡼��
	my $data = $objAcData->ReadFile($SYS->{data_dir}."errmail.cgi");
	output($data, "errmail");
} elsif ($FORM{'mode'} eq "form") {
	# ��ư�ֿ��᡼��
	my $data = $objAcData->ReadFile($SYS->{data_dir}."form.cgi");
	output($data, "form");
} elsif ($FORM{'mode'} eq "template") {
	# �ۿ��ƥ�ץ졼��
	my $data = $objAcData->ReadFile($SYS->{data_dir}."template.cgi");
	output($data, "template");
} elsif ($FORM{'mode'} eq "hist") {
	# ����ǡ���
	my $data = $objAcData->ReadFile($SYS->{data_dir}."hist.cgi");
	output($data, "hist");
} elsif ($FORM{'mode'} eq "dispcol") {
	# ������ɽ������
	my $data = $objAcData->ReadFile($SYS->{data_dir}."dispcol.cgi");
	output($data, "dispcol");
} elsif ($FORM{'mode'} eq "license") {
	# ������ɽ������
	my $data = $objAcData->ReadFile($SYS->{data_dir}."enc.cgi");
	output($data, "enc");
} elsif ($FORM{'mode'} eq "autoform") {
	# �ե���������ǡ���
	my $data = $objAcData->ReadFile($SYS->{data_dir}."autoform.cgi");
	output($data, "autoform");
}
# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# �ե��������
$data_ref->{form} = \%FORM;

# HTMLɽ��
&printhtml_tk($data_ref);
exit;

sub output() {
	my $data = shift;
	my $name = shift;
	my $size = length $data;
	my %DATE = &getdatetime();
	print "Content-Type: application/octet-stream\n"; 
	print "Content-Disposition: attachment; filename=$name$DATE{year}$DATE{mon}$DATE{mday}.csv\n"; 
	print "Content-Length: $size\n\n"; 

	print $data;
	exit;
	
}
