<!DOCTYPE html>
<html>
	<head>
		<title>渋家 || SHIBUHOUSE</title>
		<!-- typesqure 用タグ -->
		<script type="text/javascript" src="//typesquare.com/accessor/script/typesquare.js?E2mGUC7TkZ8%3D" charset="utf-8"></script>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
		<link href='./css/reset.css' rel='stylesheet' type='text/css'>	
		<!-- スライドショー -->
		<link href='./css/flexslider.css' rel='stylesheet' type='text/css'>
		<link href="css/lightbox.css" rel="stylesheet" />
		<script type="text/javascript" src="js/modernizr.js"></script>
		<script type="text/javascript">
		if (navigator.userAgent.indexOf('iPhone') != -1) {
			document.write("<link href='./css/iphone.css' rel='stylesheet' type='text/css'>");
		} else {
			document.write("<link href='./css/global.css' rel='stylesheet' type='text/css'>");
		}
		</script>
	</head>
	<body>
		<div id="wrap">
			<?php require './header.php' ?>
						<div id="slide">
				<div class="flexslider">
					<ul class="slides">
						<li><img src="./img/topimage/top_01.jpg"></li>
						<li><img src="./img/topimage/top_02.jpg"></li>
					</ul>
				</div>
			</div><!-- #slide -->
			<!--<div id="text_information">
				渋家新メンバー！　池田愛恵里さんです -> Official Web <a href="http://ameblo.jp/ikeda-aeri/">池田愛恵里オフィシャルブログ「ようこそ池田農園へ。」 powered by Ameba</a>
			</div>-->
			<div id="hot_topics">
				<div id="hot_topics_pic">
					<img src="./img/search.png"><img id="hot_topics_midashi" src="./img/hot_topics.png">
				</div><!-- hot_topics_pic -->
				<div id="hot_topics_text">
					<ul>
						<li class="topics"><sep class="topics_date">2013/11/29</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">[NEWS]  <a href="https://www.facebook.com/events/702796986406881/?ref_dashboard_filter=upcoming" target="_blank">11/29（金）「渋家」代表交代 6代目代表に齋藤桂太が就任</sep></li>
						<li class="topics"><sep class="topics_date">2013/11/29</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">[MEDIA] <a href="http://www.eater.co.jp/" target="_blank">11/29（金）記事掲載 『EATER 2014 REBIRTH』（地引雄一:編集）発売</a></sep></li>
						<li class="topics"><sep class="topics_date">2013/11/29</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">[MEDIA] <a href="http://www.nhk.or.jp/jirenma/" target="_blank">11/30（土）齋藤桂太 NHK Eテレ「ニッポンのジレンマ」出演</a></sep></li>
						<li class="topics"><sep class="topics_date">2013/11/29</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">[EVENT] <a href="http://yama.cs8.biz/" target="_blank">12/20（金）Maltine Records主催イベント「山」（WWW）参加</a></sep></li>
						<li class="topics"><sep class="topics_date">2013/11/29</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">[ART]   <a href="http://ca-mp.blogspot.jp/" target="_blank">12/21（土）CAMP主催イベント「現在のアート＜2013＞」（森美術館）出演</a></sep></li>
						<li class="topics"><sep class="topics_date">2013/11/29</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">[EVENT] 12/22（日）「渋家ゴールデンマキシマムファンタスティックエクストリームホームパーティー」（ニュージャパン）主催</sep></li>
						<li class="topics"><sep class="topics_date">2013/11/29</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">[ART]   <a href="http://www.mori.art.museum/contents/roppongix2013/" target="_blank">12/22（日）「六本木クロッシング2013展」関連イベント「ディスカーシブ・プラットホームとは？」（森美術館）出演</a></sep></li>
					</ul>
				</div><!-- hot_topics_text -->
			</div><!-- #hot_topics -->
			<div id="content">
				<div id="what" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img  style="margin-bottom:47px" src="./img/whats_shibuhouse.png">
					<div class="midashi_text">
						<?php require 'text/what.php' ?>
					</div>
					<a style="margin:0 auto; display: block;" href="./about.php" id="midashi_about"></a>
					<!--<img style="margin:0 auto; display: block;" src="./img/hatena_midashi.png">-->
					<img style="margin:0 auto; display: block;" src="./img/about_midahsi.png">
					</div><!-- .inner_midashi -->
				</div><!-- #what -->

				<div id="bio" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img style="margin-bottom:47px" src="./img/bio_midashi.png">
						<div class="midashi_text">
						<?php require './text/bio.php' ?>
						</div>
						<a href="./bio.php#ac_art" id="bio_art"></a>
						<a href="./bio.php#ac_media" id="bio_event"></a>
						<a href="./bio.php#ac_event" id="bio_media"></a>
						<img style="margin:0 auto; display: block;" src="./img/hovers/bio_midashi.png">
						<div style="clear:both;"></div>
						<!-- <img style="margin:0 auto; display: block;" src="./img/bio_images.png"> -->
					</div><!-- .inner_midashi -->
				</div><!-- #bio -->

				<div id="member" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img style="margin-bottom:47px" src="./img/member_midashi.png">
						<div class="midashi_text">
						<?php require './text/member.php' ?>
						</div>				

						<a href="./member.php" id="picture_member"></a>	
						<!--<img style="margin:0 auto 30px auto; display: block;" src="./img/midashi_smile.png">-->
						<img style="margin:0 auto; display: block;" src="./img/midashi_member.png">
					</div><!-- .inner_midashi -->
				</div><!-- member -->

				<div id="information" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img style="margin-bottom:47px" src="./img/information.png">
						<div class="midashi_text">
						<?php require './text/information.php' ?>	
						</div>					
						<img style="margin:0 auto 30px auto; display: block;" src="./img/midashi_mail.png">
						<p style="margin: 0 auto;
display: block;
width: 335px;
font-size: 40px;
font-family: monospace;">080-3310-4083</p>
						<p style="margin: 0 auto;
width: 435px;
font-size: 34px;
font-family: monospace;
display: block;">shibuhouseinfo@gmail.com</p>
						<!--<img style="margin:0 auto 16px auto; display: block;" src="./img/call_number.png">-->
						<!--<img style="margin:0 auto; display: block;" src="./img/mailadd.png">-->
					</div><!-- .inner_midashi -->
				</div><!-- #information -->
			</div><!-- #content -->
		</div><!-- #wrap -->
		<?php require './footer.php' ?>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
		<script defer src="js/jquery.flexslider.js"></script>
		<script type="text/javascript" src="js/scroll_top.js"></script>
		<script type="text/javascript">
		$(window).load(function() {
			$('.flexslider').flexslider({
				animation: "slide"
			});
		});
		</script>
	</body>
</html>
