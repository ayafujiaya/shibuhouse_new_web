#!/usr/bin/perl
#
# 暗号化クラス
# 呼び出し元でcommon.pmを参照のこと

package clsHex;
use Crypt::RC4;
use strict;


# コンストラクタ
# 引　数：なし
sub new {
	my $pkg = shift;
	bless {
	} ,$pkg;
}

# デコード
# 引　数：パスワード　対象文字列
# 戻り値：デコード文字列
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

# エンコード
# 引　数：パスワード　対象文字列
# 戻り値：エンコード文字列
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
