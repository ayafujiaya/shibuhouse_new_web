<!DOCTYPE html>
<html>
	<head>
		<title>渋家 || SHIBUHOUSE</title>
		<!-- typesqure 用タグ -->
		<script type="text/javascript" src="//typesquare.com/accessor/script/typesquare.js?E2mGUC7TkZ8%3D" charset="utf-8"></script>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
		<link href='./css/reset.css' rel='stylesheet' type='text/css'>
		<link href='./css/global.css' rel='stylesheet' type='text/css'>
		<!-- スライドショー -->
		<link href='./css/flexslider.css' rel='stylesheet' type='text/css'>
		<script type="text/javascript" src="js/modernizr.js"></script>
	</head>
	<body>
		<div id="wrap">
			<?php require './header.php' ?>
			<div id="member_midashi">
				<img style="float:left" src="./img/member_smile.png">
				<div id="member_midashi_text">
					集団的知性は、細菌、動物、人間、コンピュータなど様々な集団の、意思決定の過程で発生する。集団的知性の研究は、社会学、計算機科学、集団行動の研究[1]などに属する。
				</div>
			</div>
			<div id="member_profile">
				<div id="inner_member_profile">
					<div class="profile">
						<img class="small_image" src="./img/aeri/01.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/02.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/03.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/04.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/05.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/06.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/07.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/09.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/10.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/11.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/12.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/13.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
					<div class="profile">
						<img class="small_image" src="./img/aeri/13.gif">
						<div class="profile_name">
							<p class="full_name">AERI IKEDA</p>
						</div>
					</div>
				</div>
			</div>
		</div><!-- #wrap -->
		<?php require './footer.php' ?>
		<script type="text/javascript">
			$(".profile_name").hide();
			$(".profile").hover(
				function () {
					$(this).children(".profile_name").addClass( "hover" );
					$(".hover").show();
				},
				function () {
					$(".hover").hide();
					$(this).children(".profile_name").removeClass( "hover" );
					

				}
			);
		</script>
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