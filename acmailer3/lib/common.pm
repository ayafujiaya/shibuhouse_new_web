

sub form {
	my $buffer;
	my %FORM;
	my $noexchange = shift;
	my $noencode = shift;
	# フォームからの入力
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	}else {
		$buffer = $ENV{'QUERY_STRING'};
	}
	my @pairs = split(/&/,$buffer);
	foreach (@pairs) {
		my ($name, $value) = split(/=/, $_);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
		$name =~ tr/+/ /;
		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
		$name =~ s/\r\n/\n/g;
		$name =~ s/\r/\n/g;
		$value =~ s/\r\n/\n/g;
		$value =~ s/\r/\n/g;

		if ($noencode ne "noencode") {
			#&jcode::convert(\$name,'euc','sjis');
			#&jcode::convert(\$value,'euc','sjis');
		}
		
		if($noexchange ne "noexchange"){
			$name =~ s/;/；/g;
			$value =~ s/;/；/g;
			$name =~ s/,/，/g;
			$value =~ s/,/，/g;
			$name =~ s/&/＆/g;
			$value =~ s/&/＆/g;
			$name =~ s/=/＝/g;
			$value =~ s/=/＝/g;
			$name =~ s/'/’/g;
			$value =~ s/'/’/g;
			$name =~ s/"/”/g;
			$value =~ s/"/”/g;
		}
		
		$FORM{$name} = $value;
		# 10/04/05 配列でも受け取れるように
		push(@{$FORM{"array_".$name}}, $value);
	
	}
	return %FORM;

}

sub form_multi {
	my $query = shift;
	my %FORM;
	my @names = $query->param;
	foreach(@names){
		$FORM{$_} =  $query->param($_);
	}
	return %FORM;
}

#各種エラーチェック関数
sub errorcheck(){
	my $str = shift;
	my $type = shift;
	my $com = shift;
	
	# type = 1 入力がなければエラー
	if($type == 1){
		
		if(!$str){
			&error($com);
		}
		
	# type = 2 メールアドレス正規表現チェック
	}elsif($type == 2){
		
		if(!CheckMailAddress($str)){
			&error($com);
		}
		
	}
	return 1;
}

sub openfile2array{
	my $filepath = shift;
	my @DATA;
	&syserror("$filepathのオープンに失敗しました。") unless -e $filepath;
	
	#データファイルオープン
	open (IN,$filepath) || &syserror("データファイルのオープンに失敗しました。");
	flock(IN,1);
	my @DATA_ORG = <IN>;
	close (IN);

	#改行取り除き
	foreach(@DATA_ORG){
		$_ =~ s/\r\n//g;
		$_ =~ s/\r//g;
		$_ =~ s/\n//g;
		
		#from_to($html_data, 'utf8', 'shiftjis');
		#&Jcode::convert(\$_, "euc");
		if($_){
			push(@DATA,$_);
		}
	}
	return @DATA;

}

sub CheckMailAddress {

	my $mailadr = shift;
	my $mail_regex = q{(^[\w|\!\%\'\=\-\^\\\~\+\*\.\?\/]+)\@([\w|\!\#\$\%\'\(\)\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)(\.\w+)+$};
	
	#シェルスクリプト展開時のエラー回避
	if ($mailadr =~ /\`/){return undef;}
	if ($mailadr =~ /^-/){return undef;}
	if ($mailadr =~ /\)/){return undef;}
	if ($mailadr =~ /\(/){return undef;}
	if ($mailadr =~ /\"/){return undef;}
	if ($mailadr =~ /\'/){return undef;}
	if ($mailadr =~ /\;/){return undef;}
	if ($mailadr =~ /\|/){return undef;}
	if ($mailadr =~ /&/){return undef;}
	if ($mailadr =~ /\\/){return undef;}
	
	
	if ($mailadr =~ /$mail_regex/ ){
		return 1;
	}else{
		return undef;
	}
}

# 不正アクセス防止
sub limit_access{
	my $filename = shift;
	my @url = split(/,/, $filename);
	my $ng = 1;
	my $ng_url;
	
	# 管理情報取得
	my $objAcData = new clsAcData($SYS->{data_dir});
	my $admindata = $objAcData->GetAdminData();
	
	foreach my $n (@url) {
		my $ref_url = $admindata->{homeurl}.$n if $n;
		$ref_url =~ s/^http(.+)/http\(s\)\?$1/;
		
		if ($ref_url) {
			
			if (!$ENV{'HTTP_REFERER'} || $ENV{'HTTP_REFERER'} !~ /^$ref_url/) {
				$ng_url = $ref_url;
			} elsif ($ENV{'HTTP_REFERER'} =~ /^$ref_url/) {
				$ng = 0;
				return 1;
			}
		}
	}
	
	
	if ($ng) { &error("不正なアクセスです。<br>$ng_url"); }
}

# HTML特殊文字エスケープ＆改行を<br>に変換
sub plantext2html{
	my $text = shift;
	my $type = shift;
	
	#type一覧
	#onlybr = \nを<BR>に変換のみ
	#nobr = \nを<BR>に変換しない
	#それ以外 = HTMLタグをエンティティー化
	
	if($type eq "onlybr"){
		$text =~ s/\n/<br>/g;
		return $text;
	}

	$text =~ s/&/&amp;/g;
	$text =~ s/</&lt;/g;
	$text =~ s/>/&gt;/g;
	$text =~ s/\"/&quot;/g;

	if($type ne "nobr"){
		$text =~ s/\n/<br>/g;
	}

	return $text;
}
# plantext2htmlの逆
sub html2plantext{
	my $text = shift;
	my $br = shift;
	if ($text){
		$text =~ s/&amp;/&/g;
		$text =~ s/&lt;/</g;
		$text =~ s/&gt;/>/g;
		$text =~ s/&quot;/\"/g;
		$text =~ s/<br>/\n/g unless $br;
	}
	return $text;
}

#コンマを付加
sub comma{

	my $d = shift;
	my $opt = shift;
	
	if(!$d){$d=0;}
	
	if($d !~ /^[0-9]+$/){ return $d; }
	
	$d=~s/\G((?:^-)?\d{1,3})(?=(?:\d\d\d)+(?!\d))/$1,/g;
	if(!$opt){
		return $d."円";
	}
	if($opt eq "not"){
		return $d;
	}
	if($opt eq "zeronull"){
		if($d){
			return $d."円";
		}else{
			return "&nbsp;";
		}
	}
	# return "\\".$d;
}

sub Countup {
	my $fn = './upload/count';
	if (! -e $fn) {
		`touch $fn`;
		`chmod 777 $fn`;
	}
	open COUNT,"+<$fn" or &error("カウンタファイルが開けません。$fn $!");
	flock COUNT, 2;
	my $count = <COUNT>;
	seek COUNT, 0, 0;
	$count++;
	print COUNT $count;
	flock COUNT, 8;
	close COUNT;
	$count;
}


# 画像アップロード
sub UploadFile($) {
	my $p_filename = shift;
	my $filename = $$p_filename;
	my $create_name = "";
	my $checktype = ',.jpg,.jpeg,.gif,.png';
	my $ostype;
	
	#OSの自動認識
	if(!$ostype){
		if($ENV{HTTP_USER_AGENT} =~ /Win/){
			$ostype = "MSWin32";
		}elsif($ENV{HTTP_USER_AGENT} =~ /Mac/){
			$ostype = "MacOS";
		}else{
			$ostype = "VMS";
		}
	}
	# $ostiypeにセット
	# グローバル変数の変更なので、この関数内で元に戻す
	my $old_fstype = fileparse_set_fstype($ostype);
	
	my @suffixlist;
	my $basename = basename($filename,@suffixlist);
	my $dirname = dirname($filename);
	
	my (@suffix, $num);
	#ファイル名から拡張子とそれ以外を取り出す。
	if($basename =~ /^(.*)(\.[a-zA-Z0-9]+)$/){
		$suffix[$num] = lc $2;
	}
	if(!$suffix[$num] || $basename =~ /\\\//){
		&error("ファイル名の取得に失敗しました。ファイル拡張子を設定するなどし再度アップしてください。");
	}
	
	my $ok = 0;
	my @type = split(/,/, $checktype);
	foreach my $n (@type) {
		if (!$n) { next; }
		if($suffix[$num] =~ /$n$/i){
			$ok = 2;
		} elsif ($ok != 2) {
			$ok = '';
		}
	}
	
	if ($suffix[$num] eq ".jpeg") {
		$suffix[$num] = ".jpg";
	}
	
	if (!$ok) {
		&error("ファイルタイプは「.jpg」「.jpeg」「.gif」「.png」をアップロードしてください。アップロードされたファイル→$suffix[$num]");
	}
	
	my $file;
	my $BUFFSIZE = 2048;
	my $buffer;
	my $file_size;
	my $bytesread;
	while ($bytesread = read($filename, $buffer, $BUFFSIZE)) {
		$file .= $buffer;
		$file_size += 2048;
	}
	
	if ($file_size > 100000) { &error("ファイルサイズが大きすぎます。アップロードするファイルの容量は100k以下にしてください。"); }
	
	# カウントアップ
	my $id = &Countup();
	my $id = sprintf("%03d", $id);
	
	$create_name = './upload/'.$id.$suffix[$num];
	
	# 書き込み処理	
	# 受信データを書き込む
	open OUT,"> $create_name" || &error("画像ファイルの書き込みに失敗しました。", '');
	binmode(OUT);
	print (OUT $file);
	#print OUT $in{'image_file'};
	close OUT;
	chmod (0666, $create_name);

	fileparse_set_fstype($old_fstype);

	return 1;
}

# アップロードされているファイル一覧取得
sub get_uploadimage() {
	opendir DATA, './upload/';
	my @files = readdir DATA;
	closedir DATA;
	@files = grep /^\d*\.(jpg|gif|jpeg|png)$/i, @files;
	@files = sort { $b cmp $a } @files;
	my @f;
	foreach my $n (@files) {
		my $row;
		$row->{file_name} = $n;
		push(@f, $row);
	}
	return @f;
}

# HTMLテンプレートオープン
sub newtemplate{
	my $templatedir = "";		# テンプレートのあるディレクトリ
	my $templatesuffix = '.tmpl';	# テンプレートファイルの拡張子
	my $fn_template = shift;
	# CGIとテンプレートとのファイル名の関連づけ
	if (!$fn_template){
 		my ($base,$path,$suffix) = fileparse($0);
		$base =~ s/\.cgi$//;
		$fn_template = $base.$templatesuffix;
	}
	
	my $template = HTML::Template->new(filename => $fn_template , die_on_bad_params => 0, path => [ './tmpl/']);

	return $template;
}

sub getmail{
	my $mail = shift;
	my $mail_regex = q{([\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)\@([\w|\!\#\$\%\'\(\)\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)};
	if($mail =~ /$mail_regex/o){
		$mail =~ s/($mail_regex)(.*)/$1/go;		# メールアドレスの最後以降を削除
		$mail =~ s/(.*)[^\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+($mail_regex)/$2/go;		# メールアドレスまでを削除
	}
	return $mail;
}

# テンプレートを使用しないエラー関数（システムエラー）
sub syserror {
	my $errortext=$_[0];
	
	print "Content-type: text/html; charset=UTF-8;\n\n";
	print "<html><head><title>SYSTEM ERROR</title></head>\n";
	print "<body>\n";
	print "SYSTEM ERROR<br><br>$errortext<br>";
	print "</body></html>\n";
	exit;

}

# テンプレートを使用したエラー関数
sub error{
	my $errordata = shift;
	
	# 管理情報取得
	my $objAcData = new clsAcData($SYS->{data_dir});
	my $admindata = $objAcData->GetAdminData();
	
	my $data_ref;
	foreach my $n (keys %$admindata) {
		$data_ref->{admindata}{$n} = $admindata->{$n};
	}
	&writing_check(\$data_ref);
	$data_ref->{ERRDATA} = $errordata;
	#$data_ref->{writing} = $admindata->{writing};
	$data_ref->{title} = $admindata->{title};
	$data_ref->{form}{sid} = $SYS->{sid};
	
	if(!-e $SYS->{tmpl_error_file}){
		&syserror("エラーテンプレートの設定が正しくありません");
	}
	
	# 共通変数読み込み
	&set_common_value(\$data_ref, $admindata);
	
	my $mobile = &isMobile();
	
	if ($mobile) {
		$SYS->{tmpl_error_file} = "tmpl/m_error.tmpl";
		&printhtml_tk($data_ref, $SYS->{tmpl_error_file}, 1, "Shift_JIS");
		exit;
	}
	
	# HTML表示
	&printhtml_tk($data_ref, $SYS->{tmpl_error_file}, 1);
	exit;
}

# 携帯端末かどうかの判別
sub isMobile() {
	
	#携帯振り分け
	my $mobile;
	if($ENV{'HTTP_USER_AGENT'} =~ /^(docomo\/1)/i){
		$mobile = 2;
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /^(L-mode)/i){
		$mobile = 1;
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /^(ASTEL)/i){
		$mobile = 1;
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /^J\-PHONE/i){
		$mobile = 4;
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /^Vodafone/i){
		$mobile = 4;
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /^SoftBank/i){
		$mobile = 4;
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /^MOT\-/i){
		$mobile = 1;
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /^(docomo\/2)/i){
		$mobile = 2;
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /^(KDDI)/i){
		$mobile = 3;
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /^up\.browser/i){
		$mobile = 1;
	}
	return $mobile;
}

# HTMLテンプレート出力
sub printhtml{
	my $template = shift;
	my $mozicode = shift;
	my $nocache = shift;
	if ($mozicode){
		if ($nocache) {
			print "Content-Type: Text/html;charset=EUC-JP\n";
			print "Pragma: no-cache\n";
			print "Cache-Control: no-cache\n";
			print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\n\n";
		} else {
			print "Content-Type: Text/html;charset=EUC-JP\n\n";
		}
		my $html_data = $template->output;
		#&jcode::convert(\$html_data, 'sjis', 'euc');
		
		print $html_data
	}else{
		print "Content-Type: Text/html;charset=EUC-JP\n\n";
		print $template->output;
	}
}

sub printhtml_sjis{
	my $template = shift;
	
	print "Content-Type: Text/html;charset=Shift_JIS\n\n";
	my $html_data = $template->output;
	&jcode::convert(\$html_data, 'sjis', 'euc');
	print $html_data
}


# 時間取得
sub getdatetime{
	my %TIME;
	my $time = shift;
	my $nn = shift;
	if(!$time){
		$time = time;
	}
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time);
	my $year4;
	my $year2;
	$mon++;
	$year4 = $year + 1900;
	$year2 = $year - 100;
	if(!$nn){
		$sec = "0$sec" if $sec < 10;
		$min = "0$min" if $min < 10;
		$hour = "0$hour" if $hour < 10;
		$mday = "0$mday" if $mday < 10;
		$mon = "0$mon" if $mon < 10;
		$year2 = "0$year2" if $year2 < 10;
	}
	
	my $week =  ("Sun","Mon","Tue","Wed","Thu","Fri","Sat")[$wday];
	my $week_jp = ("日", "月", "火", "水", "木", "金", "土")[$wday];
	$TIME{year}		= $year4;
	$TIME{year2}	= $year2;
	$TIME{mon}		= $mon;
	$TIME{mday}		= $mday;
	$TIME{week}		= $week;
	$TIME{'week-jp'}  = $week_jp;
	$TIME{hour}		= $hour;
	$TIME{min}		= $min;
	$TIME{sec}		= $sec;
	$TIME{time}		= $time;
	
	$TIME{monint} = int($TIME{mon});
	$TIME{mdayint} = int($TIME{mday});
	$TIME{hourint} = int($TIME{hour});
	$TIME{minint} = int($TIME{min});
	$TIME{secint} = int($TIME{sec});
	
	$TIME{nowdate}	= "$year4/$mon/$mday($week) $hour:$min:$sec";
	return %TIME;
}

# セッションID暗号化
sub encrypt_id {
	my $id = shift;
	my @id;
	my $newid;
	my $x = substr($id , -1);
	my $x2;
	my @ids;
	if($x == 0){$x2 = 10;}
	else{$x2=$x;}
	$id = ($id +1) * 97 * ($x2);
	@ids = $id =~ /[\x00-\x7F]/og;
	for(reverse @ids){
		$newid = $newid.$_;
	}
	$newid = $newid.$x;
	return $newid;
}

# セッションID復元化
sub decrypt_id {
	my $str = shift;
	my $newstr;
	my @strs;
	my $x = substr($str , -1 ,1,"");
	my $x2;
	if($x == 0){$x = 10;}
	else{$x2=$x;}
	@strs = $str =~ /[\x00-\x7F]/og;
	for(reverse @strs){
		$newstr = $newstr.$_;
	}
	$newstr = ($newstr / (97 * $x)) -1;
	return $newstr;
}


# クッキーからデーターを取得
sub getcookie{
	my %COOKIE = ();
	my @cookie_pairs = split(/;/,$ENV{'HTTP_COOKIE'});

	if ($ENV{'HTTP_COOKIE'}){
		foreach (@cookie_pairs){
			$_ =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
			my ($name, $value) = split(/=/, $_);
			$name =~ s/ //g;
			$value =~ s/ //g;
			$COOKIE{$name}=$value;
		}
	}else{
		return undef;
	}
	return %COOKIE;
}
# セッションからデータを取得
# 入力：クッキーからの暗号化されているセッションID
# 出力：連想配列
sub getsession{
	my $sid = shift;
	my $sid_form = shift;
	my %S;
	my $fn_session;
	my $sdata;
	my @s;
	
	$SYS->{sid} = $sid;
	
	if ($sid_form) { $sid = $sid_form; }
	
	if (!$sid) { return %S; }
	
	$sid = decrypt_id($sid);
	$fn_session = $SYS->{dir_session}.".".$sid.".cgi";
	open (IN,"$fn_session") || return undef;
	while(<IN>){
		$sdata .= $_;
	}
	close (IN);

	&jcode::convert(\$sdata, "euc");
	@s = split(/;/,$sdata);

	foreach (@s){
		my ($l,$r) = split(/=/,$_);
		if($l){
			$S{$l} = $r;
		}
	}
	return %S;
}
sub setsession{
	my $sid = shift;
	my %S = @_;
	my $sdata;	foreach (keys %S){
		$sdata .= "$_=$S{$_};";
	}

	$sid = decrypt_id($sid);
	my $fn_session = $SYS->{dir_session}.".".$sid.".cgi";

#	&error("$sid<hr>");
	# セッション保存
	if(!-e $fn_session){
		# 新規の場合
		open (F,"> $fn_session") or &error($fn_session);
		print(F $sdata);
		close(F);
		chmod (0666,"$fn_session");
	}else{
		# 上書きの場合
		open(F, "+< $fn_session") or &error($fn_session);
		flock(F, 2);
		truncate(F, 0);
		seek(F, 0, 0);
		print(F $sdata);
		close(F);
	}
}


# ログインチェック
sub logincheck {
	my($login_id,$login_pass, $admindata)=@_;
	# 入力チェック
	if(!$login_id || !$login_pass){
		print "Location: login.cgi \n\n";
		exit;
		#&error("認証に失敗しました。お手数ですが再びログインし直してください。<br><br><a href=\"login.cgi\">ログイン画面</a>");
	}
	my $LOGIN;
	if($admindata->{login_id} eq $login_id && $admindata->{login_pass} eq $login_pass){ 
		$LOGIN->{login_id} = $login_id;
		$LOGIN->{login_pass} = $login_pass;
		return $LOGIN;
	}else{
		# 認証失敗
		print "Location: login.cgi \n\n";
		exit;
		#&error("認証に失敗しました。お手数ですが再びログインし直してください。<br><br><a href=\"login.cgi\">ログイン画面</a>");
	}
}

# Shift_JIS用全角対応substr
sub z_substr {
	my ($s,$p,$l,$o,$opt) = @_;
	
	if ($opt ne "noconv") {
		&jcode::convert(\$s, "sjis","euc");
	}
	$s =~ s/(.)/$1\0/g;
	$s =~ s/([\x81-\x9f\xe0-\xfc])\0(.)\0/$1$2\0\0/g;
	$s = $l eq '' ? substr($s,$p*2):substr($s,$p*2,$l*2);
	if ($o) { $s =~ s/^\0\0/ /; $s =~ s/.[^\0]$/ /;}
	$s =~ tr/\0//d;
	
	if ($opt ne "noconv") {
		&jcode::convert(\$s, "euc","sjis");
	}
	
	
	##
	#Encode::from_to($s, "cp932","utf8");
	return $s;
}

sub urlencode{
	my $str = shift;
	$str=~s/([^0-9A-Za-z_ ])/'%'.unpack('H2',$1)/ge;
	$str=~s/\s/+/g;
	return $str;
}



# 機種依存文字の有無確認
# 有→1、無→0　を返す
sub depend_kisyu{
	my $name = shift;
	
	if($name){
		# 機種依存文字発見のためにsjisに変換
		&jcode::convert(\$name, "sjis","euc");
		#Encode::from_to($name, "euc-jp","cp932");
		&jcode::h2z_sjis(\$name);
		if (&get_windows_char( \$name )) {
			return 1;
		}
	}
}
sub get_windows_char() {
	my ($str)=@_;
	my ($ascii, $sjis_twoBytes, $sjis_pattern);
	&init_windows_char($ascii, $sjis_twoBytes, $sjis_pattern);	# 1回目のみテーブルを初期化
	my $errorstr;
	
#	my $i = 0;
#	while (my $buf = z_substr($$str, $i, 1000, "", "noconv")) {
#		$errorstr .= join '', $buf =~ m/\G(?:$ascii|$sjis_twoBytes)*?((?:$sjis_pattern)+)/og;
#		
#		if ($i >= 3000) {
#		print "Content-type: text/html; charset=Shift_JIS\n\n";
#		my $buf = z_substr($$str, 4604, 1000, "", "noconv");
#		print $buf;
#		exit;
#			print $buf."<br /><br />$i<br /><br />";
#		}
#$i += 1000;
#		if ($i > 1000000) { error("調査する文字数が大きすぎます。"); }
#	}
	$errorstr .= join '', $$str =~ m/\G(?:$ascii|$sjis_twoBytes)*?((?:$sjis_pattern)+)/og;
	
	return $errorstr;
}
sub htmlheader{	
	my $objAcData = new clsAcData($SYS->{data_dir});
	my $admindata = $objAcData->GetAdminData();
	my $data;
	foreach my $n (keys %$admindata) {
		$data->{admindata}{$n} = $admindata->{$n};
	}

	
	&writing_check(\$data);
	my $write = '<a href="http://www.ahref.org"><img src="img/ahref_2.jpg" alt="メルマガ配信CGI acmailer" /></a>';
	if ($data->{writing}) { $write = ""; }


my $tb_bgcolor="#ffffff";
if($_[0]){$tb_bgcolor=$_[0];}
	
print <<EOF;
Content-Type: text/html; charset=EUC-JP

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP" />
<title>メール送信</title>
<link rel="stylesheet" href="./css/common.css" type="text/css">
<link rel="stylesheet" href="./css/default.css" type="text/css">
<link rel="stylesheet" href="./css/login_etc.css" type="text/css">
<SCRIPT language="JavaScript">
<!--
var set=0;
function nidoosi() {
	if(set==0){
		set=1;
	}else{
		alert("二度押しはいけません。\\nしばらくそのままお待ちください。");
		return false
	}
}
function delcheck() {
	f = confirm("削除してよろしいですか？");
	return f
}


//-->
</SCRIPT>
</head>
<body>
<div id="containt_panel_wrapper">
	<div id="containt_panel">
    	<div id="panel_head" class="clearfix">
        	<div id="panel_head_left"><a href="http://www.acmailer.jp"><img src="img/logo.jpg" alt="メルマガ配信CGI acmailer" /></a></div>
            <div id="panel_head_right">$write</div>
        </div>
	
	
	

<div align="center"id ="title"><h3>送信中</h3>
EOF
}

# ////////////////////////////////////////////////////////////////////////// #
sub htmlfooter(){

# ///////////////////////////////////////////////////////////////// #
# 【重要】著作権表示について
# 
# AHREF フリーCGIではご使用にあたり著作権表示をお願いしております。
# 著作権表示をはずすにはこちらをご覧ください。
# ■著作権非表示について
# http://www.ahref.org/cgityosaku.html
# ///////////////////////////////////////////////////////////////// #
	my $objAcData = new clsAcData($SYS->{data_dir});
	my $data;
	my $admindata = $objAcData->GetAdminData();
	foreach my $n (keys %$admindata) {
		$data->{admindata}{$n} = $admindata->{$n};
	}
	
	&writing_check(\$data);
	my $write = '<div align="center">
<!-- ■■■■■■著作権について（重要！）■■■■■■ -->
<!-- 本システムは、AHREF(エーエイチレフ)に無断で下記著作権表示を削除・改変・非表示にすることは禁止しております -->
<!-- 著作権非表示に関しては、こちらをご確認下さい。 -->
<!-- http://www.ahref.org/cgityosaku.html -->
<!-- ■■■■■■■■■■■■■■■■■■■■■■■■ -->
    <font size="-2" color=#999999>Copyright&copy; 2000-2010 <a href="http://www.ahref.org/" title="WEBアプリケーションフリーCGI配布ahref" target="_blank">ahref</a> All Rights Reserved.
</font>
</div>';
	if ($data->{writing}) { $write = ""; }
	
print <<EOF;

<br><br>
$write
</body>
</html>
EOF
}


sub init_windows_char {
	
	my $ascii = $_[0];
	my $sjis_twoBytes = $_[1];
	my $sjis_pattern = $_[2];
	
	my %conv_table;
	my %conv_data = (
		
		0x8740=>		# 13区
		'(1) (2) (3) (4) (5) (6) (7) (8) (9)
		(10) (11) (12) (13) (14) (15) (16)
		(17) (18) (19) (20) I II III IV
		V VI VII VIII IX X . ミリ
		キロ センチ メートル グラム トン アール ヘクタール リットル
		ワット カロリー ドル セント パーセント ミリバール ページ mm
		cm km mg kg cc m^2 〓 〓 〓 〓 〓 〓 〓 〓 平成',
		
		0x8780=>		# 13区
		'" ,, No. K.K. Tel (上) (中) (下) (左)
		(右) (株) (有) (代) 明治 大正 昭和
		≒ ≡ ∫ ∫ Σ √ ⊥
		∠ Ｌ △ ∵ ∩ ∪',
		
		0xEEEF=>		# 92区
		q{i ii iii iv v vi vii viii ix x ¬ | ' ''},
		
		0xFA40=>		# 115区
		q{i ii iii iv v vi vii viii ix x
		I II III IV V VI VII VIII IX X ¬ | ' ''
		(株) No. Tel ∵ },
	);
	foreach (keys %conv_data){
		my $base_code = $_;
		&jcode::convert(\$base_code, "sjis", "euc");
		my @chars = split(/\s+/,$conv_data{$_});
		foreach (@chars){		# ↓ tr/\0//d は１バイトの半角カナ用
			my $char_code;
			($char_code = pack('C*',$base_code/256,$base_code%256)) =~ tr/\0//d;
			my $text = $_;
			&jcode::convert(\$text, "sjis", "euc");
			$conv_table{$char_code} = $text;
			$base_code++;
		}
	}
	$ascii = '[\x00-\x7F]';
	$sjis_twoBytes = '[\x81-\x9F\xE0-\xFC][\x40-\x7E\x80-\xFC]';
	# ↓半角カナと13区(\x87),89-92区(\xED\xEE),115-119区(\xFA-\xFC)
	$sjis_pattern='[\xA0-\xDF]|[\x87\xED\xEE\xFA-\xFC][\x40-\x7E\x80-\xFC]';
	&jcode::convert(\$ascii, "sjis", "euc");
	&jcode::convert(\$sjis_twoBytes, "sjis", "euc");
	&jcode::convert(\$sjis_pattern, "sjis", "euc");
	
	
	$_[0] = $ascii;
	$_[1] = $sjis_twoBytes;
	$_[2] = $sjis_pattern;
	return %conv_table;
}

sub writing_check {
	my $SYS = shift;
	my $license = &getlicense();
	
	my $initial;
	if ($license->{license2} =~ /^SAA([0-9]?)$/) {
		$initial = $1;
	}
	
	my $flg = &checkDigit($initial.$license->{license3}.$license->{license4});
	if (!$flg) { return 0; }
	
	if ($license->{license1} eq "ACML" && $license->{license2} eq "SAA1") {
		$$SYS->{license_kind} = 'エコノミーライセンス';
		$$SYS->{license_ok} = 1;
		if ($$SYS->{admindata}{writing_hide}) {
			$$SYS->{writing} = 1;
			return 1;
		} else {
			return 0;
		}
	} elsif ($license->{license1} eq "ACML" && $license->{license2} eq "SAA2") {
		$$SYS->{license_kind} = '商用ライセンス';
		$$SYS->{license_ok} = 1;
		
		if ($$SYS->{admindata}{writing_hide}) {
			$$SYS->{writing} = 1;
			return 1;
		} else {
			return 0;
		}
		return 1;
	}
	
	return 0;
}

sub RC4_dec_hex {
	my($pass, $enchex) = @_;

	my(@encbin) = ();
	while (length($enchex) > 0) {
		push(@encbin, pack("h2", $enchex));
		$enchex = substr($enchex, 2);
	}
	my($dec) = RC4($pass, join('', @encbin));
	return $dec;
}



sub kisyuizon_check {
	my ($str)= shift;
	&jcode::convert(\$str, "sjis", "euc", "z");
	&jcode::h2z_sjis(\$str);
	
	my $errorstr = &get_windows_char(\$str);
	&jcode::convert(\$errorstr, "euc", "sjis");
	if ($errorstr) {
		$errorstr = "旧字もしくは機種依存文字が含まれていますので送信できません。<br><br>検出文字列：".$errorstr;
		&error($errorstr);
		exit;
	}
}

sub conv_windows_char {
	my ($str)=@_;
	my ($ascii, $sjis_twoBytes, $sjis_pattern);
	my %conv_table = &init_windows_char($ascii, $sjis_twoBytes, $sjis_pattern);	# 1回目のみテーブルを初期化
	$$str =~ s/\G((?:$ascii|$sjis_twoBytes)*?)($sjis_pattern)/$1.($conv_table{$2}||'〓')/oeg;
	my $found_flg = 0;
	$found_flg = $$str =~ s%\G((?:$ascii|$sjis_twoBytes)*?)($sjis_pattern)%"$1<FONT COLOR=\"red\">".($conv_table{$2}||'〓')."</FONT>"%oeg;
	$found_flg;
}


sub getlicense() {
	my $data;
	my $count = 1;
	open (IN,"./data/enc.cgi");
	while(<IN>){
		$_ =~ s/\r\n|\r|\n//gi;
		$data->{"license".$count} = $_;
		$count++;
	}
	close (IN);
	return $data;
}


# 全画面必要変数
sub set_common_value() {
	my $data_ref = shift;
	my $addata = shift;
	
	# 管理者データ
	#my $objAcData = new clsAcData($SYS->{data_dir});
	#my $addata = $objAcData->GetAdminData();
	foreach my $v (keys %$addata) {
		$$data_ref->{admindata}{$v} = $addata->{$v};
	}
	
	# システム変数
	foreach my $v (keys %$SYS) {
		$$data_ref->{sys}{$v} = $SYS->{$v};
	}
	
	&writing_check(\$$data_ref);
	
	return 1;
}

# toolkit用
sub printhtml_tk {
	
	my $data_ref = shift;
	my $fn_template = shift;
	my $nocache = shift;
	my $encode_type = shift;
	my $templatedir = "tmpl/";		# テンプレートのあるディレクトリ
	my $templatesuffix = '.tmpl';	# テンプレートファイルの拡張子
	
	# デフォルトエンコード
 	if (!$encode_type) { $encode_type = "EUC-JP"; }
	my $mobile = &isMobile();
	$data_ref->{sys}{encode_type} = $encode_type;
	$data_ref->{sys}{input_type} = &makeInputType($mobile);
	if ($nocache || $data_ref->{form}{sid} || $mobile) {
		if($mobile == 2){
			# DOCOMOの場合
			print "Content-Type:application/xhtml+xml; charset=$encode_type\n";
		}else{
			print "Content-Type: Text/html;charset=$encode_type\n";
		}
		print "Pragma: no-cache\n";
		print "Cache-Control: no-cache\n";
		print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\n\n";
	} else {
		print "Content-Type: Text/html;charset=$encode_type\n\n";
	}
	# CGIとテンプレートとのファイル名の関連づけ
	my ($base,$path,$suffix) = fileparse($0);
	$data_ref->{sys}{scriptname} = $base;
	if (!$fn_template){
		$base =~ s/\.cgi$//;
		if ($data_ref->{form}{sid}) { $base = "m_".$base; }
		$fn_template = $templatedir.$base.$templatesuffix;
	} else {
		
	}

	my $htmldata;
	my $template = Template->new;
	$template->process($fn_template, $data_ref, \$htmldata);
	if ($encode_type ne "EUC-JP") {
		my $enc = "sjis";
		# 現状はSJISのみ
		if ($encode_type =~ /shift_jis|sjis/) { $enc = "sjis"; }
		&jcode::convert(\$htmldata, $enc, "euc");
	}
	print $htmldata;
}

sub makeInputType() {
	my $type = shift;
	my $str = "";
	if($type == 2){
		$str = 'istyle="3" style="-wap-input-format:&quot;*&lt;ja:en&gt;&quot;;"';
	}elsif($type == 3){
		$str = 'format="*m" style="-wap-input-format:*m;"';
	}elsif($type == 4){
		$str = 'mode="alphabet"';
	}elsif($type == 1){
		$str = 'istyle="3" mode="alphabet" format="*m"';
	}else{
		$str = 'istyle="3" mode="alphabet" format="*m"';
	}
	return $str;
}

# メール送信する際の最低限の管理設定チェック
sub CheckAdminData_MailSend() {
	my $admindata = shift;
	if(!$admindata->{admin_name}){
		&error("メール差出人名を設定してください。<a href=\"admin_edit.cgi\">→設定</a>");
	}
	if(!$admindata->{admin_email}){
		&error("メール差出人メールアドレスを設定してください。<a href=\"admin_edit.cgi\">→設定</a>");
	}
	if(!CheckMailAddress($admindata->{admin_email})){
		&error("メール差出人メールアドレスが正しくありません。<a href=\"admin_edit.cgi\">→設定</a>");
	}

	if(!-x $admindata->{sendmail_path} && $admindata->{sendmail_path}){
		&error("sendmailのパスが正しくありません。こちらより<a href=\"admin_edit.cgi\">設定</a>してください。");
	}
	return 1;
}

# 予約配信用の日時作成
sub MakeYMDSelect() {
	my $data_ref = shift;
	my %TIME = &getdatetime();
	my @year;
	for($TIME{year}..($TIME{year} + 1)) {
		my $data;
		if ($_ == $TIME{year}) { $data->{selected} = " selected "; }
		$data->{value} = $_;
		push(@year, $data);
	}
	$$data_ref->{send_year} = \@year;
	my @mon;
	for(1..12) {
		my $data;
		if ($_ == $TIME{mon}) { $data->{selected} = " selected "; }
		$data->{value} = $_;
		push(@mon, $data);
	}
	$$data_ref->{send_mon} = \@mon;
	my @day;
	for(1..31) {
		my $data;
		if ($_ == $TIME{mday}) { $data->{selected} = " selected "; }
		$data->{value} = $_;
		push(@day, $data);
	}
	$$data_ref->{send_day} = \@day;
	my @hour;
	for(0..23) {
		my $data;
		if ($_ == $TIME{hour}) { $data->{selected} = " selected "; }
		$data->{value} = $_;
		push(@hour, $data);
	}
	$$data_ref->{send_hour} = \@hour;
	my @min;
	for(qw(0 15 30 45)) {
		my $data;
		if ($_ == $TIME{min}) { $data->{selected} = " selected "; }
		$data->{value} = $_;
		push(@min, $data);
	}
	$$data_ref->{send_min} = \@min;
	
	return 1;
}

# 重複データチェック
sub CheckDoubleData() {
	my $p_DATA = shift;
	my $admindata = shift;
	my @DATA = @$p_DATA;
	my (%ZYU, $zyunum, $errornum, $i);
	
	foreach my $row (@DATA){
		$row->{i} = $i+1;
		#重複カウント
		if($ZYU{$row->{email}}){
			$zyunum++;
			# 管理画面で設定されている場合
			if (!$admindata->{double_reg}) {
				&error("メール配信を行うには、メールアドレス一覧の重複を取り除いてください。<a href=\"email_list.cgi\">（→確認）</a><br><br><a href=\"email_zyudel_ctl.cgi\" onclick=\"return confirm('重複メールアドレスを一括削除しますか？')\">今すぐ一括削除する</a>");
			}
		}else{
			#エラーカウント
			if(!CheckMailAddress($row->{email})){
				$errornum++;
				&error("メール配信を行うには、メールアドレスエラーを取り除いてください。<a href=\"email_list.cgi\">（→確認）</a><br><br><a href=\"email_errordel_ctl.cgi\" onclick=\"return confirm('エラーメールアドレスを一括削除しますか？（重複メールアドレス分のエラーメールも削除されます）')\">今すぐ一括削除する</a>");
			}else{
				#$row->{status} = "◎ (正常)";
			}
		}
		$ZYU{$row->{email}}++;
	}
}

# 表示用に絵文字タグを埋め込む
sub ReplaceEmojiDisp() {
	my $str = shift;
	# 絵文字
	my $emoji = &mobilemailimg("99");
	foreach my $n (keys %$emoji) {
		if ($n) {
			my $image = "<img src=i/$emoji->{$n}>";
			$str =~ s/\{$n\}/$image/g;
		}
	}
	return $str;
}

# 表示用に画像タグを埋め込む
sub ReplaceImageDisp() {
	my $str = shift;
	my @f = &get_uploadimage();
	foreach my $ref (@f) {
		my $n = $ref->{file_name};
		my $image = "<img src=\"upload/$n\">";
		$str =~ s/\{img_$n\}/$image/g;
	}
	return $str;
}

# 正規表現用
sub MakeRegularString() {
	my $str = shift;
	$str =~ s/\\/\\\\/g;
	$str =~ s/\*/\\\*/g;
	$str =~ s/\./\\\./g;
	$str =~ s/\?/\\\?/g;
	$str =~ s/\-/\\\-/g;
	$str =~ s/\+/\\\+/g;
	$str =~ s/\$/\\\$/g;
	$str =~ s/\|/\\\|/g;
	$str =~ s/\//\\\//g;
	$str =~ s/\{/\\\{/g;
	$str =~ s/\}/\\\}/g;
	$str =~ s/\(/\\\(/g;
	$str =~ s/\)/\\\)/g;
	$str =~ s/\[/\\\[/g;
	$str =~ s/\]/\\\]/g;
	return $str;
}

# CSVファイルダウンロード
# 引　数：データ配列　カラム名配列　ファイル名　区切り文字
sub DownloadCSV() {
	my $pdata = shift;
	my $pcol = shift;
	my $filename = shift;
	my $sep = shift;
	
	my @DATA = @$pdata;
	my @COL = @$pcol;
	if (!$filename) { $filename = 'data'; }
	if (!$sep) { $sep = ','; }
	
	my $printdata = "";
	foreach my $row (@DATA) {
		foreach my $n (@COL) {
			$printdata .= $row->{$n}.$sep;
		}
		$printdata .= "\n";
	}
	
	my $size = length $printdata;
	print "Content-Type: application/octet-stream\n"; 
	print "Content-Disposition: attachment; filename=$filename.csv\n"; 
	print "Content-Length: $size\n\n"; 
	
	Jcode::convert(\$printdata, 'sjis', 'euc');
	print $printdata;
	exit;
	
}

# チェックボックスの値に変更
sub ChangeCheckboxValue() {
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	%FORM = &GetCheckboxValue(\%FORM);
	return %FORM;
}

# チェックボックスの値を取得
sub GetCheckboxValue() {
	my $p_FORM = shift;
	my %FORM = %$p_FORM;

	# チェックボックス処理するリスト
	my @checkbox_list = split(/,/, $FORM{checkbox_list});
	my %FORM2;
	foreach my $n (keys %FORM) {
		foreach my $list (@checkbox_list) {
			
			if ($list eq $n) {
				if ($n eq "") { next; }
				foreach my $item (@{$FORM{"array_".$n}}) {
					$FORM2{$n} .= ";".$item;
				}
			}
		}
	}
	
	foreach my $n (keys %FORM2) {
		# 最初のカンマを除く
		if ($FORM2{$n} =~ /^;(.*)$/) {
			$FORM{$n} = $1;
		}
	}
	
	return %FORM;
}

# 送信元名の編集
sub SetFromName() {
	my $email = shift;
	my $name = shift;
	# 名前で使用できない文字を省く (<,>)
	$name =~ s/\<//g;
	$name =~ s/\>//g;
	# ダブルクォートとシングルクォートがあった場合はエスケープ
	$name =~ s/\'/\\\'/g;
	$name =~ s/\"/\\\"/g;
	#$name =~ s/\\/\\\\/g;
	#$name =~ s/\[/\\\[/g;
	#$name =~ s/\]/\\\]/g;
	# ダブルクォートで囲む
	#my $str = '"'.$name.'"<'.$email.'>';
	
	my $str;
	
	if (&CheckMailAddress($name)) {
		# 送信元名がメールアドレスだった場合はダブルクォートを付け加える
		# replaytoやreturnpathでメールアドレスの抽出に失敗するため
		$str = '"'.$name.'"<'.$email.'>';
	} else {
		$str = ''.$name.'<'.$email.'>';
	}
	
	return $str;
}

sub checkDigit() {
	my $str = shift;
	my $even = 0;
	my $odd = 0;
	my $checkdigit = 0;
	
	if (length($str) != 9) { return 0; }
	
	my $dstr = substr($str, 8, 1);
	$str = substr($str, 0, 8);
	
	for (1..length($str)) {
		my $row = $_;
		if ($row%2) {
			# 偶数の場合
			$even += substr($str, ($row - 1), 1);
		} else {
			# 偶数の場合
			$odd += substr($str, ($row - 1) ,1);
		}
	}

	# 偶数の３倍と奇数の値
	$checkdigit = ($even * 3) + $odd;
	# ひとけたの数値にする
	$checkdigit = substr($checkdigit, length($checkdigit) - 1, 1);
	# 0以外は10から引く
	if ($checkdigit > 0) { $checkdigit = 10 - $checkdigit; }
# 	print "Content-type: text/html; charset=EUC-JP\n\n";
# 	print $checkdigit.":".$dstr.":".$str;
# 	exit;
	if ($checkdigit eq $dstr) {
		return 1;
	} else {
		return 0;
	}
}

# 日付計算
# 加算する単位は秒
sub calcuDateTime {
	my $year = shift;
	my $mon = shift;
	my $mday = shift;
	my $hour = shift;
	my $min = shift;
	my $sec = shift;
	my $plus = shift;
	
	# 時分秒に関しては省略可能
	$hour = $hour ? $hour : 0;
	$min = $min ? $min : 0;
	$sec = $sec ? $sec : 0;

	my $time = timelocal($sec, $min, $hour, $mday, $mon - 1, $year);

	($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($time + ($plus));
	$year = sprintf("%04d", $year + 1900);
	$mon = sprintf("%02d", $mon + 1);
	$mday = sprintf("%02d", $mday);
	
	return ($year, $mon, $mday, $hour, $min, $sec);
}

# 日付が存在しているかどうかチェック
sub day_exists {
    my($year, $month, $day) = @_;
    my(@mlast) = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);

    if ($month < 1 || 12 < $month) { return 0; }

    if ($month == 2) {
	if ( (($year % 4 == 0) && ($year % 100 != 0)) || ($year % 400 == 0) ) {
	    $mlast[1]++;
	}
    }

    if ($day < 1 || $mlast[$month-1] < $day) { return 0; }

    return 1;
}

# セッション用サニタイズ
sub sessionStrEncode() {
	my $str = shift;
	$str =~ s/;/__<<semicolon>>__/gi;
	$str =~ s/=/__<<equal>>__/gi;
	$str =~ s/\t//gi;
	return $str;
}

# セッション用サニタイズ復元
sub sessionStrDecode() {
	my $str = shift;
	$str =~ s/__<<semicolon>>__/;/gi;
	$str =~ s/__<<equal>>__/=/gi;
	return $str;
}


# clsMailの生成
sub create_clsMail {
    my $admindata = shift;

    return
        clsMail->new(
            $admindata->{relay_use},
            $admindata->{relay_host},
            $admindata->{relay_port},
            $admindata->{relay_user},
            $admindata->{relay_pass},
            $admindata->{relay_send_mode},
            $admindata->{qmail},
            $admindata->{fail_send_local},
            $admindata->{sendmail_i_option}
        );
}

1;
