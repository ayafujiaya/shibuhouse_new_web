#!/usr/bin/perl
#
# �Ź沽���饹
# �ƤӽФ�����common.pm�򻲾ȤΤ���

package clsHex;
use Crypt::RC4;
use strict;


# ���󥹥ȥ饯��
# ���������ʤ�
sub new {
	my $pkg = shift;
	bless {
	} ,$pkg;
}

# �ǥ�����
# ���������ѥ���ɡ��о�ʸ����
# ����͡��ǥ�����ʸ����
sub Decode(){
	my $self = shift;
	my $pass = shift;
	my $enchex = shift;
	
	my(@encbin) = ();
	while (length($enchex) > 0) {
		push(@encbin, pack("h2", $enchex));
		$enchex = substr($enchex, 2);
	}
	my($dec) = RC4($pass, join('', @encbin));
	return $dec;
}

# ���󥳡���
# ���������ѥ���ɡ��о�ʸ����
# ����͡����󥳡���ʸ����
sub Encode(){
	my $self = shift;
	my $pass = shift;
	my $plain = shift;
	
	my($encbin) = RC4($pass, $plain);
	my(@enchex) = ();
	foreach (split(//,$encbin)) {
	 push(@enchex, unpack("h2",$_));
	}
	return join('',@enchex);
}


1;
