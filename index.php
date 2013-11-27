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
						<li class="topics"><sep class="topics_date">2013/10/11</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">アイコンを作ってみました＝〜〜〜〜〜！！！</sep></li>
						<li class="topics"><sep class="topics_date">2013/10/11</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">アイコンを作ってみました＝〜〜〜〜〜！！！</sep></li>
						<li class="topics"><sep class="topics_date">2013/10/11</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">アイコンを作ってみました＝〜〜〜〜〜！！！</sep></li>
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
					<img style="margin:0 auto; display: block;" src="./img/hatena_midashi.png">
					<img style="margin:0 auto; display: block;" src="./img/about_midahsi.png">
					</div><!-- .inner_midashi -->
				</div><!-- #what -->

				<div id="bio" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img style="margin-bottom:47px" src="./img/bio_midashi.png">
						<div class="midashi_text">
						<?php require './text/bio.php' ?>
						</div>					
						<img style="margin:0 auto; display: block;" src="./img/bio_images.png">
					</div><!-- .inner_midashi -->
				</div><!-- #bio -->

				<div id="member" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img style="margin-bottom:47px" src="./img/member_midashi.png">
						<div class="midashi_text">
						<?php require './text/member.php' ?>
						</div>					
						<img style="margin:0 auto 30px auto; display: block;" src="./img/midashi_smile.png">
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
width: 380px;
font-size: 49px;
font-family: monospace;">080-4166-4123</p>
						<p style="margin: 0 auto;
width: 435px;
font-size: 45px;
font-family: monospace;
display: block;">mail@ayafuji.com</p>
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