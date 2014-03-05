<!DOCTYPE html>
<html>
    <head>
  <meta charset="utf-8">
        <title>米米Club</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Bootstrap -->
        <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" media="screen">
	<link href="./css/site.css" rel="stylesheet">
 
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
        <script src="../../assets/js/html5shiv.js"></script>
        <script src="../../assets/js/respond.min.js"></script>
    <![endif]-->
    
    </head>
    <body>
      <canvas id="canvas"></canvas>
      <div id="container">
<div class="row">
    <div class="col-lg-12  gridsample">
        <img src="./img/komekome.jpg" width="100%">
    </div>
<div class="col-lg-12" style="color:#DDDDDD;">
hello
</div>

<div class="col-lg-12">
      <div class="col-lg-10">

	<h1>米米Clubとは</h1>
	<img src="./img/kome_party.png"></br>
	「おなかがすいてしにそうだ、だけどパーティをしていたい。」
	米米Clubは、食料を入場と入場券を交換できるイベントです。渋家のメンバーがお腹いっぱいになるために、精一杯DJやVJ, LJをします。そのために、来ていただく皆さんにはお気持ち程度の食料を持ってきていただきたいのです。
	<h1>Facebook Page</h1>
	<a href="https://www.facebook.com/events/1394900507446022/1395210474081692/"><img src="./img/fb_kome.png"></a>

	<h1>米米 Club Wish List について</h1>
	    渋家では、イベント時以外も食料の提供を受け付けています。また、右のウィッシュリストから食料を渋家に提供いただければ、注文メール一件につき「米米Club」一回の入場券としてもご利用いただくことができます。
      </div>
     
    <div class="col-lg-2">
<object width="160"><param name="movie" value="//www.youtube.com/v/OmULRemOX0E?version=3&autoplay=1&amp;hl=ja_JP&amp;rel=0"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="//www.youtube.com/v/OmULRemOX0E?autoplay=1&version=3&amp;hl=ja_JP&amp;rel=0" type="application/x-shockwave-flash" width="160" allowscriptaccess="always" allowfullscreen="true"></embed></object>

<SCRIPT charset="utf-8" type="text/javascript" src="http://ws-fe.amazon-adsystem.com/widgets/q?rt=tf_mfw&ServiceVersion=20070822&MarketPlace=JP&ID=V20070822%2FJP%2Fayafuji0a2-22%2F8001%2F462e5247-c4e2-4e11-82b4-a31d357e8b0a"> </SCRIPT> <NOSCRIPT><A HREF="http://ws-fe.amazon-adsystem.com/widgets/q?rt=tf_mfw&ServiceVersion=20070822&MarketPlace=JP&ID=V20070822%2FJP%2Fayafuji0a2-22%2F8001%2F462e5247-c4e2-4e11-82b4-a31d357e8b0a&Operation=NoScript">Amazon.co.jp ウィジェット</A></NOSCRIPT>
    </div>

<!-- <div class="col-lg-12" style="color:#DDDDDD;">
hello
</div> -->
</div>


</div><!-- #container -->
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="//code.jquery.com/jquery.js"></script>
	<script>
	  var canvas = document.getElementById('canvas');
function expandCanvas(){
    var b = document.body;
    var d = document.documentElement;
    canvas.width = Math.max(b.clientWidth , b.scrollWidth, d.scrollWidth, d.clientWidth);
    canvas.height = Math.max(b.clientHeight , b.scrollHeight, d.scrollHeight, d.clientHeight);
}

expandCanvas();
	</script>

	<script>
	  //canvas no code
	  onload = function() {
	  draw();
	  };
function draw() {
  /* canvas要素のノードオブジェクト */
  var canvas = document.getElementById('canvas');
  /* canvas要素の存在チェックとCanvas未対応ブラウザの対処 */
  if ( ! canvas || ! canvas.getContext ) {
    return false;
  }
  var ctx = canvas.getContext('2d');
  
  var imageLoadDone;  
  var img = new Image();
  img.src = "./img/cloud.png";
img.onload = function(){
    // 読み込み終了した状態を保存
    imageLoadDone = true;
};

    //options
    var point = {x:0,y:0};//座標
    var par = {x:2,y:0};//変化量
    var parax = {x:0.001, y:0.002}
    var timer;//タイマー
    var delay = 50;//タイマーを実行する間隔
    
    //描画処理を行う関数。loop()関数の中で呼び出す。
	  
    //繰り返し描画を行う関数。
    var loop = function(){
	ctx.clearRect(0,0,2000, 2000);
	//ctx.fillStyle = 'rgb(255,255,255)';
	//ctx.fillRect(0,0,500,500);
        //pointの数値をparの分だけ増やす
	par.x = par.x + parax.x;
	par.y = par.y + parax.y;
        point.x = point.x + par.x;
        point.y = point.y + par.y;
        //描画処理を呼び出す
	if(imageLoadDone) ctx.drawImage(img, point.x, point.y);
        //タイマー(一度クリアしてから再設定。)
        clearTimeout(timer);
       timer = setTimeout(loop,delay);
    }
   loop();

}
	</script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    </body>
</html>
