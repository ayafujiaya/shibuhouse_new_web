#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
$|=1;

select(STDOUT);
$|=1;
select(STDOUT);

our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å�����ꥻ�å����ǡ�������
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

$SYS->{mypath} = $admindata->{mypath};

my %FORM = &form();

if ($FORM{uninstall}) {
	# ���󥤥󥹥ȡ�����
	&uninstall($admindata);
	
}


# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;



# ���󥤥󥹥ȡ�����
sub uninstall {
	my $admindata = shift;
	
	# �������ѥ������äƤ��뤫����
	if (!$admindata->{mypath} || !-e $admindata->{mypath}."lib/setup.cgi") {
		&error("CGI���֥ѥ��������Ǥ����Ƽ�����Ρ֥����ƥ�����ע���CGI���֥ѥ��פ��ǧ���ƹ����ܥ���򲡤��Ƥ���������");
	}
	
	print "Content-type: text/html; charset=EUC-JP\n\n";
	
	# �ե����������
	&file_delete($admindata->{mypath}, "");
	
	# ��ʬ���ȤΥǥ��쥯�ȥꤹ�٤ƺ��
	&file_delete($admindata->{mypath}, "1");
	
	print "<center><b>ACMAILER�Τ����Ѥ��꤬�Ȥ��������ޤ�����</b><br><br>data�ǥ��쥯���session�ǥ��쥯�ȥ�������ޤ�����<br>";
	print "���󥹥ȡ�����Υǥ��쥯�ȥ�������ƥ��󥤥󥹥ȡ��봰λ�Ȥʤ�ޤ���</center>";
	
	# �Ǹ�˼�ʬ���Ȥ���
	unlink('./uninstall.cgi');
	
	exit;
}

# �ե��������
sub file_delete() {
	my $dir = shift;
	my $mode = shift;
	
	opendir DATA, $dir;
	my @files = readdir DATA;
	closedir DATA;
	
	foreach my $fn(@files) {
		if ($fn eq "." || $fn eq "..") { next; }
		if (-d $dir.$fn) {
			# ACMAILER��data�ǥ��쥯�ȥ��session�ǥ��쥯�ȥ�ξ�����
			if ($fn eq "data" || $fn eq "session") {
				# �ǥ��쥯�ȥ�ξ��
				#&file_delete($dir.$fn."/", $mode);
				`rm -r $dir$fn`;
			}
		} else {
			## �ե�����ξ��
			#if ($fn eq "uninstall.cgi") { next; }
			#if ($dir =~ /$SYS->{mypath}/ && $mode) {
			#	unlink($dir.$fn);
			#	$SYS->{delnowcount}++;
			#	my $per = ($SYS->{delnowcount} / $SYS->{delcount}) * 100;
			#	
			#} elsif (!$mode) {
			#	$SYS->{delcount}++;
			#}
		}
	}
	if ($dir =~ /$SYS->{mypath}/ && $mode) {
		
		rmdir($dir);
		$SYS->{delnowcount}++;
		my $per = ($SYS->{delnowcount} / $SYS->{delcount}) * 100;
		
	} elsif (!$mode) {
		$SYS->{delcount}++;
	}
	return 1;
}
